"""Async client for the Lichess game NDJSON stream."""

from __future__ import annotations

import json
from typing import Any, AsyncIterator, Dict, Optional

import httpx


class FatalStreamError(RuntimeError):
    """Raised for non-retryable stream failures such as an unknown game id."""


class TransientStreamError(RuntimeError):
    """Raised for retryable stream failures such as rate limits or network drops."""


class LichessStreamClient:
    """Consume ``GET /api/stream/game/{id}`` as decoded NDJSON messages."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        connect_timeout: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        headers = {
            "Accept": "application/x-ndjson",
            "User-Agent": "basilisgay/0.1",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        timeout = httpx.Timeout(
            connect=connect_timeout,
            read=None,
            write=connect_timeout,
            pool=connect_timeout,
        )
        self._client = httpx.AsyncClient(
            headers=headers, timeout=timeout, follow_redirects=True
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "LichessStreamClient":
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.aclose()

    async def stream_game(self, game_id: str) -> AsyncIterator[Dict[str, Any]]:
        url = f"{self._base_url}/api/stream/game/{game_id}"
        try:
            async with self._client.stream("GET", url) as response:
                if response.status_code == 404:
                    raise FatalStreamError(f"lichess game {game_id!r} was not found")
                if response.status_code == 429:
                    raise TransientStreamError("lichess rate limit reached (HTTP 429)")
                if response.status_code >= 500:
                    raise TransientStreamError(
                        f"lichess server error (HTTP {response.status_code})"
                    )
                if response.status_code >= 400:
                    await response.aread()
                    raise FatalStreamError(
                        f"lichess rejected the request (HTTP {response.status_code})"
                    )
                async for line in response.aiter_lines():
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        yield json.loads(stripped)
                    except json.JSONDecodeError as exc:
                        raise TransientStreamError(
                            f"received malformed NDJSON from lichess: {exc}"
                        ) from exc
        except httpx.HTTPError as exc:
            raise TransientStreamError(
                f"lichess stream transport error: {exc}"
            ) from exc
