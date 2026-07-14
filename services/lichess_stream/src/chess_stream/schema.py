"""Load and validate board-state snapshots against the canonical JSON schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from jsonschema import Draft202012Validator


class SchemaValidationError(ValueError):
    """Raised when a snapshot does not conform to the board-state schema."""


class BoardStateValidator:
    def __init__(self, schema_path: Path) -> None:
        self._path = schema_path
        text = schema_path.read_text(encoding="utf-8")
        self._schema: Dict[str, Any] = json.loads(text)
        Draft202012Validator.check_schema(self._schema)
        self._validator = Draft202012Validator(self._schema)

    @property
    def source(self) -> Path:
        return self._path

    def validate(self, snapshot: Dict[str, Any]) -> None:
        errors = sorted(self._validator.iter_errors(snapshot), key=lambda err: err.path)
        if errors:
            first = errors[0]
            location = "/".join(str(part) for part in first.path) or "<root>"
            raise SchemaValidationError(
                f"board state invalid at {location}: {first.message}"
            )
