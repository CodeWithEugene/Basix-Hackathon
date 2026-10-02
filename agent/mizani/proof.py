"""The answer diff: what changed between two decisions, and why.

Compares the edge decision (from the referral packet) with the reconciled
facility decision (or two successive reconciled decisions after a contest)
and emits typed changes with reasons in English and Swahili.
"""
from __future__ import annotations

LEVEL_ORDER = {"normal": 0, "watch": 1, "urgent": 2, "emergency": 3}

CHANGE_COPY = {
    "level_changed": (
        "The level changed from {a} to {b}.",
        "Kiwango kimebadilika kutoka {a} hadi {b}.",
    ),
    "action_changed": (
        "The action changed: {b}.",
        "Hatua imebadilika: {b}.",
    ),
    "premise_added": (
        "New evidence: {p}.",
        "Ushahidi mpya: {p}.",
    ),
    "premise_from_memory": (
        "From the mother's record: {p}.",
        "Kutoka kwa kumbukumbu ya mama: {p}.",
    ),
    "premise_defeated": (
        "{p} was set aside: {reason}.",
        "{p} imetengwa: {reason}.",
    ),
    "premise_revised": (
        "{p} is now stronger after merging the two witnesses.",
        "{p} imeimarika baada ya kuunganisha mashahidi wawili.",
    ),
    "premise_withdrawn": (
        "{p} was withdrawn by {by}: \"{reason}\".",
        "{p} imeondolewa na {by}: \"{reason}\".",
    ),
    "rule_changed": (
        "The deciding rule changed from {a} to {b}.",
        "Kanuni iliyoamua imebadilika kutoka {a} hadi {b}.",
    ),
    "truth_changed": (
        "Confidence changed from {a} to {b}.",
        "Uhakika umebadilika kutoka {a} hadi {b}.",
    ),
}


def _fmt_stv(t: dict | None) -> str:
    if not t:
        return "unknown"
    return f"(stv {t['f']:.2f} {t['c']:.2f})"


def diff_decisions(before: dict, after: dict) -> dict:
    """Typed change list between two decision dicts."""
    changes: list[dict] = []

    def add(type_: str, a=None, b=None, **fmt):
        en_t, sw_t = CHANGE_COPY[type_]
        changes.append({
            "type": type_,
            "before": a,
            "after": b,
            "reason_en": en_t.format(a=a, b=b, **fmt),
            "reason_sw": sw_t.format(a=a, b=b, **fmt),
        })

    if before["level"] != after["level"]:
        add("level_changed", before["level"], after["level"])
    if before["action_en"] != after["action_en"]:
        add("action_changed", before["action_en"], after["action_en"])
    if (before.get("rule") or {}).get("id") != (after.get("rule") or {}).get("id"):
        add("rule_changed",
            (before.get("rule") or {}).get("id") or "none",
            (after.get("rule") or {}).get("id") or "none")
    if before["truth"] != after["truth"]:
        add("truth_changed", _fmt_stv(before["truth"]), _fmt_stv(after["truth"]))

    before_p = {p["id"]: p for p in before.get("premises", [])}
    after_p = {p["id"]: p for p in after.get("premises", [])}

    for pid, p in after_p.items():
        if p["status"] == "withdrawn":
            for w in p.get("withdrawn", []):
                add("premise_withdrawn", None, pid, p=pid, by=w["by"], reason=w["reason"])
            continue
        if p["status"] == "defeated":
            for s in p.get("sources", []):
                if s.get("kind") == "defeated":
                    add("premise_defeated", None, pid, p=pid,
                        reason=s.get("by") or "protocol")
            continue
        was = before_p.get(pid)
        if pid not in before_p:
            memory = any(s.get("memory") for s in p.get("sources", []))
            if memory:
                add("premise_from_memory", None, pid, p=pid)
            elif p["status"] in {"used", "revised"}:
                add("premise_added", None, pid, p=pid)
        elif p.get("truth") and (was or {}).get("truth") and p["truth"] != was["truth"]:
            add("premise_revised", _fmt_stv(was["truth"]), _fmt_stv(p["truth"]), p=pid)

    return {
        "from_decision": before["id"],
        "to_decision": after["id"],
        "changes": changes,
    }
