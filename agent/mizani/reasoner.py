"""Reasoner: drives the Mizani pipeline over the PeTTa engine.

collect evidence (MeTTa) -> fold revision per finding (Omega |-nal) ->
stage reconciled atoms -> derive cross-visit findings (MeTTa) ->
fire the rule pack as NAL deduction chains (Omega |-nal via eliminate) ->
select a decision band and level -> build the proof JSON.

Every truth value in the output is computed by Omega's lib_nal.metta.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any

from . import sexpr
from .memory import Memory

LEVEL_OF_CONCLUSION = {
    "emergency-referral": "emergency",
    "pre-eclampsia-severe": "emergency",
    "urgent-referral": "urgent",
    "pre-eclampsia": "urgent",
    "watch-referral": "watch",
}
SEVERITY = {"emergency": 3, "urgent": 2, "watch": 1, "normal": 0}

EDGE_PRIORITY = [
    "r_danger_bleed", "r_danger_fits", "r_severe_htn", "r_htn_symptom",
    "r_danger_sign", "r_htn_confirmed", "r_fever", "r_rfm", "r_prom",
    "r_breath", "r_htn_unconfirmed",
]
# Facility order: the most specific clinical conclusion wins within a level,
# so pre-eclampsia beats a generic hypertension referral when both fire.
FACILITY_PRIORITY = [
    "r_pe_severe_symp", "r_pe_severe_bp", "r_severe_htn", "r_danger_bleed",
    "r_danger_fits", "r_pph", "r_pph_500", "r_shock_high",
    "r_pe", "r_htn_symptom", "r_danger_sign", "r_htn_confirmed", "r_fever",
    "r_rfm", "r_prom", "r_breath", "r_shock", "r_anaemia_severe",
    "r_htn_unconfirmed",
]

MEMORY_FINDINGS = {"early-normal-bp", "early-high-bp", "new-onset", "chronic-htn"}

# Structural and memory findings are not shown as near misses; the near-miss
# list answers "which clinical signal almost fired but did not".
NEAR_MISS_EXCLUDE = {
    "late-ga", "preterm-ga", "postpartum", "early-normal-bp", "early-high-bp",
    "prom", "abnormal-haemodynamic",
}

ACTIONS = {
    "emergency": (
        "Stabilise and transfer now. Call the senior clinician.",
        "Dharura. Mtulize na umpeleke hospitali sasa. Mwite daktari mkuu.",
    ),
    "urgent": (
        "Refer to the facility today.",
        "Haraka. Mpeleke kituo cha afya leo.",
    ),
    "urgent_facility": (
        "Admit for assessment today.",
        "Mweke kwenye tathmini leo.",
    ),
    "watch": (
        "Repeat the reading after 15 minutes rest, then reassess.",
        "Angalia. Rudia kipimo baada ya dakika 15 za kupumzika, kisha tathmini tena.",
    ),
    "normal": (
        "Continue routine antenatal care.",
        "Kawaida. Endelea na kliniki za kawaida za ujauzito.",
    ),
}


@dataclass
class Evidence:
    kind: str           # evidence | counter | defeated
    finding: str
    id: str
    from_: list         # parsed (from ...) items
    tv: tuple[float, float] | None = None
    by: str | None = None


@dataclass
class FindingResult:
    name: str
    items: list[Evidence] = field(default_factory=list)
    defeated: list[Evidence] = field(default_factory=list)
    withdrawn: list[dict] = field(default_factory=list)
    tv: tuple[float, float] | None = None
    revision_steps: list[str] = field(default_factory=list)

    @property
    def band(self) -> str:
        return band_of(self.tv)


def band_of(tv: tuple[float, float] | None) -> str:
    """Omega's documented action thresholds."""
    if tv is None:
        return "none"
    f, c = tv
    if f >= 0.6 and c >= 0.5:
        return "act"
    if f >= 0.3 and c >= 0.2:
        return "hypothesise"
    return "none"


def _num(x: Any) -> float:
    return float(x)


class Reasoner:
    def __init__(self, memory: Memory):
        self.mem = memory
        self.engine = memory.engine

    # ------------------------------------------------------------ collect

    def collect(self, ref: str, mid: str) -> dict[str, FindingResult]:
        out = self.engine.run(f"!(collapse (collect-evidence {ref} {mid}))")
        findings: dict[str, FindingResult] = {}
        if not out or out[0] in {"", "()"}:
            return findings
        for node in sexpr.parse(out[0]):
            if not isinstance(node, list) or len(node) < 4:
                continue
            head = node[0]
            if head in {"evidence", "counter"}:
                ev = Evidence(
                    kind=head,
                    finding=node[1],
                    id=node[2],
                    from_=node[3],
                    tv=(float(node[4][1]), float(node[4][2])),
                )
                findings.setdefault(node[1], FindingResult(node[1])).items.append(ev)
            elif head == "defeated":
                ev = Evidence(kind="defeated", finding=node[1], id=node[2],
                              from_=node[3], by=node[4][1] if len(node[4]) > 1 else None)
                findings.setdefault(node[1], FindingResult(node[1])).defeated.append(ev)
        return findings

    # ------------------------------------------------------------ revise

    def revise(self, fr: FindingResult, counters: list[Evidence]) -> tuple[float, float] | None:
        """Fold the finding's evidence and counter items with Omega NAL revision."""
        seq = [it.tv for it in fr.items if it.tv] + [c.tv for c in counters if c.tv]
        if not seq:
            return None
        cur = seq[0]
        steps = []
        for nxt in seq[1:]:
            r = self.engine.run(
                f"!(|-nal ({fr.name} (stv {cur[0]} {cur[1]})) ({fr.name} (stv {nxt[0]} {nxt[1]})))"
            )
            parsed = sexpr.parse(r[0])
            term = parsed
            if isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], list):
                term = parsed[0]  # collapsed form ((T (stv f c)))
            if isinstance(term, list) and len(term) == 2:
                stv = sexpr.stv_of(term[1])
                if stv:
                    cur = stv
            steps.append(f"(revision {fr.name} (stv {cur[0]:.5f} {cur[1]:.5f}))")
        fr.revision_steps = steps
        return cur

    # ------------------------------------------------------------ pipeline

    def run_pipeline(self, ref: str, mid: str, decision_id: str) -> dict:
        engine = self.engine
        engine.run("!(clear-ephemeral)")

        findings = self.collect(ref, mid)

        # separate counters from positive evidence (same collection pass)
        counters: dict[str, list[Evidence]] = {}
        for name, fr in findings.items():
            counters[name] = [it for it in fr.items if it.kind == "counter"]
            fr.items = [it for it in fr.items if it.kind == "evidence"]

        # contested atoms -> withdrawn list per finding
        contested = self._contested_items(findings, counters)

        # fold revision per finding and stage reconciled + memory atoms
        for name, fr in findings.items():
            fr.withdrawn = contested.get(name, [])
            fr.tv = self.revise(fr, counters.get(name, []))
            if fr.tv:
                engine.run(f"!(add-atom &self (reconciled {mid} {name} (stv {fr.tv[0]} {fr.tv[1]})))")
            if name in {"early-normal-bp", "early-high-bp"}:
                for it in fr.items:
                    engine.run(
                        f"!(add-atom &self (evidence-mem {name} {it.id} "
                        f"{sexpr.to_str(it.from_)} (stv {it.tv[0]} {it.tv[1]})))"
                    )

        # cross-visit derivations (new-onset, chronic-htn) in MeTTa
        derived = engine.run(f"!(collapse (derive-findings {ref} {mid}))")
        if derived and derived[0] not in {"", "()"}:
            for node in sexpr.parse(derived[0]):
                if isinstance(node, list) and node and node[0] == "evidence":
                    name = node[1]
                    tv = (float(node[4][1]), float(node[4][2]))
                    ev = Evidence(kind="evidence", finding=name, id=node[2],
                                  from_=node[3], tv=tv)
                    fr = findings.setdefault(name, FindingResult(name))
                    fr.items.append(ev)
                    fr.tv = tv
                    engine.run(f"!(add-atom &self (reconciled {mid} {name} (stv {tv[0]} {tv[1]})))")

        # fire every rule of the active pack
        fired_raw = engine.run(f"!(collapse (fire-all {mid}))")
        conclusions = []
        if fired_raw and fired_raw[0] not in {"", "()"}:
            for node in sexpr.parse(fired_raw[0]):
                if isinstance(node, list) and node and node[0] == "conclusion":
                    conclusions.append(self._parse_conclusion(node))

        decision = self._select(decision_id, ref, mid, conclusions, findings, counters)
        return decision

    # ------------------------------------------------------------ parse

    def _parse_conclusion(self, node: list) -> dict:
        """(conclusion <conc> <stv> (because (rule p i v) <steps>))"""
        conc = node[1]
        f, c = float(node[2][1]), float(node[2][2])
        because = node[3]
        rule = because[1]  # (rule pack id ver)
        steps = self._parse_steps(because[2] if len(because) > 2 else ["done"])
        return {
            "conclusion": conc,
            "truth": {"f": f, "c": c},
            "band": band_of((f, c)),
            "rule": {"pack": rule[1], "id": rule[2], "version": rule[3]},
            "steps": steps,
            "raw": sexpr.to_str(node),
        }

    def _parse_steps(self, node: list) -> list[dict]:
        steps = []
        cur = node
        while isinstance(cur, list) and cur and cur[0] == "step":
            n = cur[1]
            premise = cur[2]          # (premise <p> (stv f c))
            derived = cur[3]          # (derived <term> (stv f c))
            steps.append({
                "n": int(n),
                "premise": premise[1],
                "premise_tv": {"f": float(premise[2][1]), "c": float(premise[2][2])},
                "derived": sexpr.to_str(derived[1]),
                "derived_tv": {"f": float(derived[2][1]), "c": float(derived[2][2])},
            })
            cur = cur[4] if len(cur) > 4 else ["done"]
        return steps

    def _contested_items(self, findings: dict[str, FindingResult],
                         counters: dict[str, list[Evidence]]) -> dict[str, list[dict]]:
        out: dict[str, list[dict]] = {}
        raw = self.engine.run("!(collapse (match &self (contested $id $by $reason) (contested $id $by $reason)))")
        if not raw or raw[0] in {"", "()"}:
            return out
        # map contested ids to findings via sign/reading atoms
        id_to_finding: dict[str, str] = {}
        for name, fr in findings.items():
            for it in fr.items + fr.defeated + counters.get(name, []):
                id_to_finding[it.id] = name
        # also scan the atom space for signs/readings we excluded before collection
        signs = self.engine.run("!(collapse (match &self (sign $s $e $f $st $src) (pair $s $f)))")
        if signs and signs[0] not in {"", "()"}:
            for node in sexpr.parse(signs[0]):
                if isinstance(node, list) and node[0] == "pair":
                    id_to_finding[node[1]] = node[2]
        for node in sexpr.parse(raw[0]):
            if isinstance(node, list) and node[0] == "contested":
                cid = node[1]
                by = node[2][1] if isinstance(node[2], list) else node[2]
                reason = node[3][1] if isinstance(node[3], list) else "?"
                reason = sexpr.unquote(reason)
                finding = id_to_finding.get(cid)
                if finding:
                    out.setdefault(finding, []).append(
                        {"id": cid, "by": by, "reason": reason})
        return out

    # ------------------------------------------------------------ select

    def _select(self, decision_id: str, ref: str, mid: str,
                conclusions: list[dict], findings: dict[str, FindingResult],
                counters: dict[str, list[Evidence]]) -> dict:
        role = self.engine.role
        priority = FACILITY_PRIORITY if role == "facility" else EDGE_PRIORITY

        def rank_key(con: dict):
            level = LEVEL_OF_CONCLUSION.get(con["conclusion"], "normal")
            try:
                prio = priority.index(con["rule"]["id"])
            except ValueError:
                prio = 99
            return (-SEVERITY[level], prio, -con["truth"]["c"])

        act = [c for c in conclusions if c["band"] == "act"
               and c["conclusion"] in LEVEL_OF_CONCLUSION]
        hypo = [c for c in conclusions if c["band"] == "hypothesise"
                and c["conclusion"] in LEVEL_OF_CONCLUSION]

        if act:
            primary = sorted(act, key=rank_key)[0]
            level = LEVEL_OF_CONCLUSION[primary["conclusion"]]
            band = "act"
        elif hypo:
            primary = sorted(hypo, key=rank_key)[0]
            level = "watch"
            band = "hypothesise"
        else:
            primary = None
            level = "normal"
            band = "none"

        if primary:
            truth = primary["truth"]
            conclusion = primary["conclusion"]
            rule = primary["rule"]
            proof_tree = sexpr.parse(primary["raw"])
            proof_raw = primary["raw"]
            premises = self._premises(primary, findings)
        else:
            truth = {"f": 1.0, "c": 0.0}
            conclusion = "none"
            rule = None
            proof_tree = []
            proof_raw = ""
            # near misses: the strongest findings that did not reach the act
            # band, so the proof shows why nothing fired (for example a high
            # reading whose revised frequency fell below the threshold).
            near = sorted(
                (fr for fr in findings.values()
                 if fr.tv and fr.name not in NEAR_MISS_EXCLUDE),
                key=lambda fr: (fr.tv[0], fr.tv[1]),
                reverse=True,
            )[:3]
            premises = [
                {
                    "id": fr.name,
                    "truth": {"f": fr.tv[0], "c": fr.tv[1]},
                    "status": "below-threshold",
                    "sources": [
                        {"id": it.id, "kind": it.kind, "from": sexpr.to_str(it.from_),
                         "tv": {"f": it.tv[0], "c": it.tv[1]} if it.tv else None}
                        for it in fr.items
                    ] + [
                        {"id": c.id, "kind": "counter", "from": sexpr.to_str(c.from_),
                         "tv": {"f": c.tv[0], "c": c.tv[1]} if c.tv else None}
                        for c in counters.get(fr.name, [])
                    ],
                    "withdrawn": [],
                }
                for fr in near
            ]

        if level == "urgent" and role == "facility":
            action_en, action_sw = ACTIONS["urgent_facility"]
        else:
            action_en, action_sw = ACTIONS[level]

        return {
            "id": decision_id,
            "mother_id": mid,
            "referral_id": ref,
            "agent": role,
            "pack": self.engine.pack,
            "level": level,
            "action_en": action_en,
            "action_sw": action_sw,
            "conclusion": conclusion,
            "truth": truth,
            "band": band,
            "rule": rule,
            "premises": premises,
            "fired": [
                {"conclusion": c["conclusion"], "rule": c["rule"],
                 "truth": c["truth"], "band": c["band"]}
                for c in conclusions
            ],
            "proof_tree": proof_tree,
            "proof_raw": proof_raw,
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }

    def _premises(self, primary: dict, findings: dict[str, FindingResult]) -> list[dict]:
        """Premise ledger for the primary rule."""
        out = []
        seen = set()
        for step in primary["steps"]:
            name = step["premise"]
            if name in seen:
                continue
            seen.add(name)
            fr = findings.get(name)
            sources = []
            status = "missing"
            tv = None
            if fr:
                tv = fr.tv or (None, None)
                n_ev = len(fr.items)
                if n_ev > 1:
                    status = "revised"
                elif n_ev == 1:
                    status = "used"
                for it in fr.items:
                    sources.append({
                        "id": it.id, "kind": "evidence",
                        "from": sexpr.to_str(it.from_),
                        "tv": {"f": it.tv[0], "c": it.tv[1]} if it.tv else None,
                        "memory": name in MEMORY_FINDINGS or "derived-from" in it.from_,
                    })
                for it in fr.defeated:
                    sources.append({
                        "id": it.id, "kind": "defeated",
                        "from": sexpr.to_str(it.from_), "by": it.by,
                    })
            out.append({
                "id": name,
                "truth": {"f": tv[0], "c": tv[1]} if tv and tv[0] is not None else None,
                "status": status,
                "sources": sources,
                "withdrawn": fr.withdrawn if fr else [],
            })
        # defeated/withdrawn findings that are NOT premises of the primary rule
        # still matter for the proof (for example the defeated facility BP).
        for name, fr in findings.items():
            if name in seen:
                continue
            if fr.defeated:
                out.append({
                    "id": name, "truth": None, "status": "defeated",
                    "sources": [{"id": it.id, "kind": "defeated",
                                 "from": sexpr.to_str(it.from_), "by": it.by}
                                for it in fr.defeated],
                    "withdrawn": [],
                })
            if fr.withdrawn:
                out.append({
                    "id": name, "truth": None, "status": "withdrawn",
                    "sources": [], "withdrawn": fr.withdrawn,
                })
        return out
