# Build Spec: Mizani

> **What this file is.** The complete, end-to-end build specification for what we ship to the SingularityNET x Omega x BASIX.Market Hackathon: scope, demo script, architecture, MeTTa agent design, backend API, frontend (pure shadcn/ui), design system, data, tests, run scripts, security, docs deliverables, video and the hour-by-hour plan.
>
> **Read with:** [info.md](info.md) (the event and its rules), [problem.md](problem.md) (why this problem), [solution.md](solution.md) (the full product and why it works), [research.md](research.md) (all sources and verified technical tests).
>
> **Status:** Spec v1.0, Friday 2 October 2026, 09:30 EAT. Submission target **21:00 EAT today**.

---

## Table Of Contents

0. [The One Feature](#0-the-one-feature)
1. [Scope: P0, P1, P2 And The Cut List](#1-scope)
2. [The Demo Script That Drives The Build](#2-the-demo-script-that-drives-the-build)
3. [System Architecture](#3-system-architecture)
4. [Repository Layout](#4-repository-layout)
5. [Tech Stack And Pinned Versions](#5-tech-stack-and-pinned-versions)
6. [The Omega Agent Core (MeTTa)](#6-the-omega-agent-core-metta)
7. [Clinical Rule Packs](#7-clinical-rule-packs)
8. [Backend (FastAPI + PeTTa)](#8-backend-fastapi--petta)
9. [Jev Integration (Language Understanding)](#9-jev-integration-language-understanding)
10. [Explanations In English And Swahili](#10-explanations-in-english-and-swahili)
11. [Frontend (Next.js + Pure shadcn/ui)](#11-frontend-nextjs--pure-shadcnui)
12. [Design System (Stripe-Inspired, Pure shadcn)](#12-design-system)
13. [Pages, Screens And Components In Detail](#13-pages-screens-and-components-in-detail)
14. [Synthetic Data And Scenarios](#14-synthetic-data-and-scenarios)
15. [Testing](#15-testing)
16. [Running It: One Command](#16-running-it-one-command)
17. [Deployment (Optional)](#17-deployment-optional)
18. [Security, Privacy And Safety](#18-security-privacy-and-safety)
19. [Docs And Submission Artifacts](#19-docs-and-submission-artifacts)
20. [The 3-Minute Video](#20-the-3-minute-video)
21. [Submission Form Drafts](#21-submission-form-drafts)
22. [Risks And Fallbacks](#22-risks-and-fallbacks)
23. [Hour-By-Hour Plan](#23-hour-by-hour-plan)
24. [Definition Of Done](#24-definition-of-done)

---

## 0. The One Feature

The solo brief says: "No solo hacker attempts a complete platform. One feature, proven, is the whole assignment." So we name the feature in one sentence and build only what proves it.

> **The feature: a referral decision that two Omega agents reconcile.** A community health promoter's (CHP's) Omega agent decides offline, with a small MeTTa rule pack, whether a pregnant woman needs referral. When connectivity returns, a facility-side Omega agent that **remembers the mother** and holds the full rule pack reconciles the two witnesses' conflicting evidence with Omega's own NAL reasoning, and produces a **contestable referral proof** that shows, premise by premise and in English and Swahili, how the answer changed and why. A clinician can challenge any premise and watch the decision recompute.

| Hackathon frame | How the feature answers it |
|---|---|
| Platform track | **Omega** |
| Omega problem | **The Agent Without Borders**, challenge 02: "a low-bandwidth/offline-first agent that makes a decision locally with a small MeTTa rule set, then reconciles with a fuller Omega-style agent when connectivity returns, and shows how its answer changed and why." Also challenge 01 (reasoning explained in a local language). |
| Solo challenge | **01: One agent producing an auditable decision.** The reconciled referral is the decision; the proof is the audit trail. (It also demonstrates 03, two agents resolving one conflicting claim, but we pitch 01 to stay "one feature".) |
| "Omega's stateful, auditable-reasoning architecture has to be the actual feature" | **Stateful:** the facility agent's persistent memory of the mother (her 14-week BP) changes the conclusion. **Auditable:** every conclusion is a NAL proof term with `(stv f c)` truth values produced by Omega's unmodified `lib_nal.metta` on PeTTa, Omega's runtime. **Omega-native packaging:** the rules ship as an Omega plugin (`loadOmegaPlugin`, `add-skill`). |

**Name.** *Mizani* is Swahili for "scales" or "balance", the instrument that weighs two sides. Tagline: **"Two witnesses, one referral. Omega weighs what the community saw against what the clinic sees, and shows its working."**

---

## 1. Scope

### 1.1 P0: Must ship (this is the submission)

| # | Item | Proves |
|---|---|---|
| P0.1 | **Two Omega agent processes**, same code, different role: `community` (edge rule pack, own memory log) and `facility` (full rule pack, own memory log, the mother's longitudinal record) | Two agents, stateful |
| P0.2 | MeTTa plugin `mizani` with: provenance-tagged evidence atoms; rule atoms in versioned packs; `assess` (NAL deduction chain through Omega's `lib_nal`); `reconcile` (revision of agreeing evidence, defeat of discounted evidence); `contest` (exclude a premise and recompute); proof terms | Auditable reasoning |
| P0.3 | Persistent memory: append-only atom event log per agent (`memory/<role>.metta`), replayed at startup, identical in spirit to Omega's `memory/history.metta` | Persistence |
| P0.4 | **Offline queue and sync**: the community agent works with the facility unreachable, queues the referral packet, and syncs when "connectivity returns" (a toggle in the UI that really blocks the HTTP call) | Offline-first |
| P0.5 | **Answer diff**: edge decision vs reconciled decision, with the reason for every change | "Shows how its answer changed and why" |
| P0.6 | Explanations rendered from the proof in **English and Swahili** (deterministic templates, no LLM) | Local language |
| P0.7 | Web app (Next.js + pure shadcn/ui) with four screens: **Community Visit**, **Facility Inbox + Reconciliation**, **Mother Memory**, **Audit Log** | Usability |
| P0.8 | Three synthetic scenarios, seeded by one command | Demo reliability |
| P0.9 | Jev extraction of Swahili/Sheng/English visit notes into danger-sign toggles, with manual fallback | Neural-symbolic split; works without network |
| P0.10 | Tests: MeTTa golden proofs, API tests, one Playwright demo-path test | Technical execution |
| P0.11 | README, transcript, audit trail export, AI Disclosure, what's next | Documentation |
| P0.12 | 3-minute video | 25% of the score |

### 1.2 P1: Ship if P0 is green by 16:00 EAT (time-boxed)

| # | Item | Box |
|---|---|---|
| P1.1 | **Override becomes a reviewed rule patch with a visible MeTTa diff** (clinician overrides, the system proposes a patch, a reviewer approves, the rule version bumps, and "replay" shows which past decisions would change) | 75 min |
| P1.2 | **Ask Omega "why?" in chat**: run the real Omega agent loop (Docker `singularitynet/omega:v0.1.19` or native) with the `mizani` plugin loaded so its LLM calls our `why`/`assess` skills; show one exchange in the video | 90 min, only if Docker and an LLM key are available |
| P1.3 | Jev faithfulness check of any free-text explanation against the proof trace | 30 min |
| P1.4 | Hosted demo (frontend on Vercel, agents on Railway/Fly via Dockerfile) | 45 min |

### 1.3 P2: Only described in "What's Next", not built

USSD/SMS channel, Android on-device PeTTa, FHIR/eCHIS integration, county dashboard, DAS-backed shared memory, BASIX IP registration of the validated rule pack.

### 1.4 Cut list (we deliberately do NOT build)

Authentication and user accounts (we show role switcher instead, clearly labelled "demo"), real patient data, a mobile native app, push notifications, multi-facility routing, maps, any machine-learned risk score, any LLM making clinical decisions, a landing page beyond the app's welcome screen.

---

## 2. The Demo Script That Drives The Build

Every component exists because a beat of this script needs it. Times are wall-clock inside the 3-minute video (full video plan in section 20).

**Setting.** Kilifi County, October 2026, short rains with El Niño flooding. A flooded road has cut mobile data in the village. The mother is synthetic: **Amina, 27, G2P1, 34 weeks**.

1. **Community side, offline (0:20 to 0:55).** CHP Zawadi opens Mizani. A banner reads "Offline. Decisions run on this device's rule pack." She types in Swahili: *"Mama analalamika kichwa kinauma sana tangu jana, anaona giza kidogo. Miguu imevimba."* and enters BP **152/98** at home, 34 weeks, then repeats it after 15 minutes rest as WHO ANC guidance requires: **150/96**. Danger-sign toggles fill in (Jev when online; here offline, so she taps them, and the UI shows "Entered by CHP"). The **community agent** decides: **Urgent: refer today**, with a proof card: BP high on a repeated reading, severe headache plus blurred vision, rule `edge-v1 r_htn_symptom v1`, and the NAL truth value Omega computed for that conclusion. Explanation in Swahili and English. The referral packet is queued: "Will sync when connection returns."
2. **Connectivity returns (0:55 to 1:05).** Toggle back online. The packet syncs to the facility agent. Toast: "Referral synced to Mtwapa Health Centre."
3. **Facility side, reconciliation (1:05 to 2:05).** Night-shift nurse Baraka opens the inbox. The referral shows **two witnesses side by side**: Community (home BP 152/98 then 150/96 after rest, headache, blurred vision) and Facility (arrival BP **138/88**, measured **40 minutes after oral nifedipine** given en route; urine dipstick protein **2+**; and from **memory**: BP 116/74 at **14 weeks**). The **facility agent** reconciles with Omega's NAL:
   - The lower facility BP is **defeated** as evidence against hypertension because it was measured after an antihypertensive (defeater rule shown).
   - The 14-week reading from memory makes this **new-onset hypertension after 20 weeks**, so it is pre-eclampsia territory, not chronic hypertension.
   - Proteinuria 2+ plus new-onset hypertension plus severe headache and visual symptoms gives **pre-eclampsia with severe features**.
   - The answer changes: **Urgent → Emergency**, with its new truth value, action "Stabilise and transfer to Coast General per protocol; senior clinician now." The **diff panel** lists exactly what changed and why.
4. **Contest (2:05 to 2:30).** Baraka taps the headache premise: "Headache resolved after paracetamol." Mizani recomputes live: the severe-feature path no longer fires on symptoms, but **the conclusion stays Urgent with pre-eclampsia** (protein plus new-onset hypertension), and the proof shows which premise was withdrawn and by whom. This is the "a human reviewer could act on it" moment.
5. **Memory and audit (2:30 to 2:45).** Open Amina's memory: her visits as atoms, the event log, rule versions. Every step is in the append-only log.
6. **What's next (2:45 to 3:00).** County pilot with CHPs, eCHIS integration, BGI Nexus grant, the 24 to 25 October BASIX hackathon.

Scenarios B and C (section 14) exist for tests and for the finalist Q&A: one where reconciliation **downgrades** (unrepeated reading, normal repeat, no symptoms → "Repeat BP after 15 minutes rest"), and one where the witnesses **agree** (revision raises confidence).

---

## 3. System Architecture

```
                    ┌────────────────────────────────────────────────────────────┐
                    │                 Next.js 16 web app (pnpm)                  │
                    │     pure shadcn/ui · Tailwind v4 · next-themes · Recharts  │
                    │                                                            │
                    │  /community   /facility   /mothers/[id]   /audit   /       │
                    │        │            │            │            │            │
                    │   Route Handlers (server only): /api/community/*,          │
                    │   /api/facility/*  (proxy; holds no secrets)               │
                    └────────┬─────────────────────────────┬─────────────────────┘
                             │ HTTP JSON                   │ HTTP JSON
              ┌──────────────▼─────────────┐   sync   ┌────▼──────────────────────┐
              │ Community agent :8101      │ ───────▶ │ Facility agent :8102      │
              │ FastAPI + PeTTa engine     │ (packet) │ FastAPI + PeTTa engine    │
              │ ROLE=community             │          │ ROLE=facility             │
              │ rule pack: edge-v1         │          │ rule pack: full-v1        │
              │ memory/community.metta     │          │ memory/facility.metta     │
              │ outbox (offline queue)     │          │ the mother's longitudinal │
              │                            │          │ record (prior visits)     │
              └──────────────┬─────────────┘          └────┬──────────────────────┘
                             │ loads (pinned commit)       │
              ┌──────────────▼─────────────────────────────▼──────────────────────┐
              │ vendor/omega  = github.com/singnet/Omega @ pinned commit          │
              │   lib_nal.metta (NAL |- , stv)   lib_pln.metta   src/skills.metta │
              │ vendor/petta  = github.com/trueagi-io/PeTTa @ v1.0.4              │
              │ agent/plugins/mizani/*.metta  (our Omega plugin)                  │
              └───────────────────────────────────────────────────────────────────┘
                             │ optional (P0.9)
              ┌──────────────▼─────────────┐
              │ TypeSafe Jev (jev-1.13.0)  │  extraction of danger signs from notes
              │ server-side only, 3 s      │  falls back to manual toggles
              └────────────────────────────┘
```

**Why two processes instead of two spaces in one process.** PeTTa runs inside one SWI-Prolog instance per Python process (via janus), so the cleanest way to have two genuinely separate agents, each with its own atom space, rule pack and memory, is two processes running the same code with `MIZANI_ROLE` set differently. It also makes "offline" real: when the community agent cannot reach the facility agent's port, the packet stays in its outbox.

**Data flow for one referral.**
1. Browser posts the visit to `/api/community/visits` → community agent.
2. Community agent appends atoms to its log, runs `assess` with `edge-v1`, returns a proof, writes the referral packet to its outbox.
3. If online, the community agent POSTs the packet to the facility agent `/sync`. If offline, it retries when the UI toggles online (and on a 5-second background loop).
4. Facility agent appends the packet atoms (tagged `(witness community ...)`) to its log, merges them with its own memory of the mother and its own readings, runs `reconcile` with `full-v1`, stores the reconciled decision, and computes the diff against the edge decision in the packet.
5. Browser polls `/api/facility/referrals` and renders the two-witness view, the proof, the diff and the explanations.
6. A contest posts to `/api/facility/referrals/{id}/contest` → atom `(contested <premise-id> <by> <reason>)` → recompute → new proof and diff.

---

## 4. Repository Layout

```
Basix-Hackathon/
├── README.md                     # judge-facing front door (see section 19)
├── LICENSE.md  CODE-OF-CONDUCT.md  CONTRIBUTING.md  SECURITY.md
├── Makefile                      # make setup | make dev | make seed | make test
├── .gitignore  .env.example
├── docs/
│   ├── info.md  problem.md  solution.md  build.md  research.md
│   ├── transcript.md             # sample reasoning transcript (generated, then curated)
│   ├── audit-trail.md            # one-page audit trail sample
│   ├── ai-disclosure.md          # also summarised in README
│   ├── images/                   # screenshots for README (light + dark)
│   └── source/                   # organiser material (deck PDF)
├── agent/                        # Python 3.12, uv
│   ├── pyproject.toml  uv.lock
│   ├── mizani/
│   │   ├── __init__.py
│   │   ├── app.py                # FastAPI app factory, role-aware routes
│   │   ├── engine.py             # PeTTa host: load Omega + plugin, lock, replay log
│   │   ├── memory.py             # append-only event log (atoms), replay, export
│   │   ├── atoms.py              # safe atom builders + validators (no string injection)
│   │   ├── sexpr.py              # s-expression parser/printer, proof → JSON tree
│   │   ├── proof.py              # proof JSON model, diff between two decisions
│   │   ├── explain.py            # English + Swahili templates from proof JSON
│   │   ├── jev.py                # TypeSafe Jev client (async, gated, fallback)
│   │   ├── outbox.py             # offline queue + sync loop (community role)
│   │   ├── schemas.py            # pydantic models (requests/responses)
│   │   └── seed.py               # synthetic scenarios A, B, C
│   ├── plugins/mizani/
│   │   ├── mizani.metta          # Omega plugin entry: loadOmegaPlugin + add-skill
│   │   ├── evidence.metta        # findings from readings + provenance → truth values
│   │   ├── reason.metta          # assess, reconcile, defeat, contest, proof terms
│   │   ├── shims.metta           # small helpers (min/max etc.) if needed
│   │   └── packs/
│   │       ├── edge-v1.metta     # community rule pack (small)
│   │       └── full-v1.metta     # facility rule pack (full)
│   ├── tests/
│   │   ├── test_reasoning.py     # golden proofs for scenarios A, B, C
│   │   ├── test_api.py           # FastAPI TestClient
│   │   └── test_atoms.py         # injection and validation
│   └── vendor/                   # git submodules, pinned
│       ├── omega/                # singnet/Omega @ <commit>
│       └── petta/                # trueagi-io/PeTTa @ v1.0.4
├── web/                          # Next.js 16, pnpm, shadcn/ui
│   ├── package.json  pnpm-lock.yaml  components.json  next.config.ts
│   ├── app/
│   │   ├── layout.tsx  globals.css  page.tsx
│   │   ├── community/page.tsx
│   │   ├── facility/page.tsx  facility/[referralId]/page.tsx
│   │   ├── mothers/[motherId]/page.tsx
│   │   ├── audit/page.tsx
│   │   └── api/[role]/[...path]/route.ts   # proxy to the agents
│   ├── components/ui/            # shadcn components (generated, untouched)
│   ├── components/mizani/        # our compositions (see section 13)
│   ├── lib/  api.ts  types.ts  risk.ts  i18n.ts
│   └── tests/e2e/demo.spec.ts    # Playwright demo path
└── scripts/
    ├── dev.sh                    # start both agents + web
    ├── export-transcript.py      # writes docs/transcript.md from a live run
    └── check-no-dashes.sh        # fails if UI copy contains em or en dashes
```

---

## 5. Tech Stack And Pinned Versions

All versions below were verified on this Mac (macOS 27.2, arm64) on 2 Oct 2026 unless marked.

| Layer | Choice | Version | Why |
|---|---|---|---|
| Agent runtime | **PeTTa** (MeTTa on SWI-Prolog) | git tag `v1.0.4` | Omega's own runtime (its Dockerfile pins it) |
| Prolog | SWI-Prolog | 10.0.2 (Homebrew) | Version Omega pins |
| Python bridge | janus-swi | 1.5.3 | Hosts PeTTa inside Python |
| Omega | `singnet/Omega` | `main @ 31ff0aad` (2026-10-01), release v0.1.20 | We load its `lib_nal.metta`, `src/skills.metta`, `src/utils.metta`, `src/helper.py` unmodified |
| Python | CPython | 3.12.13 via uv | hyperon fallback wheels stop at 3.12; janus builds fine |
| API | FastAPI / uvicorn / pydantic | 0.142.2 / 0.54.0 / 2.13.5 | Verified with the PeTTa engine |
| HTTP client | httpx | latest | Sync calls between agents, Jev fallback |
| Jev | `typesafe-sdk` | 0.7.2, model pinned `jev-1.13.0` | Verified live; about 390 ms per note |
| Web | Next.js / React | 16.3.6 / 19.2.8 | shadcn default template |
| UI | shadcn/ui CLI | 4.21.x, style `base-nova`, base `base` (Base UI), icon `lucide` | Pure shadcn as required |
| CSS | Tailwind CSS v4 + tw-animate-css | ^4 | shadcn default |
| Charts | shadcn `chart` (Recharts v3) | | BP trend for the memory screen |
| Forms | react-hook-form + zod + shadcn `Field` | | Current shadcn forms pattern |
| Theme | next-themes | ^0.4.6 | Light, dark, system |
| Fonts | Inter (sans), Geist Mono (mono) via `next/font` | | Söhne (Stripe) is commercial |
| Tests | pytest, Playwright | | |
| Package managers | **uv** (Python), **pnpm** (JS). Never npm or yarn. | | Global rule |

Fallback runtime, only if PeTTa breaks on the build machine: `hyperon==0.2.10` on Python 3.12 with two shims (define `min`/`max`; call `|-nal` directly). Verified to give identical numbers (0.59049, 0.74253). See research.md.

---

## 6. The Omega Agent Core (MeTTa)

### 6.1 Design principles

1. **Rules are data.** Every rule is an atom `(rule <pack> <id> <version> <body> <stv>)` so it can be listed, versioned, diffed, contested and replaced with `remove-atom`/`add-atom`. Never only `=` definitions.
2. **Every conclusion is a proof term**, never a bare label: `(conclusion <claim> <stv> (because ...))`.
3. **Evidence carries provenance.** Readings know who measured them, where, when, at what gestational age, whether repeated after rest, and whether taken after treatment.
4. **Truth values on everything**, computed by **Omega's unmodified `lib_nal.metta`** (`|-nal` deduction and revision). We never re-implement NAL in Python.
5. **Missing is not normal.** An absent reading is `unknown` and blocks a rule; it never defaults to "normal".
6. **Conflicts resolve by defeat or revision, never by averaging silently.** Agreeing evidence is **revised** (confidence goes up). Discounted evidence is **defeated** by an explicit defeater rule, and the proof says which one.
7. **Fail safe.** If a sign is `needs_review` and unconfirmed, the referral rules treat it as present and the explanation says so.

### 6.2 Atom vocabulary

```metta
;; A mother (synthetic) known to an agent
(mother M-AMINA (age 27) (gravida 2) (para 1))

;; A visit / encounter
(encounter E-17 M-AMINA (site home) (by chp) (ga-weeks 34) (at "2026-10-02T21:40"))

;; A reading with provenance. kind: sbp dbp pulse temp protein hb
(reading R-31 E-17 sbp 152)
(reading R-32 E-17 dbp 98)
(prov R-31 (repeated no) (after-treatment none) (device aneroid))
(prov R-32 (repeated no) (after-treatment none) (device aneroid))

;; A sign: status present | absent | not-mentioned | needs-review ; source jev | chp | nurse
(sign S-11 E-17 severe-headache present (source chp))
(sign S-12 E-17 visual-disturbance present (source chp))

;; Treatment given (affects how later readings are interpreted)
(treatment T-2 E-18 nifedipine-oral (at "2026-10-02T22:50"))

;; Witness tag: which agent asserted this encounter (set on sync)
(witness E-17 community)
(witness E-18 facility)

;; Contest: a clinician withdraws a premise
(contested S-11 (by nurse-baraka) (reason "headache resolved after paracetamol"))
```

### 6.3 From readings to findings (evidence.metta)

Findings are derived symbols such as `htn` (BP at or above 140/90), `severe-htn` (at or above 160/110), `proteinuria`, `early-normal-bp` (BP below 140/90 before 20 weeks). Each finding carries an evidence truth value computed from provenance:

| Provenance | Evidence truth `(stv f c)` | Rationale |
|---|---|---|
| Reading repeated after rest, both above threshold | `(stv 1.0 0.9)` | WHO ANC guidance: confirm a raised BP with a repeat after 10 to 15 min rest |
| Single unrepeated reading above threshold | `(stv 1.0 0.6)` | Real but unconfirmed |
| Reading below threshold, no treatment given before it | `(stv 0.0 0.8)` | Negative evidence for the finding |
| Reading below threshold **taken after an antihypertensive** | defeated: not evidence against `htn` | Treatment explains the drop |
| Sign reported by mother via CHP | `(stv 1.0 0.8)` | Symptoms are self-reported |
| Sign `needs-review` and unconfirmed | `(stv 1.0 0.5)` plus flag `fail-safe` | Fail safe toward referral |
| Lab dipstick protein at or above 2+ | `(stv 1.0 0.9)` | Facility lab |

Sketch (to be finalised in code; style mirrors the verified demo):

```metta
(threshold htn sbp 140) (threshold htn dbp 90)
(threshold severe-htn sbp 160) (threshold severe-htn dbp 110)
(threshold proteinuria protein 2)

;; evidence truth from provenance
(= (reading-truth $r)
   (match &self (prov $r (repeated $rep) (after-treatment $tx) $_)
     (if (== $rep yes) (stv 1.0 0.9) (stv 1.0 0.6))))

;; a finding supported by one reading
(= (supports $m $f)
   (match &self (threshold $f $k $t)
     (match &self (reading $r $e $k $val)
       (match &self (encounter $e $m $site $by (ga-weeks $ga) $at)
         (if (>= $val $t)
             (evidence $f $r (from $e $site $k $val >= $t) (reading-truth $r))
             (empty))))))

;; a finding opposed by one reading (below threshold)
(= (opposes $m $f)
   (match &self (threshold $f $k $t)
     (match &self (reading $r $e $k $val)
       (match &self (encounter $e $m $site $by (ga-weeks $ga) $at)
         (if (< $val $t)
             (if (after-treatment? $r)
                 (defeated $f $r (because treated-before-reading))
                 (counter $f $r (from $e $site $k $val < $t) (stv 0.0 0.8)))
             (empty))))))
```

### 6.4 Reconciliation (reason.metta)

For each finding the facility agent collects supporting evidence, counter-evidence and defeated evidence from **both witnesses and its own memory**, then:

1. **Defeat.** Drop every item matched by a defeater rule, keep it in the proof under `defeated` with the defeater id.
2. **Revise.** Fold the surviving items pairwise with Omega's NAL revision (`|-nal` on two judgements about the same term). Agreeing items raise confidence; conflicting surviving items pull the frequency toward the middle, which lowers the chance the rule clears Omega's action threshold.
3. **Contest.** Any premise with a `(contested <id> ...)` atom is excluded before step 1 and listed under `withdrawn` with who and why.
4. **Deduce.** Run the pack's rules as NAL deduction chains (`|-nal`) over the reconciled findings, exactly like the verified demo (two-step conditional deduction for two-premise rules; three-premise rules chain one more step).
5. **Decide.** Map the strongest conclusion to a risk level and action using Omega's documented thresholds: **act** if `f ≥ 0.6 and c ≥ 0.5`; **hypothesise** (ask for confirmation, for example "repeat BP after 15 minutes rest") if `f ≥ 0.3 and c ≥ 0.2`; otherwise no finding.

Proof term emitted (simplified):

```metta
(decision REF-9 M-AMINA
  (level emergency) (action stabilise-and-transfer)
  (conclusion pe-severe (stv 0.9 0.61)
    (because (rule full-v1 r_pe_severe v1)
      (premise htn (stv 1.0 0.83)
        (revised (evidence htn R-31 (from E-17 home sbp 150 >= 140) (stv 1.0 0.9))
                 (evidence htn R-44 (from E-18 facility sbp 148 >= 140) (stv 1.0 0.6)))
        (defeated (evidence-against htn R-41 (from E-18 facility sbp 138 < 140))
                  (by treated-before-reading T-2)))
      (premise new-onset (stv 1.0 0.9) (from memory E-03 (ga-weeks 14) sbp 116))
      (premise proteinuria (stv 1.0 0.9) (from E-18 facility protein 2))
      (premise severe-symptom (stv 1.0 0.8) (from E-17 home severe-headache present))
      (step 1 ...) (step 2 ...) (step 3 ...)))
  (withdrawn) (witnesses community facility) (pack full-v1))
```

`R-44` in this sketch is the second facility reading (repeat at 20 minutes). The exact numbers in the shipped proof come from Omega's `lib_nal` at run time; the golden tests pin them.

### 6.5 The answer diff

`proof.py` compares the edge decision (from the packet) and the reconciled decision and emits a list of typed changes. These render in the Diff panel:

| Change type | Example |
|---|---|
| `level_changed` | Urgent → Emergency |
| `action_changed` | "Refer to facility today" → "Stabilise and transfer; senior clinician now" |
| `premise_added` | `proteinuria` from the facility lab |
| `premise_from_memory` | `new-onset` from the 14-week visit in the facility's memory |
| `premise_defeated` | facility BP 138/88 defeated by `treated-before-reading` |
| `premise_revised` | `htn` confidence 0.60 → 0.83 after two agreeing witnesses |
| `premise_withdrawn` | headache withdrawn by nurse (contest) |
| `rule_changed` | `edge.r_htn_symptom v1` → `full.r_pe_severe v1` |
| `truth_changed` | `(stv 0.9 0.49)` → `(stv 0.9 0.61)` |

### 6.6 Omega plugin entry (mizani.metta)

The same files load in our FastAPI host and as a drop-in Omega plugin. The plugin shape was verified: after `!(loadOmegaPlugin)`, `(getSkills)` lists our skills, and Omega's own `metta` skill can run them.

```metta
!(import! &self (library Omega ./plugins/mizani/evidence))
!(import! &self (library Omega ./plugins/mizani/reason))
(= (loadOmegaPlugin)
   (progn
     (add-skill assess    "Decide referral for a mother's latest encounter; returns a NAL proof" (mother))
     (add-skill reconcile "Reconcile community and facility evidence for a referral; returns proof and defeats" (referral))
     (add-skill why       "Explain which premises of a rule are present, absent, defeated or withdrawn" (referral rule_id))
     (add-skill contest   "Withdraw a premise with a reason and recompute" (referral premise_id reason))
     ()))
```

### 6.7 Memory (memory.py)

- File: `agent/memory/<role>.metta`. One line per event: `(event <iso-ts> <op> <atom>)` where op is `add` or `remove`.
- Every mutation goes through `Memory.apply(op, atom)`: write to the space, then append to the file, then `fsync`.
- Startup: load Omega, load the plugin and the role's pack, then replay the log in order.
- Export: `GET /memory/log` (JSON list) and `GET /memory/export` (raw `.metta`), used for `docs/audit-trail.md`.
- Seed: `make seed` truncates both logs and writes the scenario atoms through the same path, so seeded and live events look identical.

### 6.8 Engine host (engine.py)

```python
# key points only; see research.md for the verified workarounds
os.environ["PETTA_PATH"] = str(VENDOR / "petta")
from petta import PeTTa
import janus_swi as janus

class Engine:
    def __init__(self, role: str):
        janus.query_once(f"assertz(working_dir('{AGENT_DIR}'))")  # makes import! work when hosted
        self.m = PeTTa(); self.m.verbose = False                   # constructor flag is buggy
        self.lock = threading.Lock()                               # one Prolog engine per process
        for f in [OMEGA / "lib_nal.metta", PLUGIN / "evidence.metta",
                  PLUGIN / "reason.metta", PLUGIN / f"packs/{PACK[role]}.metta"]:
            self.m.load_metta_file(str(f))

    def run(self, code: str) -> list[str]:
        with self.lock:
            return self.m.process_metta_string(code)
```

Run uvicorn with **one worker per agent** (each worker would otherwise be a separate in-memory space).

---

## 7. Clinical Rule Packs

All thresholds come from WHO ANC recommendations and the WHO SMART Guidelines ANC decision logic, ISSHP definitions, and Kenya MOH guidance, cited in [problem.md](problem.md) and [research.md](research.md). They are simplified for a demonstration and are **not** clinical advice.

### 7.1 Edge pack `edge-v1` (community agent, small on purpose)

| Rule id | If | Then | Rule truth |
|---|---|---|---|
| `r_danger_bleed` | heavy vaginal bleeding present | emergency referral | (stv 0.95 0.9) |
| `r_danger_fits` | convulsions present | emergency referral | (stv 0.95 0.9) |
| `r_severe_htn` | severe-htn (≥160 systolic or ≥110 diastolic) | emergency referral | (stv 0.9 0.9) |
| `r_htn_symptom` | htn (≥140/90) **and** any severe symptom (severe headache, visual disturbance, epigastric pain, dizziness, vomiting) | urgent referral today (WHO ANC.DT.17) | (stv 0.9 0.9) |
| `r_danger_sign` | any WHO ANC.DT.01 danger sign on its own (severe headache, visual disturbance, severe abdominal pain, unconscious, looks very ill) | urgent referral today | (stv 0.9 0.85) |
| `r_htn_unconfirmed` | htn on a single unrepeated reading, no symptoms | **Watch**: repeat BP after 10 to 15 minutes rest (WHO ANC.DT.04) | (stv 0.8 0.8) |
| `r_htn_confirmed` | htn on a repeated reading, no symptoms | **Urgent**: refer today for urine protein testing (WHO ANC.DT.12; CHPs carry no dipstick) | (stv 0.85 0.85) |
| `r_fever` | temperature ≥ 38.0 °C | urgent referral today | (stv 0.85 0.85) |
| `r_rfm` | reduced or absent fetal movement | urgent referral today | (stv 0.85 0.85) |
| `r_prom` | membranes ruptured **and** not in labour **and** GA < 37 weeks | urgent referral today | (stv 0.85 0.85) |
| `r_breath` | difficulty breathing | urgent referral today | (stv 0.85 0.85) |

### 7.2 Full pack `full-v1` (facility agent)

Everything in `edge-v1`, plus:

| Rule id | If | Then |
|---|---|---|
| `r_new_onset` | htn at or after 20 weeks **and** memory shows BP below 140/90 before 20 weeks | finding `new-onset` (gestational hypertension or pre-eclampsia, not chronic) |
| `r_chronic` | htn recorded before 20 weeks | finding `chronic-htn` |
| `r_pe` | new-onset **and** proteinuria (≥2+) | pre-eclampsia, urgent, admit for assessment |
| `r_pe_severe` | pre-eclampsia **and** (severe-htn or severe symptom) | pre-eclampsia with severe features, **emergency**: stabilise and transfer per protocol |
| `r_shock` | shock index (pulse ÷ systolic) ≥ 0.9 refer; ≥ 1.4 urgent transfer; ≥ 1.7 critical (El Ayadi 2016; Nathan 2015, 2019; CRADLE VSA) | urgent at 0.9, emergency at 1.4 and above |
| `r_pph` | postpartum, measured blood loss ≥ 300 mL with pulse > 100 or SI > 1 or SBP < 100 or DBP < 60, or blood loss ≥ 500 mL (WHO/FIGO/ICM 2025) | emergency: start the MOTIVE bundle per protocol |
| `r_anaemia_severe` | Hb < 70 g/L (WHO 2024 severe band) | urgent |

### 7.3 Defeater rules (facility agent)

| Defeater id | Defeats | When |
|---|---|---|
| `d_treated` | a below-threshold BP as evidence against htn | the reading was taken after an antihypertensive in the same episode |
| `d_unrepeated` | does not defeat, but lowers truth to (stv 1.0 0.6) | the above-threshold reading was not repeated after rest |
| `d_stale_protein` | a proteinuria result | the dipstick is older than 7 days (P1 patch example) |
| `d_contested` | any premise | a clinician contested it (recorded with name and reason) |

### 7.4 Risk levels and actions

| Level | When | Default action copy (Title Case in UI badges, sentence case in text) |
|---|---|---|
| **Emergency** | Any emergency rule acts | "Stabilise and transfer now. Call the senior clinician." |
| **Urgent** | Any urgent rule acts | "Refer to facility today." / at facility: "Admit for assessment today." |
| **Watch** | A rule only reaches the hypothesise band | "Repeat the reading after 15 minutes rest, then reassess." |
| **Normal** | No rule fires | "Continue routine antenatal care." |

---

## 8. Backend (FastAPI + PeTTa)

### 8.1 Process model

| Process | Command | Port | Env |
|---|---|---|---|
| Community agent | `uv run uvicorn mizani.app:create_app --factory --port 8101` | 8101 | `MIZANI_ROLE=community`, `MIZANI_PEER=http://127.0.0.1:8102`, `TYPESAFE_API_KEY` (optional) |
| Facility agent | same | 8102 | `MIZANI_ROLE=facility` |

### 8.2 Endpoints

Common (both roles):

| Method | Path | Purpose | Response |
|---|---|---|---|
| GET | `/health` | Role, pack id and version, Omega commit, PeTTa version, event count | `Health` |
| GET | `/rules` | Rule atoms of the active pack | `Rule[]` |
| GET | `/mothers/{id}` | Everything this agent remembers about the mother | `MotherMemory` |
| GET | `/memory/log` | Event log (paged, newest first) | `Event[]` |
| GET | `/memory/export` | Raw `.metta` log download | text |

Community role:

| Method | Path | Purpose |
|---|---|---|
| POST | `/visits/extract` | Free-text note → Jev → proposed sign statuses + BP candidates (or `mode=offline_manual`) |
| POST | `/visits` | Confirmed visit → atoms → `assess` (edge pack) → `Decision` + packet in outbox |
| GET | `/outbox` | Pending packets |
| POST | `/connectivity` | `{online: bool}`: the demo toggle; when true, flush the outbox to the peer |

Facility role:

| Method | Path | Purpose |
|---|---|---|
| POST | `/sync` | Receive a packet from the community agent (idempotent by packet id) |
| POST | `/encounters` | Facility readings for a referral (arrival BP, repeat BP, dipstick, treatment given) |
| GET | `/referrals` | Inbox list with level, mother, time, status |
| GET | `/referrals/{id}` | Two-witness view: both witnesses' evidence, reconciled `Decision`, `Diff`, explanations |
| POST | `/referrals/{id}/reconcile` | Recompute (idempotent) |
| POST | `/referrals/{id}/contest` | `{premise_id, reason, by}` → recompute → new `Decision` + `Diff` vs previous |
| POST | `/referrals/{id}/override` | P1: clinician sets a level with reason → proposed rule patch |
| POST | `/rules/patches/{id}/approve` | P1: reviewer approves → new rule version, diff |

### 8.3 Core schemas (pydantic, abbreviated)

```python
RiskLevel = Literal["normal", "watch", "urgent", "emergency"]

class Truth(BaseModel):
    f: float; c: float                       # Omega (stv f c)

class Premise(BaseModel):
    id: str                                  # e.g. "htn", or atom id "S-11"
    label_en: str; label_sw: str
    truth: Truth
    status: Literal["used", "revised", "defeated", "withdrawn", "missing"]
    sources: list[EvidenceRef]               # reading / sign ids, encounter, site, witness
    defeated_by: str | None = None
    withdrawn_by: str | None = None; withdrawn_reason: str | None = None

class Decision(BaseModel):
    id: str; mother_id: str; agent: Literal["community", "facility"]
    pack: str; level: RiskLevel; action_en: str; action_sw: str
    conclusion: str; truth: Truth
    band: Literal["act", "hypothesise", "none"]
    premises: list[Premise]
    proof_tree: dict                         # parsed s-expression for the tree view
    proof_raw: str                           # verbatim MeTTa output
    explanation_en: list[str]; explanation_sw: list[str]
    created_at: datetime

class Change(BaseModel):
    type: Literal["level_changed", "action_changed", "premise_added", "premise_from_memory",
                  "premise_defeated", "premise_revised", "premise_withdrawn",
                  "rule_changed", "truth_changed"]
    before: str | None; after: str | None
    reason_en: str; reason_sw: str

class Diff(BaseModel):
    from_decision: str; to_decision: str; changes: list[Change]
```

### 8.4 Input validation and injection safety

The verified demo interpolated request strings into MeTTa. We do not.

- Every id is generated server side (`E-`, `R-`, `S-`, `REF-` plus a counter) or validated against `^[A-Za-z0-9_-]{1,40}$`.
- Numeric readings are pydantic `conint`/`confloat` with physiological ranges (systolic 60 to 260, diastolic 30 to 160, pulse 30 to 220, temp 34.0 to 42.5, protein 0 to 4, Hb 3 to 20, GA 4 to 44).
- Sign names and statuses are `Literal` enums. Free text (notes, contest reasons) **never enters MeTTa as code**: it is stored as a quoted MeTTa string after escaping `\` and `"`, or kept only in the JSON sidecar.
- `atoms.py` builds atoms from typed values only; `test_atoms.py` tries injection payloads such as `) (remove-atom &self` and asserts they are rejected or quoted.

### 8.5 Errors

- Consistent envelope: `{ "ok": false, "error": { "code": "...", "message": "..." } }` with HTTP 4xx/5xx.
- MeTTa returns nothing (no rule fired): this is a valid `normal` decision with `why` output, not an error.
- PeTTa exception: 500 with code `reasoner_error`, full detail logged server side, generic message to the client.
- Peer unreachable: not an error for the community agent; the packet stays queued and `/outbox` shows it.

---

## 9. Jev Integration (Language Understanding)

Jev reads; Omega decides. Jev never produces a number, a threshold or a decision. All of this was tested live on 12 Swahili, English and Sheng notes (118 of 120 sign judgements correct, no missed present sign, about 390 ms per note); see research.md.

- Endpoint: `POST https://api.typesafe.ai/v1/systemone`, model pinned `jev-1.13.0`, one request per note.
- Questions: one **Choice** per danger sign with options `present`, `absent`, `not_mentioned`; definitions carry exclusions (feet-only swelling is not face/hand swelling; shivering and confusion are not convulsions).
- BP: a regex finds every `NNN/NN` candidate; a Choice picks today's reading; code parses it. Jev cannot invent digits.
- Derived facts are never asked ("early", "severe"). We ask literal facts (membranes ruptured, labour started, gestational weeks) and the MeTTa rule decides.
- Gate: confidence below 0.60, or P(present) above 0.15 on a non-present answer, becomes `needs_review`; the CHP must tap to confirm before submit.
- Client: one shared `AsyncTypeSafeClient`, timeout 3 s, one retry. Any failure returns `mode=offline_manual` and the UI simply shows the manual toggles.
- Audit: the raw answers, request id, model version and a hash of the question set are stored with the encounter and shown in the evidence drawer ("Jev 0.98, confirmed by CHP").
- Privacy: names and phone numbers are stripped before sending. Only synthetic notes are used in this hackathon.

---

## 10. Explanations In English And Swahili

Explanations are **rendered from the proof JSON with templates**, so they cannot say anything the proof does not contain. No LLM writes clinical text.

| Key | English | Swahili |
|---|---|---|
| `htn_used` | BP {sbp}/{dbp} at {site} is at or above 140/90. | Presha {sbp}/{dbp} ({site}) iko juu ya 140/90 au zaidi. |
| `unrepeated` | It was measured once, not repeated after rest, so Mizani is less sure. | Ilipimwa mara moja tu bila kurudia baada ya kupumzika, kwa hivyo Mizani haina uhakika sana. |
| `defeated_treated` | The clinic reading {sbp}/{dbp} came after {drug}, so it does not show the pressure is normal. | Kipimo cha kliniki {sbp}/{dbp} kilichukuliwa baada ya {drug}, kwa hivyo hakionyeshi kuwa presha ni ya kawaida. |
| `from_memory_new_onset` | At {ga} weeks her BP was {sbp}/{dbp}. High BP that starts after 20 weeks points to pre-eclampsia. | Katika wiki {ga} presha yake ilikuwa {sbp}/{dbp}. Presha inayopanda baada ya wiki 20 inaashiria kifafa cha mimba (pre-eclampsia). |
| `protein` | Urine protein is {grade}+. | Protini kwenye mkojo ni {grade}+. |
| `symptom` | She reports {symptom}. | Anasema ana {symptom_sw}. |
| `withdrawn` | {premise} was withdrawn by {who}: "{reason}". | {premise_sw} imeondolewa na {who}: "{reason}". |
| `level_emergency` | Emergency. Stabilise and transfer now. Call the senior clinician. | Dharura. Mtulize na umpeleke hospitali sasa. Mwite daktari mkuu. |
| `level_urgent` | Urgent. Refer to the facility today. | Haraka. Mpeleke kituo cha afya leo. |
| `level_watch` | Watch. Repeat the reading after 15 minutes rest, then reassess. | Angalia. Rudia kipimo baada ya dakika 15 za kupumzika, kisha tathmini tena. |
| `level_normal` | Normal. Continue routine antenatal care. | Kawaida. Endelea na kliniki za kawaida za ujauzito. |

The Swahili strings must be reviewed by a fluent Kenyan speaker before the video (Eugene). Keep sentences short and concrete for low-literacy reading. Swahili clinical terms follow Kenya MOH usage where known (for example *kifafa cha mimba* for eclampsia/pre-eclampsia in community usage); flag uncertain terms in `lib/i18n.ts` comments.

---

## 11. Frontend (Next.js + Pure shadcn/ui)

### 11.1 Rules

1. **Only shadcn/ui components** (generated into `components/ui/`) plus Tailwind utilities and lucide icons. No other UI kit, no custom CSS framework. Compositions live in `components/mizani/`.
2. Base UI flavour: use the `render` prop, not `asChild`.
3. **Title Case** for every page title, heading, card title and button. Sentence case for body and helper text. **No em or en dashes in any UI copy** (enforced by `scripts/check-no-dashes.sh` over `web/app` and `web/components/mizani` and `web/lib/i18n.ts`).
4. Light and dark mode via next-themes; every screen is checked in both.
5. Colour is never the only signal: risk levels always pair colour, icon and label.
6. Works at 360 px width (the community screen is designed mobile-first; CHPs use phones).

### 11.2 Setup commands

```bash
cd web
pnpm dlx shadcn@latest init -t next -b base --pointer -n web     # base-nova, neutral, lucide, Geist
pnpm dlx shadcn@latest add @shadcn/font-inter
pnpm dlx shadcn@latest add sidebar breadcrumb separator card table badge button button-group \
  input input-group textarea select native-select checkbox radio-group switch toggle-group field label \
  dialog alert-dialog sheet drawer popover tooltip hover-card dropdown-menu command kbd \
  tabs accordion collapsible scroll-area resizable chart sonner alert progress spinner skeleton \
  empty item avatar marker
pnpm add react-hook-form @hookform/resolvers zod recharts date-fns @tanstack/react-table
pnpm add -D @playwright/test
```

Then replace the token block in `app/globals.css` with the "Stripe Clinical" tokens (section 12) and set `"packageManager": "pnpm@<version>"` in `package.json`.

### 11.3 Data fetching

- `app/api/[role]/[...path]/route.ts` proxies to `AGENT_COMMUNITY_URL` / `AGENT_FACILITY_URL` (server env). The browser never talks to the agents directly, and no secret ever reaches the browser.
- Client components use `fetch` with a small `useAgent()` hook (SWR-like polling every 2 s on the facility inbox; no extra library needed).
- Optimistic UI only for toggles; decisions always come from the agent.

---

## 12. Design System

The full research, with verified contrast ratios and colour-blindness checks, is in research.md (Design section). Summary of what we apply:

### 12.1 Look and feel

- **Stripe-inspired, pure shadcn.** Navy ink text, one blurple primary action per view, hairline borders, two-layer navy-tinted shadows, 8 px spacing grid, `radius: 0.5rem`, tabular numerals for every number, calm motion (150 to 300 ms, `cubic-bezier(0.25, 1, 0.5, 1)`, wrapped in `motion-safe`).
- Dark mode is **deep navy** (`#070e1b` background, `#0e1727` cards), not black.
- Type: Inter for UI, Geist Mono for MeTTa and proof text. App body 14 px (`text-sm`), page titles `text-2xl font-semibold tracking-[-0.015em]`, KPIs `text-3xl font-medium tabular-nums`. The welcome hero uses `text-5xl md:text-6xl font-light tracking-[-0.025em]` (light weight only at display sizes).

### 12.2 Tokens

`web/app/globals.css` uses the shadcn token set from research.md section 9.5 verbatim:
- primary `oklch(0.52 0.25 277)` (about `#5142f3`) light, `oklch(0.7 0.158 275)` dark;
- foreground `oklch(0.22 0.05 252)` (about Stripe `#061b31`);
- inputs with a 3:1 boundary;
- charts `chart-1..5` on hues that avoid the risk hues;
- a four-level **risk scale**, each level with four tokens (`--risk-<level>`, `-foreground`, `-subtle`, `-subtle-foreground`) exposed through `@theme inline` as `bg-risk-urgent`, `text-risk-watch-subtle-foreground`, and so on.

### 12.3 Risk semantics

| Level | Badge | Icon (lucide) | Extra emphasis |
|---|---|---|---|
| Normal | subtle teal-green | `CircleCheck` | none |
| Watch | subtle amber with border | `Eye` | none |
| Urgent | solid orange | `TriangleAlert` | card `border-l-4 border-l-risk-urgent` |
| Emergency | solid deep red, semibold | `Siren` | page `Alert` banner + `AlertDialog` acknowledgement |

Visual weight rises with severity. Emergencies are never shown as a toast.

### 12.4 Diff colours

Diffs do **not** use red and green (those mean clinical risk here). Added items: `bg-accent text-accent-foreground` with a `+` gutter. Removed or defeated items: `bg-muted text-muted-foreground line-through` with a `−` gutter. Changed values: old value struck through, `ArrowRight`, new value.

---

## 13. Pages, Screens And Components In Detail

### 13.1 App shell (all pages)

- `SidebarProvider` + `Sidebar variant="inset" collapsible="icon"` (pattern from `dashboard-01` / `sidebar-07`).
- Sidebar header: Mizani wordmark (`Scale` lucide icon + "Mizani") and a **role switcher** `DropdownMenu`: "Community (Zawadi, CHP)" / "Facility (Baraka, Nurse)". Labelled "Demo Roles".
- Nav: Community Visit, Facility Inbox (with `SidebarMenuBadge` count), Mothers, Audit Log, Rules.
- Footer: connectivity `Switch` ("Online" / "Offline") for the community agent, `ModeToggle` (Light, Dark, System), agent health dots (community and facility: green dot plus pack version, or "Unreachable").
- Header: `SidebarTrigger`, `Breadcrumb`, a search `Button variant="outline"` with `Kbd` ⌘K opening `CommandDialog` (Go To Inbox, New Visit, Open Amina, Toggle Theme, Toggle Offline).
- A thin top `Alert` strip on every page: "Demo with synthetic data. Decision support, not diagnosis."

### 13.2 `/` Welcome

- Hero (Stripe pattern): eyebrow "Omega Agent Without Borders", H1 **"Two Witnesses, One Referral"**, subhead "Mizani weighs what the community health promoter saw against what the clinic sees, with Omega's own reasoning, and shows its working in English and Swahili.", buttons **"Start Community Visit"** (primary) and **"Open Facility Inbox"** (ghost, `ArrowRight`).
- Three `Card`s: "Decides Offline", "Remembers The Mother", "Shows Its Working".
- A small "How It Works" strip: 4 numbered steps with icons.
- Footer line: Omega commit, PeTTa version, pack versions (from `/health`).

### 13.3 `/community` Community Visit (mobile-first)

Layout: single column on mobile; on desktop, form on the left (7 cols), live decision on the right (5 cols, sticky).

1. **Connectivity banner** (`Alert`): Offline: `WifiOff` icon, "Offline. Decisions run on this device's rule pack (edge-v1)." Online: `Wifi`, "Online. Referrals sync to Mtwapa Health Centre."
2. **Mother** (`Field` + `Select`): pick from synthetic mothers or "Register Mother" (`Dialog`). Shows GA weeks.
3. **Visit Note** (`Field` + `Textarea`): placeholder "Andika maelezo kwa Kiswahili, Kiingereza au Sheng". Button **"Read Note"** (calls `/visits/extract`; `Spinner` while working). Offline: the button is disabled with helper text "Note reading needs a connection. Tap the signs below."
4. **Danger Signs** (`FieldSet` + grid of `ToggleGroup` rows): each sign has three states: Present / Absent / Not Asked. Rows filled by Jev show a small `Badge variant="outline"` "Jev 0.98"; `needs_review` rows get an amber outline and the text "Please confirm".
5. **Vitals** (`InputGroup` with unit addons): Systolic (mmHg), Diastolic (mmHg), Pulse (bpm), Temperature (°C); `Switch` "Repeated After 15 Minutes Rest"; `NativeSelect` "Treatment Given" (None, Nifedipine, Methyldopa, Magnesium Sulphate, Other). zod validation with hard ranges and soft warnings.
6. **Submit** (`Button` "Get Decision", sticky bottom bar on mobile, `h-11`).
7. **Decision card** (right column, `DecisionCard` component, see 13.8): risk badge, action sentence (English, Swahili `Tabs`), truth `(stv f c)` shown as two small `Progress` bars labelled Frequency and Confidence, "Why" premise list, rule id and version, "Queued, will sync when connection returns" or "Synced" `Badge`.

### 13.4 `/facility` Facility Inbox

- `Card` KPIs (dashboard-01 `section-cards` pattern): Incoming Today, Emergency, Urgent, Awaiting Review.
- `Table` (TanStack): Mother (Avatar initials + name + ID), GA, Community Decision (`RiskBadge`), Reconciled Decision (`RiskBadge` or "Pending"), Changed (`Badge` "Changed" if levels differ), Arrived (relative time with `Tooltip`), Status. Sort by severity, then time. Row click → `/facility/[referralId]`.
- `Empty` state: "No Referrals Yet" with "Waiting for the community agent to sync."

### 13.5 `/facility/[referralId]` Reconciliation (the hero screen)

Desktop layout (three regions):

1. **Header**: mother name, GA, referral id, `RiskBadge` (reconciled), Emergency `Alert` banner when applicable with **"Acknowledge"** (`AlertDialog`).
2. **Two Witnesses** (`ResizablePanelGroup`, two panels; stacked `Tabs` on mobile):
   - Left `Card` "Community Witness": who, where, when, offline flag, readings with provenance chips (`Badge variant="outline"`: "Single Reading", "Home", "Aneroid"), signs with source ("Entered by CHP" / "Jev 0.98, confirmed by CHP").
   - Right `Card` "Facility Witness": arrival readings, repeat readings, dipstick, treatment given with time, and a **"From Memory"** section (`Marker` separator) listing prior encounters the agent remembers (the 14-week visit).
   - Under both: **"Add Facility Reading"** `Sheet` (form like 13.3 vitals plus dipstick protein `NativeSelect` 0 to 4+ and treatment with time).
3. **Reconciled Decision** (`DecisionCard` large) with `Tabs`: **Reasoning** | **Proof** | **Changes** | **Kiswahili**:
   - Reasoning: the **premise ledger** (`PremiseList`): each premise as an `Item` with status icon (Used `CircleCheck`, Revised `GitMerge`, Defeated `Ban`, Withdrawn `Undo2`, Missing `CircleDashed`), truth value, sources (`HoverCard` with the raw atoms), and a **"Contest"** `Button variant="outline" size="sm"` that opens a `Dialog` ("Contest This Premise": reason `Textarea`, your name, **"Withdraw Premise"** / **"Cancel"**).
   - Proof: `ProofTree` (nested `Collapsible`s with `font-mono text-xs`, step numbers, NAL rule name, premises and derived truth) plus **"Copy Proof"** button and the verbatim MeTTa in a `ScrollArea`.
   - Changes: `DiffPanel` (section 12.4 colours): "Community Said" vs "Reconciled", then the typed change list with reasons.
   - Kiswahili: the explanation sentences in Swahili (and English beside them on desktop).
4. Recompute feedback: after a contest, a `sonner` toast "Recomputed. Decision stayed Urgent." (never for emergencies) and the Changes tab shows a second diff (previous reconciled vs new).

### 13.6 `/mothers/[motherId]` Mother Memory

- Header with mother, GA, gravida/para.
- **BP Over Pregnancy** chart (`ChartContainer` + `LineChart`): systolic `chart-1`, diastolic `chart-2`, `ReferenceLine` at 140 and 90, `ReferenceArea` bands using risk subtle tokens, points marked by witness (community vs facility) with a legend. "View As Table" toggle for accessibility.
- **Encounters** timeline (`Item` list with connector line): each encounter with site, witness, readings, decision badge.
- **Memory Atoms** (`Accordion`): the raw atoms this agent holds about the mother, in mono.

### 13.7 `/audit` Audit Log

- `Tabs`: Community Agent | Facility Agent.
- `Table` of events: time, op (`Badge` Add / Remove), atom (mono, truncated with `Tooltip`), plus a filter `InputGroup`.
- **"Download Memory"** button (`/memory/export`).
- `/rules` (sub-tab or page): active pack rules as `Item`s with id, version, body in mono, truth; P1 adds the patch proposals and approvals with `DiffPanel`.

### 13.8 Component inventory (`components/mizani/`)

| Component | Built from (shadcn) | Props |
|---|---|---|
| `RiskBadge` | Badge + cva | `level` |
| `TruthMeter` | Progress ×2 + Tooltip | `f`, `c`, `band` |
| `DecisionCard` | Card, Tabs, Badge, Item | `decision`, `size` |
| `PremiseList` | Item, ItemGroup, HoverCard, Button, Dialog | `premises`, `onContest` |
| `ProofTree` | Collapsible, ScrollArea | `tree`, `raw` |
| `DiffPanel` | Item, Badge, Separator | `diff` |
| `WitnessCard` | Card, Badge, Marker, Item | `witness`, `encounters` |
| `SignToggles` | Field, ToggleGroup, Badge | `signs`, `onChange` |
| `VitalsFields` | Field, InputGroup, Switch, NativeSelect | RHF `control` |
| `ConnectivitySwitch` | Switch, Tooltip, Badge | `online`, `onToggle` |
| `AgentHealth` | Badge, Tooltip | from `/health` |
| `BpChart` | Chart (Recharts) | `encounters` |
| `ModeToggle` | DropdownMenu, Button | |
| `CommandMenu` | Command, Kbd | |

### 13.9 States checklist (every data view)

Loading (`Skeleton` with final layout), empty (`Empty`), error (`Alert variant="destructive"` with **"Try Again"**), agent unreachable (`Alert` with health dot), offline (banner), success.

### 13.10 Accessibility

Keyboard reachable everything (Base UI handles focus); `aria-label` on risk badges ("Risk level: Urgent"); proof tree uses proper headings; charts have a table alternative; touch targets at least 44 px on mobile (`max-md:h-11`); inputs `text-base` on mobile to avoid iOS zoom; colour plus icon plus text for every status.

---

## 14. Synthetic Data And Scenarios

All names, places and numbers are invented. No real person is represented.

### Scenario A: "Amina" (the video). Reconciliation escalates.

| Witness | Encounter | Data |
|---|---|---|
| Facility memory | E-03, 14 weeks, ANC visit at Mtwapa HC | BP 116/74 (repeated), protein 0, Hb 11.2 |
| Facility memory | E-08, 24 weeks | BP 124/80 |
| Community (offline) | E-17, 34 weeks, home, 21:40 | BP 152/98, repeated after 15 minutes rest 150/96 (repeated yes); severe headache present; visual disturbance present; swelling of feet (not a danger sign on its own); note in Swahili |
| Facility | E-18, 34 weeks, arrival 23:30 | nifedipine oral given 22:50 by the transfer team; BP 138/88 at 23:30; repeat BP 148/96 at 23:50 (repeated); dipstick protein 2+ |

Expected: edge decision **Urgent** (`r_htn_symptom`); reconciled **Emergency** (`r_pe_severe`): htn revised up by the agreeing community and repeat readings, 138/88 defeated by `d_treated`, new onset from memory E-03, proteinuria 2+, severe symptom. After contesting the headache and the visual symptom: **Urgent** (`r_pe`).

### Scenario B: "Wanjiku". Reconciliation de-escalates to Watch.

Community: BP 142/92 single, not repeated (the mother had to leave), no symptoms, 30 weeks → edge **Watch** (`r_htn_unconfirmed`: repeat after rest). Facility: repeat after rest 128/82 (no treatment given), protein 0, memory shows 118/76 at 12 weeks. Expected reconciled **Normal** with advice "Recheck at next visit", and the diff shows the counter-evidence was not defeated (no treatment), so revision pulled the frequency below the act band.

### Scenario C: "Nafula". Witnesses agree; confidence rises.

Community: reduced fetal movement present, BP 118/76. Facility: RFM confirmed by nurse, BP normal. Expected **Urgent** both sides (`r_rfm`), confidence rises after revision, diff shows only `premise_revised`.

`make seed` writes A, B and C through `Memory.apply` and leaves the community agent **offline** with Amina's encounter not yet created, so the video starts clean.

---

## 15. Testing

| Layer | Tool | What |
|---|---|---|
| Reasoning | pytest (`tests/test_reasoning.py`) | For A, B, C: assert level, rule id, band, which premises are used, revised, defeated or withdrawn, and the truth values to 3 decimals (golden values captured from the first correct run and reviewed by hand against NAL formulas) |
| Memory | pytest | Restart the engine and replay the log; decisions are identical before and after restart |
| Atoms | pytest | Injection payloads rejected or quoted; out-of-range readings rejected |
| API | FastAPI TestClient | Each endpoint's happy path and one error; offline queue: packet stays queued when peer is down and flushes when it comes back |
| Jev | pytest, marked `network` | Skipped without `TYPESAFE_API_KEY`; mocked client test always runs for the fallback path |
| E2E | Playwright (`web/tests/e2e/demo.spec.ts`) | The video path: offline visit → decision Urgent → go online → facility inbox shows referral → open → Emergency → contest headache → Urgent |
| Copy | `scripts/check-no-dashes.sh` | No em or en dashes in UI copy |
| Build | `pnpm build`, `pnpm lint`, `uv run pytest` | CI-style gate before recording the video |

Target coverage for `agent/mizani/` is 80% or more (`uv run pytest --cov`).

---

## 16. Running It: One Command

Prerequisites (macOS shown; Linux equivalent in README): Homebrew, `brew install swi-prolog uv pnpm`, Node 20+.

```bash
git clone --recurse-submodules https://github.com/CodeWithEugene/Basix-Hackathon.git
cd Basix-Hackathon
cp .env.example .env            # TYPESAFE_API_KEY is optional; without it notes fall back to manual toggles
make setup                      # uv sync (agent), pnpm install (web)
make seed                       # synthetic scenarios A, B, C
make dev                        # community :8101, facility :8102, web :3000
```

`make dev` runs `scripts/dev.sh`, which starts both agents and the web app, waits for `/health`, and prints the URLs. `make test` runs pytest and Playwright.

Known setup workarounds (all handled in code, documented in README "Troubleshooting"):
1. `PeTTa().verbose = False` after construction.
2. `assertz(working_dir(...))` and `PETTA_PATH` before `import!`.
3. Do not use PeTTa's `run.sh` on macOS; we host PeTTa from Python.

---

## 17. Deployment (Optional)

P1 only. A `agent/Dockerfile` based on `swipl:10.0.2` (same base Omega uses), installs uv and Python 3.12, copies `agent/`, runs one uvicorn worker. Deploy two services from the same image with `MIZANI_ROLE` set differently (Railway or Fly). Frontend on Vercel with `AGENT_COMMUNITY_URL` and `AGENT_FACILITY_URL`. The live demo must use synthetic data only and should reset nightly (`make seed`).

---

## 18. Security, Privacy And Safety

- **Synthetic data only.** No real names, phone numbers, IDs or notes anywhere in the repo, the demo or the video.
- **Secrets:** `TYPESAFE_API_KEY` lives only in the git-ignored `.env` and server env. `.env.example` has placeholders. The Next.js proxy never forwards it; it is used only by the community agent.
- **Data minimisation for Jev:** strip names and numbers that look like phones before sending; log request ids, never note bodies; `TYPESAFE_LOG_LEVEL` stays at `info` or lower.
- **Injection:** no string interpolation of user input into MeTTa (section 8.4).
- **Kenya Data Protection Act 2019:** health data is sensitive personal data. A real deployment needs a data protection impact assessment, consent, a registered data controller and processor, and local hosting decisions. Stated in README and SECURITY.md.
- **Clinical safety:** "Decision support, not diagnosis" on every screen; fail safe toward referral; every decision overridable and contestable; rule changes require reviewer approval (P1) and are versioned; no LLM decides.
- **Honesty:** limitations section in README; the agent never claims certainty it does not have (truth values are always shown).

---

## 19. Docs And Submission Artifacts

| Artifact | Content | Source |
|---|---|---|
| `README.md` | First screen: name, tagline, video link, track and challenge, one-command run, one screenshot. Then Problem, Solution, How It Works (diagram), Omega usage (exact files loaded, commit), Technology, AI Disclosure, What's Next, Limitations, Credits, License | Hand-written |
| `docs/transcript.md` | Sample reasoning transcript of Scenario A: the edge proof, the sync, the reconciled proof, the contest and recompute, verbatim MeTTa plus plain-language lines | `scripts/export-transcript.py` from a real run |
| `docs/audit-trail.md` | One-page audit trail: who did what, when, with which rule version, for Amina's referral | Same script |
| `docs/ai-disclosure.md` | Full disclosure (tools, models, how used) | Hand-written |
| `docs/images/` | Screenshots, light and dark | Playwright screenshots |

AI Disclosure (draft, keep honest and update at the end):

> **AI Disclosure.** Claude Code (Anthropic, Claude Opus 5.5) was used for research, planning, writing documentation and writing and reviewing code, with every change reviewed by the author. TypeSafe Jev (`jev-1.13.0`) is used inside the product only to read visit notes into typed danger-sign observations, which the health worker confirms; it never makes or explains a clinical decision, and it was also used once during research to score candidate ideas against the judging rubric. All clinical reasoning is done by SingularityNET Omega's own NAL library (`lib_nal.metta`) running on PeTTa, over rules written by hand from WHO and Kenya MOH guidance. No LLM generates clinical text; explanations are templates filled from the proof.

---

## 20. The 3-Minute Video

Record at 1920×1080, light mode for the facility screens and the community screen in a 390 px phone frame, captions burned in, background music low. Voice: Eugene.

| Time | Shot | Voice-over (draft) |
|---|---|---|
| 0:00 to 0:20 | Title card "Mizani. Two Witnesses, One Referral." over a still of flooded road (stock, licensed) | "In Kenya, a mother's danger signs are often seen first by a community health promoter, far from a clinic. When the rains cut the road and the network, that first witness is alone." |
| 0:20 to 0:55 | Community screen, offline banner, Swahili note, signs, BP 152/98 and the repeat 150/96, Get Decision, Urgent with proof | "Mizani's community agent runs Omega offline with a small MeTTa rule pack. It decides Urgent, and shows why: high blood pressure confirmed by a repeat after rest, a severe headache, blurred vision. Its confidence is printed, not hidden." |
| 0:55 to 1:05 | Toggle online, toast synced | "When the network returns, the referral syncs." |
| 1:05 to 2:05 | Facility reconciliation: two witnesses, memory row, proof, diff Urgent to Emergency | "At the clinic, the facility agent remembers Amina. At 14 weeks her pressure was normal, so this is new. The lower reading here came after nifedipine, so Omega defeats it as evidence. Protein is 2+. The answer changes to Emergency, and Mizani shows exactly what changed and why, in English and Swahili." |
| 2:05 to 2:30 | Contest the headache, recompute, stays Urgent | "The nurse can challenge any premise. Withdraw the headache, and Omega recomputes. It is still pre-eclampsia, still urgent. The human is in charge, and the reasoning is on the record." |
| 2:30 to 2:45 | Memory and audit log | "Every step is an atom in Omega's memory, replayable and auditable." |
| 2:45 to 3:00 | What's next card | "Next: a pilot with community health promoters in one county, eCHIS integration, and a BGI Nexus grant. Mizani: reasoning that holds up across languages, distance and doubt." |

Production notes: record each beat separately with the seeded scenario, cut in an editor, keep total under 2:55. Upload unlisted to YouTube, check the link in a private window.

---

## 21. Submission Form Drafts

- **Title (≤80):** `Mizani: Two Omega Agents Reconcile A Maternal Referral` (54 chars)
- **Tagline (≤140):** `Offline Omega agent decides, the clinic's Omega agent remembers and reconciles, and every referral shows its working in English and Swahili.` (139 chars; recount before pasting)
- **Track:** Omega. **Problem:** The Agent Without Borders. State "Solo Track, challenge 01" in the description.
- **Description (aim 2,000 to 3,500 chars, Markdown):** what it does (3 sentences), how it works (Omega `lib_nal` on PeTTa, two agents, memory, defeat and revision, contest), why it matters (Kenya maternal deaths, the facility delay, CHPs), what's next, AI Disclosure line, links to transcript and audit trail.

---

## 22. Risks And Fallbacks

| Risk | Likelihood | Impact | Mitigation / fallback |
|---|---|---|---|
| PeTTa or janus breaks on setup | Low (verified today) | High | Pin versions; keep the verified demo as reference; fallback to `hyperon==0.2.10` with shims (same numbers) |
| MeTTa reconciliation logic takes too long | Medium | High | Build Scenario A end to end first; B and C after; if needed implement defeat selection in Python **but keep every truth computation and rule firing in MeTTa via `lib_nal`**, and say so in the README |
| NAL numbers look odd on video | Medium | Medium | Show `(stv f c)` with plain labels "how often" and "how sure"; explain once in the video |
| Two processes complicate the demo | Low | Medium | `make dev` starts both; health dots show status; seed resets |
| Jev down or no key | Low | Low | Manual toggles are the primary contract; offline beat shows them anyway |
| UI takes longer than planned | Medium | High | Build the Reconciliation screen first; Community screen second; Memory and Audit can be simple tables |
| Clinical inaccuracy criticised | Medium | High | Rules cite sources; disclaimer; "simplified for demonstration"; thresholds match WHO; invite review in What's Next |
| Video runs long | Medium | Medium | Script is timed; cut the Memory beat first |
| Deadline confusion | Low | Fatal | Submit by 21:00 EAT regardless |
| Omega engineers say "not real Omega" | Medium | High | Load Omega's files unmodified from a pinned submodule; plugin format; show `(getSkills)` output in README; P1.2 if time |

---

## 23. Hour-By-Hour Plan

Friday 2 October 2026, EAT. Buffers are real; protect them.

| Time | Work | Exit check |
|---|---|---|
| 09:00 to 10:45 | Research and docs (this file and its siblings) | Docs committed |
| 10:45 to 11:15 | Repo scaffold: submodules (Omega pinned, PeTTa v1.0.4), `agent/` uv project, `web/` shadcn init, Makefile, `.env.example` | `make setup` works |
| 11:15 to 13:15 | **Agent core**: engine, memory, atoms, evidence and reason MeTTa, packs, Scenario A end to end in pytest | Golden test A passes |
| 13:15 to 13:35 | Break, eat | |
| 13:35 to 14:45 | API for both roles, outbox and sync, contest, diff, explanations en/sw; Scenarios B and C | API tests pass |
| 14:45 to 17:15 | **Frontend**: shell, Reconciliation screen, Community screen, Inbox, Memory, Audit; tokens; dark mode | Demo path clickable |
| 17:15 to 17:45 | Jev wiring and fallback; Playwright demo test; dash check; polish | All tests green |
| 17:45 to 18:00 | Freeze code. Tag `v0.1.0` | |
| 18:00 to 19:30 | Record and edit video; screenshots; transcript and audit trail export | Video under 3:00, uploaded |
| 19:30 to 20:15 | README final, AI Disclosure, submission form filled | Form saved |
| 20:15 to 20:45 | Clean-clone test of setup; fix docs | Fresh clone runs |
| **20:45** | **Submit** | Confirmation visible |
| 20:45 to 21:29 | Buffer | |

If P0 is green by 16:00, take P1.1 (override to rule patch) first, then P1.2 (Omega chat) only if Docker and an LLM key are ready.

---

## 24. Definition Of Done

- [ ] `make setup && make seed && make dev` works from a fresh clone on macOS
- [ ] Both agents report Omega commit and pack version on `/health`
- [ ] Scenario A reproduces exactly the video beats; golden tests A, B, C pass
- [ ] Restarting the agents keeps every decision (memory replay)
- [ ] Offline really blocks sync; going online flushes the outbox
- [ ] Contest recomputes and the diff explains it
- [ ] English and Swahili explanations on every decision
- [ ] Light and dark mode correct; 360 px community screen works
- [ ] No em or en dashes in UI copy; Title Case on titles and buttons
- [ ] No secrets in git; synthetic data only; disclaimer visible
- [ ] README, transcript, audit trail, AI Disclosure, What's Next
- [ ] Video under 3:00, unlisted link works logged out
- [ ] Submitted on the platform before 21:00 EAT
