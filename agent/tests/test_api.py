"""API tests against two real agent processes (community :18101, facility :18102).

Spawns uvicorn subprocesses with a temporary memory dir, exactly like
`make dev`, then exercises the HTTP surface of both roles, including the
offline queue and the sync between them.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest

AGENT = Path(__file__).resolve().parent.parent
COMM = "http://127.0.0.1:18101"
FAC = "http://127.0.0.1:18102"

VISIT = {
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
    ],
}


def wait_up(url: str, timeout: float = 60.0) -> None:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = httpx.get(f"{url}/health", timeout=2.0)
            if r.status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.5)
    raise RuntimeError(f"{url} did not come up")


FACILITY_MEMORY = [
    '(mother M-AMINA (age 27) (gravida 2) (para 1))',
    '(encounter E-03 M-AMINA (site facility) (by nurse) (ga-weeks 14) (at "2026-05-14T10:00"))',
    '(reading R-01 E-03 sbp 116)',
    '(reading R-02 E-03 dbp 74)',
    '(prov R-01 (repeated yes) (after-treatment none) (device aneroid))',
    '(prov R-02 (repeated yes) (after-treatment none) (device aneroid))',
]


@pytest.fixture(scope="module")
def agents(tmp_path_factory):
    mem = tmp_path_factory.mktemp("mem")
    # facility remembers Amina's earlier visits before the agents start
    lines = "".join(f"(event 2026-10-02T08:00:00 add {a})\n" for a in FACILITY_MEMORY)
    (mem / "log-facility.jsonl").write_text(lines)
    env = dict(
        os.environ,
        PETTA_PATH=str(AGENT / "vendor" / "petta"),
        MIZANI_MEMORY_DIR=str(mem),
        MIZANI_PEER=FAC,
        PYTHONPATH=str(AGENT),
    )
    procs = []
    for role, port in [("community", 18101), ("facility", 18102)]:
        p = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "mizani.app:create_app",
             "--factory", "--port", str(port)],
            cwd=AGENT, env={**env, "MIZANI_ROLE": role},
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        procs.append(p)
    try:
        wait_up(COMM)
        wait_up(FAC)
        yield {"mem": mem}
    finally:
        for p in procs:
            p.send_signal(signal.SIGINT)  # clean exit so coverage data is written
        for p in procs:
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                p.kill()


def test_health(agents):
    hc = httpx.get(f"{COMM}/health").json()
    hf = httpx.get(f"{FAC}/health").json()
    assert hc["role"] == "community" and hc["pack"] == "edge-v1"
    assert hf["role"] == "facility" and hf["pack"] == "full-v1"
    assert hc["omega_commit"] == hf["omega_commit"] == "31ff0aad"
    assert hc["petta"] in {"v1.0.4", "hyperon-0.2.10 (serverless runtime)"}


def test_rules_listed(agents):
    rc = httpx.get(f"{COMM}/rules").json()
    rf = httpx.get(f"{FAC}/rules").json()
    edge_ids = {r["id"] for r in rc["rules"]}
    full_ids = {r["id"] for r in rf["rules"]}
    assert {"r_htn_symptom", "r_htn_unconfirmed"} <= edge_ids
    assert {"r_pe", "r_pe_severe_symp", "r_shock", "r_pph"} <= full_ids
    assert "r_pe" not in edge_ids


def test_visit_offline_queues_then_syncs(agents):
    # offline visit: decision urgent, packet queued, nothing at facility yet
    r = httpx.post(f"{COMM}/visits", json=VISIT)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["decision"]["level"] == "urgent"
    assert body["decision"]["rule"]["id"] == "r_htn_symptom"
    assert body["queued"] is True
    assert httpx.get(f"{COMM}/outbox").json()["pending"]

    inbox = httpx.get(f"{FAC}/referrals").json()["referrals"]
    assert inbox == []

    # connectivity returns: the packet syncs
    r = httpx.post(f"{COMM}/connectivity", json={"online": True})
    assert r.status_code == 200
    assert r.json()["pending"] == 0
    inbox = httpx.get(f"{FAC}/referrals").json()["referrals"]
    assert len(inbox) == 1
    assert inbox[0]["edge_level"] == "urgent"
    assert inbox[0]["reconciled_level"] is None


def test_facility_encounter_reconcile_contest(agents):
    ref = httpx.get(f"{FAC}/referrals").json()["referrals"][0]["referral_id"]
    enc = {
        "referral_id": ref,
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
    }
    r = httpx.post(f"{FAC}/encounters", json=enc)
    assert r.status_code == 200, r.text
    refd = r.json()
    assert refd["reconciled"]["level"] == "emergency"
    assert refd["reconciled"]["rule"]["id"] == "r_pe_severe_symp"
    assert "level_changed" in [c["type"] for c in refd["diff"]["changes"]]

    for pid in ["severe-headache", "visual-disturbance"]:
        r = httpx.post(f"{FAC}/referrals/{ref}/contest",
                       json={"premise_id": pid,
                             "reason": "symptom resolved after paracetamol",
                             "by": "nurse-baraka"})
        assert r.status_code == 200, r.text
    refd = r.json()
    assert refd["reconciled"]["level"] == "urgent"
    assert refd["reconciled"]["rule"]["id"] == "r_pe"


def test_mother_memory_and_audit(agents):
    m = httpx.get(f"{FAC}/mothers/M-AMINA").json()
    assert m["mother_id"] == "M-AMINA"
    sites = {e["site"] for e in m["encounters"]}
    assert sites == {"home", "facility"}
    log = httpx.get(f"{FAC}/memory/log").json()["events"]
    assert any("(contested" in e["atom"] for e in log)
    assert any("(referral" in e["atom"] for e in log)
    raw = httpx.get(f"{FAC}/memory/export")
    assert raw.status_code == 200 and raw.text.startswith("(event")


def test_mothers_list(agents):
    m = httpx.get(f"{FAC}/mothers").json()["mothers"]
    ids = {x["id"] for x in m}
    assert "M-AMINA" in ids
    amina = next(x for x in m if x["id"] == "M-AMINA")
    assert amina["age"] == 27 and amina["ga_weeks"] == 34.0


def test_override_then_approve_bumps_rule(agents):
    ref = httpx.get(f"{FAC}/referrals").json()["referrals"][0]["referral_id"]
    r = httpx.post(f"{FAC}/referrals/{ref}/override",
                   json={"level": "urgent",
                         "reason": "reviewer judged the severe symptom differently",
                         "by": "dr-otieno"})
    assert r.status_code == 200, r.text
    patch = r.json()
    assert patch["status"] == "proposed"
    assert patch["rule_id"] == "r_pe"
    r = httpx.post(f"{FAC}/rules/patches/{patch['id']}/approve")
    assert r.status_code == 200, r.text
    approved = r.json()
    assert approved["status"] == "approved"
    assert approved["version"] == "v1.1"
    assert approved["old"] != approved["new"]
    # the rule version is now visible in the rules endpoint
    rules = httpx.get(f"{FAC}/rules").json()["rules"]
    versions = {x["id"]: x["version"] for x in rules}
    assert versions["r_pe"] == "v1.1"


def test_invalid_reading_rejected(agents):
    bad = dict(VISIT, readings=[{"kind": "sbp", "value": 999}])
    r = httpx.post(f"{COMM}/visits", json=bad)
    assert r.status_code == 400


def test_injection_rejected(agents):
    bad = dict(VISIT, mother={"id": 'M-1") (remove-atom &self (x', "age": 27, "gravida": 2, "para": 1})
    r = httpx.post(f"{COMM}/visits", json=bad)
    assert r.status_code in {400, 422}
