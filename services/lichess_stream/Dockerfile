FROM ghcr.io/astral-sh/uv:latest AS uv

FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=uv /uv /uvx /usr/local/bin/

WORKDIR /app

RUN uv venv "$VIRTUAL_ENV"

COPY services/lichess_stream/pyproject.toml services/lichess_stream/README.md /app/
COPY services/lichess_stream/src /app/src

RUN uv pip install --no-cache .

FROM cgr.dev/chainguard/python:latest AS runtime

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CHESS_STREAM_HOST=0.0.0.0 \
    CHESS_STREAM_PORT=8000 \
    CHESS_STREAM_SCHEMA_PATH=/app/schemas/board_state.schema.json

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY schemas /app/schemas

EXPOSE 8000

ENTRYPOINT ["python", "-m", "chess_stream"]
