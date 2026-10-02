"""Golden reasoning tests for scenarios A, B, C.

Each scenario side runs in its own subprocess (one PeTTa engine per
process, exactly like production). Golden truth values were captured from
the first correct run and hand-checked against the NAL formulas in
Omega's lib_nal.metta (deduction: f=f1*f2, c=f1*f2*c1*c2; revision:
w=c/(1-c), f=(w1f1+w2f2)/(w1+w2), c=(w1+w2)/(w1+w2+1)).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parent.parent
ENV = dict(os.environ, PETTA_PATH=str(AGENT / "vendor" / "petta"))


def run_side(side: str, which: str, packet: Path) -> dict:
    r = subprocess.run(
        [sys.executable, "-m", "tests.scenario_runner", side, which, str(packet)],
        cwd=AGENT, env=ENV, capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, f"{side} {which} failed:\n{r.stderr[-3000:]}"
    return json.loads(r.stdout.strip().splitlines()[-1])


@pytest.fixture(scope="module")
def scenario_a(tmp_path_factory):
    d = tmp_path_factory.mktemp("sa")
    edge = run_side("edge", "A", d / "pk.json")
    full = run_side("full", "A", d / "pk.json")
    return edge, full


@pytest.fixture(scope="module")
def scenario_b(tmp_path_factory):
    d = tmp_path_factory.mktemp("sb")
    edge = run_side("edge", "B", d / "pk.json")
    full = run_side("full", "B", d / "pk.json")
    return edge, full


@pytest.fixture(scope="module")
def scenario_c(tmp_path_factory):
    d = tmp_path_factory.mktemp("sc")
    edge = run_side("edge", "C", d / "pk.json")
    full = run_side("full", "C", d / "pk.json")
    return edge, full


# ---------------------------------------------------------------- scenario A

def test_a_edge_urgent(scenario_a):
    edge, _ = scenario_a
    d = edge["edge"]
    assert edge["queued"] is True
    assert d["level"] == "urgent"
    assert d["conclusion"] == "urgent-referral"
    assert d["rule"]["id"] == "r_htn_symptom"
    assert d["rule"]["pack"] == "edge-v1"
    assert d["band"] == "act"
    # rule (0.9,0.9) x htn (1.0,0.9545) x severe-symptom (1.0,0.8889)
    assert d["truth"]["f"] == pytest.approx(0.9, abs=1e-3)
    assert d["truth"]["c"] == pytest.approx(0.6185, abs=1e-3)
    statuses = {p["id"]: p["status"] for p in d["premises"]}
    assert statuses["htn"] == "revised"
    assert statuses["severe-symptom"] == "revised"


def test_a_reconcile_emergency(scenario_a):
    _, full = scenario_a
    d = full["reconciled"]
    assert d["level"] == "emergency"
    assert d["conclusion"] == "pre-eclampsia-severe"
    assert d["rule"]["id"] == "r_pe_severe_symp"
    assert d["rule"]["pack"] == "full-v1"
    assert d["band"] == "act"
    # chain: (0.95,0.9) x new-onset(1.0,0.9) x proteinuria(1.0,0.9) x severe-symptom(1.0,0.889)
    assert d["truth"]["f"] == pytest.approx(0.95, abs=1e-3)
    assert d["truth"]["c"] == pytest.approx(0.5556, abs=1e-3)


def test_a_reconcile_defeat_and_memory(scenario_a):
    _, full = scenario_a
    premises = {p["id"]: p for p in full["reconciled"]["premises"]}
    # the facility 138/88 taken after nifedipine is defeated, not reassuring
    assert "htn" in premises
    defeated = [p for p in full["reconciled"]["premises"] if p["status"] == "defeated"]
    defeated_ids = {p["id"] for p in defeated}
    assert "htn" in defeated_ids
    assert all(
        by == "treated-before-reading"
        for p in defeated for by in p["defeated_by"]
    )
    # new onset comes from the facility's memory of the 14-week visit
    assert premises["new-onset"]["memory"] is True
    # the diff explains the escalation
    assert "level_changed" in full["diff"]
    assert "premise_from_memory" in full["diff"]
    assert "premise_defeated" in full["diff"]


def test_a_contest_recomputes(scenario_a):
    _, full = scenario_a
    d = full["after_contest"]
    assert d["level"] == "urgent"
    assert d["conclusion"] == "pre-eclampsia"
    assert d["rule"]["id"] == "r_pe"
    assert d["truth"]["f"] == pytest.approx(0.95, abs=1e-3)
    assert d["truth"]["c"] == pytest.approx(0.6579, abs=1e-3)
    assert "level_changed" in full["contest_diff"]


# ---------------------------------------------------------------- scenario B

def test_b_edge_watch(scenario_b):
    edge, _ = scenario_b
    d = edge["edge"]
    assert d["level"] == "watch"
    assert d["rule"]["id"] == "r_htn_unconfirmed"
    assert d["band"] == "hypothesise"
    # two unrepeated readings revise (1.0,0.6)+(1.0,0.6) -> (1.0,0.75),
    # then deduction with the rule (0.8,0.8): 0.8*1*0.8*0.75 = 0.48
    assert d["truth"]["c"] == pytest.approx(0.48, abs=1e-3)


def test_b_reconcile_normal(scenario_b):
    _, full = scenario_b
    d = full["reconciled"]
    assert d["level"] == "normal"
    assert d["conclusion"] == "none"
    # revision pulled the high reading below the action band
    near = {p["id"]: p for p in d["premises"]}
    assert near["htn"]["status"] == "below-threshold"
    assert near["htn"]["truth"]["f"] == pytest.approx(0.2727, abs=1e-3)
    # the rested repeat was NOT defeated (no treatment explains it away)
    defeated = [p for p in d["premises"] if p["status"] == "defeated"]
    assert defeated == []
    assert "level_changed" in full["diff"]


# ---------------------------------------------------------------- scenario C

def test_c_confidence_rises(scenario_c):
    edge, full = scenario_c
    e = edge["edge"]
    r = full["reconciled"]
    assert e["level"] == "urgent" and r["level"] == "urgent"
    assert e["rule"]["id"] == "r_rfm" and r["rule"]["id"] == "r_rfm"
    assert e["truth"]["c"] == pytest.approx(0.578, abs=1e-3)
    assert r["truth"]["c"] == pytest.approx(0.6422, abs=1e-3)
    assert r["truth"]["c"] > e["truth"]["c"]
    assert "premise_revised" in full["diff"]
    assert "level_changed" not in full["diff"]
