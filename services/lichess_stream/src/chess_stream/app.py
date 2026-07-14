"""FastAPI application exposing the Lichess board-state stream over WebSocket."""

from __future__ import annotations

import asyncio
import logging
import re
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from .config import Settings, get_settings
from .hub import GameHub, Subscriber
from .schema import BoardStateValidator

logger = logging.getLogger(__name__)

_GAME_ID_RE = re.compile(r"^[A-Za-z0-9]{6,16}$")


def _validate_game_id(game_id: str) -> str:
    if not _GAME_ID_RE.fullmatch(game_id):
        raise HTTPException(status_code=422, detail="invalid lichess game id")
    return game_id


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    try:
        validator: BoardStateValidator | None = BoardStateValidator(
            settings.schema_path
        )
        logger.info("loaded board-state schema from %s", validator.source)
    except (OSError, ValueError) as exc:
        if settings.validate_snapshots:
            raise RuntimeError(f"cannot load board-state schema: {exc}") from exc
        validator = None
        logger.warning("schema validation disabled: %s", exc)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        hub = GameHub(settings, validator)
        app.state.hub = hub
        app.state.settings = settings
        try:
            yield
        finally:
            await hub.shutdown()

    app = FastAPI(
        title="Chess Lichess Stream",
        version="0.1.0",
        description="Subscribe to a Lichess game id and receive real-time board-state updates.",
        lifespan=lifespan,
    )

    @app.get("/healthz")
    async def healthz() -> Dict[str, Any]:
        hub: GameHub = app.state.hub
        return {
            "status": "ok",
            "active_games": hub.active_games(),
            "schema_validation": validator is not None and settings.validate_snapshots,
        }

    @app.get("/games/{game_id}/state")
    async def game_state(game_id: str) -> JSONResponse:
        _validate_game_id(game_id)
        hub: GameHub = app.state.hub
        session, subscriber = await hub.subscribe(game_id)
        try:
            message = await asyncio.wait_for(
                subscriber.get(), timeout=settings.lichess_connect_timeout + 5
            )
            while message.get("type") not in {
                "snapshot",
                "resync",
                "error",
                "game_over",
            }:
                message = await asyncio.wait_for(
                    subscriber.get(), timeout=settings.lichess_connect_timeout + 5
                )
            if message.get("type") == "error" and message.get("fatal"):
                raise HTTPException(
                    status_code=404, detail=message.get("message", "game not found")
                )
            return JSONResponse({"game_id": game_id, "state": session.current_state()})
        except asyncio.TimeoutError as exc:
            raise HTTPException(
                status_code=504, detail="timed out waiting for lichess"
            ) from exc
        finally:
            await hub.unsubscribe(game_id, subscriber)

    @app.websocket("/ws/{game_id}")
    async def ws_game(websocket: WebSocket, game_id: str) -> None:
        if not _GAME_ID_RE.fullmatch(game_id):
            await websocket.close(code=4422, reason="invalid lichess game id")
            return
        await websocket.accept()
        hub: GameHub = websocket.app.state.hub
        _, subscriber = await hub.subscribe(game_id)
        writer = asyncio.create_task(_writer(websocket, subscriber))
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        except RuntimeError:
            pass
        finally:
            writer.cancel()
            try:
                await writer
            except asyncio.CancelledError:
                pass
            await hub.unsubscribe(game_id, subscriber)

    return app


async def _writer(websocket: WebSocket, subscriber: Subscriber) -> None:
    while True:
        message = await subscriber.get()
        await websocket.send_json(message)


app = create_app()
