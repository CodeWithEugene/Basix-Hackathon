"""Mizani FastAPI app factory.

One process per role: MIZANI_ROLE=community (edge pack, outbox) or
MIZANI_ROLE=facility (full pack, the mother's longitudinal record).
The community agent syncs referral packets to the facility's /sync.
"""
from __future__ import annotations

import datetime
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from . import atoms, explain, proof, sexpr
from .atoms import AtomError, IdGen, ReadingKind, Site

# Runtime selection: PeTTa locally (Omega's own runtime on SWI-Prolog),
# hyperon on Vercel serverless (pure pip, identical NAL numbers).
_RUNTIME = os.environ.get("MIZANI_RUNTIME") or (
    "hyperon" if os.environ.get("VERCEL") else "petta"
)
if _RUNTIME == "hyperon":
    from .engine_hyperon import Engine
else:
    from .engine import Engine
from .jev import JevClient
from .memory import Memory
from .outbox import Outbox
from .reasoner import Reasoner
from .store import make_store
from .schemas import (
    ConnectivityInput,
    ContestInput,
    ExtractInput,
    FacilityEncounterInput,
    OverrideInput,
    VisitInput,
)

MEMORY_DIR = Path(os.environ.get("MIZANI_MEMORY_DIR", Path(__file__).resolve().parent.parent / "memory"))


class AgentState:
    def __init__(self, role: str, memory_dir: Path | None = None, peer: str | None = None):
        self.role = role
        self.store = make_store(role, memory_dir or MEMORY_DIR)
        self.engine = Engine(role)
        self.memory = Memory(self.engine, self.store, role)
        self.memory.replay()
        self.reasoner = Reasoner(self.memory)
        self.idgen = IdGen(self._load_ids(), tag="C" if role == "community" else "F")
        self.decisions: dict[str, dict] = self.memory.load_decisions()
        self.referrals: dict[str, dict] = self._load_referrals()
        self.jev = JevClient()
        self.outbox = Outbox(self.store, peer) if role == "community" else None
        self.patches: dict[str, dict] = {}

    # ------------------------------------------------- persistence helpers

    def _ids_name(self) -> str:
        return f"ids-{self.role}.json"

    def _load_ids(self) -> dict[str, int]:
        try:
            return json.loads(self.store.read(self._ids_name()) or "{}")
        except json.JSONDecodeError:
            return {}

    def save_ids(self) -> None:
        self.store.write(self._ids_name(), json.dumps(self.idgen.state()))

    def next_id(self, prefix: str) -> str:
        nid = self.idgen.next(prefix)
        self.save_ids()
        return nid

    def _referrals_name(self) -> str:
        return f"referrals-{self.role}.jsonl"

    def _load_referrals(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for line in self.store.read(self._referrals_name()).splitlines():
            line = line.strip()
            if line:
                r = json.loads(line)
                out[r["referral_id"]] = r
        return out

    def save_referral(self, referral: dict) -> None:
        self.referrals[referral["referral_id"]] = referral
        self.store.write(
            self._referrals_name(),
            "\n".join(json.dumps(r) for r in self.referrals.values()) + "\n",
        )


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


# ------------------------------------------------------------------ helpers

def si_readings(readings: list) -> list:
    """Compute shock-index readings from pulse/sbp pairs (host arithmetic)."""
    sbp = next((r for r in readings if r.kind == "sbp"), None)
    pulse = next((r for r in readings if r.kind == "pulse"), None)
    if sbp and pulse and sbp.value > 0:
        si = round(pulse.value / sbp.value, 3)
        return [{"kind": "si", "value": si, "repeated": sbp.repeated}]
    return []


def build_vitals_atoms(state: AgentState, eid: str, readings: list, device: str,
                       treatment: str | None, treatment_at: str | None) -> list[str]:
    """Build reading + prov atoms (plus computed shock index)."""
    out = []
    all_readings = list(readings) + [
        type("R", (), r) for r in si_readings(readings)
    ]
    for r in all_readings:
        rid = state.next_id("R-")
        kind = ReadingKind(r.kind)
        out.append(atoms.reading(rid, eid, kind, r.value))
        out.append(atoms.prov(rid, getattr(r, "repeated", False), treatment or "none", device))
    if treatment and treatment != "none":
        tid = state.next_id("T-")
        out.append(atoms.treatment(tid, eid, treatment, treatment_at or now_iso()))
    return out


def finalize_decision(state: AgentState, decision: dict) -> dict:
    """Attach explanations, persist the decision, log its atom."""
    en, sw = explain.explain(decision)
    decision["explanation_en"] = en
    decision["explanation_sw"] = sw
    state.decisions[decision["id"]] = decision
    state.memory.save_decision(decision)
    state.memory.apply("add", atoms.decision_event(
        decision["id"], decision["referral_id"], decision["mother_id"],
        decision["level"], decision["conclusion"],
        decision["truth"]["f"], decision["truth"]["c"],
    ))
    return decision


def record_visit(state: AgentState, visit: VisitInput) -> dict:
    """Community: record a visit, run the edge pack, queue the packet."""
    mid = atoms.check_id(visit.mother.id, "mother id")
    matom = atoms.mother(mid, visit.mother.age, visit.mother.gravida, visit.mother.para)
    state.memory.apply("add", matom)

    eid = state.next_id("E-")
    ref = state.next_id("REF-")
    at = visit.at or now_iso()
    encounter_atoms = [
        atoms.encounter(eid, mid, Site.home, "chp", visit.ga_weeks, at),
        atoms.witness(eid, "community"),
        atoms.in_referral(ref, eid),
    ]
    encounter_atoms += build_vitals_atoms(state, eid, visit.readings, visit.device, None, None)
    for s in visit.signs:
        sid = state.next_id("S-")
        encounter_atoms.append(atoms.sign(sid, eid, s.name, s.status, s.source))
    state.memory.apply_many(encounter_atoms)

    did = state.next_id("D-")
    decision = state.reasoner.run_pipeline(ref, mid, did)
    decision = finalize_decision(state, decision)

    packet = {
        "packet_id": state.next_id("PK-"),
        "referral_id": ref,
        "mother": {"id": mid, "age": visit.mother.age,
                   "gravida": visit.mother.gravida, "para": visit.mother.para},
        "atoms": [matom] + encounter_atoms,
        "edge_decision": decision,
        "edge_pack": state.engine.pack,
        "created_at": now_iso(),
    }
    state.outbox.enqueue(packet)
    state.memory.apply("add", atoms.referral_event(ref, mid, packet["packet_id"]))

    synced = False
    if state.outbox.online:
        import anyio
        synced = anyio.run(lambda: state.outbox.flush()) != []  # sync attempts
    return {
        "decision": decision,
        "referral_id": ref,
        "packet_id": packet["packet_id"],
        "queued": not synced,
        "synced": synced,
    }


def sync_packet(state: AgentState, packet: dict) -> dict:
    """Facility: receive a referral packet (idempotent by packet id)."""
    pid = packet["packet_id"]
    for r in state.referrals.values():
        if r["packet_id"] == pid:
            return {"ok": True, "referral_id": r["referral_id"], "detail": "duplicate"}

    ref = packet["referral_id"]
    mid = packet["mother"]["id"]
    state.memory.apply_many(packet["atoms"] + [atoms.referral_event(ref, mid, pid)])

    referral = {
        "referral_id": ref,
        "packet_id": pid,
        "mother_id": mid,
        "mother": packet["mother"],
        "edge_decision": packet["edge_decision"],
        "edge_pack": packet.get("edge_pack", "edge-v1"),
        "encounters": {"community": packet["atoms"], "facility": []},
        "reconciled": None,
        "diff": None,
        "contests": [],
        "status": "synced",
        "created_at": packet.get("created_at") or now_iso(),
    }
    state.save_referral(referral)
    return {"ok": True, "referral_id": ref}


def record_facility_encounter(state: AgentState, inp: FacilityEncounterInput) -> dict:
    """Facility: add arrival readings for a referral, then reconcile."""
    referral = state.referrals.get(inp.referral_id)
    if not referral:
        raise HTTPException(404, f"unknown referral {inp.referral_id}")
    mid = referral["mother_id"]
    eid = state.next_id("E-")
    at = inp.at or now_iso()
    new_atoms = [
        atoms.encounter(eid, mid, Site.facility, "nurse", _ga_of(referral), at),
        atoms.witness(eid, "facility"),
        atoms.in_referral(inp.referral_id, eid),
    ]
    new_atoms += build_vitals_atoms(state, eid, inp.readings, inp.device,
                                    inp.treatment, inp.treatment_at)
    for s in inp.signs:
        sid = state.next_id("S-")
        new_atoms.append(atoms.sign(sid, eid, s.name, s.status, s.source))
    state.memory.apply_many(new_atoms)

    referral["encounters"]["facility"] += new_atoms
    state.save_referral(referral)
    do_reconcile(state, inp.referral_id)
    return state.referrals[inp.referral_id]


def _ga_of(referral: dict) -> float:
    for a in referral["encounters"]["community"]:
        if a.startswith("(encounter"):
            node = sexpr.parse(a)
            return float(node[5][1])
    return 0.0


def do_reconcile(state: AgentState, ref: str) -> dict:
    referral = state.referrals[ref]
    mid = referral["mother_id"]
    did = state.next_id("D-")
    decision = state.reasoner.run_pipeline(ref, mid, did)
    decision = finalize_decision(state, decision)

    previous = referral.get("reconciled")
    if previous and previous["id"] != decision["id"]:
        referral["diff"] = proof.diff_decisions(previous, decision)
    elif referral.get("edge_decision"):
        referral["diff"] = proof.diff_decisions(referral["edge_decision"], decision)
    referral["reconciled"] = decision
    referral["status"] = "reconciled"
    state.save_referral(referral)
    return referral


def do_contest(state: AgentState, ref: str, inp: ContestInput) -> dict:
    referral = state.referrals.get(ref)
    if not referral:
        raise HTTPException(404, f"unknown referral {ref}")
    pid = inp.premise_id
    target_ids = _premise_target_ids(state, referral, pid)
    if inp.source_id:
        if inp.source_id not in target_ids:
            raise HTTPException(400, f"{inp.source_id} is not evidence for {pid}")
        target_ids = [inp.source_id]
    if not target_ids:
        raise HTTPException(400, f"premise {pid} has no contestable evidence")
    for tid in target_ids:
        state.memory.apply("add", atoms.contested(tid, inp.by, inp.reason))
    referral["contests"].append({
        "premise_id": pid, "target_ids": target_ids,
        "by": inp.by, "reason": inp.reason, "at": now_iso(),
    })
    state.save_referral(referral)
    do_reconcile(state, ref)
    return state.referrals[ref]


def _premise_target_ids(state: AgentState, referral: dict, pid: str) -> list[str]:
    """A contest names an evidence atom id (S-C11), a finding (severe-symptom),
    or a finding plus one source (severe-symptom / S-C11)."""
    if pid.startswith(("S-", "R-", "T-")):
        return [pid]
    dec = referral.get("reconciled") or referral.get("edge_decision") or {}
    ids: list[str] = []
    for p in dec.get("premises", []):
        if p["id"] == pid:
            for s in p.get("sources", []):
                if s.get("kind") == "evidence":
                    ids.append(s["id"])
    if ids:
        return ids
    # fallback: signs carrying that finding name in the referral encounters
    for a in referral["encounters"]["community"] + referral["encounters"]["facility"]:
        if a.startswith("(sign"):
            node = sexpr.parse(a)
            if node[3] == pid and node[4] in {"present", "needs-review"}:
                ids.append(node[1])
    return ids


# ------------------------------------------------------------------ factory

def create_app(role: str | None = None) -> FastAPI:
    role = role or os.environ.get("MIZANI_ROLE", "community")
    peer = os.environ.get("MIZANI_PEER")
    state = AgentState(role, peer=peer)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if state.outbox:
            await state.outbox.start_loop()
        yield
        if state.outbox:
            await state.outbox.stop_loop()

    app = FastAPI(title=f"Mizani {role} agent", lifespan=lifespan)
    app.state.agent = state

    def get_state() -> AgentState:
        return state

    # ---------------- common ----------------

    @app.get("/health")
    def health(s: AgentState = Depends(get_state)):
        h = s.engine.health()
        h["events"] = s.memory.count
        h["decisions"] = len(s.decisions)
        h["outbox_pending"] = len(s.outbox.pending()) if s.outbox else 0
        h["online"] = s.outbox.online if s.outbox else None
        return h

    @app.get("/rules")
    def rules(s: AgentState = Depends(get_state)):
        out = s.engine.run("!(collapse (match &self (rule $p $i $v $b $t) (rule $p $i $v $b $t)))")
        parsed = []
        if out and out[0] not in {"", "()"}:
            for node in sexpr.parse(out[0]):
                parsed.append({
                    "pack": node[1], "id": node[2], "version": node[3],
                    "body": sexpr.to_str(node[4]), "truth": sexpr.to_str(node[5]),
                })
        return {"pack": s.engine.pack, "rules": parsed}

    @app.get("/mothers")
    def mothers(s: AgentState = Depends(get_state)):
        out = s.engine.run(
            "!(collapse (match &self (mother $m (age $a) (gravida $g) (para $p))"
            " (mother $m (age $a) (gravida $g) (para $p))))")
        result = []
        if out and out[0] not in {"", "()"}:
            for node in sexpr.parse(out[0]):
                mid = node[1]
                ga = None
                encs = s.engine.run(
                    f"!(collapse (match &self (encounter $e {mid} (site $st) (by $b) (ga-weeks $g) (at $at)) $g))")
                if encs and encs[0] not in {"", "()"}:
                    weeks = [float(x) for x in sexpr.parse(encs[0])]
                    ga = max(weeks) if weeks else None
                result.append({
                    "id": mid,
                    "age": int(node[2][1]),
                    "gravida": int(node[3][1]),
                    "para": int(node[4][1]),
                    "ga_weeks": ga,
                })
        return {"mothers": result}

    @app.get("/mothers/{mid}")
    def mother_memory(mid: str, s: AgentState = Depends(get_state)):
        atoms.check_id(mid, "mother id")
        encs = s.engine.run(
            f"!(collapse (match &self (encounter $e {mid} (site $st) (by $b) (ga-weeks $g) (at $at))"
            f" (encounter $e {mid} (site $st) (by $b) (ga-weeks $g) (at $at))))")
        encounters = []
        if encs and encs[0] not in {"", "()"}:
            for node in sexpr.parse(encs[0]):
                eid = node[1]
                detail = {"atom": sexpr.to_str(node), "id": eid,
                          "site": node[3][1], "by": node[4][1],
                          "ga_weeks": float(node[5][1]), "at": sexpr.unquote(node[6][1]),
                          "readings": [], "signs": [], "treatments": [], "witness": None}
                for q, bucket in [
                    (f"!(collapse (match &self (reading $r {eid} $k $v) (reading $r {eid} $k $v)))", "readings"),
                    (f"!(collapse (match &self (sign $s {eid} $f $st $src) (sign $s {eid} $f $st $src)))", "signs"),
                    (f"!(collapse (match &self (treatment $t {eid} $d $at) (treatment $t {eid} $d $at)))", "treatments"),
                ]:
                    r = s.engine.run(q)
                    if r and r[0] not in {"", "()"}:
                        detail[bucket] = [sexpr.to_str(n) for n in sexpr.parse(r[0])]
                w = s.engine.run(f"!(collapse (match &self (witness {eid} $w) $w))")
                if w and w[0] not in {"", "()"}:
                    detail["witness"] = sexpr.parse(w[0])[0]
                encounters.append(detail)
        decisions = [d for d in s.decisions.values() if d["mother_id"] == mid]
        return {
            "mother_id": mid,
            "encounters": encounters,
            "decisions": decisions,
            "atom_count": s.memory.count,
        }

    @app.get("/memory/log")
    def memory_log(limit: int = 500, offset: int = 0, s: AgentState = Depends(get_state)):
        return {"role": s.role, "events": s.memory.log_events(limit, offset)}

    @app.get("/memory/export")
    def memory_export(s: AgentState = Depends(get_state)):
        return PlainTextResponse(s.memory.raw_log(), media_type="text/plain")

    # ---------------- community ----------------

    if role == "community":

        @app.post("/visits/extract")
        async def visits_extract(inp: ExtractInput, s: AgentState = Depends(get_state)):
            return await s.jev.extract(inp.note)

        @app.post("/visits")
        def create_visit(visit: VisitInput, s: AgentState = Depends(get_state)):
            try:
                return record_visit(s, visit)
            except AtomError as exc:
                raise HTTPException(400, str(exc)) from exc

        @app.get("/outbox")
        def outbox(s: AgentState = Depends(get_state)):
            return {"online": s.outbox.online, "pending": s.outbox.pending()}

        @app.post("/connectivity")
        async def connectivity(inp: ConnectivityInput, s: AgentState = Depends(get_state)):
            s.outbox.set_online(inp.online)
            synced = await s.outbox.flush() if inp.online else []
            return {"online": s.outbox.online, "synced": synced,
                    "pending": len(s.outbox.pending())}

    # ---------------- facility ----------------

    if role == "facility":

        @app.post("/sync")
        def sync(packet: dict, s: AgentState = Depends(get_state)):
            try:
                return sync_packet(s, packet)
            except (AtomError, KeyError) as exc:
                raise HTTPException(400, str(exc)) from exc

        @app.post("/encounters")
        def add_encounter(inp: FacilityEncounterInput, s: AgentState = Depends(get_state)):
            try:
                return record_facility_encounter(s, inp)
            except AtomError as exc:
                raise HTTPException(400, str(exc)) from exc

        @app.get("/referrals")
        def referrals(s: AgentState = Depends(get_state)):
            out = []
            for r in s.referrals.values():
                out.append({
                    "referral_id": r["referral_id"],
                    "mother": r["mother"],
                    "mother_id": r["mother_id"],
                    "ga_weeks": _ga_of(r),
                    "created_at": r["created_at"],
                    "status": r["status"],
                    "edge_level": (r.get("edge_decision") or {}).get("level"),
                    "reconciled_level": (r.get("reconciled") or {}).get("level"),
                    "changed": bool(r.get("reconciled")) and
                        (r.get("edge_decision") or {}).get("level") !=
                        (r.get("reconciled") or {}).get("level"),
                })
            sev = {"emergency": 0, "urgent": 1, "watch": 2, "normal": 3, None: 4}
            out.sort(key=lambda r: (sev.get(r["reconciled_level"], 5), r["created_at"]), reverse=False)
            return {"referrals": out}

        @app.get("/referrals/{ref}")
        def referral_detail(ref: str, s: AgentState = Depends(get_state)):
            r = s.referrals.get(ref)
            if not r:
                raise HTTPException(404, f"unknown referral {ref}")
            return r

        @app.post("/referrals/{ref}/reconcile")
        def reconcile(ref: str, s: AgentState = Depends(get_state)):
            if ref not in s.referrals:
                raise HTTPException(404, f"unknown referral {ref}")
            return do_reconcile(s, ref)

        @app.post("/referrals/{ref}/contest")
        def contest(ref: str, inp: ContestInput, s: AgentState = Depends(get_state)):
            try:
                return do_contest(s, ref, inp)
            except AtomError as exc:
                raise HTTPException(400, str(exc)) from exc

        @app.post("/referrals/{ref}/override")
        def override(ref: str, inp: OverrideInput, s: AgentState = Depends(get_state)):
            """P1: clinician override becomes a proposed rule patch."""
            r = s.referrals.get(ref)
            if not r:
                raise HTTPException(404, f"unknown referral {ref}")
            rec = r.get("reconciled") or r.get("edge_decision") or {}
            patch_id = s.next_id("PAT-")
            rule = rec.get("rule") or {}
            patch = {
                "id": patch_id,
                "referral_id": ref,
                "rule_id": rule.get("id"),
                "rule_pack": rule.get("pack"),
                "reason": inp.reason,
                "by": inp.by,
                "current_level": rec.get("level"),
                "override_level": inp.level,
                "status": "proposed",
                "created_at": now_iso(),
            }
            s.patches[patch_id] = patch
            return patch

        @app.post("/rules/patches/{pid}/approve")
        def approve_patch(pid: str, s: AgentState = Depends(get_state)):
            patch = s.patches.get(pid)
            if not patch:
                raise HTTPException(404, f"unknown patch {pid}")
            rid = patch.get("rule_id")
            if not rid:
                raise HTTPException(400, "patch has no rule to change")
            out = s.engine.run(
                f"!(collapse (match &self (rule $p {rid} $v $b $t) (rule $p {rid} $v $b $t)))")
            if not out or out[0] in {"", "()"}:
                raise HTTPException(404, f"rule {rid} not found")
            node = sexpr.parse(out[0])[0]
            old_atom = sexpr.to_str(node)
            old_ver = node[3]
            new_ver = old_ver + ".1"
            new_atom = f"(rule {node[1]} {node[2]} {new_ver} {sexpr.to_str(node[4])} {sexpr.to_str(node[5])})"
            s.memory.apply("remove", old_atom)
            s.memory.apply("add", new_atom)
            patch["status"] = "approved"
            patch["old"] = old_atom
            patch["new"] = new_atom
            patch["version"] = new_ver
            return patch

    @app.exception_handler(AtomError)
    async def atom_error_handler(_req, exc: AtomError):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=400,
                            content={"ok": False, "error": {"code": "invalid_atom", "message": str(exc)}})

    return app
