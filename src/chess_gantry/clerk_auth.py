from __future__ import annotations

import base64
import json
import os
import threading
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import jwt

from .errors import ConfigurationError, ValidationError

PUBLISHABLE_KEY_ENV = "CLERK_PUBLISHABLE_KEY"
SECRET_KEY_ENV = "CLERK_SECRET_KEY"
ISSUER_ENV = "CLERK_JWT_ISSUER"
JWKS_URL_ENV = "CLERK_JWKS_URL"
SESSION_COOKIE = "__session"
CLERK_JS_VERSION = "5"
KEY_PREFIXES = ("pk_test_", "pk_live_")
CLOCK_LEEWAY_SECONDS = 5
JWKS_LIFESPAN_SECONDS = 300


def _text(name: str, environment: Mapping[str, str]) -> str:
    return environment.get(name, "").strip()


def frontend_api_from_publishable_key(key: str) -> str:
    encoded = ""
    for prefix in KEY_PREFIXES:
        if key.startswith(prefix):
            encoded = key[len(prefix) :]
            break
    if not encoded:
        raise ConfigurationError(
            f"{PUBLISHABLE_KEY_ENV} must start with pk_test_ or pk_live_"
        )
    padded = encoded + "=" * (-len(encoded) % 4)
    try:
        decoded = base64.b64decode(padded, validate=True).decode("ascii")
    except (ValueError, UnicodeDecodeError) as error:
        raise ConfigurationError(
            f"{PUBLISHABLE_KEY_ENV} is not a valid Clerk publishable key: {error}"
        ) from error
    host = decoded.rstrip("$").strip().rstrip("/")
    if not host or "/" in host or ":" in host or " " in host:
        raise ConfigurationError(
            f"{PUBLISHABLE_KEY_ENV} does not encode a usable Clerk frontend API host"
        )
    return host


@dataclass(frozen=True)
class ClerkSettings:
    publishable_key: str
    frontend_api: str
    issuer: str
    jwks_url: str

    @property
    def clerk_js_url(self) -> str:
        return (
            f"https://{self.frontend_api}/npm/@clerk/clerk-js@{CLERK_JS_VERSION}"
            "/dist/clerk.browser.js"
        )

    @classmethod
    def from_environment(
        cls, environment: Optional[Mapping[str, str]] = None
    ) -> Optional["ClerkSettings"]:
        source = os.environ if environment is None else environment
        publishable_key = _text(PUBLISHABLE_KEY_ENV, source)
        if not publishable_key:
            return None
        frontend_api = frontend_api_from_publishable_key(publishable_key)
        issuer = _text(ISSUER_ENV, source) or f"https://{frontend_api}"
        jwks_url = (
            _text(JWKS_URL_ENV, source)
            or f"https://{frontend_api}/.well-known/jwks.json"
        )
        for label, url in (("issuer", issuer), ("JWKS URL", jwks_url)):
            if not url.startswith("https://"):
                raise ConfigurationError(f"the Clerk {label} must use https")
        return cls(
            publishable_key=publishable_key,
            frontend_api=frontend_api,
            issuer=issuer,
            jwks_url=jwks_url,
        )

    @classmethod
    def require_from_environment(
        cls, environment: Optional[Mapping[str, str]] = None
    ) -> "ClerkSettings":
        settings = cls.from_environment(environment)
        if settings is None:
            raise ConfigurationError(
                f"{PUBLISHABLE_KEY_ENV} is not set; the dashboard has no other way to"
                " authenticate anyone, so it refuses to start"
            )
        return settings


class ClerkVerifier:
    def __init__(
        self, settings: ClerkSettings, key_client: Optional[Any] = None
    ) -> None:
        self.settings = settings
        self._lock = threading.Lock()
        self._keys = key_client or jwt.PyJWKClient(
            settings.jwks_url,
            cache_keys=True,
            lifespan=JWKS_LIFESPAN_SECONDS,
            timeout=10,
        )

    def _signing_key(self, token: str) -> Any:
        try:
            with self._lock:
                return self._keys.get_signing_key_from_jwt(token).key
        except (jwt.PyJWKClientError, jwt.InvalidTokenError, OSError) as error:
            raise ValidationError(
                f"Clerk signing key lookup failed against {self.settings.jwks_url}: {error}"
            ) from error

    def verify(self, token: str) -> Dict[str, Any]:
        if not token:
            raise ValidationError("no Clerk session cookie was presented")
        signing_key = self._signing_key(token)
        try:
            return jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                issuer=self.settings.issuer,
                leeway=CLOCK_LEEWAY_SECONDS,
                options={"require": ["exp", "iat", "sub"], "verify_aud": False},
            )
        except jwt.InvalidTokenError as error:
            raise ValidationError(
                f"the Clerk session cookie was rejected: {error}"
            ) from error


def _script_safe_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload).replace("<", "\\u003c").replace("&", "\\u0026")


GATE_STYLE = """
#clerkGate{position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(circle at top left,#16213b,transparent 32rem),#0b0e14}
#clerkGate .gate{width:min(460px,100%);text-align:center}
#clerkGate h1{margin:0 0 10px;font-size:clamp(1.6rem,4vw,2.4rem);letter-spacing:-.04em}
#clerkGate p{margin:0 0 20px}
#clerkSignIn{display:flex;justify-content:center}
#clerkSignOut{cursor:pointer;align-self:flex-start}
"""


GATE_SCRIPT = """
(function(){
  var config=__CLERK_CONFIG__;
  var resolveReady;
  var ready=new Promise(function(resolve){resolveReady=resolve});
  var nativeFetch=window.fetch.bind(window);
  window.fetch=function(input,init){
    var url=typeof input==='string'?input:(input&&input.url)||'';
    if(url.indexOf('/api/')!==0)return nativeFetch(input,init);
    return ready.then(function(){
      var options=Object.assign({},init||{});
      options.credentials='same-origin';
      return nativeFetch(input,options);
    });
  };
  function gate(){
    var node=document.createElement('div');
    node.id='clerkGate';
    var card=document.createElement('div');
    card.className='gate';
    var title=document.createElement('h1');
    title.textContent='Chess Gantry Controller';
    var note=document.createElement('p');
    note.textContent='Sign in to reach the dashboard. Signed-in users can move physical hardware.';
    var mount=document.createElement('div');
    mount.id='clerkSignIn';
    card.append(title,note,mount);
    node.appendChild(card);
    document.body.appendChild(node);
    return {node:node,note:note,mount:mount};
  }
  window.addEventListener('load',function(){
    var view=gate();
    var main=document.querySelector('main');
    main.hidden=true;
    if(typeof window.Clerk==='undefined'){
      view.note.textContent='Clerk did not load from '+config.frontendApi+'. Check outbound HTTPS and CLERK_PUBLISHABLE_KEY.';
      return;
    }
    var mounted=false;
    var released=false;
    var signOutAdded=false;
    function showSignIn(){
      if(mounted)return;
      mounted=true;
      window.Clerk.mountSignIn(view.mount);
    }
    function addSignOut(){
      if(signOutAdded)return;
      signOutAdded=true;
      var button=document.createElement('button');
      button.id='clerkSignOut';
      button.className='pill';
      button.textContent='Sign out';
      button.onclick=function(){window.Clerk.signOut()};
      document.querySelector('header').appendChild(button);
    }
    function apply(){
      if(window.Clerk.user){
        view.node.style.display='none';
        main.hidden=false;
        addSignOut();
        if(!released){released=true;resolveReady()}
        return;
      }
      main.hidden=true;
      view.node.style.display='flex';
      showSignIn();
    }
    window.Clerk.load({appearance:{variables:{colorPrimary:'#67e8b5',colorBackground:'#151a24',colorText:'#eef3ff',colorInputBackground:'#1d2431',colorInputText:'#eef3ff'}}}).then(function(){
      window.Clerk.addListener(apply);
      apply();
    }).catch(function(error){
      view.note.textContent='Clerk failed to initialise: '+(error&&error.message?error.message:error);
    });
  });
})();
"""


def clerk_head_markup(settings: ClerkSettings) -> str:
    config = _script_safe_json(
        {
            "publishableKey": settings.publishable_key,
            "frontendApi": settings.frontend_api,
        }
    )
    body = GATE_SCRIPT.replace("__CLERK_CONFIG__", config)
    return (
        f'<style>{GATE_STYLE}</style>\n<script async crossorigin="anonymous" '
        f'data-clerk-publishable-key="{settings.publishable_key}" '
        f'src="{settings.clerk_js_url}"></script>\n<script>{body}</script>\n'
    )


def render_dashboard(html: str, settings: ClerkSettings) -> str:
    marker = "</head>"
    if marker not in html:
        raise ConfigurationError("the dashboard template has no </head> to extend")
    return html.replace(marker, clerk_head_markup(settings) + marker, 1)
