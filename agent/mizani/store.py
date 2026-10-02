"""Storage backends for agent state.

LocalStore: files under the memory dir (development, one process per role).
EdgeConfigStore: Vercel Edge Config over its REST API (serverless deployment,
where the filesystem is ephemeral and state must be shared across function
instances). Both implement the same tiny file-shaped API; appends
read-modify-write, which is fine at demo scale.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx

EDGE_API = "https://api.vercel.com/v1/edge-config"


class LocalStore:
    def __init__(self, memory_dir: Path):
        self.dir = Path(memory_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _p(self, name: str) -> Path:
        return self.dir / name

    def read(self, name: str) -> str:
        p = self._p(name)
        return p.read_text() if p.exists() else ""

    def write(self, name: str, text: str) -> None:
        tmp = self._p(name).with_suffix(".tmp")
        tmp.write_text(text)
        os.replace(tmp, self._p(name))

    def append(self, name: str, text: str) -> None:
        with open(self._p(name), "a") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())

    def delete_all(self, prefix: str = "") -> None:
        for p in self.dir.glob(f"{prefix}*" if prefix else "*"):
            if p.is_file():
                p.unlink()

    def flush(self) -> None:
        return None


class EdgeConfigStore:
    """Vercel Edge Config backend.

    Names map to keys as `mz/<name>`. Auth: a Vercel API token with
    read/write access (VERCEL_API_TOKEN env).

    Writes are buffered in memory and flushed once per key at the end of
    each request (flush()), because Edge Config has a strict write rate
    limit and the agent issues many small writes per request.
    """

    def __init__(self, config_id: str | None = None, token: str | None = None,
                 prefix: str = "mz"):
        self.config_id = config_id or os.environ.get("EDGE_CONFIG_ID", "")
        self.token = token or os.environ.get("VERCEL_API_TOKEN", "")
        self.prefix = prefix.strip("/")
        self.client = httpx.Client(
            headers={"authorization": f"Bearer {self.token}"},
            timeout=15.0,
        )
        self._buffer: dict[str, str] = {}

    def _key(self, name: str) -> str:
        # Edge Config keys: alphanumeric, _ and - only (no dots or slashes)
        return f"{self.prefix}--{name.replace('/', '-').replace('.', '-')}"

    def read(self, name: str) -> str:
        if name in self._buffer:
            return self._buffer[name]
        r = self.client.get(
            f"{EDGE_API}/{self.config_id}/item/{self._key(name)}")
        if r.status_code in {401, 403, 404}:
            return ""
        r.raise_for_status()
        try:
            value = r.json().get("value")
        except json.JSONDecodeError:
            return ""
        if isinstance(value, str):
            return value
        return json.dumps(value) if value is not None else ""

    def write(self, name: str, text: str) -> None:
        self._buffer[name] = text  # coalesced and sent on flush()

    def flush(self) -> None:
        """Write every dirty key once, last value wins."""
        for name, text in self._buffer.items():
            self._write_with_retry(self._key(name), text)
        self._buffer.clear()

    def _write_with_retry(self, key: str, text: str, attempts: int = 4) -> None:
        """Retry Edge Config's 429 write rate limit with backoff."""
        delay = 0.5
        for i in range(attempts):
            r = self.client.patch(
                f"{EDGE_API}/{self.config_id}/items",
                json={"items": [{"operation": "upsert", "key": key, "value": text}]},
            )
            if r.status_code == 429 and i < attempts - 1:
                time.sleep(delay)
                delay *= 2.5
                continue
            r.raise_for_status()
            return

    def append(self, name: str, text: str) -> None:
        self.write(name, self.read(name) + text)

    def delete_all(self, prefix: str = "") -> None:
        names = [
            "log-community.jsonl", "log-facility.jsonl",
            "decisions-community.jsonl", "decisions-facility.jsonl",
            "referrals-facility.jsonl", "referrals-community.jsonl",
            "ids-community.json", "ids-facility.json",
            "outbox-community.json", "seed-packets.json",
        ]
        items = [
            {"operation": "delete", "key": self._key(n)}
            for n in names
            if not prefix or n.startswith(prefix)
        ]
        if not items:
            return
        self._buffer.clear()
        r = self.client.patch(
            f"{EDGE_API}/{self.config_id}/items",
            json={"items": items},
        )
        if r.status_code not in {200, 204, 404}:
            r.raise_for_status()


def make_store(role: str, memory_dir: Path | None = None):
    """Pick the backend from the environment."""
    if os.environ.get("MIZANI_STORE") == "edgeconfig" or os.environ.get("EDGE_CONFIG_ID"):
        return EdgeConfigStore()
    return LocalStore(memory_dir or Path("memory"))
