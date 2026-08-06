FROM ubuntu:24.04 AS build

ENV DEBIAN_FRONTEND=noninteractive \
  UV_PYTHON_INSTALL_DIR=/opt/uv/python \
  UV_PROJECT_ENVIRONMENT=/app/.venv \
  UV_CACHE_DIR=/tmp/uv-cache \
  PATH=/root/.local/bin:$PATH

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates curl \
  && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
  && uv python install 3.11

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY tests ./tests
COPY scripts ./scripts
COPY config.json ./config.json
COPY config.demo.json ./config.demo.json
COPY config.example.json ./config.example.json
COPY examples ./examples
COPY schemas ./schemas
COPY docker/entrypoint.py ./docker/entrypoint.py
RUN uv sync --frozen --no-editable \
  && uv cache clean

FROM build AS test
COPY Dockerfile .dockerignore docker-compose.pi.yml docker-compose.lichess.yml ./
COPY chicken ./chicken
RUN ./scripts/check.sh

FROM gcr.io/distroless/cc-debian12:latest

ENV HOME=/tmp \
  PYTHONUNBUFFERED=1 \
  UV_CACHE_DIR=/tmp/uv-cache \
  CHESS_GANTRY_DISTROLESS=1 \
  PATH=/app/.venv/bin:/opt/uv/bin:$PATH

WORKDIR /app

COPY --from=build /root/.local/bin/uv /opt/uv/bin/uv
COPY --from=build /root/.local/bin/uvx /opt/uv/bin/uvx
COPY --from=build /opt/uv/python /opt/uv/python
COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/src /app/src
COPY --from=build /app/config.json /app/config.json
COPY --from=build /app/config.demo.json /app/config.demo.json
COPY --from=build /app/config.example.json /app/config.example.json
COPY --from=build /app/examples /app/examples
COPY --from=build /app/schemas /app/schemas
COPY --from=build /app/scripts/check_firmware.py /app/scripts/check_firmware.py
COPY --from=build /app/docker /app/docker

EXPOSE 8000

ENTRYPOINT ["/app/.venv/bin/python", "/app/docker/entrypoint.py"]
