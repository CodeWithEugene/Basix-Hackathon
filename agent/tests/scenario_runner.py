"""Run one scenario side in a fresh process and print JSON.

Usage:
  python scenario_runner.py edge <A|B|C> <packet_out.json>
  python scenario_runner.py full <A|B|C> <packet_in.json>

The community and facility sides always run in separate processes, exactly
like production (one PeTTa engine, one atom space, per process).
"""
import json
import sys
import tempfile

from mizani import atoms  # noqa: F401  (kept for parity with app)
from mizani.app import (
    AgentState,
    do_contest,
    record_facility_encounter,
    record_visit,
    sync_packet,
)
from mizani.schemas import ContestInput, FacilityEncounterInput, VisitInput


def slim(decision):
    if not decision:
        return None
    return {
        "id": decision["id"],
        "level": decision["level"],
        "conclusion": decision["conclusion"],
        "rule": decision["rule"],
        "truth": decision["truth"],
        "band": decision["band"],
        "premises": [
            {
                "id": p["id"],
                "status": p["status"],
                "truth": p["truth"],
                "withdrawn": p.get("withdrawn", []),
                "defeated_by": [
                    s.get("by") for s in p.get("sources", []) if s.get("kind") == "defeated"
                ],
                "memory": any(s.get("memory") for s in p.get("sources", [])),
            }
            for p in decision["premises"]
        ],
    }


VISITS = {
    "A": {
        "mother": {"id": "M-AMINA", "age": 27, "gravida": 2, "para": 1},
        "ga_weeks": 34,
        "at": "2026-10-02T21:40",
        "readings": [
            {"kind": "sbp", "value": 152},
            {"kind": "dbp", "value": 98},
            {"kind": "sbp", "value": 150, "repeated": True},
            {"kind": "dbp", "value": 96, "repeated": True},
        ],
        "signs": [
            {"name": "severe-headache", "status": "present", "source": "chp"},
            {"name": "visual-disturbance", "status": "present", "source": "chp"},
            {"name": "swelling-face-hands", "status": "not-mentioned", "source": "chp"},
        ],
    },
    "B": {
        "mother": {"id": "M-WANJIKU", "age": 31, "gravida": 3, "para": 2},
        "ga_weeks": 30,
        "at": "2026-10-02T11:20",
        "readings": [
            {"kind": "sbp", "value": 142},
            {"kind": "dbp", "value": 92},
        ],
        "signs": [],
    },
    "C": {
        "mother": {"id": "M-NAFULA", "age": 24, "gravida": 1, "para": 0},
        "ga_weeks": 36,
        "at": "2026-10-02T17:45",
        "readings": [
            {"kind": "sbp", "value": 118, "repeated": True},
            {"kind": "dbp", "value": 76, "repeated": True},
        ],
        "signs": [
            {"name": "rfm", "status": "present", "source": "chp"},
        ],
    },
}

FACILITY_MEMORY = {
    "A": [
        '(mother M-AMINA (age 27) (gravida 2) (para 1))',
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
    ],
    "B": [
        '(mother M-WANJIKU (age 31) (gravida 3) (para 2))',
        '(encounter E-11 M-WANJIKU (site facility) (by nurse) (ga-weeks 12) (at "2026-04-30T09:00"))',
        '(reading R-11 E-11 sbp 118)',
        '(reading R-12 E-11 dbp 76)',
        '(prov R-11 (repeated yes) (after-treatment none) (device aneroid))',
        '(prov R-12 (repeated yes) (after-treatment none) (device aneroid))',
    ],
    "C": [
        '(mother M-NAFULA (age 24) (gravida 1) (para 0))',
    ],
}

FACILITY_ENCOUNTERS = {
    "A": {
        "at": "2026-10-02T23:30",
        "readings": [
            {"kind": "sbp", "value": 138},
            {"kind": "dbp", "value": 88},
            {"kind": "sbp", "value": 148, "repeated": True},
            {"kind": "dbp", "value": 96, "repeated": True},
            {"kind": "protein", "value": 2, "repeated": True},
        ],
        "treatment": "nifedipine-oral",
        "treatment_at": "2026-10-02T22:50",
    },
    "B": {
        "at": "2026-10-02T15:10",
        "readings": [
            {"kind": "sbp", "value": 128, "repeated": True},
            {"kind": "dbp", "value": 82, "repeated": True},
            {"kind": "protein", "value": 0, "repeated": True},
        ],
    },
    "C": {
        "at": "2026-10-02T19:20",
        "readings": [
            {"kind": "sbp", "value": 120, "repeated": True},
            {"kind": "dbp", "value": 78, "repeated": True},
        ],
        "signs": [
            {"name": "rfm", "status": "present", "source": "nurse"},
        ],
    },
}


def run_edge(which: str, packet_out: str) -> dict:
    with tempfile.TemporaryDirectory() as d:
        comm = AgentState("community", memory_dir=d, peer=None)
        visit = VisitInput(**VISITS[which])
        res = record_visit(comm, visit)
        packet = comm.outbox.pending()[0]
        with open(packet_out, "w") as f:
            json.dump(packet, f)
        return {"edge": slim(res["decision"]), "queued": res["queued"]}


def run_full(which: str, packet_in: str) -> dict:
    with tempfile.TemporaryDirectory() as d:
        fac = AgentState("facility", memory_dir=d, peer=None)
        for a in FACILITY_MEMORY[which]:
            fac.memory.apply("add", a)
        with open(packet_in) as f:
            packet = json.load(f)
        r = sync_packet(fac, packet)
        fe = FacilityEncounterInput(referral_id=r["referral_id"], **FACILITY_ENCOUNTERS[which])
        ref = record_facility_encounter(fac, fe)
        out = {
            "reconciled": slim(ref["reconciled"]),
            "diff": [c["type"] for c in ref["diff"]["changes"]],
            "diff_detail": ref["diff"]["changes"],
        }
        if which == "A":
            for pid in ["severe-headache", "visual-disturbance"]:
                ref = do_contest(
                    fac,
                    r["referral_id"],
                    ContestInput(
                        premise_id=pid,
                        reason="symptom resolved after paracetamol",
                        by="nurse-baraka",
                    ),
                )
            out["after_contest"] = slim(ref["reconciled"])
            out["contest_diff"] = [c["type"] for c in ref["diff"]["changes"]]
        return out


if __name__ == "__main__":
    side, which, packet_path = sys.argv[1], sys.argv[2], sys.argv[3]
    if side == "edge":
        print(json.dumps(run_edge(which, packet_path)))
    elif side == "full":
        print(json.dumps(run_full(which, packet_path)))
    else:
        raise SystemExit(f"unknown side {side}")
