from __future__ import annotations

import base64
import json
import time
import unittest
from types import SimpleNamespace

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

from chess_gantry.clerk_auth import (
    ClerkSettings,
    ClerkVerifier,
    _script_safe_json,
    frontend_api_from_publishable_key,
    render_dashboard,
)
from chess_gantry.errors import ConfigurationError, ValidationError

HOST = "clerk.example.com"


def publishable_key(host: str = HOST, prefix: str = "pk_test_") -> str:
    encoded = base64.b64encode((host + "$").encode("ascii")).decode("ascii")
    return prefix + encoded.rstrip("=")


def settings(**overrides: str) -> ClerkSettings:
    environment = {"CLERK_PUBLISHABLE_KEY": publishable_key()}
    environment.update(overrides)
    return ClerkSettings.require_from_environment(environment)


class StubKeyClient:
    def __init__(self, key: object) -> None:
        self.key = key

    def get_signing_key_from_jwt(self, token: str) -> object:
        return SimpleNamespace(key=self.key)


class PublishableKeyTests(unittest.TestCase):
    def test_frontend_api_is_decoded_from_both_key_prefixes(self) -> None:
        self.assertEqual(frontend_api_from_publishable_key(publishable_key()), HOST)
        live = publishable_key("clerk.gantry.dev", "pk_live_")
        self.assertEqual(frontend_api_from_publishable_key(live), "clerk.gantry.dev")

    def test_malformed_keys_are_rejected(self) -> None:
        with self.assertRaisesRegex(ConfigurationError, "pk_test_"):
            frontend_api_from_publishable_key("sk_test_secret")
        with self.assertRaisesRegex(ConfigurationError, "valid Clerk publishable key"):
            frontend_api_from_publishable_key("pk_test_!!!!")
        with self.assertRaisesRegex(ConfigurationError, "usable Clerk frontend API"):
            frontend_api_from_publishable_key(publishable_key("clerk.dev:8080"))


class SettingsTests(unittest.TestCase):
    def test_absent_publishable_key_disables_clerk(self) -> None:
        self.assertIsNone(ClerkSettings.from_environment({}))
        self.assertIsNone(
            ClerkSettings.from_environment({"CLERK_PUBLISHABLE_KEY": "  "})
        )

    def test_a_missing_publishable_key_is_fatal_when_required(self) -> None:
        with self.assertRaisesRegex(ConfigurationError, "refuses to start"):
            ClerkSettings.require_from_environment({})

    def test_issuer_and_jwks_are_derived_from_the_publishable_key(self) -> None:
        resolved = settings()
        self.assertEqual(resolved.frontend_api, HOST)
        self.assertEqual(resolved.issuer, f"https://{HOST}")
        self.assertEqual(resolved.jwks_url, f"https://{HOST}/.well-known/jwks.json")
        self.assertIn("clerk.browser.js", resolved.clerk_js_url)
        self.assertTrue(resolved.clerk_js_url.startswith(f"https://{HOST}/"))

    def test_issuer_and_jwks_overrides_are_honoured(self) -> None:
        resolved = settings(
            CLERK_JWT_ISSUER="https://accounts.gantry.dev",
            CLERK_JWKS_URL="https://accounts.gantry.dev/.well-known/jwks.json",
        )
        self.assertEqual(resolved.issuer, "https://accounts.gantry.dev")
        self.assertEqual(
            resolved.jwks_url, "https://accounts.gantry.dev/.well-known/jwks.json"
        )

    def test_plain_http_endpoints_are_refused(self) -> None:
        with self.assertRaisesRegex(ConfigurationError, "must use https"):
            settings(CLERK_JWKS_URL="http://clerk.example.com/jwks")


class VerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.public_key = cls.private_key.public_key()

    def verifier(self, **overrides: str) -> ClerkVerifier:
        return ClerkVerifier(settings(**overrides), StubKeyClient(self.public_key))

    def token(self, **claims: object) -> str:
        now = int(time.time())
        payload = {
            "iss": f"https://{HOST}",
            "sub": "user_a",
            "iat": now,
            "exp": now + 60,
        }
        payload.update(claims)
        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def test_a_current_token_from_the_instance_is_accepted(self) -> None:
        claims = self.verifier().verify(self.token())
        self.assertEqual(claims["sub"], "user_a")

    def test_an_empty_cookie_is_refused(self) -> None:
        with self.assertRaisesRegex(ValidationError, "no Clerk session cookie"):
            self.verifier().verify("")

    def test_tokens_from_another_issuer_are_refused(self) -> None:
        with self.assertRaisesRegex(ValidationError, "rejected"):
            self.verifier().verify(self.token(iss="https://clerk.attacker.test"))

    def test_expired_tokens_are_refused(self) -> None:
        now = int(time.time())
        with self.assertRaisesRegex(ValidationError, "rejected"):
            self.verifier().verify(self.token(iat=now - 600, exp=now - 300))

    def test_unsigned_tokens_are_refused(self) -> None:
        now = int(time.time())
        payload = {
            "iss": f"https://{HOST}",
            "sub": "user_a",
            "iat": now,
            "exp": now + 60,
        }
        unsigned = jwt.encode(payload, key="", algorithm="none")
        with self.assertRaisesRegex(ValidationError, "rejected"):
            self.verifier().verify(unsigned)

    def test_missing_required_claims_are_refused(self) -> None:
        now = int(time.time())
        incomplete = jwt.encode(
            {"iss": f"https://{HOST}", "iat": now, "exp": now + 60},
            self.private_key,
            algorithm="RS256",
        )
        with self.assertRaisesRegex(ValidationError, "rejected"):
            self.verifier().verify(incomplete)

    def test_any_signed_in_user_of_the_instance_is_accepted(self) -> None:
        self.assertEqual(
            self.verifier().verify(self.token(sub="user_z"))["sub"], "user_z"
        )


class DashboardRenderingTests(unittest.TestCase):
    def test_the_gate_is_injected_before_the_head_closes(self) -> None:
        resolved = settings()
        page = render_dashboard(
            "<html><head><title>x</title></head><body></body></html>", resolved
        )
        self.assertIn(resolved.clerk_js_url, page)
        self.assertIn(resolved.publishable_key, page)
        self.assertIn("clerkSignIn", page)
        self.assertIn("mountSignIn", page)
        self.assertLess(page.index("clerkSignIn"), page.index("</head>"))
        self.assertTrue(page.endswith("<body></body></html>"))
        self.assertNotIn("Authorization", page)
        self.assertNotIn("getToken", page)

    def test_injected_configuration_cannot_close_the_script_tag(self) -> None:
        payload = _script_safe_json({"key": "</script><script>alert(1)&"})
        self.assertNotIn("<", payload)
        self.assertNotIn("&", payload)
        self.assertEqual(json.loads(payload)["key"], "</script><script>alert(1)&")

    def test_a_template_without_a_head_is_reported(self) -> None:
        with self.assertRaisesRegex(ConfigurationError, "</head>"):
            render_dashboard("<html><body></body></html>", settings())


if __name__ == "__main__":
    unittest.main()
