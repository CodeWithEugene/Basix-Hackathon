"""Outbox: queueing, dedupe, and flush behaviour with a mock peer."""
from __future__ import annotations

import asyncio

import httpx
import pytest

from mizani.outbox import Outbox


def make_transport(calls: list[str], fail: bool = False):
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        if fail:
            raise httpx.ConnectError("peer down")
        return httpx.Response(200, json={"ok": True, "referral_id": "REF-F1"})

    return httpx.MockTransport(handler)


def test_enqueue_dedupes_and_removes(tmp_path):
    ob = Outbox(tmp_path, "http://peer")
    ob.enqueue({"packet_id": "PK-1", "x": 1})
    ob.enqueue({"packet_id": "PK-1", "x": 2})
    assert ob.pending() == [{"packet_id": "PK-1", "x": 2}]
    ob.remove("PK-1")
    assert ob.pending() == []


def test_offline_flush_is_noop(tmp_path):
    ob = Outbox(tmp_path, "http://peer")
    ob.enqueue({"packet_id": "PK-1"})
    assert asyncio.run(ob.flush()) == []  # offline by default
    ob.set_online(True)
    ob.peer = None
    assert asyncio.run(ob.flush()) == []  # no peer configured


def test_flush_syncs_and_clears(tmp_path):
    calls: list[str] = []
    ob = Outbox(tmp_path, "http://peer")
    ob.set_online(True)
    ob.enqueue({"packet_id": "PK-1"})
    ob.enqueue({"packet_id": "PK-2"})
    client = httpx.AsyncClient(transport=make_transport(calls))
    synced = asyncio.run(ob.flush(client))
    assert synced == ["PK-1", "PK-2"]
    assert ob.pending() == []
    assert calls == ["http://peer/sync", "http://peer/sync"]
    asyncio.run(client.aclose())


def test_flush_keeps_queue_when_peer_down(tmp_path):
    calls: list[str] = []
    ob = Outbox(tmp_path, "http://peer")
    ob.set_online(True)
    ob.enqueue({"packet_id": "PK-1"})
    client = httpx.AsyncClient(transport=make_transport(calls, fail=True))
    assert asyncio.run(ob.flush(client)) == []
    assert len(ob.pending()) == 1
    asyncio.run(client.aclose())
