"""Persistent memory: an append-only event log of atoms per agent.

Every mutation goes through Memory.apply: write to the atom space, then
append to the log, then fsync. Startup replays the log in order, in the
same spirit as Omega's memory/history.metta episodic trace.
"""
from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine


class Memory:
    def __init__(self, engine: Engine, memory_dir: Path, role: str):
        self.engine = engine
        self.dir = Path(memory_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.role = role
        self.log_path = self.dir / f"{role}.metta"
        self.decisions_path = self.dir / f"decisions-{role}.jsonl"
        self.count = 0

    def replay(self) -> int:
        """Replay the event log into the atom space. Returns event count."""
        if not self.log_path.exists():
            return 0
        n = 0
        with open(self.log_path) as f:
            for line in f:
                line = line.strip()
                if not line.startswith("(event"):
                    continue
                inner = line[len("(event "):-1]
                _ts, rest = inner.split(" ", 1)
                op, atom = rest.split(" ", 1)
                self.engine.run(f"!({op}-atom &self {atom})")
                n += 1
        self.count = n
        return n

    def apply(self, op: str, atom: str) -> None:
        """Apply one mutation: atom space first, then the log, then fsync.

        Adds are idempotent: if the space already holds the atom, nothing is
        written and no event is logged (PeTTa spaces are multisets, so a
        duplicate add would duplicate evidence).
        """
        if op not in {"add", "remove"}:
            raise ValueError(f"op must be add or remove, got {op}")
        if op == "add" and self.exists(atom):
            return
        self.engine.run(f"!({op}-atom &self {atom})")
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        with open(self.log_path, "a") as f:
            f.write(f"(event {ts} {op} {atom})\n")
            f.flush()
            os.fsync(f.fileno())
        self.count += 1

    def exists(self, atom: str) -> bool:
        out = self.engine.run(f"!(collapse (match &self {atom} true))")
        return bool(out) and out[0] not in {"", "()"}

    def query(self, code: str) -> list[str]:
        return self.engine.run(code)

    def log_events(self, limit: int = 500, offset: int = 0) -> list[dict]:
        """Read the log newest-first for the audit endpoint."""
        if not self.log_path.exists():
            return []
        events = []
        with open(self.log_path) as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line.startswith("(event"):
                    continue
                inner = line[len("(event "):-1]
                ts, rest = inner.split(" ", 1)
                op, atom = rest.split(" ", 1)
                events.append({"n": i + 1, "ts": ts, "op": op, "atom": atom})
        events.reverse()
        return events[offset:offset + limit]

    def raw_log(self) -> str:
        if not self.log_path.exists():
            return ""
        return self.log_path.read_text()

    # --- decisions sidecar (JSON; outputs, rebuilt by replaying inputs) ---

    def save_decision(self, decision: dict) -> None:
        with open(self.decisions_path, "a") as f:
            f.write(json.dumps(decision) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def load_decisions(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        if not self.decisions_path.exists():
            return out
        with open(self.decisions_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                out[d["id"]] = d
        return out
