"""Persistent memory: an append-only event log of atoms per agent.

Every mutation goes through Memory.apply: write to the atom space, then
append to the log. Startup replays the log in order, in the same spirit as
Omega's memory/history.metta episodic trace. The log lives in the configured
store (local files in development, Vercel Blob in serverless deployment).
"""
from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING

from .store import LocalStore

if TYPE_CHECKING:
    from .engine import Engine


class Memory:
    def __init__(self, engine: Engine, store, role: str):
        self.engine = engine
        self.store = store
        self.role = role
        self.log_name = f"log-{role}.jsonl"
        self.decisions_name = f"decisions-{role}.jsonl"
        self.count = 0

    def replay(self) -> int:
        """Replay the event log into the atom space. Returns event count."""
        n = 0
        for line in self.store.read(self.log_name).splitlines():
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
        """Apply one mutation: atom space first, then the log.

        Adds are idempotent: if the space already holds the atom, nothing is
        written and no event is logged (the spaces are multisets, so a
        duplicate add would duplicate evidence).
        """
        if op not in {"add", "remove"}:
            raise ValueError(f"op must be add or remove, got {op}")
        if op == "add" and self.exists(atom):
            return
        self.engine.run(f"!({op}-atom &self {atom})")
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        self.store.append(self.log_name, f"(event {ts} {op} {atom})\n")
        self.count += 1

    def apply_many(self, atoms: list[str]) -> None:
        """Apply many adds with ONE store write (rate-limit friendly)."""
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        lines = []
        for atom in atoms:
            if self.exists(atom):
                continue
            self.engine.run(f"!(add-atom &self {atom})")
            lines.append(f"(event {ts} add {atom})\n")
            self.count += 1
        if lines:
            self.store.append(self.log_name, "".join(lines))

    def exists(self, atom: str) -> bool:
        out = self.engine.run(f"!(collapse (match &self {atom} true))")
        return bool(out) and out[0] not in {"", "()"}

    def query(self, code: str) -> list[str]:
        return self.engine.run(code)

    def log_events(self, limit: int = 500, offset: int = 0) -> list[dict]:
        """Read the log newest-first for the audit endpoint."""
        events = []
        for i, line in enumerate(self.store.read(self.log_name).splitlines()):
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
        return self.store.read(self.log_name)

    # --- decisions sidecar (JSON; outputs, rebuilt by replaying inputs) ---

    def save_decision(self, decision: dict) -> None:
        self.store.append(self.decisions_name, json.dumps(decision) + "\n")

    def load_decisions(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for line in self.store.read(self.decisions_name).splitlines():
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            out[d["id"]] = d
        return out
