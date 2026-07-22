from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, Mapping, Optional, Union
import json
import os
import tempfile

from .errors import PendingTransactionError, StateError, ValidationError
from .models import BoardState

try:
    import fcntl
except ImportError:
    fcntl = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Mapping[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StateError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(raw, Mapping):
        raise ValidationError(f"{path} must contain a JSON object")
    return raw


def atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temp_path.exists():
            temp_path.unlink()


class FileLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._handle: Optional[Any] = None

    def __enter__(self) -> "FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("a+", encoding="utf-8")
        if fcntl is not None:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self._handle is not None:
            if fcntl is not None:
                fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
            self._handle.close()
            self._handle = None


class BoardStore:
    def __init__(self, path: Union[Path, str], width: int = 8, height: int = 8) -> None:
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        self.width = width
        self.height = height

    @contextmanager
    def locked(self) -> Iterator[None]:
        with FileLock(self.lock_path):
            yield

    def load(self) -> BoardState:
        return BoardState.from_mapping(read_json(self.path), self.width, self.height)

    def save(self, state: BoardState) -> None:
        validated = BoardState.from_mapping(state.to_dict(), self.width, self.height)
        atomic_write_json(self.path, validated.to_dict())

    def initialize(self, state: BoardState, overwrite: bool = False) -> None:
        with self.locked():
            if self.path.exists() and not overwrite:
                raise StateError(f"state file already exists: {self.path}")
            self.save(state)


class JournalStore:
    def __init__(self, path: Union[Path, str]) -> None:
        self.path = Path(path)

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> Mapping[str, Any]:
        return read_json(self.path)

    def create(self, payload: Mapping[str, Any]) -> None:
        if self.exists():
            raise PendingTransactionError(
                f"pending transaction exists at {self.path}; reconcile it before another execution"
            )
        document = dict(payload)
        document.setdefault("schema_version", 1)
        document.setdefault("status", "prepared")
        document.setdefault("created_at", utc_now())
        atomic_write_json(self.path, document)

    def mark_failed(self, message: str) -> None:
        if not self.exists():
            return
        document = dict(self.load())
        document["status"] = "failed_or_unknown"
        document["error"] = message
        document["updated_at"] = utc_now()
        atomic_write_json(self.path, document)

    def clear(self) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            return


class AuditLog:
    def __init__(self, path: Union[Path, str]) -> None:
        self.path = Path(path)

    def append(self, record: Mapping[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload: Dict[str, Any] = {"timestamp": utc_now(), **dict(record)}
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
