"""Pydantic request/response models for the Mizani API."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

RiskLevel = Literal["normal", "watch", "urgent", "emergency"]
RoleName = Literal["community", "facility"]


class Truth(BaseModel):
    f: float
    c: float


class Health(BaseModel):
    role: str
    pack: str
    omega_commit: str
    omega_release: str
    petta: str
    swipl: str
    events: int
    decisions: int
    outbox_pending: int = 0
    online: bool | None = None


class SignInput(BaseModel):
    name: str
    status: Literal["present", "absent", "not-mentioned", "needs-review"]
    source: Literal["chp", "nurse", "jev"] = "chp"


class ReadingInput(BaseModel):
    kind: Literal["sbp", "dbp", "pulse", "temp", "protein", "hb", "blood-loss"]
    value: float
    repeated: bool = False


class MotherInput(BaseModel):
    id: str
    age: int = Field(ge=10, le=60)
    gravida: int = Field(ge=0, le=30)
    para: int = Field(ge=0, le=30)


class VisitInput(BaseModel):
    mother: MotherInput
    ga_weeks: float = Field(ge=0, le=44)
    at: str | None = None
    note: str | None = None
    signs: list[SignInput] = Field(default_factory=list)
    readings: list[ReadingInput] = Field(default_factory=list)
    device: str = "aneroid"


class FacilityEncounterInput(BaseModel):
    referral_id: str
    at: str | None = None
    readings: list[ReadingInput] = Field(default_factory=list)
    signs: list[SignInput] = Field(default_factory=list)
    treatment: str | None = None
    treatment_at: str | None = None
    device: str = "aneroid"


class ExtractInput(BaseModel):
    note: str
    ga_weeks: float | None = None


class ExtractedSign(BaseModel):
    name: str
    status: str
    jev_confidence: float | None = None
    probabilities: dict[str, float] | None = None


class ExtractResult(BaseModel):
    mode: Literal["jev", "offline_manual"]
    signs: list[ExtractedSign] = Field(default_factory=list)
    bp: dict[str, Any] | None = None
    model: str | None = None
    request_id: str | None = None
    error: str | None = None


class ConnectivityInput(BaseModel):
    online: bool


class ContestInput(BaseModel):
    premise_id: str
    reason: str = Field(min_length=1, max_length=300)
    by: str = Field(default="nurse-baraka")
    source_id: str | None = None  # contest one observation, not the whole premise


class OverrideInput(BaseModel):
    level: RiskLevel
    reason: str = Field(min_length=1, max_length=300)
    by: str = Field(default="nurse-baraka")


class SyncResult(BaseModel):
    ok: bool
    referral_id: str | None = None
    detail: str | None = None
