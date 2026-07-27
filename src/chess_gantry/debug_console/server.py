from __future__ import annotations

from importlib.util import find_spec
from pathlib import Path
from typing import List, Optional, Union
import os
import secrets
import socket
import threading
import webbrowser

from ..config import AppConfig
from ..controller import GantryController
from ..errors import ConfigurationError, ValidationError
from ..service import GantryService
from .runtime import (
    TOKEN_ENVIRONMENT_KEY,
    TOKEN_HEADER,
    DebugRuntime,
    generate_token,
    set_runtime,
    token_fingerprint,
)

LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
WILDCARD_HOSTS = frozenset({"0.0.0.0", "::"})
TEMPLATE_ROOT = Path(__file__).resolve().parent / "templates"


def _require_django() -> None:
    if find_spec("django") is None:
        raise ConfigurationError(
            "Django is not installed; run 'uv sync --extra debug-console'"
        )


def _allowed_hosts(allow_network: bool) -> List[str]:
    if allow_network:
        return ["*"]
    return ["127.0.0.1", "localhost", "[::1]", "testserver"]


def configure_django(*, allow_network: bool = False) -> None:
    _require_django()
    from django.conf import settings

    if settings.configured:
        return
    settings.configure(
        DEBUG=False,
        SECRET_KEY=secrets.token_urlsafe(32),
        ALLOWED_HOSTS=_allowed_hosts(allow_network),
        ROOT_URLCONF="chess_gantry.debug_console.urls",
        INSTALLED_APPS=[],
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [str(TEMPLATE_ROOT)],
                "APP_DIRS": False,
                "OPTIONS": {"context_processors": [], "builtins": []},
            }
        ],
        DATABASES={},
        USE_TZ=True,
        DEFAULT_CHARSET="utf-8",
        SECURE_CONTENT_TYPE_NOSNIFF=True,
        SECURE_REFERRER_POLICY="same-origin",
        X_FRAME_OPTIONS="DENY",
        APPEND_SLASH=False,
        LOGGING={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"plain": {"format": "[console] %(message)s"}},
            "handlers": {
                "stderr": {"class": "logging.StreamHandler", "formatter": "plain"}
            },
            "loggers": {
                "django.server": {
                    "handlers": ["stderr"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "django.request": {
                    "handlers": ["stderr"],
                    "level": "ERROR",
                    "propagate": False,
                },
            },
        },
    )

    import django

    django.setup()


def resolve_token(token: Optional[str]) -> str:
    candidate = token or os.environ.get(TOKEN_ENVIRONMENT_KEY, "").strip()
    if candidate:
        return candidate
    return generate_token()


def build_runtime(
    *,
    config: AppConfig,
    state_path: Union[Path, str],
    journal_path: Union[Path, str],
    audit_path: Union[Path, str],
    token: str,
    demo: bool = False,
    default_timeout_s: Optional[float] = None,
) -> DebugRuntime:
    service = GantryService(config, state_path, journal_path, audit_path)
    controller = GantryController(config, service, demo=demo)
    return DebugRuntime(
        config=config,
        controller=controller,
        token=token,
        audit=service.audit,
        default_timeout_s=default_timeout_s,
    )


def _local_addresses() -> List[str]:
    addresses: List[str] = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            address = info[4][0]
            if address not in addresses:
                addresses.append(address)
    except OSError:
        return addresses
    return addresses


def run_debug_console(
    *,
    config: AppConfig,
    state_path: Union[Path, str],
    journal_path: Union[Path, str],
    audit_path: Union[Path, str],
    host: str = "127.0.0.1",
    port: int = 8300,
    token: Optional[str] = None,
    open_browser: bool = True,
    demo: bool = False,
    allow_network: bool = False,
    default_timeout_s: Optional[float] = None,
) -> None:
    if not 1 <= port <= 65_535:
        raise ValidationError("the debug console port must be between 1 and 65535")
    if host not in LOOPBACK_HOSTS and not allow_network:
        raise ValidationError(
            "refusing a network-visible bind without --allow-network; this console "
            "streams raw G-code to real hardware"
        )

    _require_django()
    resolved_token = resolve_token(token)
    runtime = build_runtime(
        config=config,
        state_path=state_path,
        journal_path=journal_path,
        audit_path=audit_path,
        token=resolved_token,
        demo=demo,
        default_timeout_s=default_timeout_s,
    )
    configure_django(allow_network=allow_network)
    set_runtime(runtime)

    from django.core.handlers.wsgi import WSGIHandler
    from django.core.servers.basehttp import run

    display_host = "127.0.0.1" if host in WILDCARD_HOSTS else host
    url = f"http://{display_host}:{port}"
    print(f"Chess Gantry raw G-code debug console on {url}")
    print(f"Access token: {resolved_token}")
    print(f"Send it as the {TOKEN_HEADER} header or paste it into the page.")
    if demo:
        print("Running against a simulated Marlin controller; no hardware will move.")
    if host in WILDCARD_HOSTS or host not in LOOPBACK_HOSTS:
        for address in _local_addresses():
            print(f"Reachable on the network at http://{address}:{port}")
        print(
            "Anyone with the token can move the gantry. Keep the token private, "
            "keep the workspace clear, and stop the console when you are done."
        )
    runtime.record(
        kind="server",
        client="operator",
        message=f"console started on {host}:{port} with token {token_fingerprint(resolved_token)}",
        audit=True,
    )
    print("Press Control-C to stop it.")

    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    try:
        run(host, port, WSGIHandler(), ipv6=":" in host, threading=True)
    except KeyboardInterrupt:
        print("\nStopping the debug console...")
    finally:
        runtime.controller.disconnect()
        set_runtime(None)
