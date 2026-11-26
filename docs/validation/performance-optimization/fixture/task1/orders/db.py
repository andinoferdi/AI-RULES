import sqlite3
import time

ROUND_TRIP_SECONDS = 0.0004  # production network hop, see README


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.query_count = 0

    def _network(self):
        end = time.perf_counter() + ROUND_TRIP_SECONDS
        while time.perf_counter() < end:
            pass

    def query(self, sql, params=()):
        self._network()
        self.query_count += 1
        return self.conn.execute(sql, params).fetchall()

    def executescript(self, script):
        self.conn.executescript(script)
