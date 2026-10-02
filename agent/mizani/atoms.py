"""Safe atom builders and validators.

Every atom is built from typed values only. Ids are generated or validated
against a strict pattern; readings are range-checked; sign names and
statuses are enums; free text is always stored as an escaped MeTTa string,
never interpolated as code.
"""
from __future__ import annotations

import re
from enum import Enum
from typing import Any

ID_RE = re.compile(r"^[A-Za-z0-9_:-]{1,40}$")
COUNTER_RE = re.compile(r"^(?P<prefix>[A-Z]{1,6}-)(?P<n>\d{1,6})$")


class AtomError(ValueError):
    pass


class Site(str, Enum):
    home = "home"
    facility = "facility"


class Role(str, Enum):
    community = "community"
    facility = "facility"


class ReadingKind(str, Enum):
    sbp = "sbp"
    dbp = "dbp"
    pulse = "pulse"
    temp = "temp"
    protein = "protein"
    hb = "hb"
    si = "si"
    blood_loss = "blood-loss"


RANGES: dict[ReadingKind, tuple[float, float]] = {
    ReadingKind.sbp: (60, 260),
    ReadingKind.dbp: (30, 160),
    ReadingKind.pulse: (30, 220),
    ReadingKind.temp: (34.0, 42.5),
    ReadingKind.protein: (0, 4),
    ReadingKind.hb: (3, 20),
    ReadingKind.si: (0.3, 3.0),
    ReadingKind.blood_loss: (0, 5000),
}

SIGNS = {
    "severe-headache", "visual-disturbance", "convulsions", "vaginal-bleeding",
    "fever", "severe-abdominal-pain", "rfm", "swelling-face-hands",
    "breathing-difficulty", "membranes-ruptured", "in-labour",
    "epigastric-pain", "dizziness", "vomiting", "unconscious", "looks-very-ill",
}

SIGN_STATUSES = {"present", "absent", "not-mentioned", "needs-review"}
SIGN_SOURCES = {"chp", "nurse", "jev"}

TREATMENTS = {
    "none", "nifedipine-oral", "methyldopa", "magnesium-sulphate",
    "paracetamol", "other",
}


def check_id(value: str, what: str = "id") -> str:
    if not isinstance(value, str) or not ID_RE.match(value):
        raise AtomError(f"invalid {what}: {value!r}")
    return value


def check_number(value: Any, kind: ReadingKind) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise AtomError(f"{kind.value} is not a number: {value!r}") from None
    lo, hi = RANGES[kind]
    if not (lo <= v <= hi):
        raise AtomError(f"{kind.value} out of range {lo}..{hi}: {v}")
    return v


def fmt_num(v: float) -> str:
    """Format a number for an atom: ints without a decimal point."""
    f = float(v)
    if f == int(f):
        return str(int(f))
    return repr(round(f, 4))


def esc(text: str) -> str:
    """Escape free text for storage as a quoted MeTTa string."""
    return '"' + str(text).replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---------------------------------------------------------------- builders

def mother(mid: str, age: int, gravida: int, para: int) -> str:
    check_id(mid, "mother id")
    for name, v in (("age", age), ("gravida", gravida), ("para", para)):
        if not (0 <= int(v) <= 60):
            raise AtomError(f"invalid {name}: {v}")
    return f"(mother {mid} (age {int(age)}) (gravida {int(gravida)}) (para {int(para)}))"


def encounter(eid: str, mid: str, site: Site, by: str, ga_weeks: float, at: str) -> str:
    check_id(eid, "encounter id")
    check_id(mid, "mother id")
    if by not in {"chp", "nurse", "co"}:
        raise AtomError(f"invalid by: {by}")
    ga = float(ga_weeks)
    if not (0 <= ga <= 44):
        raise AtomError(f"invalid ga-weeks: {ga}")
    ga_s = fmt_num(ga)
    return (
        f"(encounter {eid} {mid} (site {site.value}) (by {by}) "
        f"(ga-weeks {ga_s}) (at {esc(at)}))"
    )


def reading(rid: str, eid: str, kind: ReadingKind, value: float) -> str:
    check_id(rid, "reading id")
    check_id(eid, "encounter id")
    v = check_number(value, kind)
    return f"(reading {rid} {eid} {kind.value} {fmt_num(v)})"


def prov(rid: str, repeated: bool, after_treatment: str, device: str) -> str:
    check_id(rid, "reading id")
    if after_treatment not in TREATMENTS:
        raise AtomError(f"invalid treatment: {after_treatment}")
    check_id(device, "device")
    rep = "yes" if repeated else "no"
    return f"(prov {rid} (repeated {rep}) (after-treatment {after_treatment}) (device {device}))"


def sign(sid: str, eid: str, name: str, status: str, source: str) -> str:
    check_id(sid, "sign id")
    check_id(eid, "encounter id")
    if name not in SIGNS:
        raise AtomError(f"unknown sign: {name}")
    if status not in SIGN_STATUSES:
        raise AtomError(f"invalid sign status: {status}")
    if source not in SIGN_SOURCES:
        raise AtomError(f"invalid sign source: {source}")
    return f"(sign {sid} {eid} {name} {status} (source {source}))"


def treatment(tid: str, eid: str, drug: str, at: str) -> str:
    check_id(tid, "treatment id")
    check_id(eid, "encounter id")
    if drug not in TREATMENTS - {"none"}:
        raise AtomError(f"invalid drug: {drug}")
    return f"(treatment {tid} {eid} {drug} (at {esc(at)}))"


def witness(eid: str, w: str) -> str:
    check_id(eid, "encounter id")
    if w not in {"community", "facility"}:
        raise AtomError(f"invalid witness: {w}")
    return f"(witness {eid} {w})"


def in_referral(ref: str, eid: str) -> str:
    check_id(ref, "referral id")
    check_id(eid, "encounter id")
    return f"(in-referral {ref} {eid})"


def contested(item_id: str, by: str, reason: str) -> str:
    check_id(item_id, "contested id")
    check_id(by, "contest author")
    if not reason or len(reason) > 300:
        raise AtomError("contest reason must be 1..300 chars")
    return f"(contested {item_id} (by {by}) (reason {esc(reason)}))"


def decision_event(did: str, ref: str, mid: str, level: str, conc: str, f: float, c: float) -> str:
    check_id(did, "decision id")
    check_id(ref, "referral id")
    check_id(mid, "mother id")
    if level not in {"normal", "watch", "urgent", "emergency"}:
        raise AtomError(f"invalid level: {level}")
    return (
        f"(decision {did} {ref} {mid} (level {level}) (conclusion {conc}) "
        f"(stv {fmt_num(f)} {fmt_num(c)}))"
    )


def referral_event(ref: str, mid: str, packet_id: str) -> str:
    check_id(ref, "referral id")
    check_id(mid, "mother id")
    check_id(packet_id, "packet id")
    return f"(referral {ref} {mid} (packet {packet_id}))"


class IdGen:
    """Per-role id generator with a persisted counter per prefix.

    Ids carry the agent's tag (C for community, F for facility) so evidence
    from the two witnesses can never collide when one agent holds both.
    """

    def __init__(self, start: dict[str, int] | None = None, tag: str = ""):
        self._counters: dict[str, int] = dict(start or {})
        self.tag = tag

    def next(self, prefix: str) -> str:
        check_id(prefix, "id prefix")
        n = self._counters.get(prefix, 0) + 1
        self._counters[prefix] = n
        return f"{prefix}{self.tag}{n}"

    def state(self) -> dict[str, int]:
        return dict(self._counters)
