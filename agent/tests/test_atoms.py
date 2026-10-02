"""Atom safety: injection rejected or quoted, ranges enforced."""
from __future__ import annotations

import pytest

from mizani import atoms
from mizani.atoms import AtomError, ReadingKind, Site


def test_valid_atoms_build():
    a = atoms.encounter("E-C1", "M-1", Site.home, "chp", 34, "2026-10-02T21:40")
    assert a == '(encounter E-C1 M-1 (site home) (by chp) (ga-weeks 34) (at "2026-10-02T21:40"))'
    assert atoms.reading("R-C1", "E-C1", ReadingKind.sbp, 152) == "(reading R-C1 E-C1 sbp 152)"
    assert atoms.sign("S-C1", "E-C1", "severe-headache", "present", "chp") == \
        "(sign S-C1 E-C1 severe-headache present (source chp))"


@pytest.mark.parametrize("bad", [
    "x) (remove-atom &self",
    "E-1)) (!(halt)",
    'evil "quote"',
    "a b c",
    "semi;colon",
    "x" * 41,
    "",
])
def test_id_injection_rejected(bad):
    with pytest.raises(AtomError):
        atoms.check_id(bad)


@pytest.mark.parametrize("kind,value", [
    (ReadingKind.sbp, 20), (ReadingKind.sbp, 300),
    (ReadingKind.dbp, 10), (ReadingKind.temp, 30.0),
    (ReadingKind.protein, 5), (ReadingKind.pulse, 500),
])
def test_range_enforced(kind, value):
    with pytest.raises(AtomError):
        atoms.check_number(value, kind)


def test_free_text_escaped():
    from mizani import sexpr
    payload = 'said ") (remove-atom &self (x'
    a = atoms.contested("S-C1", "nurse-baraka", payload)
    assert '\\"' in a
    # the atom still parses as exactly one s-expression, and the text round-trips
    node = sexpr.parse(a)
    assert node[0] == "contested"
    assert sexpr.unquote(node[3][1]) == payload


def test_unknown_sign_rejected():
    with pytest.raises(AtomError):
        atoms.sign("S-C1", "E-C1", "heart-attack", "present", "chp")
    with pytest.raises(AtomError):
        atoms.sign("S-C1", "E-C1", "fever", "maybe", "chp")


def test_idgen_tags_unique():
    g1 = atoms.IdGen(tag="C")
    g2 = atoms.IdGen(tag="F")
    a1, b1 = g1.next("E-"), g2.next("E-")
    assert a1 != b1
    assert a1 == "E-C1" and b1 == "E-F1"
    atoms.check_id(a1)
    atoms.check_id(b1)
