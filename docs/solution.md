# Solution: Mizani

> **What this file is.** The full, end-to-end solution for the problem in [problem.md](problem.md): who it is for, what they experience, how it works, why it works, why it is built on Omega, what is new about it, the proof that it will work, how it is governed, how it reaches real users, and what comes next. The engineering detail lives in [build.md](build.md).
>
> **Status:** v1.0, Friday 2 October 2026.

---

## Table Of Contents

1. [Mizani In One Screen](#1-mizani-in-one-screen)
2. [The Core Idea: Two Witnesses](#2-the-core-idea-two-witnesses)
3. [Audience And Personas](#3-audience-and-personas)
4. [The Experience End To End](#4-the-experience-end-to-end)
5. [How It Works](#5-how-it-works)
6. [Why It Works: Design Choice To Evidence](#6-why-it-works-design-choice-to-evidence)
7. [Why Omega And MeTTa (And Where Jev Fits)](#7-why-omega-and-metta-and-where-jev-fits)
8. [Language, Literacy And Connectivity](#8-language-literacy-and-connectivity)
9. [Safety, Governance And Law](#9-safety-governance-and-law)
10. [When And Where It Is Used](#10-when-and-where-it-is-used)
11. [What Is New, And An Honest Comparison](#11-what-is-new-and-an-honest-comparison)
12. [Proof It Will Work](#12-proof-it-will-work)
13. [Strengths, Weaknesses, Opportunities, Threats](#13-strengths-weaknesses-opportunities-threats)
14. [Sustainability: Who Pays, How It Scales](#14-sustainability-who-pays-how-it-scales)
15. [Roadmap And What's Next](#15-roadmap-and-whats-next)
16. [Success Metrics](#16-success-metrics)
17. [How It Maps To The Hackathon](#17-how-it-maps-to-the-hackathon)
18. [Pitch Library](#18-pitch-library)

---

## 1. Mizani In One Screen

| | |
|---|---|
| **Name** | **Mizani** (Swahili: "scales", the instrument that weighs two sides) |
| **One line** | **Two witnesses, one referral.** |
| **Tagline** | Omega weighs what the community saw against what the clinic sees, and shows its working. |
| **What it is** | Two SingularityNET **Omega** agents that reconcile a pregnant woman's referral between the community and the facility. The community agent decides **offline** with a small MeTTa rule pack. When the network returns, the facility agent, which **remembers the mother** and holds the full rule pack, reconciles the two witnesses' conflicting evidence with Omega's own **NAL** reasoning and produces a **contestable referral proof** in **English and Swahili**. |
| **For** | Kenya's Community Health Promoters (CHPs), the nurses and clinical officers who receive their referrals, and the county teams who review maternal deaths |
| **The one feature (solo brief)** | A referral decision that survives the handoff: reconciled, remembered, explained, and contestable |
| **Hackathon fit** | Track **Omega**; problem **The Agent Without Borders** (challenges 02 and 01); **Solo challenge 01** (one agent producing an auditable decision) |
| **Built with** | Omega (`singnet/Omega`, `lib_nal.metta`, plugin API) on **PeTTa** (Omega's runtime); FastAPI; Next.js with pure **shadcn/ui**; TypeSafe **Jev** for reading Swahili/Sheng notes |

---

## 2. The Core Idea: Two Witnesses

Every maternal referral has two witnesses who never meet.

```
   COMMUNITY WITNESS                                   FACILITY WITNESS
   CHP at the home, 21:40, offline                     Nurse at the clinic, 23:30
   ─────────────────────────────                       ─────────────────────────────
   BP 152/98, repeated 150/96                          BP 138/88 (40 min after nifedipine)
   Severe headache, blurred vision                     Repeat BP 148/96
   Swollen feet                                        Urine protein 2+
   No lab, no history                                  Memory: BP 116/74 at 14 weeks
           │                                                    │
           │   decides offline: URGENT                          │
           └───────────────────────┐        ┌───────────────────┘
                                   ▼        ▼
                        ┌───────────────────────────────┐
                        │   MIZANI RECONCILIATION       │
                        │   (Omega NAL on PeTTa)        │
                        │                               │
                        │ • revise: agreeing high BPs   │
                        │ • defeat: 138/88 was treated  │
                        │ • memory: new onset > 20 wks  │
                        │ • add: protein 2+             │
                        │ → pre-eclampsia, severe       │
                        └───────────────┬───────────────┘
                                        ▼
                     EMERGENCY. Stabilise and transfer now.
                     Proof: every premise, its source, its truth value,
                     what changed from the community decision and why.
                     The nurse can contest any premise; it recomputes.
```

Without reconciliation, the facility's 138/88 can be read as reassurance and the mother waits. Without the community witness, the facility never hears about the headache. Without memory, nobody can say the hypertension is **new**. Mizani puts all three on the same scales.

---

## 3. Audience And Personas

All personas are composites for design. No real person is represented.

### 3.1 Zawadi, Community Health Promoter (primary user, community side)

- 38, Kilifi County, covers about 100 households; trained under the 2023 CHP programme; KSh 5,000 monthly stipend (sometimes late); smartphone with eCHIS; kit with BP machine, thermometer, glucometer, timer; **no dipstick, no Hb meter**.
- Reads and writes Swahili and English, prefers Swahili for notes; mixes Sheng in speech.
- **Jobs to be done:** decide quickly whether to refer, do it correctly (repeat the BP), be believed at the facility, and learn what happened.
- **Pains:** no network during rains; paper MOH 100 forms; never hears back; feels blamed for "unnecessary" referrals and for late ones.
- **What Mizani gives her:** an offline decision with the guideline built in, a referral that carries her observations intact, and a reconciled outcome sent back to her.

### 3.2 Baraka, Nurse at a Level 3 health centre (primary user, facility side)

- 29, night shift, Mtwapa Health Centre (fictional for the demo), often the most senior clinician on site.
- **Jobs to be done:** recognise severe pre-eclampsia or haemorrhage within minutes, start the right first-line care, and transfer if needed.
- **Pains:** referral notes that say only "high BP"; no access to the mother's earlier ANC visits; readings taken after drugs given on the way; alert systems that cry wolf.
- **What Mizani gives him:** the two witnesses side by side, the mother's history, a reconciled level and action, and the ability to challenge any premise and see the result.

### 3.3 Amina, the mother (the person the system exists for)

- 27, second pregnancy, 34 weeks. Her first ANC visit at 14 weeks recorded a normal BP.
- **What she needs:** to be taken seriously, quickly, in her language.
- **What Mizani gives her:** a decision explained in Swahili that the CHP can read to her, and a facility that already knows her story when she arrives.

### 3.4 Dr. Otieno, Sub-county Reproductive Health Coordinator (secondary)

- Leads maternal death reviews (MPDSR) and supervises CHP programmes.
- **What Mizani gives him:** an append-only record of what each witness saw, which rule version decided, who contested what and why; and a governed way to change rules after a review.

### 3.5 Who is not a user in this version

Mothers do not use Mizani directly (that is the space of SMS services such as PROMPTS). Doctors at Level 5 and 6 hospitals are recipients of transfers, not users, in the first version.

---

## 4. The Experience End To End

### 4.1 Journey A: The night referral (the hero journey)

| Step | Who | Where | What happens | What Mizani does |
|---|---|---|---|---|
| 1 | Zawadi | Amina's home, 21:40, **offline** (flooded road, no data) | Amina reports a severe headache since yesterday and darkness in her eyes; her feet are swollen | Banner: "Offline. Decisions run on this device's rule pack." |
| 2 | Zawadi | Home | Types a Swahili note; taps danger signs (or, when online, Jev pre-fills them for her to confirm) | Signs recorded with their source ("Entered by CHP") |
| 3 | Zawadi | Home | Measures BP 152/98. Mizani asks for a repeat after 15 minutes rest (WHO). Repeat 150/96 | Provenance recorded: repeated yes, at home, aneroid device |
| 4 | Community agent | Phone | Applies the edge rule pack with Omega NAL | **Urgent: refer today.** Proof card: high BP confirmed by repeat, severe headache, visual disturbance; rule and version; truth value. Swahili and English. Packet queued. |
| 5 | Zawadi | Home | Arranges transport (motorbike); the transfer team gives oral nifedipine on the way per county protocol | Treatment can be recorded with time |
| 6 | Network | Roadside, 22:55 | Signal returns | Packet syncs to the facility agent; toast "Referral synced" |
| 7 | Baraka | Facility, 23:30 | Amina arrives; BP 138/88; repeat 148/96 at 23:50; urine dipstick 2+ | Baraka enters facility readings in the Reconciliation screen |
| 8 | Facility agent | Server | Merges both witnesses with its **memory** of Amina (14-week BP 116/74) and the full rule pack | **Revises** the agreeing high readings; **defeats** 138/88 as evidence against hypertension (taken after nifedipine); concludes **new-onset** hypertension after 20 weeks; adds proteinuria 2+; fires **pre-eclampsia with severe features** |
| 9 | Baraka | Facility | Sees **Emergency**, the action, the premises, and the diff: "Urgent → Emergency because: protein 2+ (new), new onset from 14-week memory, facility 138/88 defeated (after nifedipine)" | Emergency banner requires acknowledgement; never a toast |
| 10 | Baraka | Facility | Questions the headache: Amina says it eased after paracetamol. He **contests** the headache premise with that reason | Recomputes live: still **Urgent** pre-eclampsia (protein plus new onset); proof shows the premise withdrawn by Baraka with his reason |
| 11 | Baraka | Facility | Acts per protocol and arranges transfer | The decision, the contest and the action are in the audit log |
| 12 | Zawadi | Next morning, online | Opens the referral | Sees the reconciled outcome and why it changed (the back-referral the MOH 100 form intends but rarely gets) |

### 4.2 Journey B: The reading that was never repeated (de-escalation)

Zawadi visits Wanjiku at 30 weeks; one BP of 142/92; Wanjiku has to leave before a repeat; no symptoms. The community agent returns **Watch: repeat the BP after 15 minutes rest** (WHO ANC.DT.04) and a referral is queued for a check. At the facility, a rested BP is 128/82, no treatment given, protein negative, and memory shows 118/76 at 12 weeks. The facility agent does **not** defeat the normal reading (no treatment explains it), revision pulls the evidence for hypertension below Omega's action threshold, and the reconciled decision is **Normal: recheck at the next visit**. The diff shows exactly why. This is how Mizani avoids alert fatigue.

### 4.3 Journey C: Two witnesses agree

Zawadi records reduced fetal movement; the nurse confirms it. Both decide **Urgent**. Revision raises the confidence and the diff shows only "premise revised". Agreement is information too.

### 4.4 Journey D: A rule changes after a review (governed learning, P1)

After a review, the county decides that a dipstick result older than 7 days should not count as current proteinuria. A clinician's override proposes a rule patch; the coordinator reviews the **before/after MeTTa diff**; on approval the rule version bumps (for example `full-v1` to `full-v1.1`), the change is logged, and a replay shows which past referrals would have been decided differently. No rule changes itself without a human.

### 4.5 Journey E: The death review

If a mother dies, Dr. Otieno opens the audit log for her referrals: who measured what, when, with which provenance; which rule version decided; what the facility agent remembered; who contested which premise and why. The record supports a confidential-enquiry style avoidable-factor analysis.

---

## 5. How It Works

This section explains the concepts. The exact atoms, rules and code are in [build.md](build.md) sections 6 and 7.

### 5.1 Two agents, two memories

- The **community agent** and the **facility agent** are two separate Omega agents (two processes), each with its own atom space, its own rule pack and its own persistent memory (an append-only log of atoms, the same pattern as Omega's `memory/history.metta`).
- They share nothing except the **referral packet** the community agent sends when it can.
- The facility agent's memory includes the mother's earlier encounters. That memory is what turns "high BP today" into "**new-onset** high BP after 20 weeks".

### 5.2 Evidence with provenance

Every reading knows: who measured it (CHP, nurse), where (home, facility), when, at what gestational age, whether it was **repeated after rest**, whether it was taken **after treatment**, and with what device. Every sign knows its status (present, absent, not mentioned, needs review) and its source (CHP, nurse, Jev confirmed by CHP).

### 5.3 From evidence to findings, with truth values

Readings become findings such as `htn` (at or above 140/90), `severe-htn` (at or above 160/110), `proteinuria` (2+ or more), `new-onset` (hypertension after 20 weeks with a normal reading before 20 weeks in memory). Each piece of evidence carries an Omega truth value `(stv frequency confidence)`: a repeated reading is more certain than a single one; a self-reported symptom is a little less certain than a measurement; a sign Jev was unsure of and nobody confirmed is treated as present but weak, and flagged (fail safe).

### 5.4 Reconciliation: defeat, revise, contest

1. **Defeat.** Some evidence is explicitly discounted by a **defeater** rule, and the proof says which one. Example: a below-threshold BP taken after an antihypertensive is not evidence that the woman is normotensive.
2. **Revise.** Surviving evidence about the same finding is merged with Omega's **NAL revision**. Agreeing witnesses raise confidence. Conflicting surviving evidence pulls the frequency toward the middle, which can drop a conclusion from "act" to "confirm first".
3. **Contest.** A clinician can withdraw any premise with a reason. It moves to "withdrawn, by whom, why" and the decision recomputes.

### 5.5 Rules and decisions

Rules are atoms in versioned packs: the small **edge pack** on the community agent (danger signs, severe hypertension, hypertension with symptoms, unconfirmed and confirmed hypertension, fever, reduced fetal movement, preterm rupture of membranes, breathing difficulty) and the **full pack** on the facility agent (all of the edge pack plus new onset vs chronic, pre-eclampsia, pre-eclampsia with severe features, shock index tiers, the 2025 postpartum haemorrhage definition, severe anaemia). Rules fire as **NAL deduction chains** through Omega's `lib_nal.metta`, so each conclusion has a truth value and a step-by-step derivation. Omega's documented thresholds turn a conclusion into a decision band: **act** (frequency at least 0.6 and confidence at least 0.5), **confirm first** (frequency at least 0.3, confidence at least 0.2), or **none**.

### 5.6 Four levels, one action each

| Level | Meaning | Action |
|---|---|---|
| **Emergency** | Life-threatening now | Stabilise and transfer now; call the senior clinician |
| **Urgent** | Needs facility care today | Refer today / admit for assessment |
| **Watch** | Needs confirmation | Repeat the reading after 15 minutes rest, then reassess |
| **Normal** | No rule fires | Continue routine antenatal care |

### 5.7 The referral proof

What the facility (and later the CHP and the county) sees:

- The **level and action**, in English and Swahili.
- The **premises**, each with status (used, revised, defeated, withdrawn, missing), truth value, and sources (which witness, which reading, which encounter, from memory or not).
- The **rule** and **pack version** that decided.
- The **derivation** (each NAL step) and the verbatim MeTTa proof term.
- The **diff** from the community decision: level change, action change, premises added, premises from memory, premises defeated, premises revised, premises withdrawn, rule change, truth change, each with a reason.

### 5.8 Language understanding (Jev)

When online, the CHP can write a free-text note in Swahili, English or Sheng. TypeSafe **Jev** reads it into one typed status per danger sign (present, absent, not mentioned) with probabilities, and picks today's BP from the numbers in the note (a regex finds the candidates, Jev picks one, code parses it: Jev cannot invent a digit). Uncertain answers become "please confirm". The CHP confirms before the agent uses anything. Offline, the CHP simply taps the toggles.

---

## 6. Why It Works: Design Choice To Evidence

| Design choice | Evidence behind it |
|---|---|
| Target the **handoff**, not mothers' knowledge | Sub-standard care in 81.4% to 98.1% of Kenyan maternal deaths; treatment delay 41% (CEMD). 64% of severe outcomes present on arrival, 58% referred (near-miss 2018). PROMPTS danger-sign care-seeking effect not significant. |
| Output an **action**, not just an alert | Detection-only trials (CRADLE-3, CRADLE-5, CLIP, BetterBirth) did not reduce deaths; detection plus bundled action did (E-MOTIVE, 4.3% to 1.6%). |
| **Repeat-after-rest** built into the flow; unrepeated readings weaker | WHO ANC.DT.04 and DT.17 require a repeat BP before acting on hypertension. |
| **Defeat** BP readings taken after antihypertensives | Clinical pharmacology: treatment lowers the reading without removing pre-eclampsia; a lower post-treatment BP is not reassurance. |
| **Memory** of earlier visits | ISSHP: chronic (before 20 weeks) vs gestational hypertension and pre-eclampsia (new onset after 20 weeks). SMART ANC tables are single-contact; CHT stores BP as yes/no. LLMs degrade on long pregnancy histories (ObGynLongBench 2026). |
| **Contestable premises**, not just an explanation | Post-hoc explanations increased over-reliance on wrong AI advice (FAU). Contest-and-justify patterns support appropriate reliance (ConGaIT). |
| **Four levels, one action each**, de-escalation possible | Alert fatigue: 49 to 96% of drug alerts overridden; MEOWS triggered in 30% of admissions; CRADLE "yellow" alerts confused staff; Penda's tiered, mostly silent safety net cut errors 16%. |
| **Offline-first** community agent | eCHIS adoption barriers: network problems, power, logouts; rural household electricity 36%; El Niño floods. |
| **Swahili** explanations from the proof | Swahili markedly improved comprehension of health information in Kenya vs English (Translators without Borders study). CHPs must be literate in a national and the local language (PHC Act 2023). |
| **Human decision-maker**, audit log, versioned rules | DPA 2019 s.35 (no solely automated significant decisions); Digital Health Act audit trails; PPB SaMD traceability. |
| **Structured referral content** | 98.2% of maternity referral forms incomplete (Ghana audit); MOH 100 reasoning fields are free text; back-referral rarely completed. |

---

## 7. Why Omega And MeTTa (And Where Jev Fits)

### 7.1 Why not a plain rules engine

A rules engine can say "152 ≥ 140". It cannot naturally say **how sure** it is, **merge** two witnesses, **discount** one reading because of another fact, or **remember** across sessions in the same representation it reasons in. MeTTa does all four with atoms and pattern matching, and Omega's NAL library gives every conclusion a truth value and a derivation.

### 7.2 Why not an LLM

LLMs cannot produce a verifiable proof, are not deterministic, get worse when they must find evidence in long histories, and are hard to govern under Kenyan law. In Mizani, **no LLM makes or explains a clinical decision.** Explanations are templates filled from the proof, so they cannot claim anything the proof does not contain.

### 7.3 What Omega specifically contributes

| Omega capability (from `singnet/Omega`) | How Mizani uses it |
|---|---|
| `lib_nal.metta`: NAL deduction and revision with `(stv f c)` | Every rule firing and every merge of witnesses. Loaded **unmodified** from a pinned commit. |
| Stateful memory with an episodic trace (`history.metta`) | Each agent's append-only atom log, replayed on restart; the facility's memory of the mother changes the answer. |
| Self-modification via `add-atom` / `remove-atom` on `&self` | Rule packs as atoms; governed rule patches with before/after diffs (P1). |
| Plugin API (`loadOmegaPlugin`, `add-skill`) | Mizani ships as an Omega plugin: `assess`, `reconcile`, `why`, `contest` appear in Omega's `getSkills`, so a full Omega agent can call them. |
| PeTTa runtime | The same runtime Omega's Docker image pins (PeTTa v1.0.4 on SWI-Prolog 10.0.2). |
| Action thresholds (act: f ≥ 0.6 and c ≥ 0.5) | Mizani's decision bands. |

### 7.4 The neural-symbolic split

> **Jev reads. Omega decides. The human confirms and can contest.**

| Layer | Does | Never does |
|---|---|---|
| **Jev** (neural, System One judgement) | Reads Swahili/Sheng/English notes into typed sign statuses with probabilities; picks today's BP from candidates | Produce numbers, thresholds, risk levels, actions, or explanations |
| **Omega / MeTTa** (symbolic, NAL) | Evidence, provenance, defeat, revision, rules, decisions, proofs, memory | Read free text |
| **Human** (CHP, nurse, coordinator) | Confirms observations; contests premises; approves rule changes; decides | Get overruled silently |

This is exactly Ben Goertzel's framing of Omega: "The LLM is a component the cognitive layer calls on, not the thing running the show."

---

## 8. Language, Literacy And Connectivity

- **Languages.** Every decision and every premise is rendered in **Swahili and English** from the same proof. Notes can be written in Swahili, English or Sheng. Swahili clinical phrasing follows MOH community usage where known; strings are reviewed by a fluent Kenyan speaker.
- **Literacy.** Short sentences, one action per level, icons paired with every colour, MCH booklet terminology for danger signs.
- **Connectivity.** The community agent decides with no network; the packet waits in an outbox and syncs when a connection appears; the facility agent works on the facility's own server. Payloads are small (atoms, not images).
- **Devices.** The community screen is designed for a 360 px phone (eCHIS phones), touch targets at least 44 px, and works in light and dark mode.
- **Future access.** USSD/SMS summaries for feature phones and on-device PeTTa for Android are in What's Next.

---

## 9. Safety, Governance And Law

### 9.1 Clinical safety principles

1. **Decision support, not diagnosis.** Visible on every screen.
2. **Fail safe.** Uncertain or unconfirmed danger signs count as present for referral rules, and the proof says so.
3. **Missing is not normal.** Missing evidence blocks a rule instead of defaulting to reassurance.
4. **Every decision is overridable and contestable**, with the human's name and reason recorded.
5. **No silent learning.** Rule changes are proposals reviewed by a named human, versioned, logged, and replayable.
6. **Emergencies are never toasts**; they require acknowledgement.
7. **Guideline-traceable rules.** Every rule cites its source (WHO SMART ANC tables, ISSHP, WHO/FIGO/ICM 2025 PPH, shock index literature).

### 9.2 Kenyan law (for a real deployment)

| Requirement | Mizani's design response |
|---|---|
| **Data Protection Act 2019** s.2: health data is sensitive personal data | Synthetic data in the prototype; minimised atoms in production; encryption at rest and in transit |
| s.31: Data Protection Impact Assessment before high-risk processing | DPIA is step 1 of the pilot |
| s.35: no decisions based solely on automated processing that significantly affect a person | The CHP and the nurse are the decision-makers; Mizani recommends, they act, and their actions are logged |
| s.46: health data processed by or under a health care provider | Pilot run with a licensed facility or county as data controller |
| s.48 to 49 and Regulations 2021 reg. 26: transfers abroad, Kenyan data centre for primary care data | Agents host in Kenya; Jev calls send de-identified note text only, with consent, or are disabled in strict deployments (manual toggles are always available) |
| **Digital Health Act 2023**: audit trails for all activities; certified solutions | Append-only atom logs are the audit trail; certification is part of the pilot plan |
| **PPB Medical Device Software guideline** (reported in force February 2026): risk classification, traceability between software versions and outputs | Every decision records the rule pack version and Omega commit; classification is part of the pilot plan |
| **KMPDC**: licensed clinicians remain accountable | Explainable, contestable outputs protect the clinician |

### 9.3 Hackathon-specific integrity

Synthetic data only; disclaimer in the app, README and video; full AI Disclosure; every dependency credited (Omega Apache-2.0, PeTTa, shadcn/ui MIT); no secrets in the repo.

---

## 10. When And Where It Is Used

| Moment | Who | Mizani's role |
|---|---|---|
| Routine ANC home visit (WHO 8-contact schedule) | CHP | Decision on any danger sign or BP reading; repeat-after-rest prompt |
| Night or weekend danger signs | CHP, family | Offline decision and queued referral |
| Arrival at the facility | Nurse, clinical officer | Reconciliation and action |
| Transfer to a higher level | Nurse to hospital | The proof travels with the woman |
| Postnatal visits (days 1 to 42) | CHP | Postpartum hypertension and haemorrhage rules (full pack) |
| Rainy season and floods | Everyone | Offline-first operation |
| Monthly supervision and death reviews | Sub-county coordinator | Audit log and governed rule changes |

**First geography:** a coastal or flood-prone county (the demo uses Kilifi as a setting), then high-burden counties with low skilled birth attendance (Turkana 53%, Mandera 55%, Wajir 57%) and high-volume urban counties (Nairobi, Nakuru).

---

## 11. What Is New, And An Honest Comparison

### 11.1 Already done elsewhere (we do not claim these)

Danger-sign rules from WHO guidelines; "explainable, not black box" deterministic triage; digital referral with outcome notification; per-mother records; risk scores from serial vitals; LLM triage with human escalation.

### 11.2 New (not found anywhere in our search)

1. **Symbolic reasoning over cross-visit and cross-site evidence with provenance**, including protocol-aware **defeat** (post-treatment readings) and **revision** of agreeing witnesses.
2. **The referral as a contestable proof** that recomputes when a premise is withdrawn.
3. **Two agents reconciling conflicting maternal evidence** across care levels.
4. **Offline decision reconciled later with a diff of what changed and why**, in maternal care.
5. Any of this in **MeTTa on Omega**: GitHub returns zero MeTTa or Hyperon health/clinical repositories; the only MeTTa medical demo is a toy flu/migraine lookup.

### 11.3 Comparison

| | Danger-sign apps and hackathon clones | eCHIS / CHT | PROMPTS | Penda AI Consult | **Mizani** |
|---|---|---|---|---|---|
| Works offline | Some | Yes | SMS | No | **Yes (community agent)** |
| Uses provenance (repeated, after treatment) | No | No | No | Partly (LLM) | **Yes** |
| Remembers earlier visits in the reasoning | Rarely | Stores, does not reason | History visible to nurses | Within visit | **Yes, changes the answer** |
| Reconciles two sites | No | No | No | No | **Yes** |
| Truth values and derivations | No | No | No | No | **Yes (Omega NAL)** |
| Receiving clinician can contest premises | No | No | No | No | **Yes** |
| Swahili explanation | Some | Forms | Yes | No | **Yes, from the proof** |
| Governed rule changes with diffs | No | Config changes | No | No | **Yes (P1)** |

### 11.4 Honest weaknesses

- The prototype has not been validated with CHPs or nurses, and the Swahili strings need native review.
- The edge agent runs as a separate process in the demo, not on a phone; on-device PeTTa is future work.
- Jev's accuracy was tested on 12 notes we wrote, not real CHP notes.
- A real deployment is likely Software as a Medical Device and needs regulatory work.
- Reconciliation logic is only as good as the defeaters we encode; a missing defeater is a missing protection.

---

## 12. Proof It Will Work

### 12.1 Technical proof (verified on this machine, 2 October 2026)

| Claim | Evidence |
|---|---|
| Omega's runtime runs here | PeTTa v1.0.4 on SWI-Prolog 10.0.2, hosted from Python 3.12 via janus-swi 1.5.3 |
| Omega's own NAL produces our proofs | A two-step deduction for "high systolic and proteinuria imply suspected pre-eclampsia" returned confidence 0.729 then 0.59049, matching NAL formulas by hand (1 × 0.9 × 0.9 × 0.9; then × 0.9 × 0.9 × 0.729) |
| Memory across visits changes confidence | NAL revision of two agreeing visits raised confidence from 0.59049 to 0.74253 (hand-checked) |
| Persistence across restarts | Append-only atom log replayed across three separate processes |
| Rule update with a literal diff | `update-rule` returned old and new rule atoms |
| Real Omega plugin | Our skills appeared in Omega's `getSkills`; Omega's own `metta` skill ran them |
| Fallback | The same logic on `hyperon==0.2.10` gave identical numbers |
| Jev reads Kenyan notes | 118 of 120 sign judgements correct on 12 Swahili/English/Sheng notes; no present sign missed; BP picked correctly 6 of 6 among distractors; about 390 ms per note; about USD 0.00012 per note |

### 12.2 Clinical proof

Every rule is a published threshold (WHO SMART ANC DT.01, DT.04, DT.12, DT.17; ISSHP; WHO/FIGO/ICM 2025 PPH; shock index 0.9 / 1.4 / 1.7). The reconciliation logic encodes protocol facts clinicians already use (repeat after rest; treatment lowers BP; onset timing). See [problem.md](problem.md) section 8.3.

### 12.3 User proof

The pains Mizani addresses are documented by the people who live them: CHPs who never learn referral outcomes (Living Goods; Busia and Migori linkage studies), incomplete referral forms (98% in a Ghana audit), eCHIS connectivity and device problems (Muriithi et al. 2026; Amref Machakos), night-time deaths and absent seniors (first CEMD), and frontline workers in Kenya asking for AI that "protects clinical autonomy" (JMIR mHealth 2026).

### 12.4 Market and system proof

The national CHP rail exists (about 107,800 CHPs, eCHIS on 110,000 smartphones); PCNs are being built (228 by January 2026); the law requires audit trails; XR Agency's KU MOU provides an incubation path; BGI Nexus funds social-good AI; BASIX lists health as a vertical.

---

## 13. Strengths, Weaknesses, Opportunities, Threats

| Strengths | Weaknesses |
|---|---|
| Real Omega reasoning, visibly | No field validation yet |
| Memory that changes the answer | Edge agent not yet on-device |
| Contestable, human-in-the-loop | Swahili strings need native clinical review |
| Grounded in WHO and Kenyan evidence | Synthetic scenarios only |
| Fills an empty lane in this hackathon | Solo build in one day |

| Opportunities | Threats |
|---|---|
| eCHIS / CHT integration as a reasoning service | Regulatory classification (SaMD) and certification timelines |
| County pilots with PCNs | Data protection constraints on cloud services |
| BGI Nexus, Deep Funding grants | Competing national digital health priorities |
| KU / ESA-KU incubation via XR Agency | Device accuracy of CHP BP machines in pregnancy |
| Extension to postpartum haemorrhage and sepsis | Alert fatigue if packs grow without discipline |

---

## 14. Sustainability: Who Pays, How It Scales

### 14.1 Cost to run

| Item | Cost |
|---|---|
| Reasoning (Omega on PeTTa) | Runs on commodity hardware; no per-call fees |
| Jev note reading | About **USD 0.00012 per note** (about 8,000 notes per USD); optional |
| Hosting | One small Kenyan-hosted server per county for facility agents; community agents on devices (future) |

A county with 2,000 CHPs each doing 40 pregnancy visits a month generates about 80,000 notes a month: about **USD 10 a month** in Jev costs if every note is read by Jev.

### 14.2 Who pays

| Payer | Why |
|---|---|
| County governments (CHP programmes are co-funded 50/50 with the national government) | Better use of the CHP investment; fewer avoidable referrals; MPDSR evidence |
| Implementing partners (Amref, Living Goods, Jacaranda, Medic) | A reasoning layer for their existing CHP and referral programmes |
| Grants (BGI Nexus, Deep Funding, maternal health funders) | Early pilots and validation |
| SHA-linked facilities (longer term) | Quality-of-care requirements and certified digital tools |

### 14.3 How it scales

1. **Reasoning service, not a new app.** FHIR in, proof out, behind eCHIS/CHT and facility HMIS.
2. **Rule packs as governed, versioned assets.** A county's validated pack can be shared, audited and (in the BASIX model) registered as owned IP.
3. **Same pattern, new packs.** Postpartum haemorrhage, sepsis, newborn danger signs, and later non-maternal referrals (TB, malnutrition) use the same two-witness reconciliation.

---

## 15. Roadmap And What's Next

| Phase | When | What |
|---|---|---|
| **Hackathon alpha** | 2 Oct 2026 | Two Omega agents, offline sync, reconciliation, contest, Swahili, audit; three synthetic scenarios |
| **Next BASIX hackathon** | 24 to 25 Oct 2026 | Governed rule patches (override to diff to approval to replay); Omega chat agent calling Mizani skills over Telegram; Android packaging research |
| **Clinical review** | Nov to Dec 2026 | Rules reviewed by Kenyan obstetric and community health clinicians; Swahili reviewed; Jev evaluated on 100 to 200 de-identified real notes |
| **Pilot design** | Q1 2027 | DPIA; PPB classification; a county partner and one PCN; KU/ESA-KU incubation; BGI Nexus proposal |
| **Pilot** | Q2 to Q3 2027 | 1 sub-county, about 100 CHPs and 3 facilities; measure the indicators in section 16 |
| **Integration** | 2027 to 2028 | eCHIS/CHT and TaifaCare integration; USSD/SMS back-referral to CHPs; postpartum packs |

**What we would build next, in one sentence (for the README):** governed rule learning from clinician overrides, an Omega chat channel that lets a nurse ask "why?" in plain language, and an eCHIS integration so Mizani reasons behind the tools CHPs already use.

---

## 16. Success Metrics

| Level | Metric | Target in pilot |
|---|---|---|
| Use | Share of pregnancy referrals with a reconciled decision | 80% or more |
| Protocol | Share of high BPs repeated after rest at community level | 90% or more |
| Speed | Median time from arrival to a reconciled decision | Under 10 minutes |
| Safety | Missed severe pre-eclampsia at arrival (vs record review) | Reduction from baseline |
| Efficiency | Share of Watch outcomes resolved without transfer | Tracked, with no missed severe cases |
| Trust | Override and contest rates, with reasons | Tracked and reviewed monthly |
| Loop | Share of referrals with back-referral visible to the CHP | 80% or more |
| Outcome (long term) | Severe maternal outcomes and perinatal deaths per 1,000 births | Reduction vs comparison sub-counties |

---

## 17. How It Maps To The Hackathon

| Requirement | Where Mizani meets it |
|---|---|
| Built on Omega, not optional | Omega's `lib_nal.metta` unmodified from a pinned commit, on PeTTa, packaged as an Omega plugin |
| Omega's stateful, auditable reasoning as the feature | Memory changes the decision; every decision is a NAL proof with truth values and an audit log |
| One feature, proven | The reconciled, contestable referral |
| Agent Without Borders 02 | Offline small rule pack, reconcile with the fuller agent, show how and why the answer changed |
| Agent Without Borders 01 | Reasoning explained in Swahili |
| Sample reasoning transcript, memory record or audit trail | `docs/transcript.md`, `docs/audit-trail.md`, `/memory/export` |
| AI Disclosure | README and `docs/ai-disclosure.md` |
| What we would build next | Section 15 |
| Judging: technical execution 30% | One-command run, tests, real Omega |
| Judging: video 25% | One human story, live product, under 3 minutes |
| Judging: fit 25% | Track, problem and solo challenge named on the first screen |
| Judging: documentation 20% | This docs set |
| Omega rubric: Sustainability Impact 20% | Kenya's maternal deaths, the CHP rail, climate resilience, a pilot path |

---

## 18. Pitch Library

**One line.** Two witnesses, one referral.

**Ten seconds.** Mizani is two Omega agents that reconcile a pregnant woman's referral between the community health promoter who saw her at home and the nurse who receives her, and show their working in Swahili.

**Thirty seconds.** In Kenya, a mother's danger signs are usually seen first by a community health promoter, often with no network, and hours later by a nurse who sees different numbers and none of the history. Nobody reconciles the two. Mizani's community agent decides offline with a small MeTTa rule pack. When the network returns, the facility agent, which remembers the mother, reconciles both witnesses with Omega's own reasoning: it discounts a reading taken after treatment, recognises new-onset hypertension from her 14-week visit, and changes Urgent to Emergency, showing exactly what changed and why. The nurse can challenge any premise and watch it recompute.

**For Ben Goertzel and the Omega engineers.** The LLM is not in charge. Omega's NAL does every inference, memory changes the answer, and the whole thing ships as an Omega plugin on PeTTa.

**For XR Agency and partners.** It sits behind Kenya's national CHP system, it is designed for Kenyan law, and it has a pilot path through KU incubation and county health departments.

**For the media judges.** Amina, Zawadi and Baraka: a flooded road, two readings that disagree, and an agent that weighs them honestly.
