"""PeTTa engine host: loads Omega's lib_nal and the Mizani plugin.

One PeTTa engine per process (janus hosts one SWI-Prolog instance), so the
engine is guarded by a lock and uvicorn must run a single worker per agent.
"""
from __future__ import annotations

import os
import threading
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
VENDOR = AGENT_DIR / "vendor"
OMEGA = VENDOR / "omega"
PETTA = VENDOR / "petta"
PLUGIN = AGENT_DIR / "plugins" / "mizani"

os.environ.setdefault("PETTA_PATH", str(PETTA))

import janus_swi as janus  # noqa: E402
from petta import PeTTa  # noqa: E402

PACKS = {"community": "edge-v1", "facility": "full-v1"}

_OMEGA_RELEASE = "v0.1.20"


def omega_commit() -> str:
    try:
        gitdir = OMEGA / ".git"
        if gitdir.is_file():
            # submodule: .git is a file pointing at the real gitdir
            pointer = gitdir.read_text().strip()
            gitdir = (OMEGA / pointer.split(":", 1)[1].strip()).resolve()
        text = (gitdir / "HEAD").read_text().strip()
        if text.startswith("ref:"):
            ref = (gitdir / text[5:].strip()).read_text().strip()
            return ref[:8]
        return text[:8]
    except OSError:
        return "unknown"


class Engine:
    def __init__(self, role: str):
        self.role = role
        self.pack = PACKS[role]
        janus.query_once(f"assertz(working_dir('{AGENT_DIR}'))")
        self.m = PeTTa()
        self.m.verbose = False  # constructor flag is a truthy string; set after
        self.lock = threading.Lock()
        for f in [
            OMEGA / "lib_nal.metta",           # Omega's NAL, loaded unmodified
            PLUGIN / "shims.metta",
            PLUGIN / "evidence.metta",
            PLUGIN / "reason.metta",
            PLUGIN / "packs" / f"{self.pack}.metta",
        ]:
            self.m.load_metta_file(str(f))

    def run(self, code: str) -> list[str]:
        with self.lock:
            return self.m.process_metta_string(code)

    def health(self) -> dict:
        return {
            "role": self.role,
            "pack": self.pack,
            "omega_commit": omega_commit(),
            "omega_release": _OMEGA_RELEASE,
            "petta": "v1.0.4",
            "swipl": "10.0.2",
        }
