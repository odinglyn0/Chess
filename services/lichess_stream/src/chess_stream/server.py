"""Uvicorn server bootstrap running on the uvloop event loop."""

from __future__ import annotations

import logging

import uvicorn

from .config import get_settings


def _select_loop() -> str:
    try:
        import uvloop  # noqa: F401
    except ModuleNotFoundError:
        return "auto"
    return "uvloop"


def run() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    uvicorn.run(
        "chess_stream.app:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        loop=_select_loop(),
        ws="auto",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
