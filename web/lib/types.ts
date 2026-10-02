// Shared types mirroring the Mizani agent API.
export type RiskLevel = "normal" | "watch" | "urgent" | "emergency";
export type Role = "community" | "facility";
export type PremiseStatus = "used" | "revised" | "defeated" | "withdrawn" | "missing" | "below-threshold";

export interface Truth {
  f: number;
  c: number;
}

export interface EvidenceSource {
  id: string;
  kind: "evidence" | "counter" | "defeated";
  from: string;
  tv?: Truth | null;
  by?: string | null;
  memory?: boolean;
}

export interface Withdrawn {
  id: string;
  by: string;
  reason: string;
}

export interface Premise {
  id: string;
  truth: Truth | null;
  status: PremiseStatus;
  sources: EvidenceSource[];
  withdrawn: Withdrawn[];
}

export interface RuleRef {
  pack: string;
  id: string;
  version: string;
}

export interface Decision {
  id: string;
  mother_id: string;
  referral_id: string;
  agent: Role;
  pack: string;
  level: RiskLevel;
  action_en: string;
  action_sw: string;
  conclusion: string;
  truth: Truth;
  band: "act" | "hypothesise" | "none";
  rule: RuleRef | null;
  premises: Premise[];
  fired: { conclusion: string; rule: RuleRef; truth: Truth; band: string }[];
  proof_tree: unknown;
  proof_raw: string;
  explanation_en: string[];
  explanation_sw: string[];
  created_at: string;
}

export interface Change {
  type: string;
  before: string | null;
  after: string | null;
  reason_en: string;
  reason_sw: string;
}

export interface Diff {
  from_decision: string;
  to_decision: string;
  changes: Change[];
}

export interface Mother {
  id: string;
  age: number;
  gravida: number;
  para: number;
  ga_weeks: number | null;
}

export interface ReferralListItem {
  referral_id: string;
  mother: { id: string; age: number; gravida: number; para: number };
  mother_id: string;
  ga_weeks?: number | null;
  created_at: string;
  status: string;
  edge_level: RiskLevel | null;
  reconciled_level: RiskLevel | null;
  changed: boolean;
}

export interface Referral {
  referral_id: string;
  packet_id: string;
  mother_id: string;
  mother: { id: string; age: number; gravida: number; para: number };
  edge_decision: Decision;
  edge_pack: string;
  encounters: { community: string[]; facility: string[] };
  reconciled: Decision | null;
  diff: Diff | null;
  contests: { premise_id: string; by: string; reason: string; at: string }[];
  status: string;
  created_at: string;
}

export interface Health {
  role: string;
  pack: string;
  omega_commit: string;
  omega_release: string;
  petta: string;
  swipl: string;
  events: number;
  decisions: number;
  outbox_pending: number;
  online: boolean | null;
}

export interface EncounterDetail {
  atom: string;
  id: string;
  site: "home" | "facility";
  by: string;
  ga_weeks: number;
  at: string;
  readings: string[];
  signs: string[];
  treatments: string[];
  witness: string | null;
}

export interface MotherMemory {
  mother_id: string;
  encounters: EncounterDetail[];
  decisions: Decision[];
  atom_count: number;
}

export interface LogEvent {
  n: number;
  ts: string;
  op: "add" | "remove";
  atom: string;
}

export interface RuleItem {
  pack: string;
  id: string;
  version: string;
  body: string;
  truth: string;
}

export interface SignState {
  name: string;
  status: "present" | "absent" | "not-mentioned" | "needs-review";
  source: "chp" | "nurse" | "jev";
}

export interface ReadingState {
  kind: "sbp" | "dbp" | "pulse" | "temp" | "protein" | "hb" | "blood-loss";
  value: number;
  repeated: boolean;
}

export interface ExtractResponse {
  mode: "jev" | "offline_manual";
  signs: { name: string; status: string; jev_confidence?: number | null; probabilities?: Record<string, number> | null }[];
  bp?: { systolic: number; diastolic: number; candidates: string[]; picked: string; confidence: number } | null;
  model?: string | null;
  request_id?: string | null;
  error?: string | null;
}
