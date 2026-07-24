from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, Iterator, Mapping, Optional
import json
import re
import time
import uuid

from .errors import PendingTransactionError, StateError
from .models import BoardState
from .persistence import utc_now


_GAME_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,120}$")


def redis_client(
    url: Optional[str] = None,
    *,
    upstash_url: Optional[str] = None,
    upstash_token: Optional[str] = None,
) -> Any:
    if upstash_url or upstash_token:
        if not upstash_url or not upstash_token:
            raise StateError(
                "both UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN are required"
            )
        try:
            from upstash_redis import Redis
        except ImportError as exc:
            raise StateError(
                "Upstash support is not installed; run 'python -m pip install -e .'"
            ) from exc
        try:
            client = Redis(
                url=upstash_url,
                token=upstash_token,
                allow_telemetry=False,
            )
            client.ping()
            return client
        except Exception as exc:
            raise StateError(f"cannot connect to Upstash Redis: {exc}") from exc
    if not url:
        raise StateError("a Redis URL or Upstash REST credentials are required")
    try:
        import redis
    except ImportError as exc:
        raise StateError(
            "Redis support is not installed; run 'python -m pip install -e .'"
        ) from exc
    try:
        client = redis.Redis.from_url(url, decode_responses=True)
        client.ping()
        return client
    except redis.RedisError as exc:
        raise StateError(f"cannot connect to Redis: {exc}") from exc


class RedisGameStorage:
    def __init__(
        self,
        client: Any,
        game_id: str,
        width: int = 8,
        height: int = 8,
        *,
        key_prefix: str = "chess-gantry",
        completed_ttl_s: int = 86400,
    ) -> None:
        if not _GAME_ID_RE.fullmatch(game_id):
            raise StateError("game id contains unsupported characters")
        if completed_ttl_s <= 0:
            raise StateError("completed game TTL must be positive")
        self.client = client
        self.game_id = game_id
        self.width = width
        self.height = height
        self.completed_ttl_s = completed_ttl_s
        self.root_key = f"{key_prefix}:game:{game_id}"
        self.state_key = f"{self.root_key}:state"
        self.journal_key = f"{self.root_key}:journal"
        self.audit_key = f"{self.root_key}:audit"
        self.lock_key = f"{self.root_key}:lock"
        self.is_upstash = client.__class__.__module__.startswith("upstash_redis")
        self.store = RedisBoardStore(self)
        self.journal = RedisJournalStore(self)
        self.audit = RedisAuditLog(self)

    def initialize_game(self) -> BoardState:
        initial = BoardState.standard(self.width, self.height)
        self.client.set(self.state_key, json.dumps(initial.to_dict()), nx=True)
        return self.store.load()

    def finish_game(self) -> None:
        keys = (self.state_key, self.journal_key, self.audit_key)
        for key in keys:
            self.client.expire(key, self.completed_ttl_s)


class _UpstashLock:
    def __init__(
        self, client: Any, key: str, timeout: int, blocking_timeout: int
    ) -> None:
        self.client = client
        self.key = key
        self.timeout = timeout
        self.blocking_timeout = blocking_timeout
        self.token = uuid.uuid4().hex

    def acquire(self, blocking: bool = True) -> bool:
        deadline = time.monotonic() + self.blocking_timeout
        while True:
            if self.client.set(self.key, self.token, nx=True, ex=self.timeout):
                return True
            if not blocking or time.monotonic() >= deadline:
                return False
            time.sleep(0.1)

    def release(self) -> None:
        self.client.eval(
            "if redis.call('get', KEYS[1]) == ARGV[1] then "
            "return redis.call('del', KEYS[1]) else return 0 end",
            keys=[self.key],
            args=[self.token],
        )


class RedisBoardStore:
    def __init__(self, storage: RedisGameStorage) -> None:
        self.storage = storage
        self.path = storage.state_key
        self.width = storage.width
        self.height = storage.height

    @contextmanager
    def locked(self) -> Iterator[None]:
        lock = (
            _UpstashLock(
                self.storage.client,
                self.storage.lock_key,
                timeout=180,
                blocking_timeout=30,
            )
            if self.storage.is_upstash
            else self.storage.client.lock(
                self.storage.lock_key, timeout=180, blocking_timeout=30
            )
        )
        if not lock.acquire(blocking=True):
            raise StateError(f"timed out locking game {self.storage.game_id!r}")
        try:
            yield
        finally:
            try:
                lock.release()
            except Exception:
                pass

    def load(self) -> BoardState:
        encoded = self.storage.client.get(self.storage.state_key)
        if encoded is None:
            return self.storage.initialize_game()
        try:
            raw = json.loads(encoded)
        except (TypeError, json.JSONDecodeError) as exc:
            raise StateError("Redis board state is invalid JSON") from exc
        return BoardState.from_mapping(raw, self.width, self.height)

    def save(self, state: BoardState) -> None:
        validated = BoardState.from_mapping(state.to_dict(), self.width, self.height)
        self.storage.client.set(
            self.storage.state_key, json.dumps(validated.to_dict(), sort_keys=True)
        )

    def initialize(self, state: BoardState, overwrite: bool = False) -> None:
        validated = BoardState.from_mapping(state.to_dict(), self.width, self.height)
        written = self.storage.client.set(
            self.storage.state_key,
            json.dumps(validated.to_dict(), sort_keys=True),
            nx=not overwrite,
        )
        if not written:
            raise StateError(f"state already exists for game {self.storage.game_id!r}")


class RedisJournalStore:
    def __init__(self, storage: RedisGameStorage) -> None:
        self.storage = storage
        self.path = storage.journal_key

    def exists(self) -> bool:
        return bool(self.storage.client.exists(self.storage.journal_key))

    def load(self) -> Mapping[str, Any]:
        encoded = self.storage.client.get(self.storage.journal_key)
        if encoded is None:
            raise StateError("pending Redis transaction does not exist")
        return json.loads(encoded)

    def create(self, payload: Mapping[str, Any]) -> None:
        document = dict(payload)
        document.setdefault("schema_version", 1)
        document.setdefault("status", "prepared")
        document.setdefault("created_at", utc_now())
        written = self.storage.client.set(
            self.storage.journal_key, json.dumps(document, sort_keys=True), nx=True
        )
        if not written:
            raise PendingTransactionError(
                f"pending transaction exists for game {self.storage.game_id!r}"
            )

    def mark_failed(self, message: str) -> None:
        if not self.exists():
            return
        document = dict(self.load())
        document.update(status="failed_or_unknown", error=message, updated_at=utc_now())
        self.storage.client.set(
            self.storage.journal_key, json.dumps(document, sort_keys=True)
        )

    def clear(self) -> None:
        self.storage.client.delete(self.storage.journal_key)


class RedisAuditLog:
    def __init__(self, storage: RedisGameStorage) -> None:
        self.storage = storage
        self.path = storage.audit_key

    def append(self, record: Mapping[str, Any]) -> None:
        payload: Dict[str, Any] = {"timestamp": utc_now(), **dict(record)}
        self.storage.client.rpush(
            self.storage.audit_key, json.dumps(payload, sort_keys=True)
        )
