"""Runtime configuration for the streaming service."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_schema_path() -> Path:
    candidates = [
        Path("/app/schemas/board_state.schema.json"),
        Path(__file__).resolve().parents[4] / "schemas" / "board_state.schema.json",
        Path.cwd() / "schemas" / "board_state.schema.json",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


class Settings(BaseSettings):
    """Environment-driven settings."""

    model_config = SettingsConfigDict(
        env_prefix="CHESS_STREAM_", env_file=None, extra="ignore"
    )

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = Field(default="info")

    lichess_base_url: str = Field(default="https://lichess.org")
    lichess_token: Optional[str] = Field(default=None)
    lichess_connect_timeout: float = Field(default=10.0, gt=0)

    reconnect_initial_delay: float = Field(default=1.0, gt=0)
    reconnect_max_delay: float = Field(default=30.0, gt=0)

    subscriber_queue_size: int = Field(default=256, ge=1)
    max_processed_events: int = Field(default=1024, ge=1)

    schema_path: Path = Field(default_factory=_default_schema_path)
    validate_snapshots: bool = Field(default=True)

    def stream_url(self, game_id: str) -> str:
        return f"{self.lichess_base_url.rstrip('/')}/api/stream/game/{game_id}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
