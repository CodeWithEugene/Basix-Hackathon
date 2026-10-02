"""Storage backends for agent state.

LocalStore: files under the memory dir (development, one process per role).
BlobStore: Vercel Blob over its REST API (serverless deployment, where the
filesystem is ephemeral and state must be shared across function instances).
Both implement the same tiny file-shaped API; appends read-modify-write,
which is fine at demo scale (single user, a few KB per file).
"""
from __future__ import annotations

import os
from pathlib import Path

import httpx

BLOB_API = "https://blob.vercel-storage.com"


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


class BlobStore:
    """Vercel Blob backend. Token from BLOB_READ_WRITE_TOKEN."""

    def __init__(self, prefix: str = "mizani", token: str | None = None):
        self.token = token or os.environ.get("BLOB_READ_WRITE_TOKEN", "")
        self.prefix = prefix.strip("/")
        self.client = httpx.Client(
            headers={"authorization": f"Bearer {self.token}"},
            timeout=15.0,
        )

    def _path(self, name: str) -> str:
        return f"{self.prefix}/{name}"

    def read(self, name: str) -> str:
        r = self.client.get(
            f"{BLOB_API}/{self._path(name)}",
            params={"download": "1"},
            headers={"x-api-version": "7"},
        )
        if r.status_code in {401, 403, 404}:
            return ""
        r.raise_for_status()
        return r.text

    def write(self, name: str, text: str) -> None:
        r = self.client.put(
            f"{BLOB_API}/{self._path(name)}",
            params={"addRandomSuffix": "0"},
            headers={
                "x-api-version": "7",
                "content-type": "application/octet-stream",
            },
            content=text.encode(),
        )
        r.raise_for_status()

    def append(self, name: str, text: str) -> None:
        self.write(name, self.read(name) + text)

    def delete_all(self, prefix: str = "") -> None:
        r = self.client.get(
            BLOB_API,
            params={"prefix": f"{self.prefix}/{prefix}", "limit": "1000"},
            headers={"x-api-version": "7"},
        )
        if r.status_code != 200:
            return
        blobs = r.json().get("blobs", [])
        if not blobs:
            return
        self.client.request(
            "DELETE",
            BLOB_API,
            headers={"x-api-version": "7", "content-type": "application/json"},
            json={"pathnames": [b["pathname"] for b in blobs]},
        )


def make_store(role: str, memory_dir: Path | None = None):
    """Pick the backend from the environment."""
    if os.environ.get("MIZANI_STORE") == "blob" or os.environ.get("BLOB_READ_WRITE_TOKEN"):
        return BlobStore(prefix=os.environ.get("MIZANI_BLOB_PREFIX", "mizani"))
    return LocalStore(memory_dir or Path("memory"))
