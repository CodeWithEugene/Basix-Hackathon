"""Seed: truncates and writes scenarios A, B and C through the real code paths."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

AGENT = Path(__file__).resolve().parent.parent
ENV = dict(os.environ, PETTA_PATH=str(AGENT / "vendor" / "petta"))


def run_seed(role: str, mem: Path) -> str:
    env = dict(ENV, MIZANI_MEMORY_DIR=str(mem))
    r = subprocess.run(
        [sys.executable, "-m", "mizani.seed", role],
        cwd=AGENT, env=env, capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, f"seed {role} failed:\n{r.stderr[-2000:]}"
    return r.stdout


def test_seed_scenarios(tmp_path):
    run_seed("truncate", tmp_path)
    run_seed("community", tmp_path)
    out = run_seed("facility", tmp_path)
    assert "2 referrals" in out

    # the facility holds the seeded referrals and memory
    referrals = [json.loads(l) for l in (tmp_path / "referrals-facility.jsonl").read_text().splitlines() if l.strip()]
    assert len(referrals) == 2
    by_mother = {r["mother_id"]: r for r in referrals}
    assert by_mother["M-WANJIKU"]["reconciled"]["level"] == "normal"
    assert by_mother["M-NAFULA"]["reconciled"]["level"] == "urgent"

    log = (tmp_path / "facility.metta").read_text()
    # Amina's 14-week memory is seeded; no current referral for her
    assert "(encounter E-03 M-AMINA" in log
    assert "(reading R-01 E-03 sbp 116)" in log
    assert "M-AMINA (packet" not in log

    # the community outbox is empty and offline
    assert json.loads((tmp_path / "outbox-community.json").read_text()) == []
