"""Offline queue and sync for the community agent.

Packets wait in a JSON outbox while the facility is unreachable. The sync
loop retries every few seconds when online; the UI connectivity toggle and
the background loop both drive flushing. The queue lives in the configured
store (local file in development, Vercel Blob in serverless deployment).
"""
from __future__ import annotations

import asyncio
import json

import httpx


class Outbox:
    def __init__(self, store, peer_url: str | None):
        self.store = store
        self.name = "outbox-community.json"
        self.peer = (peer_url or "").rstrip("/") or None
        self.online = False
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()

    def pending(self) -> list[dict]:
        try:
            return json.loads(self.store.read(self.name) or "[]")
        except json.JSONDecodeError:
            return []

    def _write(self, packets: list[dict]) -> None:
        self.store.write(self.name, json.dumps(packets, indent=1))

    def enqueue(self, packet: dict) -> None:
        packets = [p for p in self.pending() if p["packet_id"] != packet["packet_id"]]
        packets.append(packet)
        self._write(packets)

    def remove(self, packet_id: str) -> None:
        self._write([p for p in self.pending() if p["packet_id"] != packet_id])

    def set_online(self, online: bool) -> None:
        self.online = online

    async def flush(self, client: httpx.AsyncClient | None = None) -> list[str]:
        """Try to sync every pending packet. Returns synced packet ids."""
        if not self.online or not self.peer:
            return []
        synced: list[str] = []
        close = client is None
        client = client or httpx.AsyncClient(timeout=5.0)
        try:
            for packet in self.pending():
                try:
                    r = await client.post(f"{self.peer}/sync", json=packet)
                    if r.status_code == 200 and r.json().get("ok"):
                        synced.append(packet["packet_id"])
                        self.remove(packet["packet_id"])
                except httpx.HTTPError:
                    break  # peer unreachable; keep queued
        finally:
            if close:
                await client.aclose()
        return synced

    async def start_loop(self, interval: float = 5.0) -> None:
        self._stop.clear()

        async def loop() -> None:
            while not self._stop.is_set():
                try:
                    await self.flush()
                except Exception:
                    pass
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=interval)
                except asyncio.TimeoutError:
                    pass

        self._task = asyncio.create_task(loop())

    async def stop_loop(self) -> None:
        self._stop.set()
        if self._task:
            await asyncio.gather(self._task, return_exceptions=True)
