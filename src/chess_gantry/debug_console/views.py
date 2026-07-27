from __future__ import annotations

from typing import Any, Dict, Mapping, Optional
import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from ..errors import GantryError, ValidationError
from .runtime import (
    CLIENT_HEADER,
    TOKEN_HEADER,
    DebugRuntime,
    client_names,
    current_runtime,
)

MAX_BODY_BYTES = 262_144
MAX_CLIENT_NAME_CHARS = 48


class Unauthorized(Exception):
    pass


def _envelope(payload: Mapping[str, Any], status: int = 200) -> JsonResponse:
    response = JsonResponse(dict(payload), status=status)
    response["Cache-Control"] = "no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response


def _supplied_token(request: HttpRequest) -> Optional[str]:
    header = request.headers.get(TOKEN_HEADER)
    if header:
        return header.strip()
    authorization = request.headers.get("Authorization", "")
    prefix = "bearer "
    if authorization.lower().startswith(prefix):
        return authorization[len(prefix) :].strip()
    return None


def _authorize(request: HttpRequest) -> DebugRuntime:
    runtime = current_runtime()
    if not runtime.authorize(_supplied_token(request)):
        raise Unauthorized("a valid access token is required")
    return runtime


def _client_label(request: HttpRequest, payload: Mapping[str, Any]) -> str:
    address = request.META.get("REMOTE_ADDR") or "unknown"
    raw = payload.get("client")
    if raw is None:
        raw = request.headers.get(CLIENT_HEADER)
    if raw is None:
        return address
    if not isinstance(raw, str):
        raise ValidationError("client must be a string")
    name = " ".join(raw.split())[:MAX_CLIENT_NAME_CHARS]
    if not name:
        return address
    return f"{name} ({address})"


def _read_json(request: HttpRequest) -> Dict[str, Any]:
    body = request.body
    if len(body) > MAX_BODY_BYTES:
        raise ValidationError("the request body is too large")
    if not body:
        return {}
    try:
        value = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError("the request body must be valid JSON") from exc
    if not isinstance(value, dict):
        raise ValidationError("the request body must be a JSON object")
    return value


def _integer_or_none(value: Any, field: str) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValidationError(f"{field} must be an integer or null")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must be an integer or null") from exc


def _handle(request: HttpRequest, action: str) -> JsonResponse:
    try:
        runtime = _authorize(request)
    except Unauthorized as exc:
        return _envelope({"ok": False, "error": str(exc)}, 401)
    try:
        payload = {} if request.method == "GET" else _read_json(request)
        return _ACTIONS[action](request, runtime, payload)
    except ValidationError as exc:
        return _envelope(
            {"ok": False, "error": str(exc), "status": runtime.snapshot()}, 400
        )
    except GantryError as exc:
        return _envelope(
            {"ok": False, "error": str(exc), "status": runtime.snapshot()}, 409
        )


def _status(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    return _envelope({"ok": True, "status": runtime.snapshot()})


def _ports(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    ports = [item.as_dict() for item in runtime.controller.available_ports()]
    return _envelope({"ok": True, "ports": ports})


def _log(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    after = _integer_or_none(request.GET.get("after"), "after") or 0
    if after < 0:
        raise ValidationError("after cannot be negative")
    events, latest = runtime.log.since(after)
    return _envelope(
        {
            "ok": True,
            "events": list(events),
            "latest_sequence": latest,
            "clients": client_names(events),
            "status": runtime.snapshot(),
        }
    )


def _connect(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    client = _client_label(request, payload)
    port = payload.get("port")
    if port is not None and not isinstance(port, str):
        raise ValidationError("port must be a string or null")
    baudrate = _integer_or_none(payload.get("baudrate"), "baudrate")
    status = runtime.controller.connect(port=port or None, baudrate=baudrate)
    runtime.record(
        kind="connect",
        client=client,
        message=f"connected to {status.get('port')} at {status.get('baudrate')} baud",
        detail=[str(status.get("firmware") or "no firmware identity reported")],
        audit=True,
    )
    return _envelope({"ok": True, "status": runtime.snapshot()})


def _disconnect(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    client = _client_label(request, payload)
    runtime.controller.disconnect()
    runtime.record(
        kind="disconnect", client=client, message="closed the serial link", audit=True
    )
    return _envelope({"ok": True, "status": runtime.snapshot()})


def _gcode(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    client = _client_label(request, payload)
    source = payload.get("commands", payload.get("command"))
    if source is None:
        raise ValidationError("commands is required")
    timeout = payload.get("timeout_s")
    stop_on_error = payload.get("stop_on_error", True)
    if not isinstance(stop_on_error, bool):
        raise ValidationError("stop_on_error must be a boolean")
    results = runtime.controller.send_raw_program(
        source,
        timeout_s=runtime.default_timeout_s if timeout is None else timeout,
        stop_on_error=stop_on_error,
    )
    failures = sum(1 for item in results if item["error"])
    detail = []
    for item in results:
        detail.append(f"> {item['command']}")
        detail.extend(item["responses"])
        if item["error"]:
            detail.append(f"ERROR: {item['error']}")
    sent = len(results)
    summary = f"sent {sent} command{'' if sent == 1 else 's'}"
    if failures:
        summary = f"{summary} with {failures} rejected"
    runtime.record(
        kind="gcode", client=client, message=summary, detail=detail, audit=True
    )
    return _envelope(
        {
            "ok": True,
            "results": [dict(item) for item in results],
            "failures": failures,
            "status": runtime.snapshot(),
        }
    )


def _stop(
    request: HttpRequest, runtime: DebugRuntime, payload: Mapping[str, Any]
) -> JsonResponse:
    client = _client_label(request, payload)
    if payload.get("confirm") is not True:
        raise ValidationError("the emergency stop requires explicit confirmation")
    runtime.controller.emergency_stop()
    runtime.record(
        kind="stop",
        client=client,
        message=(
            f"sent {runtime.config.safety.emergency_stop_command}; "
            "the controller needs a reset or power cycle"
        ),
        audit=True,
    )
    return _envelope({"ok": True, "status": runtime.snapshot()})


_ACTIONS = {
    "status": _status,
    "ports": _ports,
    "log": _log,
    "connect": _connect,
    "disconnect": _disconnect,
    "gcode": _gcode,
    "stop": _stop,
}


@require_GET
def console_page(request: HttpRequest) -> HttpResponse:
    runtime = current_runtime()
    response = render(
        request,
        "debug_console/console.html",
        {
            "limits": runtime.limits(),
            "profile": runtime.profile(),
            "demo": runtime.controller.demo,
            "token_header": TOKEN_HEADER,
        },
    )
    response["Cache-Control"] = "no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response


@require_GET
def api_status(request: HttpRequest) -> JsonResponse:
    return _handle(request, "status")


@require_GET
def api_ports(request: HttpRequest) -> JsonResponse:
    return _handle(request, "ports")


@require_GET
def api_log(request: HttpRequest) -> JsonResponse:
    return _handle(request, "log")


@require_POST
def api_connect(request: HttpRequest) -> JsonResponse:
    return _handle(request, "connect")


@require_POST
def api_disconnect(request: HttpRequest) -> JsonResponse:
    return _handle(request, "disconnect")


@require_POST
def api_gcode(request: HttpRequest) -> JsonResponse:
    return _handle(request, "gcode")


@require_POST
def api_stop(request: HttpRequest) -> JsonResponse:
    return _handle(request, "stop")
