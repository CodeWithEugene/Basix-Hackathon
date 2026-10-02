"""Vercel Blob REST client, shaped after the official @vercel/blob SDK.

Auth: OIDC. The runtime-injected VERCEL_OIDC_TOKEN identifies the project;
the store id goes in the x-vercel-blob-store-id header (without the
"store_" prefix). API base: https://vercel.com/api/blob.
"""
from __future__ import annotations

import os

import httpx

BLOB_API = "https://vercel.com/api/blob"


class BlobClient:
    def __init__(self, store_id: str | None = None, token: str | None = None):
        sid = store_id or os.environ.get("BLOB_STORE_ID", "")
        self.store_id = sid.removeprefix("store_")
        self.token = token or os.environ.get("VERCEL_OIDC_TOKEN", "")
        self.client = httpx.Client(
            headers={
                "authorization": f"Bearer {self.token}",
                "x-vercel-blob-store-id": self.store_id,
                "x-api-version": "11",
            },
            timeout=20.0,
        )

    def _host(self, access: str = "private") -> str:
        return f"https://{self.store_id}.{access}.blob.vercel-storage.com"

    def put(self, pathname: str, data: bytes) -> dict:
        r = self.client.post(
            BLOB_API,
            params={"pathname": pathname, "addRandomSuffix": "0"},
            content=data,
        )
        r.raise_for_status()
        return r.json()

    def get(self, pathname: str) -> str | None:
        url = f"{self._host()}/{pathname}"
        r = self.client.get(url)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.text

    def list(self, prefix: str = "", limit: int = 1000) -> list[dict]:
        r = self.client.get(BLOB_API, params={"prefix": prefix, "limit": str(limit)})
        r.raise_for_status()
        return r.json().get("blobs", [])

    def delete(self, pathnames: list[str]) -> None:
        r = self.client.post(
            f"{BLOB_API}/delete",
            json={"urls": [f"{self._host()}/{p}" for p in pathnames]},
        )
        r.raise_for_status()
