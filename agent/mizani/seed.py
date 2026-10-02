"""Synthetic scenarios A, B and C, written through the same code paths as live use.

All names, places and numbers are invented. No real person is represented.

`python -m mizani.seed community` writes the community agent's memory
  (mothers, plus Wanjiku's and Nafula's completed visits; Amina is
  registered but has no encounter yet, so the video starts clean).
`python -m mizani.seed facility` writes the facility agent's memory
  (Amina's 14 and 24 week visits, Wanjiku's 12 week visit, and the synced,
  reconciled referrals for scenarios B and C).

Run community first: it hands the referral packets to the facility seed
through agent/memory/seed-packets.json.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from . import atoms
from .app import AgentState, record_facility_encounter, record_visit, sync_packet
from .atoms import Site
from .schemas import FacilityEncounterInput, VisitInput

MEMORY_DIR = Path(os.environ.get("MIZANI_MEMORY_DIR", Path(__file__).resolve().parent.parent / "memory"))
PACKETS = MEMORY_DIR / "seed-packets.json"

MOTHERS = [
    ("M-AMINA", 27, 2, 1),
    ("M-WANJIKU", 31, 3, 2),
    ("M-NAFULA", 24, 1, 0),
]

AMINA_MEMORY = [
    '(encounter E-03 M-AMINA (site facility) (by nurse) (ga-weeks 14) (at "2026-05-14T10:00"))',
    '(reading R-01 E-03 sbp 116)',
    '(reading R-02 E-03 dbp 74)',
    '(prov R-01 (repeated yes) (after-treatment none) (device aneroid))',
    '(prov R-02 (repeated yes) (after-treatment none) (device aneroid))',
    '(encounter E-08 M-AMINA (site facility) (by nurse) (ga-weeks 24) (at "2026-07-21T10:00"))',
    '(reading R-05 E-08 sbp 124)',
    '(reading R-06 E-08 dbp 80)',
    '(prov R-05 (repeated yes) (after-treatment none) (device aneroid))',
    '(prov R-06 (repeated yes) (after-treatment none) (device aneroid))',
]

WANJIKU_MEMORY = [
    '(encounter E-11 M-WANJIKU (site facility) (by nurse) (ga-weeks 12) (at "2026-04-30T09:00"))',
    '(reading R-11 E-11 sbp 118)',
    '(reading R-12 E-11 dbp 76)',
    '(prov R-11 (repeated yes) (after-treatment none) (device aneroid))',
    '(prov R-12 (repeated yes) (after-treatment none) (device aneroid))',
]

VISIT_B = {
    "mother": {"id": "M-WANJIKU", "age": 31, "gravida": 3, "para": 2},
    "ga_weeks": 30, "at": "2026-10-02T11:20",
    "readings": [{"kind": "sbp", "value": 142}, {"kind": "dbp", "value": 92}],
    "signs": [],
}

VISIT_C = {
    "mother": {"id": "M-NAFULA", "age": 24, "gravida": 1, "para": 0},
    "ga_weeks": 36, "at": "2026-10-02T17:45",
    "readings": [
        {"kind": "sbp", "value": 118, "repeated": True},
        {"kind": "dbp", "value": 76, "repeated": True},
    ],
    "signs": [{"name": "rfm", "status": "present", "source": "chp"}],
}

FACILITY_B = {
    "at": "2026-10-02T15:10",
    "readings": [
        {"kind": "sbp", "value": 128, "repeated": True},
        {"kind": "dbp", "value": 82, "repeated": True},
        {"kind": "protein", "value": 0, "repeated": True},
    ],
}

FACILITY_C = {
    "at": "2026-10-02T19:20",
    "readings": [
        {"kind": "sbp", "value": 120, "repeated": True},
        {"kind": "dbp", "value": 78, "repeated": True},
    ],
    "signs": [{"name": "rfm", "status": "present", "source": "nurse"}],
}


def truncate() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    for p in MEMORY_DIR.glob("*"):
        if p.is_file():
            p.unlink()


def seed_community() -> None:
    state = AgentState("community", memory_dir=MEMORY_DIR, peer=None)
    for mid, age, g, p in MOTHERS:
        state.memory.apply("add", atoms.mother(mid, age, g, p))
    packets = []
    for visit in (VISIT_B, VISIT_C):
        record_visit(state, VisitInput(**visit))
    packets = state.outbox.pending()
    PACKETS.write_text(json.dumps(packets, indent=1))
    # the demo treats B and C as synced long ago; the community outbox is
    # empty and offline, and Amina's encounter is not created yet
    for p in packets:
        state.outbox.remove(p["packet_id"])
    state.outbox.set_online(False)
    print(f"community: {state.memory.count} events, {len(packets)} packets handed off")


def seed_facility() -> None:
    state = AgentState("facility", memory_dir=MEMORY_DIR, peer=None)
    for mid, age, g, p in MOTHERS:
        state.memory.apply("add", atoms.mother(mid, age, g, p))
    for a in AMINA_MEMORY + WANJIKU_MEMORY:
        state.memory.apply("add", a)
    packets = json.loads(PACKETS.read_text())
    for packet, facility_in in zip(packets, (FACILITY_B, FACILITY_C)):
        r = sync_packet(state, packet)
        record_facility_encounter(
            state,
            FacilityEncounterInput(referral_id=r["referral_id"], **facility_in),
        )
    print(f"facility: {state.memory.count} events, {len(state.referrals)} referrals, "
          f"{len(state.decisions)} decisions")


if __name__ == "__main__":
    role = sys.argv[1] if len(sys.argv) > 1 else None
    if role == "truncate":
        truncate()
        print("memory truncated")
    elif role == "community":
        seed_community()
    elif role == "facility":
        seed_facility()
    else:
        raise SystemExit("usage: python -m mizani.seed [truncate|community|facility]")
