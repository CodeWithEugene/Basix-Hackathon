"""Hyperon engine host: runs Omega's lib_nal.metta on the `hyperon` pip
package (Rust core, wheels for CPython 3.12, no system dependencies).

This is the runtime used for the Vercel serverless deployment, where
SWI-Prolog (and therefore PeTTa) is not available. It implements the same
Engine interface and, per the research notes (G6 to G8), is numerically
identical to PeTTa for our usage:
- min/max shims (hyperon_shims.metta) for Truth_Revision
- we call |-nal directly everywhere (the |- wrapper needs unique-atom on an
  Expression, which hyperon does not evaluate)
- results are filtered to s-expressions whose stv components are numbers,
  because hyperon returns non-matching rules unreduced
"""
from __future__ import annotations

import threading
from pathlib import Path

from hyperon import MeTTa  # type: ignore

AGENT_DIR = Path(__file__).resolve().parent.parent
VENDOR = AGENT_DIR / "vendor"
OMEGA = VENDOR / "omega"
PLUGIN = AGENT_DIR / "plugins" / "mizani"


def _lib_nal_path() -> Path:
    """Prefer the pinned submodule; fall back to the vendored copy."""
    sub = OMEGA / "lib_nal.metta"
    if sub.exists():
        return sub
    return PLUGIN / "vendor" / "lib_nal.metta"

PACKS = {"community": "edge-v1", "facility": "full-v1"}
_OMEGA_RELEASE = "v0.1.20"


def omega_commit() -> str:
    try:
        gitdir = OMEGA / ".git"
        if gitdir.is_file():
            pointer = gitdir.read_text().strip()
            gitdir = (OMEGA / pointer.split(":", 1)[1].strip()).resolve()
        text = (gitdir / "HEAD").read_text().strip()
        if text.startswith("ref:"):
            return (gitdir / text[5:].strip()).read_text().strip()[:8]
        return text[:8]
    except OSError:
        return "unknown"


def _atom_strings(results: list) -> list[str]:
    """Keep only results that look like real output (numeric stv or plain).

    Hyperon returns unevaluated expressions for non-matching rules; those
    contain variables like $x or unreduced calls, never a numeric stv.
    """
    out = []
    for r in results:
        s = str(r)
        if "$" in s:
            continue
        out.append(s)
    return out


class Engine:
    def __init__(self, role: str):
        self.role = role
        self.pack = PACKS[role]
        self.m = MeTTa()
        self.lock = threading.Lock()
        for f in [
            PLUGIN / "hyperon_shims.metta",
            _lib_nal_path(),  # Omega's NAL, loaded unmodified
            PLUGIN / "shims.metta",
            PLUGIN / "evidence.metta",
            PLUGIN / "reason.metta",
            PLUGIN / "packs" / f"{self.pack}.metta",
        ]:
            self._load(f)

    def _load(self, path: Path) -> None:
        with self.lock:
            self.m.run(path.read_text())

    def run(self, code: str) -> list[str]:
        with self.lock:
            results = self.m.run(code)
        flat: list[str] = []
        for r in results:
            if isinstance(r, (list, tuple)):
                flat.extend(_atom_strings(r))
            else:
                flat.append(str(r))
        return flat

    def health(self) -> dict:
        return {
            "role": self.role,
            "pack": self.pack,
            "omega_commit": omega_commit(),
            "omega_release": _OMEGA_RELEASE,
            "petta": "hyperon-0.2.10 (serverless runtime)",
            "swipl": "n/a",
        }
