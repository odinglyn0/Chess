# Chess Lichess Stream

A dockerised, `uvloop`-powered FastAPI service. Point it at a Lichess game id and it streams
that game in real time, translating every move into updates against the canonical
[`schemas/board_state.schema.json`](../../schemas/board_state.schema.json) board-state model.
Any number of clients can subscribe to the same game over a WebSocket and receive moves,
captures, castling, promotions, checks, and the final result.

## How it works

1. On the first subscriber for a game id, the service opens Lichess'
   `GET /api/stream/game/{id}` NDJSON stream (public, no auth required; ongoing games are
   delayed three moves by Lichess).
2. A `python-chess`-backed tracker keeps a **stable id per physical piece**. Ids survive
   moves and promotions; captures move a piece to a `captured` status with an incrementing
   `capture_slot`, exactly as the board-state schema describes.
3. Each move produces a move event plus a full, schema-validated board-state snapshot, which
   is fanned out to every subscriber through a bounded, latest-wins queue so one slow client
   cannot stall the others.
4. When the last subscriber for a game disconnects, the Lichess stream for that game is closed.

## API

### WebSocket `GET /ws/{game_id}`

Subscribe to a game. The server pushes JSON messages; inbound messages are ignored (they only
keep the socket alive / signal disconnect).

Message envelopes (`type` field):

| `type`      | Payload |
|-------------|---------|
| `game_info` | Lichess game description: `status`, `variant`, `speed`, `rated`, `players`, `fen`, `winner`. |
| `snapshot`  | `state`: full board state matching `board_state.schema.json`. Sent on join and on init. |
| `move`      | `move`: the move event (below); `state`: the new board state; optional `clocks` (`wc`/`bc`). |
| `resync`    | `state`: full board state, sent when the tracker had to re-derive from a FEN. |
| `game_over` | `status`, `winner`. |
| `error`     | `fatal` (bool), `message`. Non-fatal errors are retried automatically. |

Move event fields: `event_id`, `ply`, `move_number`, `color`, `san`, `uci`, `piece` (moving
piece id), `from`/`to` (`{x, y}`), `capture` (`{piece, kind, x, y, capture_slot}` or `null`),
`castle` (`{rook, from, to}` or `null`), `promotion` (piece name or `null`), `check`,
`checkmate`, `stalemate`, `fen`.

### HTTP `GET /games/{game_id}/state`

Returns the current board-state snapshot for a game (opens a short-lived subscription to fetch it).

### HTTP `GET /healthz`

Liveness plus the list of currently active games.

## Run with Docker

Built on the latest Chainguard Python image with `uv` for dependency resolution.

```bash
docker compose up --build
```

Then subscribe (any WebSocket client works):

```bash
# using websocat, replace GAMEID with a real lichess game id
websocat ws://localhost:8000/ws/GAMEID
```

Or in Python:

```python
import asyncio, json, websockets

async def main(game_id: str):
    async with websockets.connect(f"ws://localhost:8000/ws/{game_id}") as ws:
        async for raw in ws:
            msg = json.loads(raw)
            print(msg["type"], msg.get("move", {}).get("san", ""))

asyncio.run(main("GAMEID"))
```

## Configuration

All settings are environment variables prefixed with `CHESS_STREAM_`:

| Variable | Default | Purpose |
|----------|---------|---------|
| `CHESS_STREAM_HOST` | `0.0.0.0` | Bind host. |
| `CHESS_STREAM_PORT` | `8000` | Bind port. |
| `CHESS_STREAM_LOG_LEVEL` | `info` | Log level. |
| `CHESS_STREAM_LICHESS_BASE_URL` | `https://lichess.org` | Lichess origin. |
| `CHESS_STREAM_LICHESS_TOKEN` | _(unset)_ | Optional Lichess API token (higher rate limits). |
| `CHESS_STREAM_SCHEMA_PATH` | `/app/schemas/board_state.schema.json` | Board-state schema location. |
| `CHESS_STREAM_VALIDATE_SNAPSHOTS` | `true` | Validate every snapshot against the schema. |
| `CHESS_STREAM_SUBSCRIBER_QUEUE_SIZE` | `256` | Per-client message buffer. |
| `CHESS_STREAM_RECONNECT_MAX_DELAY` | `30` | Max reconnect backoff (seconds). |

## Local development

```bash
uv sync
uv run chess-lichess-stream
uv run pytest
```
