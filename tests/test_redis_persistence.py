from __future__ import annotations

import json
import unittest

from chess_gantry.models import GridPosition, MoveDelta
from chess_gantry.redis_persistence import RedisGameStorage


class FakeLock:
    def acquire(self, blocking=True):
        return True

    def release(self):
        return None


class FakePipeline:
    def __init__(self, client):
        self.client = client
        self.expiries = []

    def expire(self, key, ttl):
        self.expiries.append((key, ttl))
        return self

    def execute(self):
        for key, ttl in self.expiries:
            self.client.ttls[key] = ttl
        return [True] * len(self.expiries)


class FakeRedis:
    def __init__(self):
        self.values = {}
        self.lists = {}
        self.ttls = {}

    def set(self, key, value, nx=False):
        if nx and key in self.values:
            return False
        self.values[key] = value
        return True

    def get(self, key):
        return self.values.get(key)

    def exists(self, key):
        return key in self.values or key in self.lists

    def delete(self, key):
        self.values.pop(key, None)
        self.lists.pop(key, None)

    def rpush(self, key, value):
        self.lists.setdefault(key, []).append(value)

    def lock(self, key, timeout, blocking_timeout):
        return FakeLock()

    def pipeline(self):
        return FakePipeline(self)

    def expire(self, key, ttl):
        self.ttls[key] = ttl
        return self.exists(key)


class RedisPersistenceTests(unittest.TestCase):
    def test_game_auto_initializes_and_is_shared_between_instances(self):
        client = FakeRedis()
        first = RedisGameStorage(client, "game123")
        state = first.initialize_game()
        move = MoveDelta.from_mapping(
            {
                "event_id": "game123.1",
                "position": "white_pawn_e",
                "px": 4,
                "py": 1,
                "nx": 4,
                "ny": 3,
            }
        )
        first.store.save(state.applied(move, None))

        restarted = RedisGameStorage(client, "game123")
        loaded = restarted.store.load()
        self.assertEqual(loaded.revision, 1)
        self.assertEqual(
            loaded.pieces["white_pawn_e"].board_position, GridPosition(4, 3)
        )
        self.assertEqual(loaded.processed_events, ("game123.1",))

    def test_games_are_isolated_and_completion_sets_ttl(self):
        client = FakeRedis()
        first = RedisGameStorage(client, "game-one", completed_ttl_s=90)
        second = RedisGameStorage(client, "game-two", completed_ttl_s=90)
        first.initialize_game()
        second.initialize_game()
        first.audit.append({"status": "completed"})
        first.journal.create({"move": {}})

        first.finish_game()

        self.assertNotEqual(first.state_key, second.state_key)
        self.assertNotIn(second.state_key, client.ttls)
        self.assertEqual(client.ttls[first.state_key], 90)
        self.assertEqual(client.ttls[first.journal_key], 90)
        self.assertEqual(client.ttls[first.audit_key], 90)
        self.assertEqual(
            json.loads(client.lists[first.audit_key][0])["status"], "completed"
        )


if __name__ == "__main__":
    unittest.main()
