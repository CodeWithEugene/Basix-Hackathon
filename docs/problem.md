# Problem: What We Could Solve, What We Chose, And Why

> **What this file is.** The problem document. It lists every problem we seriously considered (maternal health and beyond), the evidence for each, how we scored them, and the one problem we are building for, with the full evidence chain behind it.
>
> **Read with:** [info.md](info.md) (the event), [solution.md](solution.md) (what we build to solve it), [build.md](build.md) (how we build it), [research.md](research.md) (every source in full).
>
> **Status:** v1.0, Friday 2 October 2026. All statistics carry a source. **UNVERIFIED** marks numbers taken from press summaries or where sources conflict.

---

## Table Of Contents

1. [The Problem In One Paragraph](#1-the-problem-in-one-paragraph)
2. [How We Chose](#2-how-we-chose)
3. [The Burden: Why Maternal Health In Kenya](#3-the-burden-why-maternal-health-in-kenya)
4. [Where Mothers Actually Die: The Three Delays In Kenya](#4-where-mothers-actually-die-the-three-delays-in-kenya)
5. [Eight Maternal Health Problems We Could Solve](#5-eight-maternal-health-problems-we-could-solve)
6. [Problems Outside Maternal Health We Considered](#6-problems-outside-maternal-health-we-considered)
7. [Scoring And Decision](#7-scoring-and-decision)
8. [The Chosen Problem In Depth](#8-the-chosen-problem-in-depth)
9. [Why Existing Solutions Do Not Solve It](#9-why-existing-solutions-do-not-solve-it)
10. [Why Now](#10-why-now)
11. [Why This Problem Wins This Hackathon](#11-why-this-problem-wins-this-hackathon)
12. [The Hard Questions (And Our Answers)](#12-the-hard-questions-and-our-answers)
13. [What We Are Deliberately Not Solving](#13-what-we-are-deliberately-not-solving)
14. [Key Sources](#14-key-sources)

---

## 1. The Problem In One Paragraph

When a pregnant woman in rural Kenya shows danger signs, the **first witness** is usually a Community Health Promoter (CHP) at her home, often with no network. The **second witness** is a nurse at a facility hours later, who sees different numbers (often after treatment given on the way), does not see what the CHP saw, and does not see the mother's earlier pregnancy history. **The two witnesses disagree, nobody reconciles them, and the referral note that should carry the reasoning is a scrap of paper or a yes/no field.** Kenya's confidential enquiry found sub-standard care in **81.4% (2014) to 98.1% (2015/16)** of maternal deaths, with **delay in treatment in 41%** [CEMD]. In Kenya's national near-miss study, **64% of severe maternal outcomes were already present on arrival at the referral hospital, and 58% of those had been referred from lower facilities** [Near-miss 2018]. The problem we solve is **the reasoning gap between the community witness and the facility witness**: making the referral decision survive the handoff, reconcile conflicting evidence honestly, remember the mother, and show its working to the person who must act on it.

---

## 2. How We Chose

### 2.1 The goal

**First place**, not a finish. That means maximising the judging rubric while respecting the solo brief ("one feature, proven").

### 2.2 Criteria (weighted by the hackathon's own rubrics)

| Criterion | Weight we used | Comes from |
|---|---|---|
| Technical showcase of real Omega (memory that changes the answer, truth-valued auditable reasoning, reconciliation) | 30% | All-tracks rubric "Technical execution" 30%; Omega "Technical Implementation" 30% |
| 3-minute video and story clarity | 25% | All-tracks rubric 25% |
| Track fit (Omega, "Agent Without Borders" or "Two Agents One Truth") | 25% | All-tracks rubric 25% |
| Sustainability Impact (real-world, East Africa, adoption path) | 10% | Omega rubric 20% (shared with track fit in our weighting) |
| Novelty (vs 2026 hackathon clones and products) | 5% | Omega "Innovation & Creativity" 30% (partly in technical and fit) |
| Buildability (one developer, about 8 hours) | 5% | Solo brief; schedule |

### 2.3 Method

1. Six parallel research streams on 2 October 2026: the hackathon and its people; Omega/MeTTa (with live installs and tests); maternal health evidence (89 references); competitive landscape and novelty (20+ systems, 15+ GitHub clones); design; and Jev (live accuracy tests). A seventh stream scanned non-maternal alternatives.
2. Each candidate problem was checked for **evidence of need**, **saturation** (GitHub search and web), **data available for a convincing demo**, **judge appeal**, and **risk**.
3. The top four candidates were scored against the rubric by **TypeSafe Jev** (`jev-1.13.0`, request `req_01a0fb4ebfe3765f90016be221792eaa`) as an independent check on our own judgement, then the final decision was made by us.

---

## 3. The Burden: Why Maternal Health In Kenya

### 3.1 Global

| Statistic | Value | Source |
|---|---|---|
| Maternal deaths worldwide, 2023 | **260,000** (about 712 per day) | UN MMEIG, *Trends in maternal mortality 2000 to 2023* (April 2025) |
| Global MMR, 2023 | **197** per 100,000 live births (down 40% since 2000) | MMEIG |
| Share in sub-Saharan Africa | **about 70%** (about 182,000) | MMEIG |
| Pace since 2016 | about **1.5% per year**, vs nearly 15% per year needed for SDG 3.1 | UNICEF Data |
| SDG 3.1 | Global MMR below 70 by 2030; **no country above 140** | MMEIG |

### 3.2 Kenya

| Statistic | Value | Source |
|---|---|---|
| Kenya MMR, 2023 | **379 per 100,000 live births** (80% UI 267 to 547) | WHO GHO API, MMEIG 2025 round (verified) |
| Kenya maternal deaths, 2023 | **about 5,700** (5,682) | WHO GHO API (verified) |
| Trend | 453 (2015) to 379 (2023): about **2.2% per year**. Reaching 70 by 2030 needs about **21% per year**. | Computed from WHO GHO |
| Births per year | about **1.5 million** | Implied from GHO deaths and MMR |
| Stillbirths, 2023 | **16.3 per 1,000** total births | WHO GHO / UN IGME (verified) |
| Neonatal mortality | **21 per 1,000** (stalled since 2014) | KDHS 2022 |

> **Conflict note.** The World Bank WDI API (updated July 2026) shows Kenya MMR **149** for 2023. This does not match the MMEIG round published by WHO (379). We could not find a revision explaining it, so we use **379 and about 5,700 deaths (MMEIG via WHO GHO)** and say so. Other Kenyan figures (355 from the 2019 census; facility MMR 99) measure different things and are not interchangeable.

### 3.3 Causes

| Cause | Kenya (CEMD) | Global (WHO 2009 to 2020) |
|---|---|---|
| Obstetric haemorrhage | **39.7% (2014), 35.5% (2015/16)**; 38% (2015 to 2018, UNVERIFIED press) | 27% |
| Hypertensive disorders (pre-eclampsia, eclampsia) | **15.3% rising to 17.9%**; 19% (2015 to 2018, UNVERIFIED) | 16% |
| Non-obstetric / indirect | 19.8% to 22.2% | 23% |
| Sepsis, abortion, obstructed labour | in the top five direct causes | sepsis 7%, abortion 8% |
| Anaemia as contributing condition | **53%** of deaths (2015 to 2018, UNVERIFIED) | |
| Timing | **66% postpartum; 61% of those within 24 hours** (UNVERIFIED) | |

Sources: Ameh, Godia, Ogutu (RCOG World Congress 2019, comparison of first and second Kenya CEMD); The Standard summary of CEMD 2015 to 2018; Cresswell et al., Lancet Global Health 2025.

### 3.4 Quality, not access, is the binding constraint

Kenya has **near-universal ANC contact (98%)** and **89% skilled birth attendance** (KDHS 2022), yet MMR is about 379. The confidential enquiry found:

| Finding | 2014 | 2015/16 |
|---|---|---|
| Deaths reviewed | 484 (referral hospitals) | 1,334 |
| **Sub-optimal care** | **81.4%** | **98.1%** |
| Delay in treatment | 33% | **41.3%** |
| Inadequate monitoring | 27% | 30.9% |
| Inadequate clinical skills | 28% | 29.1% |

The 2017 report launch summarised this as "9 out of 10 women who died received sub-standard care". Press coverage of the first enquiry also reported "92% received poor care" (Nation); we cite the CEMD abstract figures above as the more primary source.

---

## 4. Where Mothers Actually Die: The Three Delays In Kenya

| Delay | Kenyan evidence | Implication |
|---|---|---|
| **1. Deciding to seek care** | 72% of reviewed deaths involved delayed decision-making (CEMD 2015 to 2018, UNVERIFIED). In the PROMPTS RCT (6,139 women, 40 facilities), SMS raised danger-sign knowledge slightly but **danger-sign care-seeking was not significant** (+0.04 SD, p = 0.096). | Information to mothers alone has the weakest trial evidence. |
| **2. Reaching care** | 75% of deaths involved delayed arrival (UNVERIFIED). **64% of severe maternal outcomes were already present on arrival; 58% of those were referred from lower facilities** (54 referral hospitals, 2018). Ambulances carried just over 10% of referrals. | **The referral chain is where women are lost.** |
| **3. Receiving adequate care** | Sub-optimal care in **81 to 98%** of deaths; treatment delay 41%. Only **77%** of women with severe pre-eclampsia or eclampsia received **magnesium sulphate** even at referral hospitals; only 67% of women with APH who needed blood got it. 72% of deaths in the first enquiry happened outside working hours (Nation). | **The receiving clinician needs the right information, fast, at night.** |

**Takeaway.** In Kenya, Delay 3 is at least as large as Delays 1 and 2, and Delays 2 and 3 meet at the **handoff**: the moment the community witness's evidence must become the facility's decision.

---

## 5. Eight Maternal Health Problems We Could Solve

Ranked on: share of deaths addressed; strength of evidence that the mechanism works; safety and encodability with deterministic rules; feasibility for one developer in Kenya's regulatory and connectivity context; fit with existing rails (eCHIS, MCH booklet, CHP kit).

### P1. Hypertension triage and BP surveillance for CHPs and ANC clinics

- **Problem.** Hypertensive disorders cause 15 to 19% of Kenyan maternal deaths and their share is rising. CHPs already carry BP machines in their kits but have no pregnancy-specific triage logic or history view. Only 29% start ANC in the first trimester; only 35% of mothers had BP taken at the postnatal check (KDHS 2022).
- **Evidence the mechanism works.** Thresholds are strong (WHO SMART ANC DT.04, DT.12, DT.17: repeat at 10 to 15 minutes, ≥140/90, ≥160/110, protein ++, severe symptoms). Impact evidence is mixed: CRADLE-3 had no significant effect after adjusting for time trends; CLIP had no reduction in the primary composite. Positive signals appeared where contact frequency and referral worked.
- **Verdict.** Strong clinical logic, crowded as a stand-alone app, and the trials say detection alone is not enough.

### P2. Postpartum first-24-hour early warning (PPH and sepsis)

- **Problem.** 66% of deaths are postpartum and 61% of those within 24 hours (UNVERIFIED). Haemorrhage causes 36 to 40%. Anaemia (40% prevalence) makes small bleeds lethal.
- **Evidence.** The strongest of all: **E-MOTIVE** (NEJM 2023, Kenyan sites) cut severe PPH, laparotomy or death from **4.3% to 1.6%**; detection rose from 51% to 93%, bundle adherence from 19% to 91%. WHO/FIGO/ICM 2025 PPH definition (≥300 mL plus abnormal vital sign, or ≥500 mL). Shock index tiers 0.9 / 1.4 / 1.7.
- **Verdict.** High impact but inside facilities with calibrated drapes; a weaker story for "community vs facility" and needs facility workflows we cannot demo credibly in one day.

### P3. Closed-loop referral: structured handoff, pre-alert and back-referral

- **Problem.** 64% of severe outcomes present on arrival; 58% referred. The MOH 100 back-referral section is rarely completed. In northern Ghana, **98.2% of 217 maternity referral forms were incomplete** and reasoning and treatment times were often missing (PMC8925182). CRADLE-5's benefit appeared only where referral worked.
- **Evidence.** Strong observational evidence that referral is the failure point. **No RCT of digital closed-loop maternal referral found** (an evidence gap, not a negative).
- **Verdict.** The highest-leverage place to intervene, but logistics-only versions exist (eCHIS to TaifaCare closed loop, June 2026; Living Goods SMS confirmation). The open space is the **clinical reasoning** in the handoff.

### P4. Swahili and Sheng danger-sign triage of mothers' messages

- **Problem.** Delay 1. Mothers are 78% phone owners, 43% smartphone owners.
- **Evidence.** PROMPTS proves scale (more than 2.5 million mothers, USD 0.74 per enrollee) but danger-sign care-seeking was not significant.
- **Verdict.** Direct competition with Jacaranda's UlizaLlama; better to partner than compete.

### P5. ANC continuity and risk worklist for CHPs

- **Problem.** ANC 4+ 66%, ANC 8+ **4%**, first-trimester booking 29%. eCHIS identified 161,000 pregnant women and referred 63,500 without visible follow-through.
- **Evidence.** CLIP showed contact frequency was the limiting factor.
- **Verdict.** Valuable and buildable as eCHIS tasks, but reads as a scheduler on video and does not showcase Omega reasoning.

### P6. Clinician "safety-net" audit at primary facilities

- **Problem.** Sub-optimal care 81 to 98%; MgSO4 and blood gaps.
- **Evidence.** Penda Health AI Consult cut diagnostic errors 16% and treatment errors 13% (39,849 visits, not randomised).
- **Verdict.** Clearly Software as a Medical Device under PPB; needs a facility partner and real records.

### P7. Commodity-aware referral routing (EmONC readiness)

- **Problem.** Reported shortages of MgSO4 (48% of facilities), oxytocin (40%) (UNVERIFIED press). Only about 50% of facilities equipped.
- **Verdict.** Depends on live facility data we do not have.

### P8. MPDSR and confidential enquiry review assistant

- **Problem.** KHIS records about half of modelled deaths; reviews are labour-intensive.
- **Verdict.** Highly sensitive data, users are county committees, weak demo.

---

## 6. Problems Outside Maternal Health We Considered

Eugene authorised looking beyond maternal health, with the goal of first place. A time-boxed scan stress-tested the same Omega framings in other domains.

| Rank | Idea | Fits | Verdict |
|---|---|---|---|
| 2 | **Mafuriko flood two-witness**: a village volunteer's community reports reconciled with GloFAS/Open-Meteo data | Agent Without Borders 02 | Close second. Very timely (El Niño more than 90% likely for the October to December rains; 18 counties flagged high-risk), free APIs verified. Loses because memory is about a place not a person, reconciliation is mostly numeric, and a Kenyan MeTTa weather/agri project exists nearby. |
| 3 | **RVF One Health**: livestock keeper reports, vet-side agent reconciles with lab and El Niño warnings, rule update with diff | Agent Without Borders / Grows Up | Explicit 2026 RVF warning for Kenya; niche, synthetic herd data, weaker video. |
| 4 | **Dawa Halisi** pharmacy recall check | Auditable decision | Real need (58 PPB recalls since Jan 2025) but reads as a database lookup; many 2026 drug-verification repos. |
| 5 | **Chama loan audit** | BASIX workflow | Head to head with `basix-trustgate` in this hackathon; several chama repos exist. |
| 6 | **BASIX phigital artist onboarding** | BASIX Mature Build | CourtLens already on BASIX; weak Sustainability Impact; depends on BASIX integration. |
| 7 | **Ardhi land record reconciliation** | Two Agents One Truth | Data hard to get, politically sensitive. |
| 8 | **Crop disease advisory** | Agent Without Borders | Saturated: PlantVillage Nuru already works offline in Swahili; Zindi hackathons; Farmlingua grant. Dropped. |

Also observed: "Two Agents One Truth" is crowded with generic entries (4 repos created 27 to 30 Sept, including Med-Verdict and a WhatsApp scam checker), and some Omega entries are AI Studio boilerplate. A specific domain plus real MeTTa on PeTTa stands out.

**Borrowed from the flood idea:** we set our demo during the El Niño short rains, with a flooded road as the reason the CHP is offline and the referral is delayed. That makes the Sustainability Impact story about **climate-resilient primary care** for one scene's worth of work.

---

## 7. Scoring And Decision

### 7.1 Jev rubric scoring (independent check)

Each idea was described in one paragraph and scored by `jev-1.13.0` on six criteria with five ordered levels (0 = very weak to 4 = very strong). Weighted with the weights in section 2.2.

| Idea | Technical showcase | Video story | Track fit | Sustainability impact | Novelty | Buildability | **Weighted (0 to 4)** |
|---|---|---|---|---|---|---|---|
| **Mizani maternal two-witness referral** | **3.93** | **3.28** | **3.99** | **3.28** | **3.46** | 0.74 | **3.53** |
| Mafuriko flood two-witness | 2.81 | 2.43 | 3.57 | 2.64 | 1.75 | 1.54 | 2.77 |
| RVF One Health | 2.71 | 1.67 | 3.15 | 2.06 | 2.58 | 1.21 | 2.41 |
| Chama loan audit | 2.58 | 1.72 | 1.65 | 2.02 | 1.05 | 1.76 | 1.96 |

**Re-run after a correction.** The first run's Mizani description quoted "92% of maternal deaths had poor care", a press figure. We corrected it to the confidential enquiry's "sub-optimal care in 81 to 98% of maternal deaths" and re-ran (request `req_01a0fb6a5c0e7ff883c136d87b7b2de8`). Results barely moved: Mizani **3.54**, flood 2.79, RVF 2.43, chama 1.90; ranking unchanged; Mizani buildability still 0.74. Caveat: one-paragraph descriptions of uneven length and detail can bias any judge, human or model, so this scoring is a sanity check, not the decision.

**Balanced re-run (the fairest test).** The first descriptions were lopsided (Mizani's listed strengths, the others listed weaknesses). We rewrote all four at similar length, each with one strength and one weakness, and re-ran (request `req_01a0fb6ae331767da44f3c8332c90c63`):

| Idea | Technical | Video | Fit | Impact | Novelty | Build | **Weighted** |
|---|---|---|---|---|---|---|---|
| **Mizani maternal** | 3.23 | 2.86 | **3.97** | **3.22** | 1.42 | 1.08 | **3.12** |
| Flood | 2.62 | 2.37 | 3.68 | 2.83 | 1.55 | 1.60 | 2.74 |
| RVF One Health | 2.91 | 1.67 | 3.76 | 2.49 | 2.54 | 1.03 | 2.66 |
| Chama loan | 3.03 | 1.80 | 2.14 | 2.71 | 0.79 | 1.85 | 2.30 |

Mizani still ranks first, by a smaller margin. Its **novelty dropped to 1.42** once the description admitted "many maternal danger-sign apps already exist". That is the most useful finding of the whole exercise, and it agrees with the landscape research: **Mizani is only novel if it is pitched as two-witness reconciliation with a contestable proof, never as "a maternal danger-sign app".** Every pitch, title and the first 20 seconds of the video follow that rule.

### 7.2 What the scoring told us

1. The maternal two-witness referral leads on **every criterion except buildability**.
2. Buildability is its weakest score. **We treat that as a warning, not a veto**: the build spec cuts everything that is not the one feature (see [build.md](build.md) section 1), and the two hardest technical risks (running Omega's runtime and producing NAL proofs, persistence, rule diffs) were already proven on this machine during research.

### 7.3 Decision

> **We build for problem P3 (the referral handoff), using P1's hypertension logic as the clinical core and P2's shock-index rules as a secondary path, framed as two Omega agents that reconcile the community witness and the facility witness.**

---

## 8. The Chosen Problem In Depth

### 8.1 Problem statement

> **A referral decision made at a pregnant woman's home does not survive the journey to the facility.** The CHP's evidence (often taken offline, sometimes unrepeated, always without lab tests) and the facility's evidence (often taken after treatment en route, without the CHP's observations, and without the mother's earlier history) conflict, and no one reconciles them explicitly. The receiving clinician gets a paper note or a yes/no field, cannot see why the CHP worried, cannot see the mother's earlier readings, and cannot challenge the reasoning. The result is under-triage on arrival (a lower BP after nifedipine read as reassurance), over-triage (an unrepeated high reading never re-checked), and lost time.

### 8.2 Who suffers, and who acts

| Person | Situation | What they need |
|---|---|---|
| **The mother** (for example, 27 years old, second pregnancy, 34 weeks) | Severe headache and blurred vision at night; the road is flooded | A correct, fast decision, and to be taken seriously |
| **The CHP** (about 107,800 in Kenya, each covering about 100 households, KSh 5,000 per month stipend, kit includes a BP machine, eCHIS on a smartphone) | Often offline; carries a BP machine but no dipstick or Hb meter; accountable to a supervisor; rarely learns the outcome of a referral | A decision that works offline, uses the guideline correctly (repeat the BP after rest), and is respected at the facility |
| **The receiving nurse or clinical officer** (Level 2 to 4 facility, night shift) | Many patients, little time, no senior on site; 72% of deaths in the first enquiry occurred out of hours | A 30-second read: what the CHP saw, what has changed, what is known from earlier visits, what to do now, and why |
| **The county and MPDSR committee** | Must reconstruct what happened when a mother dies | An audit trail of evidence, rule versions and human actions |

### 8.3 The evidence chain (why solving this reduces deaths)

1. **Most deaths involve sub-standard care and delay at the facility end** (81 to 98% sub-optimal care; 41% treatment delay) [CEMD].
2. **Most severe outcomes are already present when women arrive, and most of those were referred** (64%; 58%) [Near-miss 2018]. The handoff is the choke point.
3. **Referral documentation is poor**: 98% of maternity referral forms incomplete in a Ghana audit; the MOH 100 form's reasoning fields are free text and its back-referral is rarely completed [PMC8925182; MOH 100].
4. **Measurement protocol errors are common and consequential**: WHO requires a repeat BP after 10 to 15 minutes rest before acting on hypertension (ANC.DT.04), and a lower reading after an antihypertensive does not mean the disease has gone. A system that knows the provenance of each reading can avoid both false reassurance and false alarm.
5. **Timing classification needs memory**: ISSHP distinguishes chronic hypertension (before 20 weeks) from gestational hypertension and pre-eclampsia (new onset after 20 weeks). A single-visit checklist cannot make this distinction without the mother's history.
6. **Detection alone has not reduced deaths in trials** (CRADLE-3, CRADLE-5, CLIP, BetterBirth). **Detection coupled to action does** (E-MOTIVE). So the output must be an action the facility takes, not just an alert.
7. **LLMs degrade when they must pull evidence from long pregnancy histories** (ObGynLongBench, September 2026), so longitudinal reasoning should be explicit and symbolic, not left to a context window.
8. **Explanations can increase over-reliance on wrong AI advice** (FAU glaucoma referral study), so the receiving clinician must be able to **check and contest premises**, not just read a rationale.
9. **Kenyan law points the same way**: the Data Protection Act s.35 restricts decisions based solely on automated processing that significantly affect a person; the Digital Health Act requires audit trails; the PPB software-as-medical-device guideline (reported in force February 2026) asks for traceability between software versions and outputs.

### 8.4 What "solved" would look like (measurable)

| Outcome | Indicator | Data source in a pilot |
|---|---|---|
| Fewer missed severe cases at arrival | Proportion of severe pre-eclampsia correctly flagged within 15 minutes of arrival | Facility records vs Mizani log |
| Faster action | Time from arrival to MgSO4 / antihypertensive where indicated | Partograph, Mizani log |
| Correct measurement protocol | Proportion of high BPs repeated after rest at community level | Mizani log |
| Fewer avoidable referrals | Proportion of "Watch" outcomes resolved by a repeat reading | Mizani log |
| Closed reasoning loop | Proportion of referrals with a reconciled decision and back-referral sent to the CHP | Mizani log |
| Trust | Override and contest rates, with reasons | Mizani log |
| Mortality and morbidity (long term) | Severe maternal outcomes and perinatal deaths per 1,000 births in pilot vs comparison sub-counties | County MPDSR, KHIS |

---

## 9. Why Existing Solutions Do Not Solve It

| System | What it does well | What it does not do (for this problem) |
|---|---|---|
| **Kenya eCHIS** (Medic CHT, about 95k CHPs; closed-loop referral to TaifaCare shown June 2026) | National CHP rail; danger-sign forms; referral logistics and outcome notification | Stores BP as a yes/no risk factor in the reference app; no reasoning over provenance or history; no reconciliation of conflicting readings; no contestable proof |
| **WHO SMART ANC DAK** (CQL decision tables) | Executable, authoritative per-contact logic | Almost no cross-contact logic (only "symptoms persist" and "weight gain since last contact"); no handoff artefact; published CQL has transcription errors |
| **Jacaranda PROMPTS + UlizaLlama** | SMS for 2.5M+ mothers; Swahili LLM triage of about 15k messages a day | Mother-facing, not CHP-to-facility; LLM classifier, not symbolic; danger-sign care-seeking effect not significant |
| **Penda Health AI Consult** | LLM safety net in Nairobi primary care, 16% fewer diagnostic errors | Clinician-facing single visit; LLM, not symbolic; not maternity-specific |
| **CRADLE VSA / CLIP / PIERS** | Validated devices and risk scores | Single readings or scores; null or non-attributable effects in trials; no handoff |
| **Living Goods closed-loop SMS** | Confirms the referred client arrived | Attendance only, not clinical reasoning |
| **2026 hackathon clones** (MamaAlert, SafeMother-CDSS, Maitri, MaTriX, Mama na Mtoto Plus, MediBora and others) | Danger-sign triage, some "explainable", one with an audit trail | Single-visit, single-site; no reconciliation, no contestation; none in MeTTa |
| **MeTTa/Hyperon health projects** | One toy flu/migraine lookup demo (Fetch.ai Innovation Lab) | GitHub search for MeTTa or Hyperon health/clinical/pregnancy returns **zero** repositories |

**What is not done anywhere we searched:** symbolic reasoning over **cross-visit and cross-site** evidence with provenance; the referral as a **contestable proof** that recomputes; **two agents reconciling conflicting maternal readings**; any of this in **MeTTa/Omega**.

---

## 10. Why Now

1. **The rail exists.** About 107,800 CHPs are now trained, paid, kitted with BP machines and on eCHIS smartphones (2023 to 2025). The question is no longer "can CHPs measure BP" but "does the measurement turn into the right action at the facility".
2. **The rains.** El Niño is more than 90% likely for the October to December 2026 short rains, with 18 counties flagged high-risk for flooding. Floods cut roads and networks exactly when referrals matter most. Offline-first is a requirement, not a feature.
3. **The law.** The Digital Health Act 2023 (audit trails), the Data Protection Act (no solely automated decisions), and the PPB software-as-medical-device guideline (traceability) all push toward auditable, human-in-the-loop decision support.
4. **The technology.** Omega (renamed from OmegaClaw on 30 September 2026) gives a runnable neural-symbolic agent with truth-valued reasoning and persistent memory, and PeTTa runs it on a laptop today.
5. **The partners.** XR Agency's Kenyatta University MOU (July 2026) has an incubation path for viable projects; BGI Nexus funds social-good AI; BASIX's ecosystem lists health as a vertical.

---

## 11. Why This Problem Wins This Hackathon

| What judges reward | How this problem delivers it |
|---|---|
| "Omega's stateful, auditable-reasoning architecture has to be the actual feature" | The decision **changes because of what the facility agent remembers**, and every step is a NAL truth value from Omega's own `lib_nal.metta` |
| Agent Without Borders 02: decide offline with a small MeTTa rule set, reconcile with a fuller Omega agent, show how and why the answer changed | That sentence is literally our demo |
| Agent Without Borders 01: reasoning explained in a local language | Every decision explained in Swahili and English from the proof |
| Past BGI/HyperSprint winners: memory that matters, human approval, trust scoring | Memory changes the answer; the nurse contests premises; truth values are shown |
| 20% Sustainability Impact | Kenya's 5,700 maternal deaths a year; a ready national CHP rail; a climate-resilience angle |
| East Africa adoption (Sheila Wanjiru), KU MOU, beneficial AGI (Ben Goertzel) | A Kenyan problem, Kenyan workflows, a credible pilot path |
| A memorable one-line pitch | "Two witnesses, one referral." |
| Open lane | No public entry on "The Agent Without Borders" and none on maternal health |

---

## 12. The Hard Questions (And Our Answers)

| Question a judge may ask | Answer |
|---|---|
| "CLIP and CRADLE put risk tools in CHW hands and found no overall effect. Why will this work?" | Those trials improved **detection**. The confidential enquiry says women die from **delay and sub-standard care at the facility end**. We target the handoff and the facility's decision, and we make the output an **action**, which is what worked in E-MOTIVE. |
| "Isn't this just a danger-sign checklist?" | No. A checklist sees one visit at one site. Mizani reasons over **two witnesses and the mother's history**, defeats evidence that the protocol says to discount (a BP after nifedipine), revises agreeing evidence, and lets the receiving clinician contest premises. |
| "Why not just use an LLM?" | LLMs degrade on long pregnancy histories (ObGynLongBench) and cannot give a verifiable proof. We use Jev only to read notes into typed observations that the CHP confirms; Omega's NAL makes every decision. |
| "Is this a medical device?" | A deployed version likely is Software as a Medical Device under PPB. The prototype is decision support with a human decision-maker, synthetic data, and a disclaimer. The pilot path includes classification, a DPIA and a licensed facility partner. |
| "Will it cause alert fatigue?" | Four levels only, one action per level, and the reconciliation can **downgrade** (Scenario B: an unrepeated high reading resolved by a normal repeat). |
| "CHP BP machines may not be validated for pregnancy." | True and unverified. Provenance includes the device; a validated-device flag can raise or lower evidence weight. It is listed in What's Next. |
| "Why should eCHIS not just do this?" | It should, eventually. Mizani is positioned as a **reasoning service** behind eCHIS/TaifaCare (FHIR in, proof out), not a parallel CHP app. |

---

## 13. What We Are Deliberately Not Solving

- Mothers' knowledge and care-seeking (Delay 1 messaging): Jacaranda does this at scale.
- Transport and ambulances (Delay 2 logistics).
- Commodity supply (MgSO4, oxytocin, blood).
- Diagnosis or prescribing: Mizani recommends a referral level and an action category; clinicians decide and treat.
- Machine-learned risk prediction.
- Real patient data of any kind in this hackathon.

---

## 14. Key Sources

Full numbered bibliography in [research.md](research.md). The most important:

- WHO Global Health Observatory API, MMEIG 2025 round: Kenya MMR and deaths. https://ghoapi.azureedge.net/api/MDG_0000000026?$filter=SpatialDim%20eq%20'KEN' ; https://ghoapi.azureedge.net/api/MORT_MATERNALNUM?$filter=SpatialDim%20eq%20'KEN'
- WHO et al. Trends in maternal mortality 2000 to 2023 (April 2025). https://www.who.int/publications/i/item/9789240108462
- Ameh C, Godia P, Ogutu O. Comparison of the first and second Kenya CEMD (RCOG 2019). https://research.lstmed.ac.uk/en/publications/improving-the-quality-of-maternal-and-newborn-health-care-in-keny/
- The Standard. CEMD 2015 to 2018 summary (UNVERIFIED). https://www.standardmedia.co.ke/health/health-science/article/2001468321/bleeding-a-leading-cause-of-maternal-death-report
- Owolabi OO et al. Maternal near-miss in Kenya 2018, 54 referral hospitals. Sci Rep 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7495416/
- KNBS and ICF. Kenya DHS 2022 Key Indicators and Summary Reports. https://dhsprogram.com/pubs/pdf/PR143/PR143.pdf ; https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf
- WHO SMART Guidelines ANC decision tables. https://github.com/WorldHealthOrganization/smart-anc
- ISSHP hypertension classification summary. https://pmc.ncbi.nlm.nih.gov/articles/PMC11588921/
- Gallos I et al. E-MOTIVE. NEJM 2023. https://www.who.int/news/item/09-05-2023-lifesaving-solution-dramatically-reduces-severe-bleeding-after-childbirth
- Vousden N et al. CRADLE-3. Lancet Glob Health 2019. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6379820/
- von Dadelszen P et al. CLIP trials. Lancet 2020. https://scholars.aku.edu/en/publications/the-community-level-interventions-for-pre-eclampsia-clip-cluster-/
- Vatsa R et al. PROMPTS RCT. PLoS Med 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11835334/
- Korom R et al. Penda Health AI Consult. arXiv 2507.16947. https://arxiv.org/abs/2507.16947
- Maternity referral form completeness, northern Ghana. https://pmc.ncbi.nlm.nih.gov/articles/PMC8925182/
- MOH 100 Community Referral Form. https://tciurbanhealth.org/wp-content/uploads/2018/04/Community-Referral-form-MOH-100.pdf
- ObGynLongBench. arXiv 2609.07601. https://arxiv.org/pdf/2609.07601
- Explanations and over-reliance (FAU). https://open.fau.de/handle/openfau/38109
- Data Protection Act 2019. https://new.kenyalaw.org/akn/ke/act/2019/24/eng@2022-12-31 ; Digital Health Act 2023. https://new.kenyalaw.org/akn/ke/act/2023/15/eng@2023-11-24
- Amref: 107,000 CHPs. https://newsroom.amref.org/blog/2025/06/built-from-the-ground-up-how-107000-community-health-promoters-are-changing-the-face-of-health-care-in-kenya/ ; CHP kit list: https://www.kenyanews.go.ke/nyeri-governor-flags-off-chp-kits/
