"""Jev integration: fallback paths and the gate, with a mocked client."""
from __future__ import annotations

import asyncio
import json

import pytest

from mizani.jev import JevClient, _gate, _strip_pii


def test_no_key_falls_back(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    c = JevClient(api_key=None)
    monkeypatch.setenv("TYPESAFE_API_KEY", "")
    res = asyncio.run(c.extract("Mama analalamika kichwa kinauma sana"))
    assert res.mode == "offline_manual"


def test_gate_logic():
    assert _gate({"choice": "present", "confidence": 0.9,
                  "probabilities": {"present": 0.9}}) == "present"
    assert _gate({"choice": "absent", "confidence": 0.9,
                  "probabilities": {"absent": 0.9, "present": 0.02}}) == "absent"
    assert _gate({"choice": "absent", "confidence": 0.4,
                  "probabilities": {"absent": 0.6, "present": 0.3}}) == "needs-review"
    assert _gate({"choice": "not_mentioned", "confidence": 0.9,
                  "probabilities": {"not_mentioned": 0.7, "present": 0.2}}) == "needs-review"


def test_strip_pii():
    assert "0712345678" not in _strip_pii("call 0712345678 now")
    assert _strip_pii("no phone here") == "no phone here"


def test_mocked_client_extract(monkeypatch):
    """A fake typesafe SDK: extract returns gated signs and the picked BP."""

    class FakeResp:
        request_id = "req_fake"

        class raw_http_response:
            @staticmethod
            def json():
                answers = {}
                for name in [
                    "severe-headache", "visual-disturbance", "convulsions",
                    "vaginal-bleeding", "fever", "severe-abdominal-pain", "rfm",
                    "swelling-face-hands", "breathing-difficulty",
                    "membranes-ruptured", "in-labour",
                ]:
                    answers[f"sign__{name}"] = {
                        "choice": "not_mentioned", "confidence": 0.99,
                        "probabilities": {"not_mentioned": 0.99, "present": 0.0, "absent": 0.01},
                    }
                answers["sign__severe-headache"] = {
                    "choice": "present", "confidence": 1.0,
                    "probabilities": {"present": 1.0, "absent": 0.0, "not_mentioned": 0.0},
                }
                answers["bp_today"] = {
                    "choice": "152/98", "confidence": 0.99,
                    "probabilities": {"152/98": 0.99, "12/10": 0.01},
                }
                return {"model": "jev-1.13.0", "answers": answers}

    class FakeClient:
        async def system_one(self, state, questions):
            return FakeResp()

    c = JevClient(api_key="fake")

    async def fake_make():
        return FakeClient()

    monkeypatch.setattr(c, "_make_client", fake_make)
    res = asyncio.run(c.extract("kichwa kinauma sana. BP 152/98 leo, 12/10 tarehe"))
    assert res.mode == "jev"
    by_name = {s.name: s for s in res.signs}
    assert by_name["severe-headache"].status == "present"
    assert by_name["fever"].status == "not-mentioned"
    assert res.bp["systolic"] == 152 and res.bp["diastolic"] == 98


def test_questions_cover_all_signs():
    c = JevClient(api_key="fake")
    qs = c._questions()
    from mizani.jev import SIGNS
    assert set(qs.keys()) == {f"sign__{n}" for n in SIGNS}
    assert "convulsions" in SIGNS
    assert "NOT convulsions" in SIGNS["convulsions"]
    assert "feet or legs does NOT count" in SIGNS["swelling-face-hands"]
