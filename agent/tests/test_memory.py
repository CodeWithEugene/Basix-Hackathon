"""Memory: restarting the engine and replaying the log keeps every decision."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

AGENT = Path(__file__).resolve().parent.parent
ENV = dict(os.environ, PETTA_PATH=str(AGENT / "vendor" / "petta"))

SCRIPT = """
import json, sys
from mizani.app import AgentState, record_visit
from mizani.schemas import VisitInput
from tests.scenario_runner import VISITS

mem = sys.argv[1]
phase = sys.argv[2]
if phase == "write":
    comm = AgentState("community", memory_dir=mem, peer=None)
    res = record_visit(comm, VisitInput(**VISITS["A"]))
    print(json.dumps(res["decision"]))
else:
    comm = AgentState("community", memory_dir=mem, peer=None)
    assert comm.memory.count > 0, "log should have events"
    did = open(mem + "/decision-id.txt").read().strip()
    d = comm.decisions.get(did)
    assert d is not None, "decision should survive restart"
    print(json.dumps(d))
"""


def run_phase(mem: Path, phase: str) -> dict:
    r = subprocess.run(
        [sys.executable, "-c", SCRIPT, str(mem), phase],
        cwd=AGENT, env=ENV, capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, f"phase {phase} failed:\n{r.stderr[-2000:]}"
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_replay_keeps_decisions(tmp_path):
    before = run_phase(tmp_path, "write")
    (tmp_path / "decision-id.txt").write_text(before["id"])
    after = run_phase(tmp_path, "replay")
    assert before["level"] == after["level"] == "urgent"
    assert before["rule"]["id"] == after["rule"]["id"] == "r_htn_symptom"
    assert before["truth"] == after["truth"]
    assert before["proof_raw"] == after["proof_raw"]
