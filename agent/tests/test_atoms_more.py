"""More atom builder coverage: every builder and edge case."""
from __future__ import annotations

import pytest

from mizani import atoms
from mizani.atoms import AtomError, ReadingKind, Site


def test_mother_builder():
    a = atoms.mother("M-1", 27, 2, 1)
    assert a == "(mother M-1 (age 27) (gravida 2) (para 1))"
    with pytest.raises(AtomError):
        atoms.mother("M-1", 99, 2, 1)


def test_prov_treatment_witness_referral():
    assert atoms.prov("R-1", True, "nifedipine-oral", "aneroid") == \
        "(prov R-1 (repeated yes) (after-treatment nifedipine-oral) (device aneroid))"
    assert atoms.prov("R-1", False, "none", "mercury") == \
        "(prov R-1 (repeated no) (after-treatment none) (device mercury))"
    with pytest.raises(AtomError):
        atoms.prov("R-1", True, "ibuprofen", "aneroid")
    assert atoms.treatment("T-1", "E-1", "magnesium-sulphate", "2026-10-02T22:50") == \
        '(treatment T-1 E-1 magnesium-sulphate (at "2026-10-02T22:50"))'
    with pytest.raises(AtomError):
        atoms.treatment("T-1", "E-1", "none", "t")
    assert atoms.witness("E-1", "community") == "(witness E-1 community)"
    with pytest.raises(AtomError):
        atoms.witness("E-1", "god")
    assert atoms.in_referral("REF-1", "E-1") == "(in-referral REF-1 E-1)"


def test_decision_and_referral_events():
    a = atoms.decision_event("D-1", "REF-1", "M-1", "urgent", "urgent-referral", 0.9, 0.6185)
    assert a == "(decision D-1 REF-1 M-1 (level urgent) (conclusion urgent-referral) (stv 0.9 0.6185))"
    with pytest.raises(AtomError):
        atoms.decision_event("D-1", "REF-1", "M-1", "critical", "x", 1.0, 1.0)
    assert atoms.referral_event("REF-1", "M-1", "PK-1") == \
        "(referral REF-1 M-1 (packet PK-1))"


def test_fmt_num_and_ga():
    assert atoms.fmt_num(152) == "152"
    assert atoms.fmt_num(36.5) == "36.5"
    assert "(ga-weeks 34)" in atoms.encounter("E-1", "M-1", Site.home, "chp", 34, "t")
    assert "(ga-weeks 0)" in atoms.encounter("E-1", "M-1", Site.facility, "nurse", 0, "t")
    assert "(ga-weeks 36.5)" in atoms.encounter("E-1", "M-1", Site.home, "chp", 36.5, "t")
    with pytest.raises(AtomError):
        atoms.encounter("E-1", "M-1", Site.home, "chp", 50, "t")
    with pytest.raises(AtomError):
        atoms.encounter("E-1", "M-1", Site.home, "robot", 34, "t")


def test_si_and_float_ranges():
    assert atoms.check_number(0.9, ReadingKind.si) == 0.9
    with pytest.raises(AtomError):
        atoms.check_number("not-a-number", ReadingKind.sbp)
    with pytest.raises(AtomError):
        atoms.check_number(0.1, ReadingKind.si)


def test_contested_builder():
    a = atoms.contested("S-C1", "nurse-baraka", "headache resolved after paracetamol")
    assert a == '(contested S-C1 (by nurse-baraka) (reason "headache resolved after paracetamol"))'
    with pytest.raises(AtomError):
        atoms.contested("S-C1", "nurse-baraka", "x" * 301)
    with pytest.raises(AtomError):
        atoms.contested("S-C1", "nurse-baraka", "")


def test_sign_statuses_and_sources():
    for status in ["present", "absent", "not-mentioned", "needs-review"]:
        assert f" {status} " in atoms.sign("S-1", "E-1", "fever", status, "chp")
    for source in ["chp", "nurse", "jev"]:
        assert f"(source {source})" in atoms.sign("S-1", "E-1", "fever", "present", source)
