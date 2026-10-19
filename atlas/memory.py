"""Versioned, auditable memory of verified arithmetic patterns.

The SQLite database is local to the experiment. This is retrieval of verified
examples, not training or a general-purpose AI memory.
"""
import json
import sqlite3
from pathlib import Path


class VerifiedMemory:
    def __init__(self, path=":memory:"):
        self.connection = sqlite3.connect(str(path))
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS lessons (
                lesson_id TEXT PRIMARY KEY,
                operation TEXT NOT NULL,
                rule_json TEXT NOT NULL,
                verified INTEGER NOT NULL CHECK (verified = 1)
            )"""
        )
        self.connection.commit()

    def add_verified(self, lesson_id, operation, rule):
        if operation not in ("addition", "multiplication", "subtraction"):
            raise ValueError("Unknown operation")
        if rule not in ("compute_sum", "compute_product", "compute_difference"):
            raise ValueError("Unknown rule")
        allowed = {"addition": "compute_sum", "multiplication": "compute_product",
                   "subtraction": "compute_difference"}
        if allowed[operation] != rule:
            raise ValueError("Rule mismatches operation")
        self.connection.execute(
            "INSERT INTO lessons (lesson_id, operation, rule_json, verified) VALUES (?, ?, ?, 1)",
            (lesson_id, operation, json.dumps({"rule": rule}, sort_keys=True)),
        )
        self.connection.commit()

    def retrieve(self, operation):
        row = self.connection.execute(
            "SELECT rule_json FROM lessons WHERE operation=? AND verified=1 ORDER BY lesson_id LIMIT 1",
            (operation,),
        ).fetchone()
        return json.loads(row[0])["rule"] if row else None

    def close(self):
        self.connection.close()
