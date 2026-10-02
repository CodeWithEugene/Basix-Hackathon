"""TypeSafe Jev client: reads visit notes into typed danger-sign observations.

Jev reads; Omega decides. Jev never produces a number, a threshold, a risk
level, an action or an explanation. Every answer is gated; uncertain answers
become needs_review for the health worker to confirm. Any failure returns
mode=offline_manual and the UI falls back to manual toggles.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from typing import Any

from .schemas import ExtractResult, ExtractedSign

MODEL = "jev-1.13.0"
CONFIDENCE_FLOOR = 0.60
PRESENT_REVIEW_FLOOR = 0.15

BP_RE = re.compile(r"\b(\d{2,3})\s*/\s*(\d{2,3})\b")
PHONE_RE = re.compile(r"\b(?:\+?254|0)\d{9}\b")
NAME_RE = re.compile(r"\b(?:mama|mama\s+kubwa|mzee)\s+[A-Z][a-z]+\b")

# The ten danger signs, with clinical exclusion criteria in the definitions.
SIGNS: dict[str, str] = {
    "severe-headache": "A very strong headache, not a mild one.",
    "visual-disturbance": "Blurred vision, seeing darkness or spots, or temporary loss of sight.",
    "convulsions": "Fits or convulsions (kifafa, degedege): shaking of the whole body, loss of consciousness, or rolling eyes. Shivering from fever, dizziness, confusion or talking strangely are NOT convulsions.",
    "vaginal-bleeding": "Any bleeding from the vagina, including spotting, during pregnancy or after birth.",
    "fever": "Fever or a hot body (homa), measured or reported.",
    "severe-abdominal-pain": "Severe pain in the abdomen, not a mild backache or normal cramps.",
    "rfm": "The baby is moving less than usual, has stopped moving, or the mother reports reduced fetal movement.",
    "swelling-face-hands": "Swelling of the face or hands. Swelling of only the feet or legs does NOT count.",
    "breathing-difficulty": "Difficulty breathing, fast breathing, or being unable to breathe well at rest.",
    "membranes-ruptured": "The waters have broken (maji yamevunja), with or without labour.",
    "in-labour": "The mother is in labour now (uchungu, labour pains).",
}

STATUS_CRITERIA = {
    "present": "The note says the mother has this sign now (reported by her, a relative, or observed by the CHP).",
    "absent": "The note explicitly says the mother does NOT have this sign.",
    "not_mentioned": "The note says nothing about this sign either way.",
}


def _strip_pii(note: str) -> str:
    note = PHONE_RE.sub("[phone]", note)
    note = NAME_RE.sub(lambda m: m.group(0).split()[0], note)
    return note


def _gate(answer: dict) -> str:
    if answer.get("confidence", 0.0) < CONFIDENCE_FLOOR:
        return "needs-review"
    if answer.get("choice") != "present" and answer.get("probabilities", {}).get("present", 0.0) > PRESENT_REVIEW_FLOOR:
        return "needs-review"
    return answer.get("choice", "not_mentioned").replace("_", "-")


class JevClient:
    """Async Jev client with a hard fallback to manual entry."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY")
        self._client = None

    def available(self) -> bool:
        return bool(self.api_key)

    async def _make_client(self):
        if self._client is not None:
            return self._client
        from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy  # type: ignore
        self._client = AsyncTypeSafeClient(
            api_key=self.api_key,
            model=MODEL,
            timeout=3.0,
            retry=RetryPolicy(max_retries=1, backoff_initial=0.3, backoff_max=1.0, timeout=4.0),
        )
        return self._client

    def _questions(self) -> dict:
        from typesafe_sdk import Choice  # type: ignore
        qs = {}
        for name, definition in SIGNS.items():
            qs[f"sign__{name}"] = Choice(
                instructions={
                    "danger_sign": {"sign": name, "definition": definition},
                    "context": "`visit_note` is a Community Health Promoter's note about a pregnant or recently delivered mother in Kenya. It may be in English, Swahili, or Sheng.",
                    "question": "According to `visit_note`, what is the status of `danger_sign` for the mother?",
                },
                criteria=STATUS_CRITERIA,
            )
        return qs

    async def extract(self, note: str) -> ExtractResult:
        """One request per note: every sign Choice plus the BP pick."""
        if not self.available():
            return ExtractResult(mode="offline_manual", error="no_api_key")
        clean = _strip_pii(note)
        try:
            from typesafe_sdk import Choice, TypeSafeError  # type: ignore
            client = await self._make_client()
        except Exception as exc:  # SDK not installed / client failed
            return ExtractResult(mode="offline_manual", error=type(exc).__name__)

        questions = self._questions()
        candidates = list(dict.fromkeys(f"{a}/{b}" for a, b in BP_RE.findall(clean)))
        if candidates:
            criteria = {c: None for c in candidates}
            criteria["none"] = "No blood pressure was measured today."
            questions["bp_today"] = Choice(
                instructions="Which value in `visit_note` is the mother's blood pressure measured at TODAY's visit? Ignore readings from earlier visits.",
                criteria=criteria,
            )
        q_hash = hashlib.sha256(
            json.dumps(sorted(questions.keys())).encode()
        ).hexdigest()[:16]

        t0 = time.perf_counter()
        try:
            resp = await client.system_one({"visit_note": clean}, questions)
        except Exception as exc:
            return ExtractResult(mode="offline_manual", error=type(exc).__name__)
        latency_ms = round((time.perf_counter() - t0) * 1000)

        raw = resp.raw_http_response.json()
        answers = raw.get("answers", {})
        out_signs: list[ExtractedSign] = []
        for name in SIGNS:
            a = answers.get(f"sign__{name}")
            if not a:
                continue
            out_signs.append(ExtractedSign(
                name=name,
                status=_gate(a),
                jev_confidence=a.get("confidence"),
                probabilities=a.get("probabilities"),
            ))
        bp = None
        bp_a = answers.get("bp_today")
        if bp_a and bp_a.get("choice") not in {None, "none"} and bp_a.get("confidence", 0) >= CONFIDENCE_FLOOR:
            s, d = bp_a["choice"].split("/")
            bp = {
                "systolic": int(s), "diastolic": int(d),
                "candidates": candidates, "picked": bp_a["choice"],
                "confidence": bp_a.get("confidence"),
            }
        return ExtractResult(
            mode="jev",
            signs=out_signs,
            bp=bp,
            model=raw.get("model", MODEL),
            request_id=resp.request_id,
        )
