# Research Log And Evidence Library: Mizani

> **What this file is.** The consolidated, exhaustive research log behind **Mizani** (Swahili for "scales"), our solo entry to the SingularityNET x Omega x BASIX.Market Hackathon. It merges seven research workstreams run on Friday 2 October 2026 into one evidence library: the event and its organisers, the Omega/MeTTa/PeTTa/hyperon stack (with commands we actually ran), the maternal health evidence for Kenya, the competitive landscape and novelty stress test, the alternative ideas we rejected (with a Jev rubric scoring), the TypeSafe Jev live tests, and the design research. Every number is tied to its URL. Every claim we could not check ourselves is labelled.
>
> **The project in one paragraph.** Two SingularityNET Omega agents reconcile conflicting maternal evidence. The **community agent** runs on the community health promoter (CHP) side, offline, with a small MeTTa rule pack. The **facility agent** holds the mother's longitudinal memory and the full rule pack. When connectivity returns, the facility agent reconciles the two witnesses' evidence using **Omega's own `lib_nal.metta` running on PeTTa** (Omega's runtime) and outputs a **contestable referral proof**, explained in English and Swahili. Platform track: **Omega**. Omega problem: **The Agent Without Borders**. Solo track: **challenge 01, one agent producing an auditable decision**.
>
> **Read with.** [info.md](info.md) (the event, rules, judges and deadlines in full), [build.md](build.md) (the build specification), [problem.md](problem.md) and [solution.md](solution.md).
>
> **Last updated.** Friday 2 October 2026, EAT (Nairobi, UTC+3).

---

## Table Of Contents

1. [Purpose And Method](#1-purpose-and-method)
2. [Research Question Map](#2-research-question-map)
3. [The Hackathon And Organisers](#3-the-hackathon-and-organisers)
4. [Omega, MeTTa, PeTTa And Hyperon](#4-omega-metta-petta-and-hyperon)
5. [Maternal Health Evidence](#5-maternal-health-evidence)
6. [Competitive Landscape And Novelty](#6-competitive-landscape-and-novelty)
7. [Alternatives Considered And The Decision](#7-alternatives-considered-and-the-decision)
8. [Jev (TypeSafe) Findings](#8-jev-typesafe-findings)
9. [Design Research Summary](#9-design-research-summary)
10. [Open Questions And Unverified Items](#10-open-questions-and-unverified-items)
11. [Bibliography](#11-bibliography)

---

## 1. Purpose And Method

### 1.1 Why This File Exists

A solo builder with one day to ship needs three things from research: (a) facts about the judging that change what to build, (b) technical certainty that the chosen stack really runs, and (c) clinical and contextual evidence strong enough that the product is honest and the pitch survives a knowledgeable judge. This file is the single place where all of that evidence lives, with sources, so that [info.md](info.md), [build.md](build.md), the README, the video script and the submission form can all cite one library.

### 1.2 What Was Researched

| # | Workstream | Scope | Main methods | Raw notes (scratchpad) |
|---|---|---|---|---|
| W1 | Hackathon and organisers | Rules, tracks, rubric, deadlines, form limits, IP, privacy, organisers, partners, judges, past editions, competitors | Official deck (35 slides), live fetches of basix.market and partner sites, platform JS chunks, GitHub API, public Telegram previews, web search | `research_hackathon.md` |
| W2 | Omega and MeTTa stack | What Omega is, its runtime, reasoning libraries, memory, plugins, install paths, gotchas, a working clinical demo | `gh api`, source reading of `singnet/Omega` at commit `31ff0aa`, hands-on installs and runs on macOS arm64 | `research_omega_metta.md`, `metta-test/demo/` |
| W3 | Maternal health evidence | Burden (global, Kenya, county), causes, Three Delays, CEMD, near-miss, KDHS 2022, CHPs, eCHIS, referral, thresholds, trials, failures, law, language | WHO GHO API, World Bank API, KDHS PDFs, Kenya Law texts, WHO SMART ANC CQL and FHIR on GitHub, journal articles, press | `research_maternal.md` |
| W4 | Competitive landscape and novelty | Production systems, research literature, hackathon clones, MeTTa health prior art, user pain points, novelty verdict | Web search, `gh search repos`, code inspection of `smart-anc` CQL and `cht-core` forms | `research_landscape.md` |
| W5 | Alternative ideas | Six alternative concepts plus three dropped, with saturation and data checks | `gh search repos` and `gh search code` (2026-created filters), web search, live Open-Meteo API probe | `research_alternatives.md` |
| W6 | Jev (TypeSafe System One) | API, SDKs, pricing, limits, live accuracy on Swahili, Sheng and English CHP notes, faithfulness checks, FastAPI integration | TypeSafe docs, live API calls with `jev-1.13.0`, Python SDK `typesafe-sdk` 0.7.2 | `research_jev.md`, `jev-test/` |
| W7 | Design | shadcn/ui state of play, Stripe visual language, token set, WCAG contrast, risk semantics | Raw shadcn docs, a real `shadcn init` scaffold with pnpm, Stripe production CSS bundles, a WCAG 2.x luminance script | `research_design.md`, `tokens/check3.py` |
| W8 | Idea scoring | Four finalist ideas scored on six criteria | One live Jev request with 24 Score questions | `jev-test/score_ideas.py`, `jev-test/idea_scores.json` |

### 1.3 How (Tools)

| Tool | Used for | Notes |
|---|---|---|
| Web search and page fetch | Organiser sites, press, journals, guidelines | Paywalled or blocked pages are labelled UNVERIFIED (for example Nation articles, LinkedIn) |
| GitHub API (`gh api`, `gh search repos`, `gh search code`) | Repo metadata (stars, push dates, redirects), commit authors, competitor discovery, MeTTa health prior art | Queries logged in section 6.10 and section 7.1 |
| Public APIs | WHO Global Health Observatory (MMR, maternal deaths, stillbirths, anaemia), World Bank WDI, Open-Meteo Flood and forecast APIs | Values read directly from API JSON are VERIFIED |
| Primary documents | KDHS 2022 Key Indicators Report and Summary Report PDFs, Kenya Law (DPA 2019, PHC Act 2023, Digital Health Act 2023, FIF Act 2023), ODPC regulations, WHO SMART ANC CQL and PlanDefinition JSON, MOH MCH Handbook, MOH 100 form | Section numbers quoted from the legal texts were read on Kenya Law |
| Live tests on macOS 27.2 arm64 | Homebrew SWI-Prolog 10.0.2, PeTTa v1.0.4, janus-swi 1.5.3, hyperon 0.2.10 via pip on Python 3.12, FastAPI 0.142.2, Omega `lib_nal.metta` and plugin API | uv at `~/.local/bin/uv`; Pythons 3.11, 3.12.13, 3.13.9 and 3.14.6 available |
| Jev API live tests | 12 notes x 10 danger signs x 3 variants, BP selection, PROM decomposition, determinism, faithfulness, error probes, FastAPI end to end, idea scoring | Model `jev-1.13.0`; key read from the shell environment only, never written to disk |
| shadcn CLI and Stripe CSS | `pnpm dlx shadcn@latest init -t next -d` scaffold; token extraction from Stripe's CSS bundles | Contrast verified with `tokens/check3.py` |

### 1.4 When

All research was carried out on **Friday 2 October 2026**:

| Approximate time | Activity | Evidence of time |
|---|---|---|
| About 06:10 UTC (09:10 EAT) | Platform scan: 451 registered, 5 entries | research_hackathon.md header |
| About 09:15 EAT | PeTTa clinical demo run across three processes | Event log timestamps `2026-10-02T09:15:02` |
| About 09:30 to 09:50 EAT | Alternatives scan | research_alternatives.md header |
| Morning | Jev live tests, design scaffold, maternal evidence, landscape | Respective files dated 2026-10-02 |

### 1.5 Labelling Convention

| Label | Meaning |
|---|---|
| **VERIFIED** | We ran it on our machine, or read the value directly in the primary source (repo code, release notes, an API response, the PDF table, the Act on Kenya Law, the CQL on GitHub). |
| **UNVERIFIED** | From a secondary source (press, search-engine summary, a page we could not open in full, a conference abstract where the primary report was not opened), or something we did not run. Do not put these in the pitch or the product without checking. |
| **CONFLICT** | Two credible sources disagree. Both values are shown with the reason we prefer one. |
| **COMPUTED** | A number we derived ourselves from cited inputs (for example annual rates of reduction, NAL hand checks, cost per note). The formula is shown. |
| **NOT FOUND** | Not found in the searches listed. This is not proof of absence. |

Labels from the original workstream files are preserved. Where a workstream file wrote "[UNVERIFIED]" in brackets, this file writes **UNVERIFIED** in bold.

### 1.6 Local Artefacts

All raw material is in the session scratchpad (`/private/tmp/claude-501/-Users-eugenius-Work-Basix-Hackathon/021936bd-ed76-485e-86e5-093237eece22/scratchpad/`):

| Path | Contents |
|---|---|
| `deck.txt` | Text of the official deck (same file as `docs/source/260924_SingularityNET-Omega-BASIX-Hackathon_SJIT-KU-2026_24HR+TEAM.pptx.pdf`) |
| `omega-src/` | Clone of `singnet/Omega` at commit `31ff0aa` (2026-10-01) |
| `petta/` | Clone of `trueagi-io/PeTTa` at tag `v1.0.4` |
| `metta-test/demo/` | `clinical.metta`, `kb.py`, `demo1.py`, `api.py`, `hyperon_check.py`, `t_plugin.py`, `tp.py`, `t_api.py` |
| `jev-test/` | `cases.py`, `run_extraction.py`, `run_hard.py`, `followup.py`, `jev_service.py`, `app_test.py`, `score_ideas.py`, logs (`run1.log`, `run_hard.log`, `followup.log`), raw answers (`results.json`, `results_hard.json`, `results_followup.json`, `idea_scores.json`), and `docs/` (downloaded TypeSafe doc pages) |
| `shadcn-probe/probe-app/` | A default scaffolded shadcn Next.js project |
| `stripe/` | `all.css`, `hds.txt`, `docs.css` (Stripe CSS and extracted tokens) |
| `tokens/check3.py` | WCAG 2.x contrast and colour-vision-deficiency check |

### 1.7 Limits Of This Research

1. Time-boxed to one day. Breadth was preferred where depth would not change a build decision.
2. We could not log in to basix.market, so the submission form field list is inferred (section 3.6).
3. Several Kenyan primary reports were inaccessible (CEMD 2017 and 2015/16 full reports; GHDx returned 403 and the Harvard-hosted PDF was removed). CEMD figures therefore come from a conference abstract and press (section 5.7).
4. The full Omega agent loop was not run: it needs an LLM key, torch and ChromaDB, and the Docker daemon was not running (section 4.19).
5. Jev accuracy numbers come from 12 notes written and labelled by us. They are a plausibility check, not a validation (section 8.20).
6. Nothing here is clinical advice. Thresholds are simplified for a demonstration.

---

## 2. Research Question Map

The questions we needed answered before building, the short answer, and where the evidence lives.

| # | Question | Short answer | Section |
|---|---|---|---|
| Q1 | Which deadline counts? | Two exist: deck 11:59 PM IST 2 Oct (21:29 EAT) and platform 23:59 UTC 2 Oct (02:59 EAT 3 Oct). We plan for the earlier and submit by 21:00 EAT. | 3.2 |
| Q2 | Which track and problem do we pick as a solo builder? | Platform has no Solo track. Pick **Omega**, problem **The Agent Without Borders**, and name **solo challenge 01** in the description. | 3.3, 3.4 |
| Q3 | How is it judged? | All-track rubric 30/25/25/20 (technical, video, fit, docs); Omega rubric 30/30/20/20 (innovation, technical, **sustainability impact**, docs). | 3.5 |
| Q4 | What must be submitted, and with what limits? | Public repo, README with AI Disclosure, one Omega feature, a transcript or audit trail, a 3-minute video, what's next. Form limits from platform JS. | 3.4, 3.6 |
| Q5 | Who are the judges and what impresses them? | 14 judges: about 5 technical Omega/MeTTa, 5 media and business, 3 ecosystem. Real Omega use, memory that changes the answer, human override, a story that can air on YouTube. | 3.9 |
| Q6 | What won similar events? | BGI Sprint and HyperSprint winners: memory that visibly matters, human approval, trust scoring, real Omega loop and NAL. No healthcare winner yet. | 3.10 |
| Q7 | What is Omega, technically? | `singnet/Omega` (formerly OmegaClaw), a roughly 200-line MeTTa agent loop on **PeTTa** (MeTTa on SWI-Prolog), with `lib_nal.metta` and `lib_pln.metta` for truth-valued reasoning, three-part memory and a plugin API. | 4.1, 4.2 |
| Q8 | Can we run Omega's reasoning on this Mac today? | Yes. PeTTa v1.0.4 on Homebrew SWI-Prolog 10.0.2, hosted from Python 3.12 via janus-swi 1.5.3, loads Omega's unmodified `lib_nal.metta`, skills, utils, helper and a custom plugin. VERIFIED. | 4.6 to 4.12 |
| Q9 | What breaks during install, and how do we fix it? | Four PeTTa gotchas (janus links Python 3.9; verbose flag; `working_dir/1`; library path resolution) and hyperon wheel limits (cp38 to cp312). All have workarounds. | 4.7, 4.13 |
| Q10 | Do the NAL numbers check out by hand? | Yes: deduction 0.729 then 0.59049; revision of two equal conclusions 0.74253. | 4.10 |
| Q11 | Is there a fallback runtime? | `pip install hyperon==0.2.10` on Python 3.12 with two shims gives identical numbers. VERIFIED. | 4.13 |
| Q12 | How big is the maternal mortality problem in Kenya? | MMR 379 per 100,000 (2023, MMEIG via WHO GHO), about 5,700 deaths per year, falling only about 2.2% per year. World Bank WDI shows 149, an unexplained conflict. | 5.2, 5.3 |
| Q13 | Where do women die in the chain? | Sub-optimal care in 81.4% (2014) to 98.1% (2015/16) of reviewed deaths; 64% of severe outcomes already present on arrival at referral hospitals; MgSO4 given in only 77% of severe cases. Delay 3 is at least as large as Delays 1 and 2. | 5.7, 5.9, 5.10 |
| Q14 | Who is the community witness and what do they carry? | About 107,800 paid CHPs, each about 100 households, with a BP machine but no Hb meter or dipstick, using eCHIS on smartphones. | 5.12, 5.13 |
| Q15 | Which thresholds are safe to encode? | WHO SMART ANC DAK decision tables (DT.01, DT.04, DT.06, DT.12, DT.17, DT.25, DT.27), ISSHP onset timing (20 weeks), shock index tiers, WHO/FIGO/ICM 2025 PPH definition, WHO 2024 Hb cut-offs. | 5.17 |
| Q16 | Does decision support work? What failed? | Detection plus a forced bundle works (E-MOTIVE). Detection alone often does not (CRADLE-3, CRADLE-5, CLIP, BetterBirth). Failures: alert fatigue, no downstream capacity, low contact fidelity, black boxes, no referral feedback, connectivity. | 5.18, 5.19 |
| Q17 | What does Kenyan law require of us? | DPA 2019 s.31 DPIA, s.35 no solely automated significant decisions, s.46 health data via providers, s.48 to 49 transfers, reg. 26 local copy; Digital Health Act audit trails; PPB medical device software guideline. | 5.20 |
| Q18 | Is the idea novel? | The generic "danger-sign triage plus referral" is crowded (15+ repos). Not found anywhere: symbolic cross-visit, cross-site reconciliation with provenance; the referral as a contestable proof; any of this in MeTTa. | 6.7 |
| Q19 | What are the framing risks? | "Rising BP" alone is not predictive; CHPs have no Hb meter; CLIP was null; explanations can increase over-reliance; scope creep. | 6.8 |
| Q20 | Is there a better idea? | No. Flood early warning was the closest challenger. Jev rubric scoring: Mizani 3.53, flood 2.77, RVF 2.41, chama 1.96 (0 to 4). | 7 |
| Q21 | Can Jev read Swahili and Sheng CHP notes reliably enough to pre-fill toggles? | On 12 test notes: 118 of 120 sign judgements correct with Choice, no missed present sign, about 390 ms per note. Errors teach two design rules (ask literal facts; put exclusions in definitions). | 8.10, 8.11 |
| Q22 | How much does Jev cost and how fast is it? | $0.042 per million input tokens, output free; about $0.00012 per note; median about 385 to 398 ms. | 8.5, 8.10 |
| Q23 | What is the current shadcn/ui default and how do we get a Stripe look? | CLI 4.21.1, Base UI default, style base-nova; replace tokens with a navy and blurple set; verified contrast. | 9 |
| Q24 | What remains unknown? | See the consolidated list. | 10 |

---

## 3. The Hackathon And Organisers

Condensed here. **The full, authoritative detail (schedule by session, every track's text, every judge, the submission checklist) is in [info.md](info.md).** This section keeps every key fact and URL so the research log stands on its own.

### 3.1 Key Facts

| Item | Value | Source |
|---|---|---|
| Name | SingularityNET x Omega x BASIX.Market Hackathon; platform title "BASIX Omniversity: Hackathon" | Deck slide 1; https://basix.market/lms/hackathon/1 |
| Theme | "Building beneficial AI with MeTTa & Omega" | Deck slide 1 |
| Platform tagline | "building the AI Infrastructure Layer across three tracks on a single platform." | https://basix.market/lms/hackathon/1 |
| Format | "2 + 1": build 30 Sept and 1 Oct; polish, record and submit 2 Oct | Deck slides 1, 4, 23 to 25 |
| Mode for us | Online/Virtual (Kenyatta University virtual stream) | Platform page; deck slide 4 |
| Platform window | Start 30 Sept 07:01 UTC; submissions due 2 Oct 23:59 UTC; event ends 3 Oct 05:59 UTC | https://basix.market/lms/hackathon/1 |
| Prize pool | **USD 1,700**, split not published (**UNVERIFIED** split) | https://basix.market/lms/hackathon/1 |
| Winners | **5 winners** enter "A New BASIX.MARKET hackathon, 24th & 25th October 2026" | Deck slides 1, 3 |
| Registered / entries | **451 registered, 5 entries** at about 06:10 UTC on 2 Oct | https://basix.market/lms/hackathons |
| Team size | 3 to 4 per team, or solo; solo hackers must build on Omega | Deck slides 5, 26 |
| Our team | "Technetians", solo, lead Eugene Mutembei; stage declared "Just an idea"; problem declared "We are reducing maternal health related deaths." | Platform page (see info.md section 3) |
| Operator | XR-AGENCY PTE. LTD., 2 Venture Drive #19-21, Vision Exchange, Singapore 608526, UEN 202425407R; terms dated 28 September 2026 | https://basix.market/terms |
| Platform stack | Next.js on Vercel, Clerk (`clerk.basix.market`), Resend, Neon | https://basix.market/privacy |

### 3.2 Deadlines And Judging Times

| Moment | Source | UTC | EAT (Nairobi, UTC+3) |
|---|---|---|---|
| Deck hard deadline: "11:59 PM IST, October 2" | Deck slides 22, 25, 35 | 18:29, 2 Oct | **21:29, Fri 2 Oct** |
| Platform deadline | https://basix.market/lms/hackathon/1 | 23:59, 2 Oct | 02:59, Sat 3 Oct |
| Eligibility check by BASIX and technical staff | Deck slide 27 (10:30 to 14:00 IST) | 05:00 to 08:30, 3 Oct | 08:00 to 11:30 |
| Judges receive repos, docs, videos | Deck slide 27 (14:00 to 18:00 IST) | 08:30 to 12:30 | 11:30 to 15:30 |
| Virtual finalist presentations | Deck slide 27 (19:30 to 21:00 IST) | 14:00 to 15:30 | **17:00 to 18:30** |

Rule adopted: **submit by 21:00 EAT on Friday 2 October**, and keep 17:00 to 18:30 EAT on Saturday free. Conversion: EAT = IST minus 2 hours 30 minutes.

### 3.3 Tracks And Problems As The Platform Encodes Them

From the platform's public JavaScript (`https://basix.market/_next/static/chunks/7031-3142d4b527d0f389.js` and the `/lms/hackathon/[id]` chunk), VERIFIED:

| Track key | Label | Problems |
|---|---|---|
| `metta` | MeTTa | The Glass Box Agent; The Agent That Grows Up |
| `omega` | Omega | Two Agents One Truth; **The Agent Without Borders**; BASIX.Market Mature Build |
| `next-level` | Next Level Developed | The Agent That Can Be Trusted With Money; The NPC That Won't Break Character |
| `ai-infra` | AI Infrastructure Layer | Build the AI Infrastructure Layer |

- **There is no Solo track in the dropdown.** The deck's five solo challenges do not appear in the platform code.
- Project stage options: "Just an idea", "Planning and design", "Early build, some code written", "Working prototype".
- Institutions offered: SJIT (St Joseph Institute of Technology), Kenyatta University (Nairobi), CodeSlayer (developer community).
- Event statuses: draft, open, judging, closed. Teams join via invite links (`?code=...#register`).
- **Recommendation adopted:** Omega, The Agent Without Borders, framed as solo challenge 01 (one auditable decision) delivered across language and connectivity limits. Whether staff have a hidden solo flag is **UNVERIFIED**.

The Agent Without Borders (deck slide 14) offers three options: (1) a reasoning agent that explains its decisions in a **local language**; (2) a **low-bandwidth/offline-first** agent that decides locally with a small MeTTa rule set, then **reconciles with a fuller Omega-style agent when connectivity returns, and shows how its answer changed and why**; (3) an accessibility-first agent. Mizani implements option 2 as its core and option 1 in its explanations.

### 3.4 Solo Track Requirements

From deck slides 26 and 27 (full text in info.md section 8):

| Requirement | Wording (deck) |
|---|---|
| Runtime | "Built on Omega, not optional." "If you're building solo, you're building on Omega, full stop." |
| What must be the feature | "Some visible piece of Omega's stateful, auditable-reasoning architecture has to be the actual feature, not decoration." |
| Scope | "No solo hacker attempts a complete platform. One feature, proven, is the whole assignment." |
| Challenges (choose one) | 01 one agent producing an auditable decision; 02 one agent learning and updating a rule; 03 two agents resolving one conflicting claim; 04 one NPC demonstrating persistent memory; 05 one BASIX workflow completing a defined business task |
| Deliverables | Working GitHub repo shared with BASIX.Market; short README (problem, solution, technology, AI Disclosure); one functioning Omega feature; a sample reasoning transcript, memory record or audit trail; a 3-minute demo video; a short statement of what you would build next |
| AI Disclosure | Mandatory. "Undisclosed use, if discovered, is a disqualifying integrity issue; disclosed use is not." |
| Registration | "MUST BE COMPLETED WITH INSTITUTION DECLARED" (deck slide 22); "Taking part in a hackathon requires an organisation on your profile" (https://basix.market/privacy) |
| Video reuse | "All submission videos can and will be used on the BeyondTheCode.ai BGI Comms YouTube" (deck slide 29). Treat as public: synthetic data, no faces without consent |

### 3.5 Rubrics

| All-track rubric (deck slides 22, 27) | Weight | Omega track rubric (deck slide 12) | Weight |
|---|---|---|---|
| Technical execution | 30% | Innovation & Creativity | 30% |
| Clarity of the 3-minute video/demo | 25% | Technical Implementation | 30% |
| Fit to track (Omega/MeTTa/BASIX) | 25% | **Sustainability Impact** | **20%** |
| Documentation & build process | 20% | Documentation & Presentation | 20% |

Quality bar (deck slide 22): deliverables should be "closer to a working alpha than an experiment"; judging rewards usability and completeness over non-functional ideation.

### 3.6 Submission Form Limits

VERIFIED from platform JS validation: `title {min:3,max:80}`, `tagline {min:10,max:140}`, `description {min:120,max:4000}`, `url {max:300}`. The field list itself is **UNVERIFIED** (no login); a competitor's repo copies it field by field: Project title, Tagline (one line), Description (Markdown; what it does, how it works, what's next), GitHub repository, Live demo, Slide deck, Track, Demo video. https://github.com/simpleHacker0893/basix-venture-route/issues/150

### 3.7 IP, Terms And Privacy

| Topic | Finding | Source |
|---|---|---|
| Ownership (deck) | "Students retain Partnership with BASIX.MARKET and own 100% creative control." | Deck slide 30 |
| Ownership (terms s.7) | Users keep ownership; BASIX gets a "simple, non-exclusive licence" to store, display and review; jointly built projects are governed by separate agreements | https://basix.market/terms |
| Originality (terms s.6) | Bans "submitting work that is not your own as your own" | https://basix.market/terms |
| Truthful registration (terms s.3) | Details must be "truthful and complete" | https://basix.market/terms |
| Event rules (terms s.5) | Event-page rules apply on top of the terms | https://basix.market/terms |
| KU incubation caution | XR Agency's KU practice: "Every student project developed on BASIX Market is jointly owned by the platform and the student builders, recorded in a signed Ownership Schedule before anything is deployed or monetized" (applies to incubation, not the entry) | https://xragency.org/institutional-practice.html |
| Public results | Result pages "show the names of participants who submitted an entry, together with the entry's title, link, placement and prize" | https://basix.market/privacy |
| Repo visibility | For a linked repo BASIX requests "the repository's public list of contributors", so the repo must be public. No BASIX or XRA GitHub org was found to invite (checked basixmarket, basix-market, xragency, beyondthecodeai and others) | https://basix.market/privacy |
| Prize balances | The system tracks "prize-money balances" (**UNVERIFIED** that prizes are credited on platform) | https://basix.market/privacy |
| On-chain data | "PII stays in the LMS; only hashes and IDs go on chain." | https://basix.market/ops |

### 3.8 Organisers And Partners

| Organisation | Role | What it cares about (evidence) | Source |
|---|---|---|---|
| SingularityNET | Technology partner; Omega comes from them | Renamed OmegaClaw to Omega in Sept 2026 to centre "the agent itself": how it "retains experience, continues operating over time, and develops an understanding of its user" (post of 2026-09-10). Ben Goertzel: "Omega is not so much the hands. Omega is the mind." and "The LLM is a component the cognitive layer calls on, not the thing running the show." (2026-09-15) | https://t.me/s/snetann ; https://bengoertzel.substack.com/p/how-omega-lost-its-claw ; https://github.com/singnet/Omega |
| BASIX.Market / XR Agency (XRA) | Host and operator | Woman-led, founded 2020; offices in Singapore, NYC, LA, Munich, Addis Ababa, Nairobi, Chennai; "We report retention, not registration"; turning "hackathon teams into retained contributors"; "Secure first"; MeTTa case study promised grants, integrations and 6-month mentorship to winners and next-step recommendations to others; plans for "Sub-Saharan Africa"; "Omega Claw" is XRA incubator Program 02 | https://xragency.org/ ; https://xragency.org/case-study.html |
| BASIX homepage and pages | Platform | "BASIX Omniversity Incubator. A Web3 & AGI incubator where you learn MeTTa, build real software in live cohorts, and own what you build as verifiable on-chain IP"; DICE co-ownership (Developers, Investors, Creators, Entrepreneurs); "2 Cohorts Live Now · SJIT & ESU KU"; curriculum "Hackathon placement → on-chain credential + record"; verticals "agri · sport · health · energy"; students "Learn MeTTa, OmegaClaw & Web3 tools"; a "Sponsor a hackathon" path | https://basix.market/ ; https://basix.market/curriculum ; https://basix.market/ecosystem ; https://basix.market/join |
| basixmarket.io | Mirror | Redirects to the same site; XRA describes BASIX Market as "A developer-owned marketplace for building, certifying and monetising AI datasets, with on-chain royalties and an IP certification system" | https://xragency.org/ |
| Partners page | Partner list | SingularityNET, ASI Alliance, Fetch.ai, Cardano Foundation, iCog Labs, BGI Commons, BGI Summit, Rejuve.bio and Expand Health ("Longevity & health"), DevSphereIndia, SJIT, Wada; embedded "Edge of Show" health videos | https://basix.market/partners |
| BGI Comms / Commons / Nexus | Help desk and community; HyperSprints; grants | BGI Commons is "part of the SingularityNET ecosystem" and runs HyperSprints; BGI Nexus funds "social and environmental good" (2025 Round 1 awardees included GlucoseDAO, a sign-language translator and Farmlingua) | https://bgicommons.org/hypersprint ; https://singularitynet.io/announcing-the-bgi-nexus-grant-round-01-awardees/ |
| iCog Labs (Addis Ababa) | Developers and mentors; virtual internship | Long-time SingularityNET partner; Ben Goertzel is Chief Scientific Advisor; 2026 AI Talent Program batch 1; 2024 partnership with XR Agency and Hanson Robotics "to advance Africa's position in AI and AGI" | https://icog-labs.com/about-us/ ; https://geezjobs.com/job-detail/ai-internship-program-icog-labs-1 ; https://t.me/s/snetann |
| BeyondTheCode.ai | Media; films the event | AGI docuseries about Ben Goertzel, produced by Nefertiti Strong, narrated by Macy Gray; plans to cover the Cardano Africa Tech Summit 2026 in Nairobi | https://www.beyondthecode.ai/ ; https://www.einpresswire.com/article/697493862/xr-agency-revolutionizing-immersive-experiences-and-web-3-0-solutions-with-groundbreaking-docuseries-beyondthecode-ai ; https://www.youtube.com/@BeyondTheCode_AI_ |
| Blockwee | Two judges | "A global video studio for tech companies", "Made with love in SF"; clients include Sentient, OpenGradient, Solana Superteam | https://blockwee.com |
| Heir | One judge | "Onchain estate planning"; family office reportedly focused on "fiscal, organic, and agentic longevity" (**UNVERIFIED**, search snippet) | https://theorg.com/org/heir-es/org-chart/logan-golema ; https://in.marketscreener.com/insider/LOGAN-GOLEMA-A46EDM/ |
| Cognitive Sprints | BASIX.Market Dev Rel | "CS AI Labs", Carrollton, Texas; programmes in India, Malawi, Zambia, Liberia, DRC; "CS AI Agriculture" | https://cognitive-sprints.in |
| DevSphereIndia | Special guest (CodeSlayer 2K26) | Developer community; no public CodeSlayer 2K26 page found (**UNVERIFIED**); a different "Code Slayer" ran at NIT Delhi in Nov 2025 | https://www.linkedin.com/company/devsphereindia-community ; https://nitdelhi.ac.in/campus/clubs/uba-cell/gallery/Code%20Slayer |
| SJIT, Chennai | Live venue | "MeTTa Omniversity", South India's "first AGI bioregional hub", about 40 developers per cohort, "keynoted by Dr. Ben Goertzel" | https://xragency.org/ |
| Kenyatta University / ESA-KU | Virtual venue | MOU signed **July 2026**, 12-month term; carries "the projects they judge viable through to incubation, managed development, and deployment"; data handled under the Kenya Data Protection Act 2019 | https://xragency.org/institutional-practice.html |
| Rejuve.bio, Expand Health | "Longevity & health" partners | Rejuve: "an AI-driven research platform" with a neural-symbolic knowledge graph, Goertzel as Chief AI Officer. Expand Health: "AI co-pilot for health professionals", clinics in Cape Town and Bucharest | https://www.rejuve.bio ; https://www.expandhealth.io |
| Channels | Official hub | t.me/metta_omniversity: "BASIX MeTTa Omniversity Cohort 2 - powered by XRAgency.org DevRel", 233 members, private; onward link t.me/beyondthecode_DocuSeries | https://basix.market/channels ; https://t.me/metta_omniversity |

### 3.9 Judges (Condensed)

Fourteen names appear on deck slides 33 and 34. Full table with what to show each judge: info.md section 17.

| Judge | Role | Evidence of what they value | Source |
|---|---|---|---|
| Dr. Ben Goertzel | CEO and Chief Scientist, SingularityNET; Chief AI Officer, Rejuve | LLM subordinate to symbolic cognition; impressed by an agent "that remembered months of interactions" | https://bengoertzel.substack.com/p/how-omega-lost-its-claw ; https://www.rejuve.bio |
| Haley Lowy | Chief of Staff, SingularityNET / BGI Commons (appointed Apr 2026) | Likely GitHub `HWLowy`: 7 commits to singnet/Omega including "Add disclaimer about OmegaClaw usage and risks", "Enhance README with memory and metacognition details", "guideline for concise responses"; hosts "Technical Tuesdays: Omega: Beyond the Claw" | https://lifeboat.com/ex/bios.haley.lowy ; https://github.com/singnet/Omega/commits?author=HWLowy ; https://t.me/s/snetann |
| Rafael Presa | AI Community Strategy Manager | Deep Funding team, decentralised community programmes (search snippet) | https://forum.cardano.org/t/decentralising-artificial-intelligence/118468 |
| Nefertiti Strong | Co-founder, CVO and COO, XRA; oversees BeyondTheCode | Grammy-nominated, Sundance-screened; "inclusion and cultural infrastructure" | https://xragency.org/about.html |
| Saskia N. Betz | Co-founder, CEO and CMO, XRA | CompTIA Security+; "human-first creative ambition with information-security discipline" | https://xragency.org/about.html |
| Rosyan "Rosy" Salutem | Head of Partnerships, XRA | Climate Change Fellow; "partnerships that unlock human potential, not just platform growth" | https://xragency.org/about.html |
| Sheila Wanjiru | Head of Business Development, XRA | "East Africa market entry and institutional adoption"; LinkedIn mentions "Code Quarium" (blocked from fetch) | https://xragency.org/about.html ; https://www.linkedin.com/in/sheila-wanjiru-925bb7177/ |
| Yeabesera Derese | Lead developer and CTO, XRA / BASIX; researcher on self-improving AI; CTO of worldtennis.app | No public footprint found (**UNVERIFIED** beyond deck) | Deck slides 33 to 34 |
| Prateek Choudhary | Help Desk lead; HackIndia '24 and '25 national winner | No public footprint found (**UNVERIFIED**) | Deck slide 34 |
| Samuel Wondimagegnehu | AI/ML engineer and team lead, iCog Labs | Neuro-symbolic systems, symbolic music generation (**UNVERIFIED** footprint) | Deck slides 33 to 34 |
| Surafel Fikru | Software/AI engineer, iCog / SingularityNET; "working on the Omega projects" | GitHub `surafelfikru` ("Building aisdk.rs"); commits to singnet/Omega: Telegram file-download proxy, OpenRouter provider with reasoning support, parenthesis-balancing fixes. No public profile linking him to Omega beyond the deck and commits (**UNVERIFIED**) | https://github.com/singnet/Omega/commits?author=surafelfikru |
| Shiva Shukla | Head of Design, Blockwee | AI, filmmaking, storytelling | https://blockwee.com |
| Luvai Darwajawala | Co-founder and COO, Blockwee | YC, Emergent Labs, Solana; 80+ awards (**UNVERIFIED** beyond deck) | Deck slide 34 |
| Logan Golema | CEO and founder, Heir | Onchain estate planning; "AI agent architect" | https://theorg.com/org/heir-es/org-chart/logan-golema ; https://www.linkedin.com/in/logan-ryan-golema-115b59249/ |

**Panel takeaways.** About 5 of 14 judges are technical in Omega/MeTTa (Goertzel, Lowy, Derese, Wondimagegnehu, Fikru); about 5 lean media and business (Strong, Betz, Shukla, Darwajawala, Golema); about 3 lean ecosystem and partnerships (Presa, Salutem, Wanjiru). With 25% on video and 20% Omega "Sustainability Impact", a socially grounded, well-filmed entry is favoured.

### 3.10 History And Analogous Events

| Event | Facts | Winners | Source |
|---|---|---|---|
| MeTTa TRAINING/HACKATHON 2025, Nairobi ("The Developer Pathway Into AGI") | Hosted by BASIX and beyondthecode.ai with SingularityNET, Wada, iCog; co-hosted by GDG on Campus Kenyatta University; onboarding 1 to 8 Aug, virtual teaching 9 to 15 Aug, in-person 18 to 28 Aug 2025 at the Blockchain Centre, Rose Avenue; tracks Knowledge Graphs, Media Identity, Real-World Agents, Visual Agents; 603 registered | **UNVERIFIED** (never published). Known entries: "MeTTa LLM Security Guard" (pure-MeTTa prompt-injection defence, 45 tests); an unfinished locally adapted AI education project | https://luma.com/y5jblri6 ; https://t.me/s/snetann ; https://gdg.community.dev/events/details/google-gdg-on-campus-kenyatta-university-nairobi-kenya-presents-metta-training-amp-hackathon-the-developer-pathway-to-agi/cohost-gdg-on-campus-kenyatta-university-nairobi-kenya/ ; https://github.com/snjiraini/MeTTa_AI_Hackathon2025 ; https://github.com/eunice-mwicigi/LOCALLY-ADAPTED-AI-and-TECH-EDUCATION-SCHOOL |
| SJIT MeTTa Omniversity cohorts | Documented on video | No winners lists found | https://www.youtube.com/watch?v=heM5EOJdnQ4 ; https://www.youtube.com/watch?v=i4hwXoC6iD0 |
| BGI Sprint I (1 to 28 Jun 2026; 28 teams) | Judged on "impact, code quality, and BGI safety alignment"; open source required; non-monetary prize; top teams presented to Goertzel and BGI researchers | ThreadKeeper (budget-aware hybrid local/cloud OmegaClaw orchestration); Claw & Order (adversarial alignment auditor with safety grade and rewritten goal); Utsa (an agent that "remembers across weeks", matching #need and #offer) | https://bgicommons.org/hackathons/bgi-sprint-i |
| HyperSprint #1: OmegaClaw (30 Jul to 30 Aug 2026; 14 teams) | | Team Midnight (narrative agent); OmegaClaw Launchpad ("small, verifiable missions" showing "the real OmegaClaw loop, MeTTa/NAL reasoning, and human approval"); Local Trust (H3 Trust Harness: trust scores for local service firms from verifiable sources) | https://bgicommons.org/hackathons/hypersprint-1-omegaclaw |
| HyperSprint #2: Build What's Next for Omega (11 to 30 Sep 2026; 6 teams; judging) | Criteria Alignment, Quality & Build, Innovation; "Small, polished, reusable contributions are often more valuable than ambitious but incomplete ideas."; open source, docs, setup, video of 3 minutes or less; Track 1 examples include "Domain-specific assistants" | Not yet announced | https://bgicommons.org/hackathons/hypersprint-2-omega |
| HackIndia | XRA ran SingularityNET's track; Team Hackstreet won a HackIndia Spark with a MeTTa finance chatbot (search snippet) | | https://singularitynet.io/singularitynet-latest-ecosystem-updates-march-2025/ |
| Other MeTTa wins | Cognify (uAgents + Redis + MeTTa) and Atelier OS won the Colosseum Cypherpunk ASI track; MintCondition took 2nd at ETHGlobal NYC (search snippet) | | https://superintelligence.io/ethglobal-nyc-winners/ |
| Follow-on, 24 to 25 Oct 2026 | No public page: `/lms/hackathon/2` returns "That hackathon is not available."; theme likely NFT marketplace and phigital assets (**UNVERIFIED**, inferred) | | https://basix.market/lms/hackathons |

**Pattern across winners:** long-term memory that visibly matters, human approval or override, safety and trust scoring, real use of the Omega loop and NAL. **No healthcare winner found, so health is an open lane.**

### 3.11 Competition Seen On GitHub (2 Oct)

| Entry | Track | Note | URL |
|---|---|---|---|
| MED-VERDICT | Omega, Two Agents One Truth | Oncology second-opinion reconciler; static JS; README says "There is no language model behind this chat"; no Omega/MeTTa runtime seen | https://github.com/celstro/Med-Verdict-Two-agents-One-truth |
| MedTriage | MeTTa Glass Box | Emergency bed triage | https://github.com/Balaji150508/Medtriage |
| Venture Route | MeTTa | Nairobi team; very polished; Playwright-recorded video; SUBMISSION.md | https://github.com/simpleHacker0893/basix-venture-route |
| basix-trustgate (Fractional Approval Agent) | Next Level | Micro-lending approval | https://github.com/kaniska-praba007/basix-trustgate |
| CourtLens | Unknown | BASIX-named | https://github.com/katelyn-signa/courtlens.BASIX.MARKET |
| TruthBridge | Omega | Claims "a real MeTTa plugin loaded through Omega", run from `~/PeTTa` | https://github.com/Brian20264/TruthBridge |
| glassbox-agent | Glass Box | FastAPI, Flutter, Docker | https://github.com/Gitika2008/glassbox-agent |
| omega-real-formal-ablation-v1 | Omega | Calls Omega's real NAL revision; criticises hand-written Python NAL | https://github.com/fanz23-cell/omega-real-formal-ablation-v1 |

**No public entry found for "The Agent Without Borders" and none for maternal health** (GitHub repo search, 2 Oct). Additional Two Agents One Truth clones are in section 7.1.

### 3.12 Social And In-Event Channels

- SingularityNET announcements channel (last about 500 posts scanned): **no post about this BASIX hackathon**; 2026 posts cover HyperSprints, Technical Tuesdays and the Omega rename. https://t.me/s/snetann
- X, LinkedIn, Discord: no public posts found for "BASIX Omniversity", "basix.market hackathon" or "#BASIXhackathon" (**NOT FOUND**; login walls). Related X posts: https://x.com/SingularityNET/status/2049126570699174296 (OmegaClaw) and https://x.com/SingularityNET/status/2098133734839276013 (Omega rename).
- Help Desk "adjacent to the Live stream, Virtual track, and on BASIX.Market", "Mentors online", "iCog devs on Virtual" (deck slide 29). Office hours 17:15 to 17:45 IST on Day 1 and 17:00 to 17:45 IST on Day 2.

### 3.13 What This Means For Mizani

| Finding | Design consequence |
|---|---|
| Solo must be on Omega, and Omega's stateful auditable reasoning must be the feature | Load Omega's unmodified `lib_nal.metta` on PeTTa; package rules as an Omega plugin; show `(stv f c)` in the UI |
| Agent Without Borders option 2 is "offline decide, reconcile later, show how the answer changed" | The community agent decides offline; the facility agent reconciles; the diff panel is the hero |
| Winners had memory that mattered and human override | The facility agent's memory of a 14-week BP changes the conclusion; a clinician can contest any premise |
| Half the panel judges story and video | A synthetic Kenyan mother and CHP; a 3-minute arc; captions |
| 20% Sustainability Impact; KU MOU; Wanjiru's East Africa remit | Kenyan maternal burden, CHPs and eCHIS, an adoption path (county pilot, BGI Nexus, KU incubation) |
| Rival repos claim Omega without running it; two judges commit to the Omega repo | Pinned Omega commit, `(getSkills)` evidence, reproducible setup |
| Repo must be public; video will be public | Public repo; synthetic data only; disclaimers |

---
## 4. Omega, MeTTa, PeTTa And Hyperon

Researched 2 October 2026 on macOS 27.2 arm64. The Omega clone used is `singnet/Omega` at commit `31ff0aa` (2026-10-01); the PeTTa clone is tag `v1.0.4`. Test code: `scratchpad/metta-test/demo/`.

### 4.1 TL;DR

1. **"Omega" is `singnet/Omega`**, formerly **OmegaClaw** (`asi-alliance/OmegaClaw-Core`), which grew out of Patrick Hammer's **MeTTaClaw** (`patham9/mettaclaw`). It is a roughly 200-line MeTTa agent loop running on **PeTTa**, the SWI-Prolog MeTTa implementation. **It is not `pip install hyperon`.** An LLM picks "skills"; reasoning goes through Omega's own `lib_nal.metta` (NAL, operator `|-`) and `lib_pln.metta` (PLN, operator `|~`), which output `(stv f c)` truth values. Memory has three parts: a `pin` working slot, ChromaDB `remember`/`query`, and the append-only `memory/history.metta` episodic trace. Plugins add skills with `add-skill`. VERIFIED (repo).
2. **An embeddable Omega runtime works on macOS arm64** with Homebrew SWI-Prolog 10.0.2, PeTTa v1.0.4 and janus-swi in a Python 3.12 uv venv. Omega's unmodified `lib_nal.metta`, `src/skills.metta`, `src/utils.metta`, `src/helper.py` and a custom Omega plugin all load and run. VERIFIED.
3. **Fallback:** `hyperon` 0.2.10 from pip on Python 3.12 runs the same `lib_nal.metta` after two small shims and gives identical numbers. Wheels exist only for cp38 to cp312; Python 3.13 and 3.14 fail with "No matching distribution found". VERIFIED.
4. **Recommended build:** the clinical rules as an **Omega MeTTa plugin**, run in-process through PeTTa behind FastAPI. Visible features: the NAL proof trail with `stv` math; patient memory across visits as an append-only atom event log (the `history.metta` pattern), with NAL **revision** raising confidence across visits; `update-rule` returning an old/new diff. Optionally the full Omega agent (Docker, LLM key, `wschat` channel) as a chat front end (not verified here).

### 4.2 Identity And Lineage (VERIFIED)

| Fact | Evidence |
|---|---|
| Canonical repo `github.com/singnet/Omega`; Apache-2.0; created 2026-04-02; last push 2026-10-01; 143 stars | `gh api repos/singnet/Omega`; https://github.com/singnet/Omega |
| README definition matches the deck: "a neural-symbolic agent framework built on the Hyperon AGI stack… stateful cognitive architecture capable of auditable inference, autonomous self-improvement, and long-term persistence… continuous execution loop… auditable proof trails… minimalist MeTTa-based core of approximately 200 lines" | https://github.com/singnet/Omega/blob/main/README.md |
| **Renamed from OmegaClaw on 2026-09-30.** Release v0.1.20 lists PR #331 "Rename OmegaClaw to Omega" | https://github.com/singnet/Omega/releases/tag/v0.1.20 |
| Previous home `asi-alliance/OmegaClaw-Core` now redirects to `singnet/Omega`; release notes up to v0.1.19 link PRs there | `gh api repos/asi-alliance/OmegaClaw-Core`; https://github.com/singnet/Omega/releases/tag/v0.1.19 |
| Origin `patham9/mettaclaw` by Patrick Hammer, created 2026-02-21 | https://github.com/patham9/mettaclaw |
| iCog Labs contributes directly: PR #353 merged from `iCog-Labs-Dev/feat/telegram-file-proxy-route` on 2026-10-01 | `gh api repos/singnet/Omega/commits` |
| First deployed agent "Oma", a Telegram bot (t.me/ASI_Alliance) | README |
| Docker images `singularitynet/omega` (latest, v0.1.19, SHA tags; amd64 and arm64; about 2.3 GB) and older `singularitynet/omegaclaw` | https://hub.docker.com/r/singularitynet/omegaclaw ; Docker Hub API |
| Deck speaker list: one presenter "Currently working on The Omega projects" at iCog Labs | deck.txt line 1084 |

UNVERIFIED secondary coverage:
- MindStudio (2026-09-07): one Docker command; memory survived a container restart; "no web UI" (chat channels only). https://www.mindstudio.ai/blog/omegaclaw-symbolic-ai-agent
- openclawdatabase (2026-09-06): Docker test. https://openclawdatabase.com/news/videos/2026-09-06-omegaclaw-symbolic-agent-docker-test/
- Fetch.ai Innovation Lab: OmegaClaw plus Agentverse skills, tag `hackathon2604`. https://innovationlab.fetch.ai/resources/docs/examples/openclaw/omegaclaw-agentverse-skills

### 4.3 Architecture (VERIFIED From Source)

**Runtime is PeTTa, not hyperon-experimental.** The Dockerfile builds `trueagi-io/PeTTa` `v1.0.4` on `swipl:10.0.2`, plus FAISS and `petta_lib_chromadb`. `run.metta` is:

```metta
(import! &self (library lib_import))
(git-import! "https://github.com/singnet/Omega.git")
(import! &self (library Omega lib_omega))
!(omega)
```

Sources: https://github.com/singnet/Omega/blob/main/Dockerfile , https://github.com/singnet/Omega/blob/main/run.metta

**Agent loop** (`src/loop.metta`, about 118 lines). `(omega $k)` runs the steps below and then recurses on `(omega (+ 1 $k))`. https://github.com/singnet/Omega/blob/main/src/loop.metta

| Step | What happens |
|---|---|
| 1 | `receive` from the channel |
| 2 | `getContext`: PROMPT, SKILLS, LAST_SKILL_USE_RESULTS, HISTORY, TIME |
| 3 | `llmProviderChat` |
| 4 | `sread` the reply into up to 5 skill s-expressions |
| 5 | `eval` each skill |
| 6 | `addToHistory` |
| 7 | `sleep` |

**Persistence and audit trail.**

| Mechanism | Detail | Source |
|---|---|---|
| Episodic trace | `addToHistory` appends a timestamp, the human message, the LLM's s-expression commands and any `ERROR_FEEDBACK` to `memory/history.metta`; `episodes <time>` reads it back | https://github.com/singnet/Omega/blob/main/src/memory.metta |
| Semantic memory | `remember`/`query` use ChromaDB with local `intfloat/e5-large-v2` embeddings (or OpenAI or ASICloud) | https://github.com/singnet/Omega/blob/main/docs/reference-internals-memory-store.md |
| Working memory | `pin` slot | src/memory.metta |

**Reasoning.**

| Library | Size | What it implements | Operator |
|---|---|---|---|
| `lib_nal.metta` | 202 lines | NAL truth functions (deduction, abduction, induction, revision and others); rules as `(= (\|-nal premise1 premise2) conclusion)`, wrapped by `(\|- a b)` | `\|-` |
| `lib_pln.metta` | 309 lines | PLN (modus ponens, abduction, revision, inversion and others), borrowed from hyperon-pln | `\|~` |

The LLM calls them through the skill `(metta "(|- ...)")`. The docs give action thresholds: **ACT** when `f ≥ 0.6 and c ≥ 0.5`; **HYPOTHESIZE** when `f ≥ 0.3 and c ≥ 0.2`. Sources: https://github.com/singnet/Omega/blob/main/lib_nal.metta , https://github.com/singnet/Omega/blob/main/docs/introduction.md , https://github.com/singnet/Omega/blob/main/docs/tutorial-05-reasoning-with-nal-pln.md

**Self-modification and extension.** `add-skill`, `remove-skill`, `add-prompt-extension` and `add-heartbeat-listener` work by `add-atom`/`remove-atom` on `&self` (`src/skills.metta`). Plugins are MeTTa or Python modules exposing `loadOmegaPlugin`, listed in `config/plugins.yaml`. https://github.com/singnet/Omega/blob/main/docs/reference-plugin-api.md

**Channels.** IRC (default), Telegram, Slack, Mattermost, `wschat` (WebSocket JSON frames `user_message`/`agent_message`, configured with `WS_URL`), and mock. https://github.com/singnet/Omega/blob/main/channels/wschat.py

**LLM providers.** Anthropic (default), OpenAI, ASICloud, ASIOne, OpenRouter, and `OpenAIAPI` (any OpenAI-compatible URL, so a local server works). README.

**Maturity notes.**
- Version v0.1.x, with an experimental disclaimer.
- The docs admit "LLM premise formulation errors (up to ~16.6%)" and confidence decay of about 10% per hop.
- "Memory import does not work in a standalone Omega run".
- `lib_omega.metta` imports `./src/context`, which is **not in the repo at HEAD**. This looks like a live bug or work in progress; we did not run the full loop.

### 4.4 Official Install Paths (Full Agent Paths UNVERIFIED Here)

| Path | Command or steps | Status |
|---|---|---|
| Docker | `curl -fsSL https://github.com/singnet/Omega/raw/refs/tags/v0.1.19/scripts/omegaclaw \| bash -s -- singularitynet/omega:v0.1.19` (interactive: licence acceptance, channel and provider prompts; needs an LLM API key) | Not tested: the Docker daemon was not running on this Mac |
| Native | (1) `git clone PeTTa`, then into `PeTTa/repos/` clone `Omega` and `petta_lib_chromadb`; (2) create a venv; (3) `pip install -r repos/Omega/requirements.txt` (torch 2.12.1, chromadb 1.5.9, sentence-transformers and others); (4) `OMEGA_AUTH_SECRET=… sh run.sh run.metta IRC_channel=…` | Not run: heavy (torch plus a roughly 1.3 GB embedding model) and needs an LLM key |

### 4.5 MeTTa Runtimes: State Of Play (October 2026)

| Runtime | Status | Notes | Source |
|---|---|---|---|
| **PeTTa** (`trueagi-io/PeTTa`) | **What Omega uses.** v1.0.4 pinned in the Dockerfile; last push 2026-08-25 | MeTTa transpiled to SWI-Prolog; Python interop via janus (`py-call`); a Python host package (`from petta import PeTTa`). VERIFIED working | https://github.com/trueagi-io/PeTTa |
| **hyperon-experimental** (`pip install hyperon`) | v0.2.10 (2026-02-11); repo last push 2026-02-11 | Rust core; wheels **only for CPython 3.8 to 3.12** (macOS arm64 included) | https://pypi.org/project/hyperon/ ; https://github.com/trueagi-io/hyperon-experimental |
| MeTTa-WAM / MeTTaLog (`trueagi-io/metta-wam`) | Last push 2026-03-29 | Prolog WAM transpiler; not used by Omega | https://github.com/trueagi-io/metta-wam |
| MettaWamJam (`trueagi-io/MettaWamJam`) | Last push 2026-04-21 | SWI-Prolog HTTP server for PeTTa (`/metta`, `/metta_stateless`, port 5001); an alternative to FastAPI; UNVERIFIED | https://github.com/trueagi-io/MettaWamJam |
| MORK (`trueagi-io/MORK`) | Active (2026-09-15) | Rust hypergraph kernel; optional PeTTa backend via `mork_ffi` (`build.sh`); needs nightly Rust; skip for a hackathon | https://github.com/trueagi-io/MORK |
| DAS (`singnet/das`) | 1.2.0 (2026-07-30), active | Distributed AtomSpace persistence (MongoDB/Redis) through `das-cli`; integrated with hyperon-experimental, not PeTTa; **too heavy for 12 hours** | https://github.com/singnet/das |
| PLN | `trueagi-io/PLN`, `trueagi-io/pln-experimental` | Omega ships its own `lib_pln.metta` | https://github.com/trueagi-io/PLN ; https://github.com/trueagi-io/pln-experimental |

### 4.6 Test Environment And Install Commands That Worked (VERIFIED)

Machine: macOS 27.2, arm64. uv at `~/.local/bin/uv`. Pythons available: 3.11, 3.12.13, 3.13.9, 3.14.6.

**Embeddable Omega runtime (the path we build on):**

```bash
brew install swi-prolog                      # bottled 10.0.2, the version Omega pins
git clone --depth 1 --branch v1.0.4 https://github.com/trueagi-io/PeTTa.git petta
git clone --depth 1 https://github.com/singnet/Omega.git omega-src
uv venv --python 3.12 .venv-petta
uv pip install --python .venv-petta/bin/python janus-swi ./petta fastapi uvicorn
```

**hyperon via pip (fallback):**

```bash
cd scratchpad/metta-test
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python hyperon   # hyperon==0.2.10 OK
/opt/homebrew/bin/python3.14 -m venv v314 && ./v314/bin/pip install hyperon
#   ERROR: No matching distribution found for hyperon   (no cp313/cp314 wheels)
python3.12 -m venv v312pip && ./v312pip/bin/pip install hyperon                    # also OK with plain pip
```

The hyperon Python API (`t_api.py`) worked: `MeTTa().run(code)`; `space().add_atom(m.parse_single("(obs P1 v1 sbp 150)"))`; `space().query(pattern)` returning binding dicts; `register_atom("now-iso", OperationAtom(..., unwrap=True))` for grounded Python functions; `!(bind! &patients (new-space))` for named spaces; `space().get_atoms()` to serialise a space.

### 4.7 Gotchas And Workarounds (VERIFIED)

| # | Symptom | Cause | Workaround |
|---|---|---|---|
| G1 | `sh run.sh` fails to load janus, so `py-call` breaks | The Homebrew `janus.so` links Xcode CLT's Python 3.9 framework; macOS SIP strips `DYLD_*` variables when going through `/bin/sh` | For the CLI: `DYLD_FALLBACK_FRAMEWORK_PATH=/Library/Developer/CommandLineTools/Library/Frameworks swipl --stack_limit=8g -q -s src/main.pl -- file.metta` directly. Core MeTTa works without janus |
| G2 | Python interop needed | | Better route: host PeTTa from Python. `uv pip install janus-swi ./petta` into a py3.12 venv. janus-swi 1.5.3 builds against the brew swipl and uses the venv's Python, so `py-call` works (`!(py-call (math.sqrt 16.0))` gives `4.0`) |
| G3 | `PeTTa(verbose=False)` still prints compile noise | The code sets `self.verbose="false"`, a truthy string | `p = PeTTa(); p.verbose = False` |
| G4 | `import!` fails silently when PeTTa is hosted from Python | `Unknown procedure: working_dir/1`, which only the CLI `main.pl` asserts | `janus.query_once(f"assertz(working_dir('{os.getcwd()}'))")` and set `PETTA_PATH` to the clone. `(library Omega X)` resolves to `$PETTA_PATH/Omega/X`, so symlink `petta/Omega -> omega-src`. Alternative: `p.load_metta_file(abs_path)` |
| G5 | `pip install hyperon` fails on Python 3.13 or 3.14 | No cp313/cp314 wheels | Use Python 3.12 |
| G6 | `lib_nal.metta` on hyperon: `min`/`max` undefined | Missing in hyperon's stdlib (used by `Truth_Revision`) | Shim: `(= (min $a $b) (if (< $a $b) $a $b)) (= (max $a $b) (if (> $a $b) $a $b))` |
| G7 | `(\|- a b)` returns unevaluated on hyperon | `unique-atom` takes an `Expression`-typed argument, so hyperon does not evaluate it (PeTTa does) | Call `\|-nal` directly, or define `(= (\|-h $a $b) (let $r (collapse (superpose ((\|-nal $a $b) (\|-nal $b $a)))) (unique-atom $r)))` |
| G8 | Non-matching rules come back unreduced on hyperon | Hyperon returns `(\|-nal …)` and `(if (…Guard…) …)` expressions when no rule matches (PeTTa simply fails) | Filter results to those whose `stv` arguments are numbers |
| G9 | Concurrency | One PeTTa engine per process | Guard with a `threading.Lock`; sync endpoints in FastAPI's threadpool work. Never run uvicorn with multiple workers (each would be a separate in-memory space) |
| G10 | Full loop import error | `lib_omega.metta` imports `./src/context`, absent at HEAD | Do not depend on the full loop for P0; load `lib_nal`, `skills`, `utils`, `helper` and the plugin directly |

### 4.8 Omega's NAL Running Natively On PeTTa (VERIFIED, `tp.py`)

```
!(|- ((--> golden_retriever friendly) (stv 1.0 0.9)) ((--> friendly family_friendly) (stv 0.9 0.85)))
=> (((--> golden_retriever family_friendly) (stv 0.9 0.6885)) ((--> family_friendly golden_retriever) (stv 1.0 0.4077…)))

!(|- ((==> (∧ sbp_high proteinuria) preeclampsia) (stv 0.9 0.9)) (sbp_high (stv 1.0 0.9)))
=> (((==> proteinuria preeclampsia) (stv 0.9 0.729)))
```

The first result matches Omega's own tutorial value of 0.6885. The second shows conjunction elimination by deduction: knowing `sbp_high` reduces the rule to `proteinuria ==> preeclampsia` at confidence 0.729.

### 4.9 Clinical Demo: Trace, Persistence Across Processes, Rule Update With Diff (VERIFIED)

Files: `demo/clinical.metta` (knowledge base), `demo/kb.py` (facade), `demo/demo1.py` (three separate processes), `demo/api.py` (FastAPI).

How `clinical.metta` works:
- Thresholds are data, for example `(threshold sbp_high sbp 140)`.
- Rules are versioned atoms: `(rule r_pe v1 (==> (∧ sbp_high proteinuria_pos) suspected_preeclampsia) (stv 0.9 0.9))`.
- `fire` chains two NAL steps through Omega's `|-nal` and returns a proof term.
- `why` reports which conjuncts are present or absent.
- `update-rule` removes the old atom, adds the new one, and returns `(rule-diff (old …) (new …))`.

Run output across three separate Python processes sharing `mem.metta`:

```
=== visit1   (process 1)
final: suspected_preeclampsia (stv 0.9 0.59049)
(conclusion suspected_preeclampsia (stv 0.9 0.59049)
  (because (rule r_pe v1)
    (step 1 (premise sbp_high (stv 1.0 0.9) (from visit1 sbp 150 >= 140))
            (premise (==> (∧ sbp_high proteinuria_pos) suspected_preeclampsia) (stv 0.9 0.9))
            (derived (==> proteinuria_pos suspected_preeclampsia) (stv 0.9 0.729)))
    (step 2 (premise proteinuria_pos (stv 1.0 0.9) (from visit1 protein 2 >= 1))
            (premise (==> proteinuria_pos suspected_preeclampsia) (stv 0.9 0.729))
            (derived suspected_preeclampsia (stv 0.9 0.59049)))))
=== visit2   (process 2: memory replayed from log)
rules after restart: ((rule r_pe v1 ...))     visits remembered: (visit1)
(rule-status r_pe v1 suspected_preeclampsia (check sbp_high absent) (check proteinuria_pos absent))   <- visit3, why-not
(revision suspected_preeclampsia (stv 0.9 0.59049) + (stv 0.9 0.59049) => (revised suspected_preeclampsia (stv 0.9 0.74253)))
=== update   (process 3)
-((rule r_pe v1 (==> (∧ sbp_high proteinuria_pos) suspected_preeclampsia) (stv 0.9 0.9)))
+((rule r_pe v2 (==> (∧ dbp_high proteinuria_pos) suspected_preeclampsia) (stv 0.95 0.9)))
(rule-status r_pe v2 ... (check dbp_high absent) (check proteinuria_pos present))
=== log (memory file = audit trail)
(event 2026-10-02T09:15:02 add (rule r_pe v1 ...))
(event 2026-10-02T09:15:02 add (obs P1 visit1 sbp 150))
...
(event 2026-10-02T09:15:02 remove (rule r_pe v1 ...))
(event 2026-10-02T09:15:02 add (rule r_pe v2 ...))
```

What this proves: (1) a proof term, not a bare label; (2) memory survives process restarts by replaying an append-only atom log; (3) "why not" reporting; (4) revision across visits raises confidence from 0.59 to 0.74, so stateful memory does real reasoning work; (5) a rule update is an atom swap with an old/new diff recorded in the log.

Note: the demo's proteinuria threshold was `protein 2 >= 1` (dipstick 1+). Mizani's packs use 2+ (WHO ANC.DT.17 trigger "proteinuria ++ or more"), see section 5.17 and build.md section 7.

### 4.10 NAL Math Hand Checks (COMPUTED)

NAL truth functions as used by `lib_nal.metta` (and checked against its output):
- **Deduction:** `f = f1·f2`; `c = f1·f2·c1·c2`.
- **Revision:** convert confidence to evidence weight `w = c / (1 - c)` (with evidential horizon k = 1); `w_total = w1 + w2`; `f = (w1·f1 + w2·f2) / w_total`; `c = w_total / (w_total + 1)`.
- **Exemplification (second result of the golden retriever example):** `f = 1`; `c = w / (w + 1)` with `w = f1·f2·c1·c2`.

| Check | Inputs | Hand calculation | Engine output | Match |
|---|---|---|---|---|
| Golden retriever deduction | (1.0, 0.9) and (0.9, 0.85) | f = 1.0 × 0.9 = 0.9; c = 1.0 × 0.9 × 0.9 × 0.85 = **0.6885** | (stv 0.9 0.6885) | Yes |
| Golden retriever exemplification | w = 0.6885 | c = 0.6885 / 1.6885 = **0.40776** | (stv 1.0 0.4077…) | Yes |
| Step 1 deduction (rule with sbp_high) | rule (0.9, 0.9), sbp_high (1.0, 0.9) | f = 0.9 × 1.0 = 0.9; c = 1 × 0.9 × 0.9 × 0.9 = **0.729** | (stv 0.9 0.729) | Yes |
| Step 2 deduction (with proteinuria_pos) | derived rule (0.9, 0.729), proteinuria_pos (1.0, 0.9) | c = 1 × 0.9 × 0.9 × 0.729 = **0.59049** | (stv 0.9 0.59049) | Yes |
| Revision of two equal visits | (0.9, 0.59049) twice | w = 0.59049 / 0.40951 = 1.44194; w_total = 2.88389; c = 2.88389 / 3.88389 = **0.74253**; f = 0.9 | (stv 0.9 0.74253) | Yes |

Implications for Mizani:
1. Confidence decays with every deduction hop (0.9 → 0.729 → 0.59049), matching Omega's documented "about 10% per hop". Long rule chains will fall below the ACT band (`c ≥ 0.5`) fast, so rules should be shallow (two or three steps).
2. Revision of independent agreeing witnesses (the CHP's repeated home reading and the facility's repeat reading) **raises** confidence. This is the mathematical core of "two witnesses".
3. Under ACT `f ≥ 0.6 ∧ c ≥ 0.5`, the two-step 0.59049 conclusion acts, and a revised 0.74253 acts with more margin.

### 4.11 FastAPI Facade (VERIFIED)

`kb.py` (about 90 lines):
- Loads `omega-src/lib_nal.metta` and `clinical.metta` into PeTTa.
- Replays `(event ts add|remove atom)` lines with `!(add-atom &self …)` / `!(remove-atom &self …)`.
- `_apply()` both mutates the space and appends to the log.
- A 10-line s-expression parser turns the proof term into a JSON tree for the UI.

`api.py` (uvicorn 0.54, FastAPI 0.142.2), exercised with curl:

| Call | Result |
|---|---|
| `POST /patients/P9/obs` (sbp 152) | `why` shows proteinuria absent |
| `POST /patients/P9/obs` (protein 2) | rule fires with c = 0.59049 |
| `GET /patients/P9/assess` | `trace_tree` JSON |
| `PUT /rules/r_pe` | `{old,new}` |
| `GET /memory/log` | event list |

The single PeTTa engine is guarded with a `threading.Lock`.

### 4.12 Clinical KB As A Real Omega Plugin (VERIFIED, `demo/t_plugin.py`)

`omega-src/plugins/clinical/clinical.metta`:

```metta
!(import! &self (library Omega ./plugins/clinical/clinical_kb))
(= (loadOmegaPlugin)
   (progn
     (add-skill fire "Assess a patient visit against a danger-sign rule, returns NAL proof trail" (patient visit rule_id))
     (add-skill why "Explain which rule conditions are present or absent for a visit" (patient visit rule_id))
     (add-skill update-rule "Replace a rule with a new version, returns old/new diff" (rule_id version body truth))
     ()))
```

Load order from Python into PeTTa: Omega's own `lib_nal`, `src/helper.py`, `src/utils`, `src/skills`, then the plugin. Results:
- `!(loadOmegaPlugin)` returned `()`.
- `(getSkills)` contains `- Assess a patient visit …: fire patient visit rule_id` (and the other two), so the skills enter the LLM prompt in a full Omega run.
- Omega's own `metta` skill, `!(metta "(fire P1 visit1 r_pe)")`, returns the proof trail.

**So the same MeTTa file is both the web app's reasoning core and a drop-in Omega skill.** This is the evidence we show judges who check for "real Omega".

### 4.13 Hyperon Fallback (VERIFIED, `demo/hyperon_check.py`)

Omega's `lib_nal.metta` loads in hyperon 0.2.10 with the shims G6 to G8 above. With them, `fire`, `why`, revision and `update-rule` give identical numbers on hyperon (0.59049, 0.74253) in about 0.2 s. Use only if PeTTa breaks on the build machine.

### 4.14 Healthcare And Explainability Prior Art In The MeTTa Ecosystem

| Item | Finding | Source |
|---|---|---|
| Fetch.ai x SingularityNET "Medical Agent with MeTTa" | hyperon ≥0.2.6; atoms like `(symptom fever flu)`, `(treatment flu …)`, `!(match &self (symptom fever $d) $d)`; a lookup knowledge graph, not reasoning; an LLM fills gaps only when `LEARN=1`; one keyword per query; disclaimers. UNVERIFIED (doc read only) | https://innovationlab.fetch.ai/resources/docs/examples/singularityNet/medical-agent-metta ; https://github.com/fetchai/innovation-lab-examples |
| `Brian20264/TruthBridge` | "a real MeTTa plugin loaded through Omega", run from `~/PeTTa` | https://github.com/Brian20264/TruthBridge |
| `fanz23-cell/omega-real-formal-ablation-v1` | Calls the real Omega NAL revision engine; criticises hand-written Python re-implementations of NAL | https://github.com/fanz23-cell/omega-real-formal-ablation-v1 |
| `Gitika2008/glassbox-agent` | FastAPI, Flutter, Docker | https://github.com/Gitika2008/glassbox-agent |
| Earlier Omega repos | `MesTTo/omegaclaw-deontic` (event calculus/deontic), `marcelosite/omegaclaw-launchpad` | https://github.com/MesTTo/omegaclaw-deontic ; https://github.com/marcelosite/omegaclaw-launchpad |
| Hyperon framework paper | No clinical application | https://arxiv.org/pdf/2310.18318 |
| GitHub search "metta medical / health / clinical / pregnancy / diagnosis / symptom", "hyperon healthcare / medical" | **Zero** repositories (NOT FOUND); MeTTa repos are mostly practice projects (for example Icog-metta_lang_practice, MeTTa stdlib docs) | https://github.com/Kalkidan-Amare/Icog-metta_lang_practice ; https://github.com/eyuuab/MeTTa-lang-stdlib-documentation |

### 4.15 MeTTa Idioms For Explainable Decisions (Used In The Demo And In Mizani)

1. Keep rules as **data atoms** (`(rule id ver body tv)`) rather than only `=` definitions, so they can be listed, diffed and replaced with `remove-atom`/`add-atom`.
2. Return a **proof term** (`(conclusion C tv (because (rule …) (step …)…))`) instead of a bare answer.
3. Use `let*` pattern destructuring to bind evidence and filter non-matches.
4. Report **why-not** with `(collapse (finding …))` checked against `()`.
5. Put **truth values on everything** and use NAL revision to merge evidence over time.
6. Persist an **append-only event log of atoms** (Omega does the same with `history.metta`).
7. Hyperon has `trace!`; PeTTa's translator also supports `trace!` (seen in `src/translator.pl`).

### 4.16 Recommended Architecture (From The Omega Workstream)

```
Next.js (Vercel or local)
  ├─ Patient timeline: visits + observations (POST /patients/{id}/obs)
  ├─ "Reasoning receipt" panel: render trace_tree as a proof tree
  │     step 1 / step 2 premises with (stv f c), source observation, rule id+version
  │     ACT / HYPOTHESIZE / IGNORE badge from Omega's thresholds (f≥0.6∧c≥0.5 …)
  ├─ "Why not?" chips per rule (check X present/absent)
  ├─ Memory panel: live event log (GET /memory/log). This is the audit trail
  └─ Rule editor: PUT /rules/{id}; show unified diff old→new, then re-assess
        │ HTTPS/JSON
FastAPI (Python 3.12 venv: janus-swi + petta + fastapi)
  ├─ one PeTTa engine + threading.Lock
  ├─ loads: omega-src/lib_nal.metta (+ lib_pln), plugins/clinical/clinical_kb.metta
  ├─ memory/kb.metta  (append-only (event ts add|remove atom) log, replayed at boot)
  └─ optional: /chat. Run the full Omega agent (Docker singularitynet/omega, commchannel=websocket,
       WS_URL=ws://backend/ws) so an LLM turns free-text notes into (obs …) and calls the
       plugin skills fire/why/update-rule. Requires LLM key + Docker; UNVERIFIED here.
```

Why this satisfies "Omega's stateful, auditable-reasoning architecture is the feature":
- **Auditable reasoning.** Every alert is a NAL proof produced by Omega's own `lib_nal.metta` (unmodified, loaded from `singnet/Omega`) on Omega's runtime (PeTTa).
- **Stateful.** The patient record lives as atoms; revision across visits changes the confidence you see.
- **Self-modification.** `update-rule` is a MeTTa atom swap with a diff, recorded in the log.
- **Pluggable into the Omega agent.** Packaged as an Omega plugin (`loadOmegaPlugin` / `add-skill`).

**How Mizani adapts it (see build.md section 3).** Two processes running the same code with `MIZANI_ROLE=community` (port 8101, rule pack `edge-v1`, its own memory log and an offline outbox) and `MIZANI_ROLE=facility` (port 8102, `full-v1`, the mother's longitudinal record). Two processes rather than two spaces in one process because PeTTa runs inside one SWI-Prolog instance per Python process via janus, and because separate ports make "offline" real.

Original 12-hour build order from this workstream (superseded by build.md section 23): backend from `demo/` (1 h); severe features and a gestational age conjunct by chaining one more `|-nal` step (2 h); Next.js UI for timeline, proof tree, diff and log (4 h); README, AI disclosure, sample transcript and video (2 h); optional Omega chat via Docker and `wschat` (2 h).

### 4.17 Hardening Notes

| Risk | Mitigation |
|---|---|
| **Injection.** The demo's `update_rule` and `add_obs` interpolate strings into MeTTa | Validate `patient`/`visit`/`key` against `^[A-Za-z0-9_]+$`; require `value` to be a float; parse `body`/`tv` with `sexpr()` against a symbol whitelist before sending to PeTTa. build.md section 8.4 goes further: typed atom builders only, free text never enters MeTTa as code |
| **Multiple results.** `fire` can return several conclusions if a visit has repeated observations; `assess` took the first | Collect all results with `collapse`, select explicitly, and show the alternatives in the proof |
| **Single engine.** | One engine per process; no multi-worker uvicorn; the log is the source of truth |
| **Clinical framing.** | Decision support, not diagnosis; thresholds from guidelines (section 5.17) |

### 4.18 Exact Versions Used (VERIFIED)

| Component | Version |
|---|---|
| Python | 3.12.13 (uv-managed) |
| hyperon | 0.2.10 |
| SWI-Prolog | 10.0.2 (Homebrew bottle, arm64-darwin) |
| janus-swi | 1.5.3 |
| PeTTa | git tag v1.0.4, installed as `petta 0.1.0` from the local clone |
| Omega | `singnet/Omega` main @ `31ff0aad` (2026-10-01; latest tag v0.1.20) |
| FastAPI / uvicorn / pydantic | 0.142.2 / 0.54.0 / 2.13.5 |

### 4.19 Not Verified In This Workstream

- The full Omega agent loop (needs an LLM key, torch and ChromaDB; Docker daemon not running).
- The DAS and MORK backends.
- The MettaWamJam HTTP server.
- Whether the missing `./src/context` import breaks the current HEAD loop in Docker images (the v0.1.19 image may predate it).

---
## 5. Maternal Health Evidence

Prepared 2 October 2026 for a solo builder targeting Kenya's Community Health Promoters (CHPs) and primary care facilities. "VERIFIED" here means we read the number in the primary dataset or document (for example the WHO GHO API, the KDHS 2022 PDF tables, the Kenya Law text of an Act, or the WHO SMART ANC decision tables on GitHub).

### 5.1 The Numbers That Matter

| # | Statistic | Value | Source | Status |
|---|---|---|---|---|
| 1 | Kenya maternal mortality ratio (MMR), 2023 | **379 per 100,000 live births** (378.8; 80% UI 267 to 547) | [WHO GHO API, MMEIG 2025 round](https://ghoapi.azureedge.net/api/MDG_0000000026?$filter=SpatialDim%20eq%20'KEN') | VERIFIED (API) |
| 2 | Kenya maternal deaths, 2023 | **about 5,700** (5,682; UI 4,006 to 8,202) | [WHO GHO API](https://ghoapi.azureedge.net/api/MORT_MATERNALNUM?$filter=SpatialDim%20eq%20'KEN') | VERIFIED (API) |
| 3 | Annual rate of MMR reduction 2015 to 2023 | about **2.2% per year** (453 to 379); about **21% per year** needed to reach 70 by 2030 | Derived from #1 | COMPUTED |
| 4 | Share of reviewed Kenyan maternal deaths with sub-optimal care (CEMD) | **81.4% (2014) rising to 98.1% (2015/16)** | [Ameh, Godia, Ogutu, RCOG 2019 abstract](https://research.lstmed.ac.uk/en/publications/improving-the-quality-of-maternal-and-newborn-health-care-in-keny/) | Conference abstract; primary report not opened |
| 5 | Leading causes (CEMD 2015 to 2018) | Haemorrhage **38%**, hypertensive **19%**, non-obstetric **18%**; anaemia contributing in **53%** | [The Standard](https://www.standardmedia.co.ke/health/health-science/article/2001468321/bleeding-a-leading-cause-of-maternal-death-report) | **UNVERIFIED** (press summary of MOH/LSTM report) |
| 6 | Timing of death (CEMD 2015 to 2018) | **66%** postpartum; **61%** of those within 24 hours | Same | **UNVERIFIED** |
| 7 | ANC 4+ / ANC 8+ / first ANC in trimester 1 (KDHS 2022) | **66% / 4% / 29%** | [KDHS 2022 KIR](https://dhsprogram.com/pubs/pdf/PR143/PR143.pdf); [KDHS 2022 Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf) | VERIFIED (PDF) |
| 8 | Skilled birth attendance (KDHS 2022) | **89%** national; **53%** Turkana, **55%** Mandera, **57%** Wajir and Samburu | [KDHS 2022 KIR](https://dhsprogram.com/pubs/pdf/PR143/PR143.pdf) | VERIFIED (PDF) |
| 9 | Postnatal BP check | Only **35%** of mothers who had a postnatal check had BP measured | [KDHS 2022 Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf) | VERIFIED (PDF) |
| 10 | CHPs | about **107,800** paid, kitted (kit includes a **BP machine**) and given smartphones for eCHIS; stipend **KSh 5,000/month** split 50/50 national and county | [Amref](https://newsroom.amref.org/blog/2025/06/built-from-the-ground-up-how-107000-community-health-promoters-are-changing-the-face-of-health-care-in-kenya/); [The Standard 2024](https://www.standardmedia.co.ke/health/health-science/article/2001496277/seven-months-later-chp-programme-yet-to-fully-take-off); [KNA kit list](https://www.kenyanews.go.ke/nyeri-governor-flags-off-chp-kits/) | Mostly VERIFIED; stipend from press |

**Big picture.** Kenya has near-universal ANC contact (98%) and high skilled birth attendance (89%), yet MMR is around 379 and almost all reviewed deaths involve sub-standard care. The binding constraint is **quality and timeliness of recognition, referral and treatment** (Delays 1 and 3), not access to a first contact. This argues for tools that make the right action happen at the right time (deterministic triage, escalation, closed-loop referral, audit) and against another information-only app.

### 5.2 Global Burden

UN MMEIG "Trends in maternal mortality 2000 to 2023" (April 2025): [WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/maternal-mortality), [WHO report](https://www.who.int/publications/i/item/9789240108462), [UNFPA](https://www.unfpa.org/publications/trends-maternal-mortality-2000-2023), [UNICEF Data](https://data.unicef.org/resources/trends-in-maternal-mortality-2000-to-2023/).

| Fact | Value | Source |
|---|---|---|
| Maternal deaths, 2023 | **260,000** (about 712 per day) | WHO fact sheet |
| Global MMR | Fell **40%**, from 328 (2000) to **197** (2023) | WHO fact sheet; WHO report |
| Sub-Saharan Africa share | About **70%** of global deaths (about 182,000) | WHO fact sheet |
| WHO African Region MMR 2023 | **442** | [WHO GHO API](https://ghoapi.azureedge.net/api/MDG_0000000026?$filter=SpatialDim%20eq%20'KEN') (regional rows), VERIFIED |
| Stalled progress | Global MMR declined only about **1.5% per year since 2016** | UNICEF Data |
| Needed for SDG 3.1 | Nearly **15%** annual global reduction | WHO fact sheet |
| SDG 3.1 target | Global MMR below 70 by 2030, **no country above 140** | WHO fact sheet |
| Where | About 92% of deaths in low and lower-middle income countries; most preventable | WHO fact sheet |

### 5.3 Kenya: National Burden

| Year | MMR (per 100,000) | Maternal deaths | Source |
|---|---|---|---|
| 2000 | 445.1 | | [WHO GHO API](https://ghoapi.azureedge.net/api/MDG_0000000026?$filter=SpatialDim%20eq%20'KEN') |
| 2015 | 453.4 | 6,599 | [WHO GHO API](https://ghoapi.azureedge.net/api/MORT_MATERNALNUM?$filter=SpatialDim%20eq%20'KEN') |
| 2020 | 421.2 | | WHO GHO API |
| **2023** | **378.8** (UI 267.0 to 546.8) | **5,682** (UI 4,006 to 8,202) | WHO GHO API (MMEIG 2025 round, dated 10 April 2025), VERIFIED |

Business Daily reported the same headline (445 to 379) and said Kenya is "off track"; it reports MMEIG annual reductions of about 0% (2000 to 2015) and about 2% (2016 to 2023). [Business Daily](https://www.businessdailyafrica.com/bd/corporate/health/un-says-kenya-off-track-to-meet-maternal-mortality-target-4998378)

**Trajectory (COMPUTED from the GHO values):**
- Annual reduction 2015 to 2023: `1 - (378.8 / 453.4)^(1/8)` = **2.2% per year**.
- At that rate, MMR in 2030 = 378.8 × (1 - 0.022)^7 = **about 324**.
- Reaching 70 by 2030 needs `1 - (70 / 378.8)^(1/7)` = **about 21% per year**.
- Even the "no country above 140" floor needs about **13% per year**.
- Implied live births: 5,682 / 378.8 × 100,000 = **about 1.5 million births per year** (use for sizing).

> **CONFLICT: World Bank WDI vs MMEIG (UNVERIFIED, unresolved).** The [World Bank WDI API](https://api.worldbank.org/v2/country/KEN/indicator/SH.STA.MMRT?format=json) (last updated 13 July 2026) gives Kenya MMR **149** (2023), **2,200** deaths, a lifetime risk of 1 in 209, and **206** for 2000. These do not match the WHO GHO figures from the published MMEIG 2000 to 2023 round (379 and 5,682). We found no published MMEIG revision that explains the WDI series; some aggregator sites repeat 149. **Use 379 / about 5,700 (MMEIG via WHO GHO) and cite it as such. Treat 149 as unexplained until a newer MMEIG report is located.**

**Other Kenyan MMR figures you will see (none interchangeable with MMEIG):**

| Figure | What it is | Source | Status |
|---|---|---|---|
| 355 | 2019 Census household-deaths module; county range 67 (Nyeri) to 641 (Garissa) | [KNBS 2019 KPHC Analytical Report](https://new.knbs.or.ke/wp-content/uploads/2023/09/2019-Kenya-population-and-Housing-Census-Analytical-Report-on-Population-Dynamics.pdf) | **UNVERIFIED** (search summary; PDF table not opened) |
| 355 and "5,000 mothers lost annually" | MOH's Dr Amoth at IMNHC 2026 | [The Standard](https://www.standardmedia.co.ke/business/health-science/article/2001543638/amoth-how-kenya-loses-5000-mothers-to-preventable-childbirth-failures) | Press |
| 342 | Used in press coverage of the CEMD 2015 to 2018 | [The Standard](https://www.standardmedia.co.ke/health/health-science/article/2001468321/bleeding-a-leading-cause-of-maternal-death-report) | **UNVERIFIED** |
| 594 | CS Duale, September 2025, attributed to a "2024 USAID report" | [The Star](https://www.the-star.co.ke/news/2025-09-28-duale-no-woman-should-die-giving-life) | **UNVERIFIED; source unclear; do not use** |
| 99 (2022) | Institutional (facility) MMR from KHIS; declined 2011 to 2018, then stagnated; covers only facility deaths | [Muthee et al., BMC Pregnancy Childbirth 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12427102) | Peer reviewed |
| 2,851 (FY2024/25) and 2,656 (FY2025/26), a 6.8% fall; neonatal deaths 6,909 to 5,777 | KHIS facility-notified counts | [Daily Nation](https://nation.africa/kenya/health/maternal-deaths-drop-by-6-8pc-but-home-births-surge-as-sha-replaces-linda-mama-5553740) | **UNVERIFIED** (paywalled; search summary) |

The KHIS counts are about half of the modelled 5,700. That gap is itself evidence of under-notification of community deaths.

### 5.4 County Hotspots

- **Facility-based MMR, 2019 to 2022 (KHIS)** ([Muthee 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12427102)): Garissa highest at **271**; Mombasa above 200; Kisumu, Isiolo and Tana River 150 to 200; Nairobi **132**; Nyamira, Elgeyo Marakwet and Nandi below 50. CS Duale (September 2025) named **Siaya, Tana River, Garissa and Isiolo** as the four highest by facility data and said 20 counties have "persistently high" MMR ([The Star](https://www.the-star.co.ke/news/2025-09-28-duale-no-woman-should-die-giving-life)).
- **Population-based (2009 census, UNFPA/PSRI, published 2014):** Mandera **3,795**, Wajir 1,683, Turkana 1,594, Marsabit 1,127. Top ten: Mandera, Wajir, Turkana, Marsabit, Isiolo, Siaya, Lamu, Migori, Garissa, Taita Taveta ([UNFPA Kenya](https://kenya.unfpa.org/en/node/45574); [The Star 2017](https://www.the-star.co.ke/news/realtime/2017-06-20-how-to-reduce-maternal-deaths-in-the-worst-counties-to-give-birth-in)). **UNVERIFIED and dated**: small-sample census estimates with very wide uncertainty. The often-repeated claim that "15 counties contribute 98% of maternal deaths" comes from the same exercise and is implausible given that Nairobi and Nakuru have the largest absolute numbers. **Do not reuse it.**
- **Absolute numbers:** Nairobi, Nakuru and Kakamega record the most deaths ([Capital FM, ICRHK data, Aug 2026](https://capitalfm.africa/kenya-records-drop-in-skilled-birth-attendance-as-maternal-health-gaps-persist/)). Press analysis of KHIS put PPH deaths for January 2024 to October 2025 at Nairobi 98, Nakuru 97 and Garissa 84 ([Kenyans.co.ke](https://www.kenyans.co.ke/news/120705-nairobi-tops-list-counties-highest-childbirth-deaths)) (**UNVERIFIED**, press). Design implication: arid and semi-arid (ASAL) counties have the highest *risk*; large urban and peri-urban counties have the most *deaths*.
- **Nairobi informal settlements:** MMR **706** per 100,000 (Korogocho and Viwandani, 2003 to 2005, NUHDSS verbal autopsy); leading causes abortion complications, haemorrhage, sepsis, eclampsia, ruptured uterus ([Ziraba et al., Reprod Health 2009](https://doaj.org/article/f412d783c0234a75b70fa2fae701805f)). Old, but still the best population estimate for slums.

**Service coverage gaps by county (KDHS 2022 Key Indicators Report, VERIFIED)** ([PR143](https://dhsprogram.com/pubs/pdf/PR143/PR143.pdf)):

| County | ANC 4+ | Skilled birth | Facility birth | PNC check in first 2 days |
|---|---|---|---|---|
| Garissa | 31.2% | 68.1% | 61.4% | 45.4% |
| Wajir | 44.9% | 56.6% | 53.6% | 37.0% |
| Mandera | 40.4% | 54.7% | 50.4% | 45.7% |
| Marsabit | 67.1% | 68.7% | 59.3% | 40.6% |
| Turkana | 57.7% | 52.6% | 43.2% | 52.1% |
| West Pokot | 35.0% | 65.3% | 55.5% | 65.9% |
| Samburu | 56.3% | 56.6% | 49.1% | 54.1% |
| Tana River | 61.2% | 59.2% | 51.1% | 59.4% |
| Narok | 55.3% | 70.1% | 64.2% | 65.6% |
| Nairobi | 80.5% | 99.4% | 93.4% | 80.1% |
| **Kenya** | **66.0%** | **89.3%** | **82.3%** | **72.5%** |

Home births are most common in Mandera (50%), Tana River (48%), Turkana (47%), Wajir (46%) and Samburu (45%) ([KDHS 2022 Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf)).

**Why the video is set in Kilifi.** build.md's demo uses a synthetic mother in Kilifi County during the OND 2026 El Niño rains, with Mtwapa Health Centre and Coast General as fictional referral points. This is a narrative choice (coastal county, flood risk, CHP offline), not a claim about Kilifi's MMR.

### 5.5 Neonatal And Stillbirth Linkage

- Neonatal mortality: **21 per 1,000** (KDHS 2022; 22 in 2014), stalled ([KDHS Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf)). UN IGME via WDI: 21.1 (2023) and 20.7 (2024) ([World Bank API](https://api.worldbank.org/v2/country/KEN/indicator/SH.DYN.NMRT?format=json)).
- Stillbirth rate: **16.3 per 1,000 total births in 2023** (UI 15.3 to 17.4; 19.0 in 2020) ([WHO GHO API](https://ghoapi.azureedge.net/api/WHOSIS_000014?$filter=SpatialDim%20eq%20'KEN'), VERIFIED). Globally 1.9 million stillbirths in 2023, rate 14.3 per 1,000 ([UN IGME](https://data.unicef.org/resources/standing-up-for-stillbirth-report/)).
- Shared causes (hypertension, haemorrhage, obstructed labour, infection). CRADLE-5 found **newborn survival improved where referral worked** even though maternal deaths did not fall ([KCL](https://www.kcl.ac.uk/news/use-of-blood-pressure-and-pulse-monitoring-device-shows-promise-for-maternal-health-in-sierra-leone)). CLIP reduced stillbirths (OR 0.89) without reducing maternal deaths ([CLIP](https://scholars.aku.edu/en/publications/the-community-level-interventions-for-pre-eclampsia-clip-cluster-/)). **Evaluation implication:** measure perinatal outcomes too; they are more frequent and give statistical power that maternal deaths cannot.

### 5.6 Causes: Global

WHO systematic analysis 2009 to 2020 ([Cresswell et al., Lancet Glob Health 2025](https://pubmed.ncbi.nlm.nih.gov/40064189/); [Oxford summary](https://www.demography.ox.ac.uk/news/global-update-reveals-haemorrhage-leading-cause-maternal-death); [WHO news 8 March 2025](https://www.who.int/news/item/08-03-2025-many-pregnancy-related-complications-going-undetected-and-untreated--who)), 139,381 deaths, 129 countries:

| Cause | 2009 to 2020 (Cresswell 2025) | 2003 to 2009 (Say 2014) |
|---|---|---|
| Haemorrhage | **27%** | 27.1% |
| Indirect causes | **23%** | above one quarter |
| Hypertensive disorders | **16%** | 14.0% |
| Abortion | **8%** | 7.9% |
| Embolism | **7%** | |
| Sepsis | **7%** | 10.7% |
| Other direct | **10%** | |

Say et al.: [DOAJ](https://doaj.org/article/9af5e06aeb694cf0b7baf2267a3ba4bf).

### 5.7 Kenya: Causes And Avoidable Factors (CEMD, "Saving Mothers' Lives")

Kenya runs a national Confidential Enquiry into Maternal Deaths (CEMD) through the MPDSR committee in the MOH Reproductive and Maternal Health Services Unit, with LSTM support ([GHDx 2017 record](https://ghdx.healthdata.org/node/541794); [GHDx 2015 to 2016 record](https://ghdx.healthdata.org/node/541795); [LSTM news](https://www.lstmed.ac.uk/node/9013)).

**First vs second CEMD** ([Ameh, Godia, Ogutu; RCOG World Congress 2019 abstract](https://research.lstmed.ac.uk/en/publications/improving-the-quality-of-maternal-and-newborn-health-care-in-keny/)):

| Measure | First CEMD (2014, referral hospitals) | Second CEMD (2015/16) |
|---|---|---|
| Deaths reviewed | **484** | **1,334** |
| Obstetric haemorrhage | 39.7% | 35.5% |
| Hypertensive disorders | 15.3% | 17.9% |
| Non-obstetric complications | 19.8% | 22.2% |
| **Sub-optimal care** | **81.4% (394)** | **98.1% (1,310)** |
| Delay in treatment (health worker avoidable factor) | 33% | 41.3% |
| Inadequate monitoring | 27% | 30.9% |
| Inadequate clinical skills | 28% | 29.1% |

The 2017 report launch summarised this as "9 out of 10 women who died received sub-standard care" ([LSTM news](https://www.lstmed.ac.uk/node/9013)). The top five direct causes in the 2017 report were haemorrhage, hypertension, sepsis, obstructed labour and post-abortion complications (**UNVERIFIED**, second-hand via the [Nation](https://nation.africa/kenya/health/maternal-deaths-drop-by-6-8pc-but-home-births-surge-as-sha-replaces-linda-mama-5553740)).

> **How to quote the "poor care" figure (important).** The landscape workstream quoted a Daily Nation Newsplex article saying Kenya's first Confidential Enquiry found that **92% of 484 maternal deaths received poor care and 81% substandard care**, that **72% of deaths happened outside working hours**, and that an obstetrician was involved in only **1 in 9** ([Nation Newsplex](https://nation.africa/kenya/newsplex/most-maternal-deaths-occur-out-of-office-hours-says-study-17060)). We do **not** use the 92% figure in the pitch, the product or the video, for three reasons:
> 1. The Nation article is a press summary we could not open in full, and it uses two categories ("poor care" and "substandard care") that do not map cleanly onto the CEMD's own reporting.
> 2. The LSTM-hosted RCOG 2019 abstract by the CEMD authors themselves (Ameh, Godia, Ogutu) reports **sub-optimal care in 81.4% (394 of 484) of 2014 deaths and 98.1% (1,310 of 1,334) of 2015/16 deaths**. That abstract is the closest we have to the primary report (primary-adjacent), and its 81.4% for the same 484 deaths agrees with the Nation's "81% substandard".
> 3. The 2017 launch line "9 out of 10" is consistent with the abstract's range.
>
> **Rule:** cite "**81.4% (2014) to 98.1% (2015/16) of reviewed maternal deaths involved sub-optimal care**" with the LSTM abstract URL. If the out-of-hours finding is used, label it as press-reported. Note also that the Jev idea-scoring prompt (section 7.4) contained the 92% phrasing; that does not change any number we publish.

**CEMD covering 2015 to 2018 (MOH with LSTM; Standard, about 2021)** ([The Standard](https://www.standardmedia.co.ke/health/health-science/article/2001468321/bleeding-a-leading-cause-of-maternal-death-report)), all **UNVERIFIED** (primary PDF not obtained):

| Measure | Value |
|---|---|
| KHIS-notified maternal deaths | 4,295; 2,361 (55%) in review scope |
| Causes | Haemorrhage **38% (897)**, hypertensive **19% (442)**, non-obstetric **18% (423)**, other obstetric 6% |
| Contributing conditions | **Anaemia 53.2%**, HIV 14.6%, cardiac disease 8.3%, malaria 6.7%, TB 4.7% |
| Timing | **66% postpartum**; **61% of postpartum deaths within 24 hours**; 21% between 48 hours and 2 weeks |
| Delays (overlapping) | **75% delayed arriving at a facility**; **72% delayed decision-making** |
| System gaps | Missing skilled attendants, equipment, laboratory and blood bank services, emergency transport |

**Share judged preventable.** We found **no Kenyan CEMD figure that states a single "% preventable"**. The closest proxy is the sub-optimal care proportion (81 to 98%). The widely quoted "**62.4% preventable (613 of 982)**" is from **South Africa's** Saving Mothers 2017 to 2019 report, not Kenya's. **Do not attribute it to Kenya.**

### 5.8 Unsafe Abortion And Anaemia

- **Unsafe abortion:** an estimated **464,000 induced abortions** in Kenya in 2012 (48 per 1,000 women aged 15 to 49); about **120,000 women** received facility care for complications, more than three quarters moderate or severe ([Mohamed et al., BMC Pregnancy Childbirth 2015](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4546129/)). In the 2018 national near-miss study, abortive outcomes were **12% of deaths and 9% of near-misses** ([Owolabi et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7495416/)). A claim of "about 2,600 abortion deaths per year" appears online; it is implausible against 5,700 total deaths (**UNVERIFIED; do not use**).
- **Anaemia:** WHO modelled prevalence in pregnant women in Kenya **40.3%** (2019; UI 25.8 to 52.0), 2.0% severe ([WHO GHO API](https://ghoapi.azureedge.net/api/NUTRITION_ANAEMIA_PREGNANT_PREV?$filter=SpatialDim%20eq%20'KEN')). A contributing condition in 53% of CEMD deaths (**UNVERIFIED**). Anaemia increases the lethality of PPH. KDHS 2022 did not report haemoglobin testing in its summary.
- **Hb trajectory and PPH:** a rapid Hb decline was associated with 2.36 times the odds of PPH ([IJWH](https://www.dovepress.com/hemoglobin-trajectory-during-pregnancy-and-postpartum-hemorrhage-a-ret-peer-reviewed-fulltext-article-IJWH)); severe anaemia carries 7 times the risk of death or life-threatening bleeding ([LSHTM](https://www.lshtm.ac.uk/node/383046)). **Constraint:** CHP kits have no Hb meter, so Hb evidence lives on the facility side.

### 5.9 The Three Delays: Kenyan Evidence

| Delay | Kenyan evidence |
|---|---|
| **1. Deciding to seek care** (recognising danger signs, household decision, cost, trust) | 72% of CEMD 2015 to 2018 deaths involved delayed decision-making ([Standard](https://www.standardmedia.co.ke/health/health-science/article/2001468321/bleeding-a-leading-cause-of-maternal-death-report), **UNVERIFIED**). ICRHK (2026) attributed **30%** of deaths to this delay ([Capital FM](https://capitalfm.africa/kenya-records-drop-in-skilled-birth-attendance-as-maternal-health-gaps-persist/), **UNVERIFIED**). KDHS 2022: telling mothers how to recognise newborn danger signs was the *least* performed postnatal function (64%); only 33% discussed vaginal bleeding at PNC ([KDHS Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf)). In PROMPTS, SMS raised antenatal danger-sign knowledge by only 3.6 percentage points, and the danger-sign care-seeking index was not significant (0.04 SD, p=0.096) ([PROMPTS](https://pmc.ncbi.nlm.nih.gov/articles/PMC11835334/)). Skilled birth attendance fell from 69.8% (April to June 2025) to 65.5% (January to March 2026) in routine data during the Linda Mama to SHA transition, with reports of rising home births ([Capital FM](https://capitalfm.africa/kenya-records-drop-in-skilled-birth-attendance-as-maternal-health-gaps-persist/); [Nation](https://nation.africa/kenya/health/maternal-deaths-drop-by-6-8pc-but-home-births-surge-as-sha-replaces-linda-mama-5553740); **UNVERIFIED**, press) |
| **2. Reaching care** (transport, distance, referral between facilities) | 75% of CEMD deaths involved delayed arrival (**UNVERIFIED**). ICRHK reported **25%** (**UNVERIFIED**). National near-miss study (54 referral hospitals, 2018): **64% of severe maternal outcomes were already present on arrival**, and **58% of those were referred from lower facilities** ([Owolabi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7495416/)). AFCAP/Transaid work in Kenya found ambulances and emergency transport schemes carried just over 10% of referrals; most women came by motorbike or other vehicle ([Transaid/AFCAP](https://www.transaid.org/wp-content/uploads/2015/09/AFCAP-Linking-Rural-Communities-to-Health-Services.pdf)) |
| **3. Receiving adequate care** (skills, drugs, blood, monitoring) | Sub-optimal care in 81 to 98% of deaths; treatment delay 41%, inadequate monitoring 31%, inadequate skills 29% ([LSTM abstract](https://research.lstmed.ac.uk/en/publications/improving-the-quality-of-maternal-and-newborn-health-care-in-keny/)). Near-miss study: only **77%** of women with severe pre-eclampsia or eclampsia got **magnesium sulphate**; only **67%** with APH who needed blood got it; only **44%** with ruptured uterus had laparotomy within 3 hours ([Owolabi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7495416/)). ICRHK: **45%** of deaths happened after arrival because of inadequate or untimely care; shortages of magnesium sulphate (48% of facilities), benzyl penicillin (47%) and oxytocin (40%) ([Capital FM](https://capitalfm.africa/kenya-records-drop-in-skilled-birth-attendance-as-maternal-health-gaps-persist/); **UNVERIFIED**: press, and unclear whether these are "lacking" or "stocked" rates). Only about 50% of facilities were adequately equipped for maternal and newborn emergencies ([Business Daily](https://www.businessdailyafrica.com/bd/corporate/health/un-says-kenya-off-track-to-meet-maternal-mortality-target-4998378)). Only 35% of mothers had BP checked at their postnatal check ([KDHS Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf)) |

**Takeaway.** In Kenya, Delay 3 is at least as large as Delays 1 and 2. A tool aimed only at mothers' knowledge (Delay 1) hits the part with the weakest trial evidence (the PROMPTS danger-sign index was null). A tool that supports the **CHP to facility to referral chain** and **in-facility recognition** targets the places where the CEMD says women died. Mizani's two-witness handoff sits exactly at the Delay 2 to Delay 3 boundary.

### 5.10 The 2018 National Near-Miss Study (Key Source For The Handoff)

[Owolabi OO et al., Incidence of maternal near-miss in Kenya in 2018: 54 referral hospitals, Sci Rep 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7495416/):

| Finding | Value | Why it matters to Mizani |
|---|---|---|
| Severe maternal outcomes present on arrival | **64%** | Women arrive already critical; the receiving clinician must act on the incoming evidence immediately |
| Of those, referred from lower facilities | **58%** | The referral note is the information bridge; it is usually poor (98.2% of maternity referral forms incomplete in a Ghana audit, section 6.6) |
| Severe pre-eclampsia/eclampsia given MgSO4 | **77%** | Even at referral hospitals, the treatment that the recognition should trigger is missed in about 1 in 4 |
| APH needing blood that received it | **67%** | Downstream capacity limits what any alert can achieve |
| Ruptured uterus with laparotomy within 3 hours | **44%** | Same |
| Abortive outcomes | 12% of deaths; 9% of near-misses | Scope note |

### 5.11 KDHS 2022 Coverage Indicators (VERIFIED)

Sources: [Key Indicators Report](https://dhsprogram.com/pubs/pdf/PR143/PR143.pdf), [Summary Report](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf), [KNBS page](https://www.knbs.or.ke/kenya-demographic-and-health-survey-kdhs-2022/).

| Indicator | Value | Breakdowns |
|---|---|---|
| ANC from a skilled provider | **97.9%** | |
| ANC 4+ | **66.0%** | Urban 74.1%, rural 61.5%; no education 49.1%; lowest wealth quintile 53.9% |
| ANC 8+ | **4%** | |
| First ANC in first trimester | **29%** | |
| Iron during pregnancy | 90.2% | |
| Tetanus protection | 75% | |
| Skilled birth attendance | **89.3%** (41% in 2003) | Urban 97.3%, rural 84.8%, lowest quintile 69.3%, no education 54.6% |
| Facility birth | **82.3%** (KIR) vs **88%** (final Summary) | **CONFLICT:** the KIR is preliminary; prefer 88% and note the discrepancy |
| Caesarean section | 17% | |
| PNC for the mother within 2 days | **72.5%** (KIR) or **78%** (Summary) | 20% had no PNC within 41 days |
| BP measured at postnatal check | **35%** | Only **25%** received all three key checks (BP, bleeding discussion, FP) |
| Teen pregnancy (ever pregnant, 15 to 19) | 15% | From **50% in Samburu** to 5% in Nyeri and Nyandarua |
| TFR | 3.4 | |
| Literacy (15 to 49) | Women 91%, men 94%; 6% of women have no education | |
| Women's phones | **78% own a mobile phone; 43% own a smartphone**; 44% used the internet in the past 12 months | |
| Rural household electricity | 36% | |

### 5.12 Community Health Promoters (CHPs)

| Fact | Value | Source | Status |
|---|---|---|---|
| Number professionalised | More than **107,000** "trained, digitised, equipped, and remunerated" | [Amref, June 2025](https://newsroom.amref.org/blog/2025/06/built-from-the-ground-up-how-107000-community-health-promoters-are-changing-the-face-of-health-care-in-kenya/) | Press release |
| MOH-supported CHPs | **107,831**, each covering about **100 households** | [The Standard 2024](https://www.standardmedia.co.ke/health/health-science/article/2001496277/seven-months-later-chp-programme-yet-to-fully-take-off) | Press |
| Alternate count | About **95k CHPs** on eCHIS in 47 counties | [Medic](https://medic.org/stories/medic-partners-with-kenyan-government-to-transform-community-health/) | **CONFLICT** (definition likely "active eCHIS users"; prefer about 107,800 for the cadre) |
| Stipend | KSh 2,500 national + KSh 2,500 county = **KSh 5,000 per month** | The Standard 2024 | Press |
| Payment problems | Mid-2024: 20 counties not paying. By July 2024, 45 of 47 counties had received May 2024 payments (Mombasa and Mandera not on the system). 2024/25: Treasury allocated KSh 2.5 bn against KSh 3.2 bn requested. Sept 2025: the President criticised counties over unpaid CHPs. Dec 2025: plan for **permanent and pensionable** terms. Up to 13-month stipend delays reported at the Coast | [The Standard 2024](https://www.standardmedia.co.ke/health/health-science/article/2001496277/seven-months-later-chp-programme-yet-to-fully-take-off); [The Standard July 2024](https://www.standardmedia.co.ke/health/health-science/article/2001498549/health-ministry-rolls-out-electronic-system-to-boost-services); [The Star](https://www.the-star.co.ke/news/2025-09-04-ruto-slams-counties-over-unpaid-health-promoters); [Capital FM](https://capitalfm.africa/community-health-promoters-to-get-permanent-pensionable-jobs-ruto/); [The Standard Coast](https://www.thestandard.ke/business/amp/coast/article/2001519721/over-1400-chps-protest-over-13-month-stipend-delay) | **UNVERIFIED** (press) for the later items |
| Kit contents (Nyeri, Oct 2023) | Salter scale, backpack, reflector jacket, MUAC tapes (adult and child), digital thermometer, **glucometer** with lancets and 50 strips, **BP machine**, CHP badge, weighing scale, **timer** (respiratory rate), torch, water bottle, medicine book, waste bag, sharps container, first aid box. CHPs "screen for hypertension and blood sugar at the household level" and refer | [KNA](https://www.kenyanews.go.ke/nyeri-governor-flags-off-chp-kits/); [Deputy President speech](https://deputypresident.go.ke/sites/default/files/2024-05/Community%20Health%20Stipends%20Speech%20Formatted.pdf) | VERIFIED (list) |
| Kit gaps | **No Hb meter** and no urine dipstick in the list. No evidence that the kit BP device is **validated for pregnancy or pre-eclampsia**; many automated cuffs under-read in pre-eclampsia; CRADLE VSA is one of the few validated | KNA; [CRADLE feasibility](https://pmc.ncbi.nlm.nih.gov/articles/PMC5924508/) | **UNVERIFIED** (device model) |
| Legal basis | Primary Health Care Act 2023: CHPs selected by the community and appointed by the county; over 18; resident at least 5 years; "literate and can read and write in at least one of the national languages and the local language"; sets up Primary Care Networks and community health units; assented 19 October 2023; commenced 2 November 2023 | [PHC Act 2023 (No. 13)](https://new.kenyalaw.org/akn/ke/act/2023/13/eng@2023-11-24) | VERIFIED |
| Devices | July 2026: the President acknowledged "ageing and malfunctioning phones" and promised new smartphones | [People Daily](https://peopledaily.digital/news/ruto-promises-new-smartphones-and-stipend-increase-for-community-health-promoters) ([amp](https://peopledaily.digital/news/ruto-promises-new-smartphones-and-stipend-increase-for-community-health-promoters/amp)) | **UNVERIFIED** (press) |

**Design consequence.** The community witness can produce BP (with a timer for repeats), temperature, glucose and symptoms, but not Hb or urine protein. Evidence is genuinely split across sites, which is why reconciliation is needed.

### 5.13 eCHIS (Electronic Community Health Information System)

| Fact | Value | Source |
|---|---|---|
| Scale-up | Started 2023; **110,000 smartphones** to CHPs in 47 counties; **more than 100,000 CHPs** using it by 2 July 2024 | [The Standard July 2024](https://www.standardmedia.co.ke/health/health-science/article/2001498549/health-ministry-rolls-out-electronic-system-to-boost-services) |
| Volume (July 2024) | **6.9 million households** registered (target 12.5 million); **161,000 pregnant women identified, 63,500 referred** | Same |
| Rollout gaps | In 2024, Vihiga, Tana River, Marsabit, Mandera and Garissa had not rolled out; by mid-2025 all counties had | The Standard 2024; [Muriithi et al. 2026](https://chwcentral.org/wp-content/uploads/Implementation-Process-and-Acceptability-of-the-electronic-Community-Health-Information-System-among-Community-Health-Workers-in-Kenya.pdf) |
| Adoption problems | Muriithi et al., Front Health Serv June 2026 (310 CHWs, 5 counties): inadequate training, finance, and technical and management support; some CHPs reverted to paper; in Migori, adoption odds differed 14-fold between two sub-counties; unreliable power, network problems, app logouts and loading errors | Muriithi et al. 2026 |
| Platform | Built on the open-source **Community Health Toolkit (CHT, Medic)**, offline-first; Medic sits on MOH's eCHIS technical committee; CHV-NEO neonatal direct-to-client study layered on eCHIS in Siaya and Kisumu | [Medic Q2 2024](https://medic.org/q2-2024-impact-report/) |
| Referrals | 74k referrals (Machakos generative AI lessons) | [Amref Machakos](https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/) |
| Closed loop | June 2026: closed-loop eCHIS to TaifaCare HMIS referral with outcome notification back to the CHP presented | [Medic Community Roundup listing](https://unjobs.org/channels/TCrYgB812EXuz7Y0yLTGGNsXLi03/GPHorre4g-0) |
| Data quality | No entry validation and no change-tracking; CHPs "still rely on manual judgment"; connectivity gaps force a return to paper | [Amref Machakos](https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/) |

**Implication.** Do not build a parallel CHP app. Position Mizani as a **reasoning service beside eCHIS/CHT** (FHIR in, proof out), or target a user group eCHIS does not serve well (facility nurses at Levels 2 and 3). The hackathon UI is a demonstration surface, not a proposed replacement.

### 5.14 Laws And Financing Context

| Instrument | What matters | Source |
|---|---|---|
| Primary Health Care Act 2023 (No. 13) | PCNs, community health units, CHP roles | [Kenya Law](https://new.kenyalaw.org/akn/ke/act/2023/13/eng@2023-11-24) |
| Facilities Improvement Financing Act 2023 (No. 14) | Facility revenue retention, Levels 1 to 5 | [Kenya Law](https://new.kenyalaw.org/akn/ke/act/2023/14/eng@2023-11-24) |
| Digital Health Act 2023 (No. 15) | See section 5.20 | [Kenya Law](https://new.kenyalaw.org/akn/ke/act/2023/15/eng@2023-11-24) |
| Social Health Authority (SHA) | Replaced NHIF from October 2024. Linda Mama folded in, then rebranded **Linda Jamii**; reported rates **KSh 10,000 normal delivery, KSh 30,000 caesarean** (previously 2,500 and 5,000), covering ANC, delivery, up to six PNC visits and anti-D (**UNVERIFIED**, press). RUPHA survey (24 to 31 Dec 2024): **58%** of facilities had received no SHA payment for Q4 2024 claims. Governors raised SHA payment problems again in Jan 2026 | [People Daily](https://peopledaily.digital/news/duale-announces-transition-from-linda-mama-to-linda-jamii-for-maternal-care/amp); [Kenyans.co.ke](https://www.kenyans.co.ke/news/113366-duale-lauds-expanded-linda-jamii-cover-full-maternity-care-and-family-benefits); [Citizen Digital](https://citizen.digital/news/majority-of-health-facilities-unpaid-for-sha-claims-rupha-survey-reveals-n355378); [The Star](https://www.the-star.co.ke/news/2026-01-21-governors-raise-alarm-over-sha-challenges) |
| Primary Care Networks | Hub (sub-county hospital team) and spoke (dispensaries and health centres linked to community units); target **315** (one per sub-county); **221** by Feb 2025 and **228** by Jan 2026; Amref cited 74 "operationalised" in June 2025 (definitions differ) | [KEMRI-Wellcome](https://kemri-wellcome.org/policy-briefs/examining-the-implementation-experience-of-primary-care-networks-in-kenya-2); [KNA Jan 2026](https://www.kenyanews.go.ke/?p=167549); [Amref](https://newsroom.amref.org/blog/2025/06/built-from-the-ground-up-how-107000-community-health-promoters-are-changing-the-face-of-health-care-in-kenya/) |

### 5.15 Referral System And MOH 100

- The Kenya Health Sector Referral Strategy and Implementation Guidelines (2014) set six levels of care, with the community as Level 1 ([MEASURE Evaluation PIMA](https://measureevaluation.cpc.unc.edu/pima/meval-pima-news/referral-system-building-in-kenya.html)).
- The **MOH 100 Community Referral Form** has free-text "reason for referral / treatment given / comments" and a **"referral back to the community"** section: the designed feedback loop, often not completed ([MOH 100 form](https://tciurbanhealth.org/wp-content/uploads/2018/04/Community-Referral-form-MOH-100.pdf)).
- Weaknesses: late referral, little transport (section 5.9), arrival already critical (64%). Facility-level maternal mortality is highest in referral hubs (Garissa, Mombasa, Kisumu) because they receive late referrals ([Muthee 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12427102)).
- **Mizani mapping.** The contestable referral proof is designed to fill MOH 100's "reason for referral" and "treatment given" fields with structured, sourced premises, and to give the back-referral a reason to be completed (the facility's reconciled decision returns to the CHP).

### 5.16 MCH Booklet Danger Signs (MOH Mother And Child Health Handbook, 2020)

Source: [MOH MCH Handbook 2020](https://www.kenyapaediatric.org/ecd/wp-content/uploads/2021/04/Mother-Child-Health-Handbook-MOH-NEW-LAYOUT-10th-Sep-2020.pdf).

| Period | Danger signs |
|---|---|
| During pregnancy | Severe headache; vaginal bleeding; pallor ("pale"); fever; severe abdominal pain; swelling of face and hands; **reduced or no movement of the unborn baby**; breaking of water; convulsions or fits. Guidance: "seek skilled care at the health facility." |
| Mother after childbirth | Heavy bleeding; fever; severe headache; foul-smelling vaginal discharge; fits or convulsions |
| Baby | Stops breastfeeding well; difficult or fast breathing; feels hot or unusually cold; further signs in the booklet |

The booklet records blood loss in mL and checkboxes for pre-eclampsia, eclampsia, PPH and obstructed labour. PNC visits at **48 hours, 1 to 2 weeks, 4 to 6 weeks and 4 to 6 months**. These fields are a natural structured data source.

**Difference from WHO DAK.** The booklet treats facial and hand swelling as a danger sign. The WHO DAK treats oedema without other findings as a physiological symptom for counselling and checks for thrombosis if there is leg pain or redness (ANC.DT.03). Kenya-facing messaging should follow the national booklet, with clinical decision logic that pairs oedema with BP. (Jev definitions in section 8 encode "feet-only swelling is not face/hand swelling".)

### 5.17 Clinical Thresholds That Are Safe To Encode

**Principle.** Encode **published, deterministic thresholds** with their citations, show the rule that fired, and always escalate to a human. Use language models only for language. A language model must never invent a threshold or a dose.

#### 5.17.1 Machine-Readable Source: WHO SMART Guidelines ANC Digital Adaptation Kit

The WHO ANC DAK ([WHO 2021](https://www.who.int/publications/i/item/9789240020306)) is published as FHIR PlanDefinitions and CQL at [WorldHealthOrganization/smart-anc](https://github.com/WorldHealthOrganization/smart-anc) (`bundles/plandefinition/ANCDT01` to `ANCDT28`, [listing](https://github.com/WorldHealthOrganization/smart-anc/tree/master/bundles/plandefinition); CQL in [input/cql](https://github.com/WorldHealthOrganization/smart-anc/tree/master/input/cql); example [ANCDT17 JSON](https://raw.githubusercontent.com/WorldHealthOrganization/smart-anc/master/bundles/plandefinition/ANCDT17/ANCDT17-files/plandefinition-ANCDT17.json)); implementation guide: [SMART ANC IG](https://build.fhir.org/ig/costateixeira/smart-anc/documentation.html). Logic was extracted directly (VERIFIED). Tables include DT.01 danger signs; DT.04 repeat measurements; DT.06 exam results requiring referral; DT.12 urine testing; DT.17 pre-eclampsia, severe pre-eclampsia and hypertension; DT.25 anaemia and IFA; DT.26 calcium and vitamin A; DT.27 pre-eclampsia risk (aspirin); plus HIV, syphilis, hepatitis, TB, GDM, ASB, ultrasound and counselling.

| Table | Logic (as extracted) |
|---|---|
| **ANC.DT.01 Danger signs** (Quick Check before every contact; any one means refer urgently to hospital) | Central cyanosis; bleeding vaginally; convulsing; fever; severe headache; visual disturbance; imminent delivery; labour; looks very ill; severe vomiting; severe pain; severe abdominal pain; unconscious |
| **ANC.DT.04 Repeat measurements** | SBP ≥140 or DBP ≥90: **re-measure after 10 to 15 minutes rest**. Temperature ≥38°C: re-measure. Pulse <60 or >100: re-check after 10 minutes rest. FHR <100 or >180: re-measure. Any abnormal respiratory finding: oximetry |
| **ANC.DT.06 Referral from exam results** | Two temperatures ≥38°C: investigate, refer urgently if treatment unavailable. Second pulse <60 or >100: refer. Abnormal respiratory exam or **SpO2 <92%**: refer urgently. Abnormal cardiac findings: refer urgently. Amniotic fluid at <37 weeks: refer urgently. No fetal heartbeat at ≥20 weeks: refer. Persistent abnormal FHR at ≥20 weeks: refer |
| **ANC.DT.12 Urine testing** | Urine dipstick for protein if the **repeat** SBP ≥140 or repeat DBP ≥90 |
| **ANC.DT.17 Hypertension and pre-eclampsia** (both readings must meet the threshold) | **Refer urgently:** repeat BP ≥140/90 **plus any severe symptom** (severe headache, blurred vision, epigastric pain, dizziness, vomiting). **Refer urgently:** repeat BP ≥140/90 **plus proteinuria ++ or more**. **Refer urgently:** repeat **SBP ≥160 or DBP ≥110** regardless of protein (severe hypertension). **Hypertension counselling:** BP 140 to 159 / 90 to 109 with protein none or + (gestational or chronic hypertension), or known chronic hypertension |
| **ANC.DT.25 Anaemia** (matches WHO 2024 cut-offs) | **Hb <110 g/L in trimester 1 (≤12 weeks) or trimester 3 (≥28 weeks), or <105 g/L at 13 to 27 weeks, or pallor when no Hb test is available:** anaemia; counsel and give **120 mg elemental iron + 0.4 mg folic acid daily**. Otherwise 60 mg iron (or 30 to 60 mg) + 0.4 mg folic acid daily depending on population prevalence; Kenya's prevalence is about 40%, so the ≥40% branch applies |
| **ANC.DT.27 Pre-eclampsia risk** | Risk factors: multiple pregnancy; previous pre-eclampsia, eclampsia or convulsions; autoimmune disease; diabetes; chronic hypertension; kidney disease. From **12 weeks**: **aspirin 75 mg daily until delivery**, and in low-calcium-intake populations **calcium 1.5 to 2 g/day**. A CHP tool can *flag eligibility for clinician review*; it should not prescribe |

> **CQL caution (VERIFIED).** The published CQL contains apparent transcription errors: one clause pairs "SBP ≤140 with ++ protein" with urgent referral, and one has "90 mmHg" labelled as "Repeat diastolic". **Re-derive from the narrative DAK and WHO recommendations; do not copy the JSON blindly. Unit-test every branch.**

**Cross-contact logic in SMART ANC (VERIFIED by grepping `ANCContactDataElements.cql`).** Thresholds are almost entirely per contact. Cross-contact items are limited to "symptoms persist since last contact" and "weight gain since last contact". This is the gap Mizani's memory fills (section 6.7).

**WHO 2016 ANC model:** **at least 8 contacts**, at ≤12, 20, 26, 30, 34, 36, 38 and 40 weeks (return at 41 if undelivered) ([Tunçalp et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5487083/); [schedule briefer](https://www.mcsprogram.org/wp-content/uploads/2018/03/ANC-OverviewBriefer-A4-1.pdf)). Kenya's ANC8 is about 4%.

#### 5.17.2 Hypertension: Cross-Check And Timing

| Item | Threshold or definition | Source |
|---|---|---|
| Hypertension | ≥140/90 on repeat | WHO DAK; [NICE NG133](https://www.nice.org.uk/guidance/ng133); CRADLE VSA |
| Severe hypertension | ≥160/110 | Same |
| Proteinuria (NICE) | uPCR ≥30 mg/mmol or uACR ≥8 mg/mmol, or ≥300 mg per 24 hours; in Kenyan primary care the dipstick is what's available, and ++ or more is the WHO DAK trigger | NICE NG133; WHO DAK |
| Pre-eclampsia (NICE) | Hypertension after 20 weeks plus proteinuria **or** maternal organ or uteroplacental dysfunction | NICE NG133 |
| Severe hypertension care | Assess promptly; monitor BP frequently | [NICE QS35 statement 4](https://www.nice.org.uk/guidance/QS35/chapter/quality-statement-4-assessing-women-with-severe-hypertension-in-pregnancy) |
| **ISSHP onset timing** | **Chronic hypertension: before 20 weeks. Gestational hypertension: new onset at or after 20 weeks.** A single-visit checklist cannot make this distinction without history | [ISSHP summary](https://pmc.ncbi.nlm.nih.gov/articles/PMC11588921/) |
| Visit-to-visit BP variability | In CLIP (17,770 pregnancies, BP measured by CHWs), BP level and variability predicted adverse outcomes; systolic SD OR 2.09 for hypertension | [Magee et al., Hypertension 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8284372/) |
| **Caution on "rising BP"** | A rise of 30/15 mmHg while still under 140/90 did **not** predict adverse outcome | [Brown et al. 1999](https://read.qxmd.com/read/10453825/evaluation-of-a-definition-of-pre-eclampsia) |
| BP trajectory research | Women who develop pre-eclampsia have higher baseline BP and a steeper rise after the mid-trimester nadir; trajectory AUC 0.886 (training) and 0.802 (validation) in 7,923 Chinese women; research-grade, not validated in Kenya | [LSTM repository](https://research.lstmed.ac.uk/en/publications/parameterization-of-the-mid-trimester-drop-in-blood-pressure-traj-5/) |
| Weight gain and oedema | Gestational weight gain is associated with HDP, but oedema and weight gain are poor stand-alone predictors; do not alert on them alone | [PMC3807791](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3807791/); WHO DAK |
| Home vs clinic BP | Conflicting home and clinic BP is a recognised phenomenon (white-coat or masked effect) | [UCT GHI](https://journals.uct.ac.za/index.php/GHI/article/download/836/672) |

**What this means for Mizani's rules.** The longitudinal signal Mizani uses is **ISSHP onset timing** (a normal BP before 20 weeks in memory turns a raised BP at 34 weeks into new-onset hypertension, hence gestational hypertension or pre-eclampsia, not chronic), plus **persistence across witnesses** (repeated home reading and facility repeat revise each other). Mizani does **not** fire on "rising BP" below 140/90 alone (Brown 1999). See build.md rules `r_new_onset`, `r_chronic`, `r_pe`, `r_pe_severe`.

#### 5.17.3 Postpartum Haemorrhage And Shock Index

- **New WHO, FIGO and ICM definition (5 October 2025):** act when there is **objectively measured blood loss ≥300 mL with any abnormal haemodynamic sign (pulse >100, shock index >1, SBP <100 or DBP <60), or ≥500 mL**, whichever comes first, within 24 hours of birth, with particular vigilance in the first 2 hours. Treat immediately with the **MOTIVE bundle**: uterine **M**assage, **O**xytocics, **T**ranexamic acid, **I**V fluids, **V**aginal and genital tract examination, **E**scalation. 51 recommendations, based on a Lancet 2025 WHO individual-participant meta-analysis (more than 300,000 women, 23 countries). The older definition was ≥500 mL within 24 hours. ([WHO news](https://www.who.int/news/item/05-10-2025-global-health-agencies-issue-new-recommendations-to-help-end-deaths-from-postpartum-haemorrhage); [FIGO](https://www.figo.org/press-releases/global-health-agencies-issue-new-recommendations-help-end-deaths-postpartum-haemorrhage))
- **Shock index (SI = HR / SBP):**

| Source | Thresholds |
|---|---|
| [Nathan et al., BJOG 2015](https://safemotherhood.ucsf.edu/sites/g/files/tkssra10096/f/wysiwyg/Shock-index-an-effective-predictor-of-outcome-in-postpartum-haemorrhage-.pdf) (PPH ≥1500 mL) | SI <0.9 reassuring; SI ≥1.7 needs urgent attention; SI matched or outperformed conventional vital signs for ICU admission and other outcomes |
| [El Ayadi et al., PLoS One 2016](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4762936/) (958 women with hypovolaemic shock, low-resource settings) | SI **≥0.9 refer**; **≥1.4 urgent intervention at a tertiary facility**; **≥1.7 high risk of adverse outcome** |
| [Nathan et al., AOGS 2019](https://scholar.sun.ac.za/items/3edc628a-0b87-4d89-ab4a-0ff715b17502) (South Africa; PPH n=283, sepsis n=126) | SI <0.9 good rule-out; **0.9 to 1.69 and ≥1.7 both increased risk**, for **sepsis as well as haemorrhage** |
| [CRADLE VSA device](https://pmc.ncbi.nlm.nih.gov/articles/PMC5924508/) | Green: BP <140/90 and SI <0.9. **Yellow:** BP 140 to 159 / 90 to 109 or SI 0.9 to <1.7. **Red:** BP ≥160/110 or **SI ≥1.7** |
| WHO 2025 | **SI >1** as a PPH trigger with ≥300 mL loss |
| **Recommended encoding** | SI ≥0.9: abnormal, reassess and consider referral. SI >1 with any bleeding: PPH pathway now. SI ≥1.4: urgent transfer. SI ≥1.7: critical |

- **E-MOTIVE** (NEJM 2023, sites including Kenya): calibrated drape plus bundle reduced severe PPH, laparotomy or death from bleeding from **4.3% to 1.6%** (about 60% reduction); detection rose from 51.1% to **93.1%**; bundle adherence from 19.4% to **91.2%** ([Oxford WRH](https://www.wrh.ox.ac.uk/publications/publication_modal/2390339); [WHO news](https://www.who.int/news/item/09-05-2023-lifesaving-solution-dramatically-reduces-severe-bleeding-after-childbirth); [2 Minute Medicine](https://www.2minutemedicine.com/early-detection-and-treatment-of-postpartum-hemorrhage-reduces-associated-complications/)). The strongest recent evidence that **detection plus a forced action bundle** changes outcomes.

#### 5.17.4 Sepsis, Early Warning Scores And Fetal Movements

| Topic | Rule or finding | Source | Status |
|---|---|---|---|
| WHO maternal sepsis definition (2016) | "A life-threatening condition defined as organ dysfunction resulting from infection during pregnancy, childbirth, post-abortion, or postpartum period"; suspected infection plus organ dysfunction signs (tachycardia, low BP, tachypnoea, altered mental status, reduced urine output) | [World Sepsis Day](https://www.worldsepsisday.org/news/2018/1/9/who-statement-on-maternal-sepsis); [Bonet et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5450299/) | Primary statement |
| omqSOFA (SOMANZ) | At least 2 of **SBP ≤90, RR ≥25, altered mentation** | [O&G Magazine](https://www.ogmagazine.org.au/?p=9898) | **UNVERIFIED** (secondary) |
| SI and sepsis | SI ≥0.9 stratifies sepsis risk | Nathan 2019 | |
| Booklet postpartum | Fever plus foul-smelling discharge postpartum means refer | MCH Handbook | |
| MEOWS validation | 676 admissions: **sensitivity 89%, specificity 79%, PPV 39%, NPV 98%**; 30% triggered, 13% had morbidity (**the 30% trigger rate is an alert-fatigue warning**) | [Singh et al., Anaesthesia 2012](https://portaldeboaspraticas.iff.fiocruz.br/biblioteca/a-validation-study-of-the-cemach-recommended-modified-early/) | Abstract |
| MEOWS triggers | Escalate on 1 red or 2 yellow. Red: SBP <90 or >160; DBP >100; HR <40 or >120; RR <10 or >30. Yellow: SBP 90 to 100 or 150 to 160; DBP 90 to 100; HR 40 to 50 or 100 to 120; RR 21 to 30 | Secondary summaries | **UNVERIFIED**; local charts differ; pick one published chart and cite it |
| Reduced fetal movements | WHO 2016: daily formal kick-counting only in research; make women aware in the third trimester and report reductions; ask at each contact. RCOG GTG 57: no evidence for counting thresholds; report any decrease or cessation; CTG from 26+0 weeks; ultrasound from 28+0 weeks if RFM persists despite normal CTG | [WHO recommendation](https://bigg-rec.bvsalud.org/en/recommendations/33ead605397e1d6ea990c2aed0f3995ed0f52a12); [RCOG GTG 57 summary](https://opqic.org/bjog-reduced-fetal-movements-green-top-guideline-no-57/) | |
| **Safe CHP encoding for RFM** | "Reduced or no fetal movement" means **same-day facility assessment**; no numeric kick threshold. RFM is a reported symptom, not a trend | MCH Handbook | |

#### 5.17.5 Anaemia (WHO 2024 Haemoglobin Cut-Offs)

| Trimester | Mild | Moderate | Severe | Source |
|---|---|---|---|---|
| 1 and 3 | 100 to 109 g/L | 70 to 99 g/L | <70 g/L | [DHS Program blog](https://blog.dhsprogram.com/hemoglobin-collection-at-the-dhs-program-impact-of-updated-who-guidelines-on-dhs-program-anemia-data/); [Guideline Central](https://www.guidelinecentral.com/guideline/3534081/) |
| 2 | 95 to 104 g/L | 70 to 94 g/L | <70 g/L | Same |

Mizani's `full-v1` rule `r_anaemia_severe` (Hb <70 g/L → urgent) uses the severe band (build.md section 7.2).

#### 5.17.6 Trend-Based Signals Across Visits (Where Memory Adds Value)

| Signal | Use | Constraint |
|---|---|---|
| Onset timing (ISSHP) | Distinguish chronic from gestational hypertension and pre-eclampsia | Needs a recorded BP before 20 weeks (memory) |
| Persistence across contacts and witnesses | Persistent ≥140/90 across repeat and cross-site readings | Revision, not averaging |
| BP variability | Research-grade predictor (Magee 2021) | Not used for alerts in the hackathon build |
| "Rising trend, recheck sooner" nudge | A non-diagnostic prompt (for example a 15 to 20 mmHg diastolic rise from booking while still under 90) | **Not** a danger sign on its own (Brown 1999) |
| Hb falling between visits despite IFA, or no Hb by 28 weeks | Prompt a test | Facility data only (no CHP Hb meter) |
| Missed visits against the 8-contact schedule | CHP follow-up task | |

#### 5.17.7 How The Evidence Maps To Mizani's Rule Packs

Consistent with build.md section 7 (edge pack `edge-v1` for the community agent; full pack `full-v1` for the facility agent):

| Mizani rule | Evidence basis in this section |
|---|---|
| `r_danger_bleed`, `r_danger_fits`, `r_danger_sign` | ANC.DT.01; MCH booklet |
| `r_severe_htn` (≥160 or ≥110) | ANC.DT.17; NICE NG133; CRADLE red |
| `r_htn_symptom` (≥140/90 and a severe symptom) | ANC.DT.17 |
| `r_htn_unconfirmed` (single unrepeated reading → Watch, repeat after 10 to 15 minutes) | ANC.DT.04 |
| `r_htn_confirmed` (repeated reading, no symptoms → refer for urine protein) | ANC.DT.12 plus the CHP kit gap (no dipstick) |
| `r_fever`, `r_rfm`, `r_prom`, `r_breath` | ANC.DT.01, DT.04, DT.06; MCH booklet; RCOG GTG 57 |
| `r_new_onset`, `r_chronic` | ISSHP onset timing |
| `r_pe` (new onset and protein ≥2+) and `r_pe_severe` | ANC.DT.17; NICE NG133 |
| `r_shock` (SI 0.9 / 1.4 / 1.7) | El Ayadi 2016; Nathan 2015, 2019; CRADLE VSA |
| `r_pph` (≥300 mL plus abnormal haemodynamics, or ≥500 mL) | WHO/FIGO/ICM 2025 |
| `r_anaemia_severe` (Hb <70 g/L) | WHO 2024 cut-offs; ANC.DT.25 |
| Defeater `d_treated` (a lower BP after an antihypertensive is not evidence of normal BP) | Clinical pharmacology; recorded as a protocol rule with provenance |
| Provenance weight for an unrepeated reading (lower confidence) | ANC.DT.04 requires a repeat; CRADLE-3 feasibility on confusing middle tiers |

### 5.18 Trial And Programme Evidence

| Intervention | Design | Result | Lesson | Source |
|---|---|---|---|---|
| **CRADLE-3** (CRADLE VSA), Lancet Glob Health 2019 | Stepped-wedge cluster RCT, 10 clusters in 8 countries (no Kenya site), 536,223 deliveries | Composite (death, eclampsia, hysterectomy) fell from **79.4 to 72.8 per 10,000** (OR 0.92, 95% CI 0.86 to 0.97) unadjusted; **after adjustment for time trends, no significant effect (OR 1.22, 0.73 to 2.06)**. Emergency hysterectomy fell; eclampsia and death did not change. ICC 0.61 vs 0.0085 assumed. Referrals rose from 3.7% to 4.4%, and **16-fold at one site** (high anaemia) | Accurate measurement alone does not save lives; alerts can flood referral systems | [Vousden et al. 2019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6379820/); [UTS repository](https://opus.cloud1.lib.uts.edu.au/bitstream/10453/155169/2/Effect%20of%20the%20CRADLE%20vital%20signs%20alert%20device%20intervention%20on%20referrals%20for%20obstetric%20haemorrhage%20in%20low-middle%20income%20count.pdf) |
| **CRADLE-3 feasibility** | Mixed methods | "Yellow down" (SI 0.9 to 1.69) alerts were common and confusing because "many women appeared well"; training revised | Middle-tier alerts need clear, specific actions | [Vousden et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5924508/) |
| **CRADLE-5**, Sierra Leone, 2025 | National roll-out, 8 districts, 2,171 devices, more than 93,000 births | Vital sign measurement improved; **no overall reduction in maternal deaths or stillbirths**; newborn survival improved **where referral systems worked**; poor-competency facilities had more eclampsia. "Technology alone cannot save lives without parallel investment in drugs, blood, ambulances, and trained staff." | Couple alerts to downstream capacity | [KCL news, 28 Oct 2025](https://www.kcl.ac.uk/news/use-of-blood-pressure-and-pulse-monitoring-device-shows-promise-for-maternal-health-in-sierra-leone) |
| **CLIP trials** (Mozambique, Pakistan, India; about 70,000 pregnancies), Lancet 2020 | Cluster RCTs; CHWs with mHealth (PIERS on the Move) for hypertension detection, treatment and referral | **No reduction in the primary composite** (24% vs 22%, aOR 1.17, 0.90 to 1.51, as reported in the maternal workstream). Per-country: India aOR 0.92; Mozambique aOR 1.31. Stillbirths reduced (OR 0.89); no effect on maternal death | Under-delivery: too few CHW contacts; where delivered as planned, signals were positive. **Fidelity and contact frequency matter more than the algorithm** | [CLIP Lancet 2020](https://scholars.aku.edu/en/publications/the-community-level-interventions-for-pre-eclampsia-clip-cluster-/); [CLIP India](https://ecommons.aku.edu/pakistan_fhs_mc_women_childhealth_wc/115); [CLIP Mozambique](https://scholars.aku.edu/en/publications/community-level-interventions-for-pre-eclampsia-clip-in-mozambiqu/); [KCL](https://www.kcl.ac.uk/news/community-health-workers-reduce-maternal-foetal-new-born-deaths); [PIERS on the Move](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4123040/) |
| **E-MOTIVE** (includes Kenya), NEJM 2023 | Cluster RCT, about 200,000 births | Composite **4.3% to 1.6%**; detection 51.1% to 93.1%; bundle adherence 19.4% to 91.2% | Objective detection plus a bundled action works, inside facilities | Section 5.17.3 sources |
| **BetterBirth** (WHO Safe Childbirth Checklist), NEJM 2017, Uttar Pradesh | 120 facilities, more than 157,000 births | Adherence to essential birth practices **73% vs 42%**; **no effect on maternal or perinatal death or severe complications** | Process adherence does not equal outcomes when complications are not recognised and treated in time, or referral fails | [Semrau et al. 2017](https://www.hsph.harvard.edu/global-health-research-partnership/wp-content/uploads/sites/2448/2023/09/nejmoa1701075.pdf) |
| **PROMPTS** (Jacaranda Health), PLoS Med Feb 2025 | Cluster RCT, 40 facilities, 8 Kenyan counties, n=6,139 | Knowledge +0.08 SD; birth preparedness +0.08 SD; routine care-seeking +0.07 SD; **≥2 PNC visits +7.4 percentage points (18% relative)** (IPA summarises "+17% relative PNC visits"); ANC 4+ +3.1 pp; newborn care +0.09 SD; **danger-sign care-seeking +0.04 SD, not significant (p=0.096)**; no effect on postpartum or neonatal danger-sign knowledge; facility delivery 98 to 99% in both arms; **not powered for mortality**. Cost **USD 0.74 per enrollee for their lifetime on the platform**; about **86%** of helpdesk queries answered automatically; high-priority cases get a clinician within 1 minute; scale more than 2.5 to 2.77 million mothers | Reach and cost proven; triage-to-action is the gap | [Vatsa et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11835334/); [IPA](https://poverty-action.org/impact-digital-health-platform-maternal-and-newborn-care-kenya); [AI4D](https://www.ai4d.ai/blog/revolutionizing-maternal-healthcare-with-ai); [AWS](https://aws.amazon.com/blogs/publicsector/jacaranda-health-advances-maternal-infant-health-across-kenya-beyond-aws/) |
| **Penda Health AI Consult** (Nairobi, with OpenAI), arXiv July 2025 | 15 clinics, 39,849 visits; non-randomised QI design | **16% fewer diagnostic errors and 13% fewer treatment errors** (rated by independent physicians); where red alerts fired, diagnostic errors fell 31% and treatment errors 18%; all surveyed clinicians said it improved care, 75% "substantially". Caveats: non-randomised; error rates, not patient outcomes; general primary care, not maternity | A traffic-light, mostly silent safety net that interrupts only for serious issues, workflow-integrated, with active deployment | [Korom et al. 2025](https://arxiv.org/abs/2507.16947); [OpenAI](https://openai.com/index/ai-clinical-copilot-penda-health); [Citizen Digital](https://citizen.digital/news/ai-tool-cuts-diagnostic-errors-by-16-in-kenyan-clinics-study-finds-n367615) |

**Other programme evidence.**

| Programme | Result | Source |
|---|---|---|
| MomConnect (South Africa), BMJ Glob Health 2018 | More than 1.7 million women registered in 95% of public facilities; about 8% used the helpdesk; more than 14,000 compliments vs about 1,450 complaints; fewer adverse events among registrants (observational). 96% ANC attendance among engaged users vs 76% nationally (secondary) | [Barron et al. 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5922497/); [helpdesk paper](https://www.measureevaluation.org/resources/publications/ja-18-252); [Population Medicine](https://www.populationmedicine.eu/AI-Powered-Personalisation-at-Scale-Bridging-the-Equity-Gap-in-Maternal-and-Child,227345,0,2.html) |
| Mobile WACh (Nairobi RCT, n=298) | One-way and two-way SMS improved exclusive breastfeeding and early postpartum contraception; two-way SMS sustained exclusive breastfeeding (**UNVERIFIED** effect sizes) | [Unger et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6179930); [NCT01894126](https://clinicaltrials.gov/study/NCT01894126) |
| Living Goods/BRAC (Uganda cluster RCT, 214 clusters, 2011 to 2013) | **Under-5 mortality down 27%** (aRR 0.73, 0.58 to 0.93); infant mortality down 33%. Child, not maternal; shows a supervised, incentivised, digital CHW model can move mortality | [Trinity College Dublin](https://www.tcd.ie/news_events/articles/new-community-health-programme-linked-to-decreased-child-mortality-in-uganda) |
| Cochrane: decision-support tools via mobile devices in primary care (Agarwal 2021) | 8 studies (including Kenya); evidence on adherence and outcomes **mostly low certainty** (summary level) | [Cochrane CD012944.pub2](https://cochranelibrary.com/cdsr/doi/10.1002/14651858.CD012944.pub2/information) |
| mHealth for health workers in pregnancy, LMICs (Amoakoh-Coleman 2016) | 19 studies; tracking, ANC, delivery and referral; **no direct assessment of effect on maternal or neonatal mortality** | [JMIR 2016](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5010646/) |
| mCDSS in sub-Saharan Africa (Adepoju 2017) | Health workers like the tools, but added workload and altered workflow threaten sustainability; few outcome evaluations; few at scale | [JMIR mHealth 2017](https://mhealth.jmir.org/2017/3/e38) |

### 5.19 What Failed And Why (Design Checklist)

| # | Failure mode | Evidence | Fix (and where Mizani applies it) |
|---|---|---|---|
| 1 | **Alert fatigue** | 49 to 96% of drug-safety alerts overridden ([van der Sijs 2006](https://textbookofdigitalhealth.com/references/h2006overriding.html)); MEOWS triggered in 30% of admissions; CRADLE "yellow" confused staff; acceptance drops about 30% per extra reminder per encounter ([Textbook of Digital Health](https://www.textbookofdigitalhealth.com/glossary/alert-fatigue.html)) | Few tiers (Normal, Watch, Urgent, Emergency); one specific action per level; suppress repeats; measure override rates |
| 2 | **No downstream capacity** | CRADLE-5; BetterBirth | Couple alerts to destination readiness; say what to do before transfer (stabilise per protocol) |
| 3 | **Fidelity and contact frequency** | CLIP | Schedule-driven tasks; the algorithm only runs if the CHP sees the woman |
| 4 | **Black-box mistrust and liability** | Clinicians need to see *why*; Kenyan law requires audit trails (section 5.20) | Show the rule, threshold and guideline on every recommendation; log inputs, outputs and the human action (Mizani's proof and event log) |
| 5 | **Poor referral feedback** | MOH 100 back-referral under-used; CHVs could not verify attendance or outcome ([Living Goods](https://livinggoods.org/media/closed-loop-for-referrals-follow-up-of-maternal-neonatal-and-child-health-integrated-community-case-management/)) | Closed-loop status pushed back to the CHP; the reconciled decision returns to the community agent |
| 6 | **Connectivity, power, devices** | Logouts, power cuts, ageing phones; rural household electricity 36% | Offline-first rules on device; small payloads; outbox and sync (Mizani P0.4) |
| 7 | **Parallel systems and "pilotitis"** | eCHIS is the national rail; added workload kills mCDSS (Adepoju 2017) | Position as a reasoning service beside eCHIS, not a new app |

### 5.20 Data Protection, Regulation And Liability

#### 5.20.1 Kenya Data Protection Act 2019 (Cap. 411C), Text VERIFIED On Kenya Law

Source: [DPA 2019 (No. 24)](https://new.kenyalaw.org/akn/ke/act/2019/24/eng@2022-12-31); regulations: [Data Protection (General) Regulations 2021](https://www.odpc.go.ke/wp-content/uploads/2024/03/THE-DATA-PROTECTION-GENERAL-REGULATIONS-2021-1.pdf).

| Provision | Content | Consequence for Mizani |
|---|---|---|
| **s.2** | "Sensitive personal data" includes **health status**, genetic and biometric data, and **family details**. "Health data" includes data collected during registration for or provision of health services, and data linking a person to specific health services | Every visit note and reading is sensitive personal data |
| **s.31** | A **Data Protection Impact Assessment (DPIA) is mandatory before processing** likely to result in high risk | AI triage of pregnant women's health data qualifies; a DPIA is required before any real deployment |
| **s.35** | Right "not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning or significantly affects the data subject" (exceptions: contract, law, consent; notification duties apply) | A referral decision "significantly affects" her. **Keep a human (CHP or clinician) as the decision-maker, and document it.** Mizani's contest and the human-confirmed observations are designed for this |
| **s.46** | Health data may be processed only by or under the responsibility of a **health care provider**, or by a person under a legal duty of professional secrecy (with public-health and confidentiality exceptions) | A solo developer needs a licensed provider or facility as controller or partner |
| **s.48 to 49** | Transfer out of Kenya needs proof of safeguards; **sensitive personal data can be processed outside Kenya only with the data subject's consent and confirmation of appropriate safeguards (s.49(1))** | Calling foreign-hosted APIs (including Jev) with identifiable data needs consent and safeguards; hackathon uses synthetic data and strips identifiers |
| **s.50 and reg. 26** | Processing for "**provision of primary or secondary health care for a data subject in the country**" must use a **server and data centre located in Kenya**, or keep **at least one serving copy in a Kenyan data centre** | Production needs a Kenyan-hosted copy |
| **s.63** | Administrative fines up to **KSh 5 million or 1% of annual turnover, whichever is lower** | |
| Registration | Controllers and processors must register with the ODPC | |

#### 5.20.2 Digital Health Act 2023 (No. 15), Text VERIFIED On Kenya Law

Source: [Digital Health Act 2023](https://new.kenyalaw.org/akn/ke/act/2023/15/eng@2023-11-24).

| Provision | Content |
|---|---|
| s.4 | Guiding principle: "**health data is a strategic national asset**" |
| Agency | Creates the **Digital Health Agency (DHA)** as custodian of health data, with a registry of health data controllers and a National Health Data Bank |
| Security | The integrated system must have security measures including **"audit trails for all activities within the system"**, role-based rights and encrypted backup |
| Retention | At least **20 years** (s.24(5) and s.25) |
| s.41(2) | **E-health service providers must be licensed healthcare providers or facilities**; the CS develops e-health platform standards |
| s.35 | Tampering, loss, theft or unauthorised sharing of health data: fine up to **KSh 1 million and/or up to 15 years** |
| s.59 | General offence: up to KSh 1 million and/or 2 years |
| 2025 Regulations | Digital Health (Health Information Management Procedures) Regulations 2025 require **certification by the DHA of digital health solutions** used in care; SHA ties provider contracting to certified HMIS (**UNVERIFIED**: press and law-firm summaries) ([AllAfrica, Sept 2026](https://allafrica.com/stories/202609010210.html); [Clyde & Co, March 2026](https://www.clydeco.com/en/insights/2026/03/health-data-protection-in-kenya-strategic-complian)) |

#### 5.20.3 Software As A Medical Device And AI

| Instrument | Content | Status | Source |
|---|---|---|---|
| **PPB Guideline on Regulation of Medical Device Software (MDSW)** | Reported **in force from February 2026**; covers SaMD and SiMD **including AI clinical decision support**; excludes general wellness apps; risk-based (IMDRF-aligned, up to Category IV); requires IEC 62304 and ISO 14971; follows **Good Machine Learning Practice** (representative data, train/test separation, sensitivity and specificity reporting, **traceability between datasets, software versions and outputs**, bias monitoring); post-market surveillance with annual reports and version control; reported fees about USD 250 (low risk, local) to USD 2,500 (Category IV, foreign), 5-year registration; PPB has said AI should be **trained or validated on Kenyan data** and data stored in Kenya | **UNVERIFIED** (press, April 2026; guideline PDF not read) | [The Star, 22 Apr 2026](https://www.the-star.co.ke/news/2026-04-22-new-rules-set-for-health-apps-medical-software); [Health Business, 16 Apr 2026](https://healthbusiness.co.ke/10137/kenya-tightens-oversight-of-medical-device-software/); [The Standard](https://www.standardmedia.co.ke/business/opinion/article/2001551793/what-ai-bill-and-ppb-software-device-rules-mean-for-healthcare-businesses) |
| Implication | A tool that tells a CHP "refer urgently" from BP and symptoms is very likely **SaMD (clinical decision support)**; a pure reminder or education tool may not be. Classify early; frame as "organises data and shows guideline rules for a human to act on" without overstating | Analysis | |
| **KMPDC e-Health guidelines (2019)** | License "virtual medical services providers"; the application form lists **artificial intelligence** as a service type; a **Kenya-registrable medical director** is responsible for clinical care. No KMPDC guidance specific to AI liability found; under general negligence principles **the licensed clinician remains accountable** | Form read | [KMPDC form](https://kmpdc.go.ke/resources/Application%20for%20Registration%20as%20a%20Virtual%20Medical%20Services%20Provider.pdf) |
| **AI Bill 2026** (Senate, first reading April 2026) | Would classify AI medical devices as high-risk, require impact assessments and 5-year retention, penalties up to KSh 5 million | **UNVERIFIED** (status changes quickly) | [The Standard](https://www.standardmedia.co.ke/business/opinion/article/2001551793/what-ai-bill-and-ppb-software-device-rules-mean-for-healthcare-businesses) |
| Draft AI and Emerging Technologies Policy 2026; national AI-for-health guidelines in development (HELINA, May 2026) | | **UNVERIFIED** | [Bowmans](https://bowmanslaw.com/insights/kenya-ai-governance-framework-continues-to-take-shape-draft-artificial-intelligence-and-emerging-technologies-policy-2026/); [HELINA](https://helina.africa/wp-content/uploads/2026/05/Kenya-Health-Sector-AI-Regulation-Press-Release.pdf) |

#### 5.20.4 Why Auditability Matters (Pitch Summary)

1. **Legal:** the Digital Health Act requires audit trails; DPA s.35 restricts solely automated decisions; PPB GMLP requires traceability between data, software versions and outputs.
2. **Clinical trust:** Kenyan clinicians and CHPs are accountable to KMPDC and county supervisors. A recommendation they cannot trace to a rule (for example "repeat BP 162/112 ≥160/110, WHO ANC.DT.17, refer urgently") is a liability for them.
3. **Learning system:** MPDSR reviews need to reconstruct what was seen, when, and what was done. A tamper-evident log of inputs, rule version, output and the human action supports CEMD-style avoidable-factor analysis.

### 5.21 Language And Access

| Topic | Finding | Source | Status |
|---|---|---|---|
| Languages | Kiswahili and English are national languages; local languages vary by county; CHPs must read and write a national language **and** the local language | [PHC Act 2023](https://new.kenyalaw.org/akn/ke/act/2023/13/eng@2023-11-24) | VERIFIED |
| Comprehension | A Translators without Borders / CLEAR Global study in Kenya found comprehension of English health information was very limited, and **the same content in Swahili markedly improved comprehension** | [TWB Words of Relief](https://translatorswithoutborders.org/wp-content/uploads/2016/08/TWB_WoR_ImpactStudy_FINAL.pdf); [CLEAR Global](https://clearglobal.org/resources/words-of-relief-impact-study-of-rural-and-urban-kenyans/) | Report |
| Sheng | Swahili-English urban argot used in health messaging (for example COVID-19) | [IGI Global chapter](https://igi-global.com/chapter/kiswahili-video-messaging-on-covid-19-awareness-in-kenya/345946) | **UNVERIFIED** (no maternal-specific comprehension study found) |
| Code-switching | Expect "nina headache sana", "damu inatoka"; PROMPTS handles English and Swahili with a custom LLM | [AI4D](https://www.ai4d.ai/blog/revolutionizing-maternal-healthcare-with-ai) | |
| CHW knowledge | In Rongo, training and experience predicted CHW knowledge better than formal education | [Frontiers Public Health 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10173767) | **UNVERIFIED** (summary) |
| Women's phones (KDHS 2022) | 78% own a mobile phone; 43% a smartphone; 44% used the internet in the past 12 months | [KDHS Summary](https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf) | VERIFIED |
| National connectivity (CA, Q2 FY2025/26) | 78.4 million SIMs (149.5% penetration); 48.7 million smartphone vs 29.6 million feature-phone connections; **4G population coverage 97.3%**; 5G 30% | [Khusoko](https://khusoko.com/2026/04/08/kenya-ict-sector-statistics-q2-2025-2026/) | Press summary of CA statistics |
| Rural reality | Internet use about 25% rural vs 57% urban; West Pokot 9.1% and Turkana 12.7% among the lowest; Turkana, West Pokot, Samburu, Mandera, Wajir and Marsabit have the lowest phone ownership | [Ecofin Agency](https://www.ecofinagency.com/news-digital/1602-52943-kenya-moves-to-strengthen-rural-connectivity-through-spectrum-reform) | **UNVERIFIED** (secondary, likely 2019 census) |

**Implications.** Offline-first; rules run on the device; sync when possible; SMS or USSD for mothers (P2); short sentences, icons and voice for low literacy; server-side language models only for non-critical language tasks, with a Kenyan-hosted copy of data in production. Mothers are a feature-phone and SMS audience; CHPs are a smartphone (eCHIS) audience. Mizani's Swahili explanations are deterministic templates rendered from the proof (build.md section 10), to be reviewed by a fluent Kenyan speaker.

### 5.22 Ranked Problem Statements From The Maternal Workstream

Ranking criteria: (a) share of Kenyan deaths addressed, (b) strength of evidence that the mechanism works, (c) safety and encodability with deterministic rules, (d) feasibility for one developer in Kenya's regulatory and connectivity context, (e) fit with existing rails (eCHIS, MCH booklet, CHP kit).

| Rank | Problem | Agent sketch | Evidence | Main risks |
|---|---|---|---|---|
| 1 | Hypertension triage and BP surveillance for CHPs and ANC clinics. Hypertensive disorders cause 15 to 19% of deaths and their share is rising; CHPs carry BP machines; 29% book in trimester 1; 35% get postnatal BP; MgSO4 in only 77% | WHO DT.04, DT.12, DT.17; BP across visits; aspirin/calcium eligibility (DT.27) for clinician review; referral note; postpartum days 1 to 42 | Strong for thresholds; mixed for impact (CRADLE-3 null after adjustment; CLIP null); positive where contact and referral worked | BP device accuracy in pregnancy; alert volume (CRADLE 16-fold spike). Mandatory repeats, two tiers, referral-capacity awareness |
| 2 | Postpartum first-24-hour and first-week early warning (PPH and sepsis) | SI calculator plus MOTIVE checklist with WHO 2025 definition; SI tiers 0.9/1.4/1.7; timed observation reminders; CHP PNC day 1 to 2 screening (fever, SI, foul discharge, omqSOFA) | **Strongest** (E-MOTIVE) | Blood loss needs calibrated drapes; prompt for measurement, never estimate |
| 3 | Closed-loop referral: structured handoff, pre-alert, back-referral. 64% critical on arrival, 58% referred; 75% delayed arrival; MOH 100 back-referral rarely completed | SBAR-style referral summary; pre-alert the PCN hub; track status; outcome feedback to CHP; digitise MOH 100 | Strong observational evidence that referral is the failure point; **no RCT of digital closed-loop maternal referral found** | High feasibility; low clinical-decision risk (possibly not SaMD) |
| 4 | Swahili and Sheng danger-sign triage of mothers' messages | Classifier to MCH booklet and DT.01 taxonomy; positive or uncertain escalates to a human | PROMPTS proves scale and cost; gap is triage sensitivity and action | False negatives; DPA s.35 and s.49; directly competitive with Jacaranda (partner instead) |
| 5 | ANC continuity and risk worklist for CHPs | Daily prioritised list: missed contacts, no Hb by 28 weeks, low Hb, prior PE/PPH, adolescents | CLIP contact frequency; PROMPTS small gains; Living Goods | High feasibility as eCHIS/CHT tasks |
| 6 | Clinician safety-net audit at primary facilities | Penda-style silent reviewer flagging guideline-backed omissions (severe BP without MgSO4 or referral, PPH trigger without TXA, SI ≥1 without escalation, no PNC BP) | Penda (16%/13% fewer errors); E-MOTIVE | SaMD; needs a facility partner (s.46); alert budget |
| 7 | Commodity-aware referral routing (EmONC readiness) | Readiness registry per PCN hub updated by SMS | Indirect (CRADLE-5, near-miss); **evidence gap** | Depends on facility staff updating data |
| 8 | MPDSR and CEMD review assistant | Structure death-review narratives into avoidable-factor and Three-Delay taxonomy; de-identify; dashboards | MPDSR credited with recent declines (**UNVERIFIED**) | Highly sensitive data; users are county committees |

**Suggested scope from this workstream:** combine #1 and #3 (optionally #2): deterministic WHO-DAK hypertension and shock-index triage that produces an auditable, closed-loop referral, offline-first, in Swahili and English. **What we built on it:** the landscape workstream (section 6) reframed this into the two-witness reconciliation, because #1 plus #3 alone is crowded and the novel part is the reconciled, contestable handoff.

---
## 6. Competitive Landscape And Novelty

Prepared 2 October 2026 as a novelty stress test of the original concept ("glass-box maternal danger-sign agent for Kenyan CHPs"). "Not found" means not found in the searches in section 6.10; it is not proof of absence.

### 6.1 TL;DR

- **The generic concept is crowded.** "AI maternal danger-sign triage + referral for CHWs" is one of the most common hackathon health ideas in 2026. GitHub alone shows at least 15 such repositories updated in 2026 (section 6.3). Kenyan student teams won the July 2026 PPH hackathon with exactly this pitch ([Eastleigh Voice](https://eastleighvoice.co.ke/health/382799/kenyan-students-win-inaugural-pph-hackathon-with-live-saving-maternal-health-tool)). Several entries already claim "explainable, deterministic, WHO-rule based" logic ([SafeMother-CDSS](https://github.com/zinthooz/SafeMother-CDSS)), and one claims "deterministic safety rules + verifier + audit trail" ([Maitri](https://github.com/mlvpatel/maitri)).
- **Production systems already cover several pillars.** eCHIS runs on Medic's CHT for about 95k CHPs ([Medic](https://medic.org/stories/medic-partners-with-kenyan-government-to-transform-community-health/)) and in June 2026 presented a closed-loop eCHIS to TaifaCare referral with outcome notification to the CHP ([Medic roundup listing](https://unjobs.org/channels/TCrYgB812EXuz7Y0yLTGGNsXLi03/GPHorre4g-0)). WHO publishes ANC danger-sign logic as executable CQL ([smart-anc](https://github.com/WorldHealthOrganization/smart-anc)). Jacaranda's PROMPTS triages around 15k messages a day with nurse escalation ([WUSF/NPR, Sep 2026](https://www.wusf.org/2026-09-17/to-prevent-deaths-in-childbirth-kenyan-moms-turn-to-an-ai-powered-chatbot)).
- **What still looks open (no prior art found):** (1) symbolic reasoning over cross-visit and cross-site evidence; (2) the referral note as a **contestable proof object**; (3) structured reconciliation of conflicting readings between CHP and facility, with provenance; (4) clinician override turned into a reviewed rule patch with a visible diff; (5) any MeTTa/Hyperon clinical or maternal project at all.
- **Recommendation adopted:** reframe from "danger-sign checker with memory" to **"Two-Witness Referral: a CHP-side agent and a facility-side agent reconcile conflicting maternal evidence in MeTTa, and the result ships as a contestable referral proof."** This became Mizani.

### 6.2 Full Comparison Table

Legend: **Sym** = symbolic or auditable reasoning shown to the user; **Trend** = reasons over longitudinal or multi-visit data; **Handoff** = machine-generated referral content the receiving facility reads; **Learn** = clinician feedback updates rules or models through a reviewed process.

| System | What it does | Evidence | Sym | Trend | Handoff | Learn | Key weakness for our purposes |
|---|---|---|---|---|---|---|---|
| **Jacaranda PROMPTS + UlizaLlama** (Kenya) | Two-way SMS for mothers; a Swahili LLM triages messages; about 7% flagged urgent and routed to 18 nurses ([WUSF](https://www.wusf.org/2026-09-17/to-prevent-deaths-in-childbirth-kenyan-moms-turn-to-an-ai-powered-chatbot)) | RCT, 6,139 women, 40 facilities: better ANC danger-sign knowledge, +17% relative PNC visits, **no effect** on postpartum and neonatal danger-sign knowledge ([IPA](https://poverty-action.org/impact-digital-health-platform-maternal-and-newborn-care-kenya)) | No (LLM classifier) | Partial (nurse sees history) | Partial ("transmit digital records in advance", [Standard](https://www.standardmedia.co.ke/health/amp/health-science/article/2001515393/how-ai-is-transforming-maternal-healthcare-in-muranga-county)) | Human audit of answers | Mother-facing; a researcher asks who catches a mis-triaged urgent message ([WUSF](https://www.wusf.org/2026-09-17/to-prevent-deaths-in-childbirth-kenyan-moms-turn-to-an-ai-powered-chatbot)) |
| **Kenya eCHIS (Medic CHT)** | National CHP app: registration, tasks, danger-sign forms, referrals; about 95k CHPs in 47 counties ([Medic](https://medic.org/stories/medic-partners-with-kenyan-government-to-transform-community-health/)) | 74k referrals ([Amref](https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/)); closed loop to TaifaCare presented June 2026 ([roundup](https://unjobs.org/channels/TCrYgB812EXuz7Y0yLTGGNsXLi03/GPHorre4g-0)) | Form logic (XLSForm), not explained | Task scheduling only; CHT reference app stores BP as a yes/no `high_blood_pressure` risk factor ([cht-core config](https://github.com/medic/cht-core/tree/master/config/default/forms/app)) | Yes: digital referral plus outcome back | No | No entry validation, no change-tracking; CHPs "still rely on manual judgment" ([Amref](https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/)) |
| **CHT Maternal & Newborn reference app** | Danger-sign form leads to immediate referral with a follow-up task 3 days later ([CHT docs](https://docs.communityhealthtoolkit.org/reference-apps/maternal-newborn/)) | Deployment at scale | No | No numeric trending documented | Paper or digital | No | Follow-up checks attendance, not clinical reasoning |
| **WHO SMART ANC DAK / OpenSRP** | WHO ANC recommendations as decision tables plus FHIR PlanDefinition and CQL ([SMART ANC IG](https://build.fhir.org/ig/costateixeira/smart-anc/documentation.html); [JMIR 2020](https://jmir.org/2020/10/e16355)) | "Further evidence is needed" on impact ([JMIR 2020](https://jmir.org/2020/10/e16355)) | **Yes**: explicit rules (ANCDT01, ANCDT17, ANCDT04) ([repo CQL](https://github.com/WorldHealthOrganization/smart-anc/tree/master/input/cql)) | **Almost none**; per-contact thresholds; cross-contact only "symptoms persist since last contact" and "weight gain since last contact" (grep of `ANCContactDataElements.cql`) | No | Versioned artifacts ([CRMI lifecycle](https://hl7.org/fhir/uv/crmi/en/artifact-lifecycle.html)), not driven by overrides | Facility-oriented, no trend logic; a ready source of rules to transcribe into MeTTa |
| **Living Goods digital closed-loop referral** (Kisii) | SMS confirmation to the CHV when the referred client arrives ([Living Goods](https://livinggoods.org/media/closed-loop-for-referrals-follow-up-of-maternal-neonatal-and-child-health-integrated-community-case-management/)) | 476 referrals; 47% went to non-linked facilities | No | No | Attendance only | No | Closes the logistics loop, not the clinical-reasoning loop |
| **Dimagi CommCare** | Configurable CHW decision support and case management; 58 MNH projects ([Dimagi](https://dimagi.com/sectors/maternal-and-newborn-health/)) | ANC quality improved in a Nigeria pre/post study ([PMC4420494](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4420494/)) | Form logic | Configurable | Varies | No | Generic platform |
| **D-tree Safer Deliveries** (Zanzibar) | CHV app: 3 antenatal and 3 postnatal visits, danger-sign screening ([GCGH](https://gcgh.grandchallenges.org/grant/mhealth-safer-deliveries)) | Facility delivery 74% vs 55% baseline ([D-tree](https://www.d-tree.org/?p=1880)); 133k visits ([PMC10921749](https://pmc.ncbi.nlm.nih.gov/articles/PMC10921749)) | Algorithmic | No | No | No | No reasoning trail |
| **CLIP / PIERS on the Move** (India, Pakistan, Mozambique, Nigeria) | CHW app with miniPIERS risk plus BP and pulse oximetry ([PMC4123040](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4123040/)) | **No overall reduction** (India aOR 0.92; Mozambique aOR 1.31) ([CLIP India](https://ecommons.aku.edu/pakistan_fhs_mc_women_childhealth_wc/115); [CLIP Mozambique](https://scholars.aku.edu/en/publications/community-level-interventions-for-pre-eclampsia-clip-in-mozambiqu/)); benefit only where CHW contact was sufficient ([KCL](https://www.kcl.ac.uk/news/community-health-workers-reduce-maternal-foetal-new-born-deaths)) | Score (logistic model) | Serial visits (used later for BP variability) | Referral advice | No | **Closest scientific precedent, and null.** Say why Mizani differs: the handoff, not the score |
| **fullPIERS / miniPIERS / PIERS-ML** | Risk of adverse outcome in pre-eclampsia | miniPIERS AUC 0.768 (external 0.713) ([PRE-EMPT](https://pre-empt.obgyn.ubc.ca/evidence/minipiers)); PIERS-ML tested at 2 Nairobi hospitals ([Strathclyde](https://strathprints.strath.ac.uk/88885/7/MontgomeryCsoban-etal-LDH-2024-Machine-learning-enabled-maternal-risk-assessment.pdf)) | Coefficients, not rule trails | Consecutive prediction work exists ([Strathclyde](https://pureportal.strath.ac.uk/en/publications/consecutive-prediction-of-adverse-maternal-outcomes-of-preeclamps/)) | No | No | Facility-level, for women already diagnosed |
| **CRADLE Vital Signs Alert** | BP and shock-index device with traffic lights ([PMC5924508](https://pmc.ncbi.nlm.nih.gov/articles/PMC5924508)) | Reductions could not be attributed to the intervention because of variability ([UTS](https://opus.cloud1.lib.uts.edu.au/bitstream/10453/155169/2/Effect%20of%20the%20CRADLE%20vital%20signs%20alert%20device%20intervention%20on%20referrals%20for%20obstetric%20haemorrhage%20in%20low-middle%20income%20count.pdf)) | Fixed thresholds | No | No | No | Hardware; single reading |
| **Penda Health AI Consult** (Nairobi, OpenAI) | LLM safety net with green, yellow, red alerts against Kenyan guidelines ([OpenAI](https://openai.com/index/ai-clinical-copilot-penda-health)) | 39,849 visits: 16% fewer diagnostic and 13% fewer treatment errors ([Citizen](https://citizen.digital/news/ai-tool-cuts-diagnostic-errors-by-16-in-kenyan-clinics-study-finds-n367615)) | LLM rationale | Within visit | No | No | Clinician-facing; LLM, not symbolic; strong local proof that tiered alerts beat alert fatigue |
| **Safe Delivery App** (Maternity Foundation) | Offline clinical training and job aid | Ethiopia cluster RCT: PPH and resuscitation skills more than doubled ([MIT Solve](https://solve.mit.edu/solutions/19533)) | Static guidance | No | No | No | Training, not decision support |
| **MomConnect** (South Africa) | SMS registry plus helpdesk; NLP triage of priority messages ([PMC5922497](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5922497/)) | 96% ANC attendance among engaged users vs 76% nationally ([Population Medicine](https://www.populationmedicine.eu/AI-Powered-Personalisation-at-Scale-Bridging-the-Equity-Gap-in-Maternal-and-Child,227345,0,2.html)) | No | No | No | No | Mother-facing |
| **mMitra / Kilkari** (India) | Voice messages | Kilkari RCT: no effect on exclusive breastfeeding; +2.8 pp immunisation at 10 weeks ([BMJ GH](https://gh.bmj.com/content/6/Suppl_5/e008838.full)) | No | No | No | No | Education only |
| **Babylon / Babyl** (incl. Rwanda) | Symptom-checker triage | Collapsed; Lancet critique found no convincing evidence ([Digital Health](https://www.digitalhealth.net/2018/11/lancet-review-babylons-ai/)); CQC raised safety concerns ([MedCity](https://medcitynews.com/2023/09/babylon-healthcare-ai-uk/)) | No | No | No | No | Cautionary tale on overclaiming |
| **Ada Health (Swahili)** | Consumer symptom assessment; AFYA accuracy study in Tanzania ([Ada](https://about.ada.com/?p=10952)) | Accuracy study ([BMJ Open 2022](https://doaj.org/article/ef2ac35795214766a36535328d1bfe75)) | Probabilistic KB | No | No | No | Consumer-facing |
| **Ubenwa** | Newborn cry analysis for asphyxia ([arXiv 1711.06405](https://ar5iv.labs.arxiv.org/html/1711.06405)) | Claims more than 95% accuracy on about 1,400 cries ([Quartz](https://qz.com/africa/1158185/nigerian-ai-health-startup-ubenwa-hopes-to-save-thousands-of-babies-lives-every-year)) | No | No | No | No | Newborn, not maternal |
| **PeriGen PeriWatch Vigilance** (US) | AI early warning in labour: vitals, FHR, contractions ([PeriGen](https://perigen.com/periwatch-vigilance/)) | Commercial | Hospital thresholds | **Yes** (continuous in labour) | Within hospital | Hospital-set limits | Intrapartum, US hospitals |
| **Google AI ultrasound + Jacaranda** | Blind-sweep AI for gestational age and malpresentation ([Google Health](https://health.google/caregivers/ultrasound); [arXiv 2203.10139](https://arxiv.org/pdf/2203.10139)) | Non-inferior to biometry, including in Nairobi ([Business Daily](https://www.businessdailyafrica.com/bd/corporate/technology/google-tests-handheld-ai-assisted-ultrasound-machines-4768212)) | No | No | No | No | Imaging only |
| **iDeliver** (Kenya) | Digital labour and delivery support ([JMIR Form Res 2022](https://formative.jmir.org/2022/6/e34741)) | Captured 45% of deliveries over 22 months | Workflow | Within labour | No | No | Adoption gaps |
| **Hackathon clones** (2026) | Danger-sign triage plus alerts (section 6.3) | Prototypes | Some (heuristics, verifier) | Few ([Haven](https://github.com/samruddhikhade/Haven-AI-) tracks ΔMAP with XGBoost) | Maitri outputs a "CHW card + audit trail" | No | **Defines the bar judges have seen.** "Explainable rules" alone is not differentiating |

### 6.3 Hackathon And GitHub Saturation (2026)

Repos found via `gh search repos` (updated 2026), each a direct overlap with "danger-sign triage + referral":

| Repo | What it claims |
|---|---|
| [Code-blize/mamaalert](https://github.com/Code-blize/mamaalert) | Triage plus geospatial routing (Nigeria) |
| [helenmenim/mamacare-ai-danger-sign-assistant](https://github.com/helenmenim/mamacare-ai-danger-sign-assistant) | RAG plus a "rule-based safety engine" |
| [MehGerald/MamaAlert](https://github.com/MehGerald/MamaAlert) | Voice-call screening with WHO triage |
| [Najeev-lab/MamaAlert-HW](https://github.com/Najeev-lab/MamaAlert-HW) | CHW registration, risk classes, referrals |
| [zinthooz/SafeMother-CDSS](https://github.com/zinthooz/SafeMother-CDSS) | Offline, deterministic, "avoids Black Box AI" |
| [mlvpatel/maitri](https://github.com/mlvpatel/maitri) | Gemma 4 specialist, deterministic safety rules, verifier, audit trail, CHW card. **Closest to "auditable referral"**; LLM-centric, single-visit, no contestation |
| [Mangalasridharan/MaTriX](https://github.com/Mangalasridharan/MaTriX-AI-Maternal-Triage-Escalation-Intelligence) | Maternal triage escalation |
| [uthy4r/mamacord-gemma4](https://github.com/uthy4r/mamacord-gemma4) | Gemma 4 maternal assistant |
| [Davidic-02/maternal-triage-system](https://github.com/Davidic-02/maternal-triage-system) | SHAP plus Flutter |
| [samruddhikhade/Haven-AI-](https://github.com/samruddhikhade/Haven-AI-) | Longitudinal vitals with ΔMAP into XGBoost |
| [Tech-sis123/My-baby](https://github.com/Tech-sis123/My-baby) | Rule-based flagging between ANC visits plus a doctor dashboard |
| [WeCODE22/safepass](https://github.com/WeCODE22/safepass) | Maternal referral network over USSD and SMS |
| [mljadama/maternal-health-risk-alert](https://github.com/mljadama/maternal-health-risk-alert) | DHIS2 high-risk detection |
| [rubayatkhan/who-anc-skill](https://github.com/rubayatkhan/who-anc-skill) | WHO ANC SMART as a Claude skill |

Kenyan precedent:
- **Mama na Mtoto Plus** won the inaugural PPH hackathon (24 July 2026) with app plus USSD danger-sign logging that alerts the facility and the CHP ([Eastleigh Voice](https://eastleighvoice.co.ke/health/382799/kenyan-students-win-inaugural-pph-hackathon-with-live-saving-maternal-health-tool)).
- **MediBora** connects mother, CHW and clinician via app, SMS and USSD ([Prime Progress](https://primeprogressng.com/spotlight/when-pregnancy-is-not-a-risk-african-students-build-ai-system-for-danger-warning/)).

**Implication.** A judge who has seen any of these will read "danger-sign triage + explainable rules + referral" as a commodity. Lead with the reconciliation and the contestable handoff.

### 6.4 Research Literature (2020 To 2026)

**Interpretable or neuro-symbolic maternal CDS.**

| Paper | Finding | Relevance |
|---|---|---|
| Scoping review of 19 interpretable CDSS in high-risk pregnancy ([BMC Pregnancy Childbirth, Jan 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12870301/)) | SHAP dominates; evaluations mostly retrospective; minimal clinician involvement; alert fatigue and workflow misalignment in deployed systems; very few real deployments (iDeliver in Kenya cited); **no symbolic longitudinal reasoning or contestable handoff described** | Confirms the gap |
| SK-MOEFS fuzzy-rule pre-eclampsia classifier ([PMC12190940](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12190940/)) | Accuracy 91%, AUC 0.89 | Rules can perform |
| Hybrid fuzzy-XGBoost, Bangladesh ([arXiv 2601.07866](https://arxiv.org/pdf/2601.07866)) | 71.4% of 14 clinicians preferred the hybrid explanations; only 54.8% trusted it for clinical use; clinicians asked for obstetric history and gestational age, which are **longitudinal inputs** | Clinicians want history |
| Graph-neurosymbolic CDS with Horn-clause rules ([PMLR v319](https://proceedings.mlr.press/v319/akande26a.html)); TrustKG ([L3S](https://www.l3s.de/trustkg-reliable-ai-for-medical-decision-making/)) | Generic, not maternal | |
| **Neuro-symbolic guideline conflict resolution** ([arXiv 2604.17340, Apr 2026](https://arxiv.org/pdf/2604.17340)) | Multi-agent guideline-to-logic translation with SAT verification; **90.6% of conflicts were "local"** (overlapping rule conditions); **F1 0.861, beating LLMs** | Direct support for "symbolic reconciliation beats LLM debate" and for MeTTa as a conflict-handling substrate. Note: it resolves conflicts between *guidelines*, not *patient evidence* |
| Argumentation-based CDS for conflicting guidelines (ASPIC-G; Čyras & Oliveira) ([Argument & Computation 2021](https://journals.sagepub.com/doi/full/10.3233/AAC-200523); [arXiv 1902.07526](https://arxiv.org/pdf/1902.07526)) | Formal precedent for an agent pair resolving claims with explicit attack and support | Mizani's "defeat" relation is in this tradition |

**LLMs for maternal care.**

| Paper | Finding | Relevance |
|---|---|---|
| India maternal chatbot ([arXiv 2603.13168](https://arxiv.org/pdf/2603.13168)) | Stage-aware triage with expert templates; **86.7% emergency recall on 150 cases**; authors call for "defense-in-depth" and multi-method evaluation; missed-emergency vs over-escalation trade-off | LLM triage misses about 1 in 8 emergencies |
| **ObGynLongBench** ([arXiv 2609.07601, Sep 2026](https://arxiv.org/pdf/2609.07601)) | LLMs do well when evidence is handed to them; **accuracy drops when they must pull evidence from full pre-decision pregnancy histories**; earlier failures predict later ones | **The strongest 2026 citation for why longitudinal maternal reasoning should be symbolic and explicit rather than left to an LLM's context window** |
| RAG over Colombian maternal guidelines ([Biomédica 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931962/)) | Context precision below 0.39 for all 7 LLMs; "final decisions must remain with specialists" | |
| Systematic review of GPT maternal agents ([PMC12862967](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12862967/)) | Review | |
| Multi-agent medical LLM debate ([MedAgents](https://arxiv.org/abs/2311.10537v4); [MAD benchmark](https://neurips.cc/virtual/2023/75421)) | LLM debate on exam QA | Existing "two agents" medical work is LLM debate, not symbolic patient-evidence reconciliation |

**Longitudinal signals that are clinically defensible.** BP level and visit-to-visit variability in CLIP ([Magee 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8284372/)); Hb trajectory and PPH ([IJWH](https://www.dovepress.com/hemoglobin-trajectory-during-pregnancy-and-postpartum-hemorrhage-a-ret-peer-reviewed-fulltext-article-IJWH); [LSHTM](https://www.lshtm.ac.uk/node/383046)); **ISSHP onset timing needs memory** ([ISSHP](https://pmc.ncbi.nlm.nih.gov/articles/PMC11588921/)); caution on "rising BP" alone ([Brown 1999](https://read.qxmd.com/read/10453825/evaluation-of-a-definition-of-pre-eclampsia)). Details in section 5.17.2.

**Contestability and explanation risk.**

| Source | Finding | Design response in Mizani |
|---|---|---|
| ConGaIT "Contest & Justify" pattern ([arXiv 2507.22300](https://arxiv.org/html/2507.22300v1)) | Clinician contestation of AI | The contest action on any premise |
| **Explanations can backfire** ([FAU glaucoma referral study](https://open.fau.de/handle/openfau/38109)) | Post-hoc explanations **increased over-reliance on wrong AI recommendations**; human-AI teams (60%) underperformed the AI alone (80%) | Make the receiving clinician *check premises*, not just read a rationale; contest is a first-class action, not a footnote |
| Override comments as CDS fuel ([Healthcare IT News, "cranky comments"](https://www.healthcareitnews.com/news/how-cranky-comments-can-help-spot-cds-alert-errors)) | Override comments spot CDS alert errors (Partners HealthCare) | P1: override becomes a reviewed rule patch |
| Override ambiguity ([Mindbowser summary](https://www.mindbowser.com/alert-fatigue-healthcare/)) | Most CDS cannot tell "alert wrong" from "alert right but proceeding", so cannot learn | Contest records a premise and a reason, which disambiguates |

### 6.5 OpenCog / MeTTa / Hyperon Healthcare Prior Art

- Hyperon framework paper ([arXiv 2310.18318](https://arxiv.org/pdf/2310.18318)): no clinical application.
- The Fetch.ai x SingularityNET "medical agent MeTTa" example ([Innovation Lab](https://innovationlab.fetch.ai/resources/docs/examples/singularityNet/medical-agent-metta)) is explicitly a **toy**: symptom → disease → treatment graph (flu, migraine), one keyword per query, disclaimers. This is the bar for MeTTa health demos, and it is low.
- `gh search repos` for "metta medical / health / clinical / pregnancy / diagnosis / symptom" and "hyperon healthcare / medical" returned **zero** repositories.
- Previous MeTTa hackathon tracks (Knowledge Graphs, Media Identity, Real-World Agents, Visual Agents) had no healthcare winner ([Luma](https://luma.com/y5jblri6)).
- No SingularityNET Deep Funding proposal on maternal health found ([Deep Funding](https://deepfunding.ai/)).
- **Verdict:** a clinically grounded MeTTa maternal agent would be a first in the visible MeTTa ecosystem, provided MeTTa is doing real reasoning (pattern matching over an atom space with provenance, nondeterministic rule firing, truth values), not a lookup table.

### 6.6 Sentiment And Pain Points

| Pain point | Evidence | Source |
|---|---|---|
| Referral feedback gap | Kenyan CHVs could not verify whether a referred client attended, was treated, or the outcome; community-facility linkage "sub-optimal" in Busia and Migori; eCHIS now closing the logistics loop, but nothing found closes the clinical-reasoning loop | [Living Goods](https://livinggoods.org/media/closed-loop-for-referrals-follow-up-of-maternal-neonatal-and-child-health-integrated-community-case-management/); [Health Policy & Planning via CHW Central](https://chwcentral.org/resources/factors-influencing-community-facility-linkage-for-case-management-of-possible-serious-bacterial-infections-among-young-infants-in-kenya/); [Medic roundup](https://unjobs.org/channels/TCrYgB812EXuz7Y0yLTGGNsXLi03/GPHorre4g-0) |
| Referral notes are poor | Northern Ghana: **98.2% of 217 maternity referral forms incomplete**; only **11.1%** more than 75% complete; reasoning and treatment times missing; illegible handwriting. Kenya's MOH 100 has free-text reason, treatment and comments plus back-referral | [PMC8925182](https://pmc.ncbi.nlm.nih.gov/articles/PMC8925182/); [MOH 100](https://tciurbanhealth.org/wp-content/uploads/2018/04/Community-Referral-form-MOH-100.pdf) |
| Care at the facility is the killer delay | CEMD: sub-optimal care in 81.4% (2014) to 98.1% (2015/16). Press: 72% of first-CEMD deaths outside working hours; obstetrician involved in 1 in 9 (the same article's "92% poor care" is not used; see section 5.7) | [LSTM abstract](https://research.lstmed.ac.uk/en/publications/improving-the-quality-of-maternal-and-newborn-health-care-in-keny/); [Nation Newsplex](https://nation.africa/kenya/newsplex/most-maternal-deaths-occur-out-of-office-hours-says-study-17060) |
| eCHIS data trust | No entry validation, no change-tracking; connectivity forces paper; ageing phones; stipends unpaid up to 13 months; CHPs want refresher training | [Amref](https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/); [Standard](https://www.thestandard.ke/business/amp/coast/article/2001519721/over-1400-chps-protest-over-13-month-stipend-delay); [People Daily](https://peopledaily.digital/news/ruto-promises-new-smartphones-and-stipend-increase-for-community-health-promoters/amp) |
| Data-entry burden | Double entry into registers and phones; higher workload while learning | [CHW mHealth scoping review](https://chwcentral.org/resources/mobile-health-mhealth-applications-for-community-health-workers-in-low-and-middle-income-countries-a-scoping-review/) |
| Alert fatigue | Acceptance drops about 30% per extra reminder per encounter; Penda deliberately used tiered traffic lights | [Textbook of Digital Health](https://www.textbookofdigitalhealth.com/glossary/alert-fatigue.html); [OpenAI/Penda](https://openai.com/index/ai-clinical-copilot-penda-health) |
| Scepticism about AI triage | "What happens when the system gets a message wrong?"; Babylon's collapse; Kenyan frontline workers want AI tools that "protect clinical autonomy" | [WUSF](https://www.wusf.org/2026-09-17/to-prevent-deaths-in-childbirth-kenyan-moms-turn-to-an-ai-powered-chatbot); [Digital Health](https://www.digitalhealth.net/2018/11/lancet-review-babylons-ai/); [JMIR mHealth 2026](https://mhealth.jmir.org/2026/1/e81829) |
| Social media | No Reddit or X threads specific to Kenyan CHP tools surfaced (NOT FOUND) | |

### 6.7 Novelty Verdict

**Already done (do not claim as novel):**

| Pillar | Prior art |
|---|---|
| Danger-sign rules from WHO guidelines | WHO SMART ANC CQL; CHT forms; 10+ hackathon repos |
| "Explainable / not black box" deterministic triage | SafeMother, Maitri, mamacare |
| Digital referral with outcome notification | eCHIS to TaifaCare (June 2026); Living Goods |
| Per-mother longitudinal record | eCHIS/CHT, PROMPTS history, Haven, My-baby |
| Risk scores from serial vitals | CLIP/POM, PIERS-ML consecutive prediction |
| LLM triage with human escalation | PROMPTS, Penda, India chatbot |

**Not found anywhere (defensible novelty):**

1. **Symbolic reasoning over cross-visit and cross-site evidence with provenance.** SMART ANC is single-contact; CHT stores BP as yes/no; LLMs degrade on long histories (ObGynLongBench).
2. **The referral as a contestable proof.** The receiving clinician challenges one premise (for example "BP not repeated after rest"); the agent recomputes and shows which conclusion survives. Maitri has an audit trail but no contestation; ConGaIT has contestation but is not maternal, not symbolic and not about handoffs.
3. **Two agents reconciling conflicting maternal readings** (home vs facility BP, reported vs observed fetal movement, stale Hb) using explicit measurement-protocol knowledge. Existing multi-agent medical work is LLM debate on exam QA; symbolic conflict resolution exists for guidelines, not for patient evidence between care levels.
4. **Override turned into a reviewed rule patch with a visible diff** in maternal CDS. Override mining exists in EHR medication alerts, not in guideline-encoded CHW tools.
5. **Any of the above in MeTTa.**

**How Mizani's claims map to this verdict:** Mizani claims 1, 2, 3 and 5 as P0 and 4 as P1 (build.md section 1). It does not claim novelty for the danger-sign rules themselves, which it transcribes from WHO and cites.

### 6.8 Risks In The Framing And How Mizani Answers Each

| # | Risk | Evidence | Mizani's answer |
|---|---|---|---|
| 1 | "Rising BP" as a trend trigger is clinically weak | 30/15 mmHg rise below 140/90 not predictive ([Brown 1999](https://read.qxmd.com/read/10453825/evaluation-of-a-definition-of-pre-eclampsia)) | Use (a) ISSHP onset timing, (b) persistence across contacts and witnesses, (c) BP variability only as research context. No "rising BP" alert on its own |
| 2 | "Falling Hb" needs facility labs | CHP kit has no Hb meter ([kit list](https://deputypresident.go.ke/sites/default/files/2024-05/Community%20Health%20Stipends%20Speech%20Formatted.pdf)) | Hb lives on the facility side; that split is a reason for two witnesses |
| 3 | CLIP's null result will be the sharpest question from a knowledgeable judge | [CLIP India](https://ecommons.aku.edu/pakistan_fhs_mc_women_childhealth_wc/115); [CLIP Mozambique](https://scholars.aku.edu/en/publications/community-level-interventions-for-pre-eclampsia-clip-in-mozambiqu/) | CLIP improved *detection*; Mizani targets the *handoff and the facility response* (Delay 3), which the CEMD shows dominates (sub-optimal care in 81.4% to 98.1% of reviewed deaths). (The original landscape note phrased this as "92% poor care"; we use the abstract figures instead, see section 5.7) |
| 4 | "Glass box" can increase over-reliance | [FAU](https://open.fau.de/handle/openfau/38109) | The facility side actively contests premises |
| 5 | Scope: memory + trends + audit + override learning + missing data + conflict handling is three solo tracks in 12 hours | Solo brief: "One feature, proven" | One loop (offline decide, sync, reconcile, contest); override learning is P1; Jev rubric scoring flagged buildability as the weakest criterion (section 7.4) |
| 6 | Learning rules from overrides is a safety hazard if automatic | [HL7 CRMI](https://hl7.org/fhir/uv/crmi/en/artifact-lifecycle.html) | "Proposed patch → human review → versioned", never automatic |
| 7 | Integration realism: eCHIS owns the CHP UI | [Medic](https://medic.org/stories/medic-partners-with-kenyan-government-to-transform-community-health/) | Position as a reasoning service behind eCHIS/TaifaCare (FHIR in, proof out) in What's Next |

### 6.9 The Alternative Angles And The Combination Adopted

**A. "Two-Witness Referral" (recommended; headline: two agents resolving a conflicting claim).** At 21:40 the CHP-side agent records home BP 152/98 at 34 weeks plus a new headache; the night-shift facility agent records 136/86 on arrival and "no headache now". Instead of averaging, they reconcile in MeTTa with **provenance atoms** (who measured, device, repeated after rest per ANCDT04, time, gestational age), **memory atoms** (BP at 14 weeks 118/76, so new onset after 20 weeks per ISSHP), and **protocol rules** (an unrepeated reading has weak support; treatment en route explains a lower facility BP; symptom absence after analgesia does not refute earlier presence). Output: a resolved claim with a truth value, surviving and defeated premises (with reasons), and an action. Why it should work: home vs clinic BP conflict is recognised ([UCT GHI](https://journals.uct.ac.za/index.php/GHI/article/download/836/672)); eCHIS lacks validation and change-tracking; CHT's sync conflict handling is document-level, not clinical ([CHT offline-first](https://docs.communityhealthtoolkit.org/technical-overview/concepts/offline-first/)); symbolic methods beat LLMs at local-conflict detection ([arXiv 2604.17340](https://arxiv.org/pdf/2604.17340)); evidence is genuinely split across sites (CHPs measure BP; facilities measure Hb and urine protein, [SMART ANC ANCDT12](https://github.com/WorldHealthOrganization/smart-anc/tree/master/input/cql)). Original 12-hour build: about 25 MeTTa rules from ANCDT01, ANCDT04, ANCDT17 and ISSHP; 2 agent processes; 3 scripted cases (agree; conflict resolved toward referral; conflict resolved toward "repeat in 15 min"); rendered referral-proof HTML.

**B. "Contestable Referral Proof + Override-to-Diff" (headline: auditable decision).** Every referral is a proof tree mapped onto MOH 100 fields. The receiving clinician taps one premise ("proteinuria ++ was from 3 weeks ago, stale") to contest it; the agent re-derives live. If the clinician overrides, the agent proposes a rule patch (for example "proteinuria evidence expires after 7 days") as a before/after MeTTa diff; a reviewer approves v1.1; "replay" shows which past cases would change. Evidence: 98% of referral notes incomplete; override comments fuel CDS fixes; contestation counters over-reliance; versioned knowledge artifacts are standard. Risk: overlaps Maitri's audit-trail framing; the differentiator is live re-derivation plus the diff.

**C. "Offline Decision, Reconciled Later" (headline: rule update with visible diff).** The CHP device decides offline under rule pack v3; the county publishes v4 after a death review; on sync the agent re-evaluates every offline decision under v4 and flags changes ("2 women now meet urgent referral") with the rule diff. Evidence: connectivity forces paper ([Amref](https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/)); CHT is offline-first ([CHT](https://docs.communityhealthtoolkit.org/core/overview/offline-first)); the SMART L3 guidance asks national adaptations for feedback mechanisms ([SMART L3 checklist](https://smart.who.int/ig-starter-kit/v1.0.0/checklist.html)). Risk: less vivid on video, less maternal-specific.

**Combination adopted (and how build.md implements it).**

| Landscape recommendation | build.md implementation |
|---|---|
| Build A as the core | P0.1 to P0.5: two agent processes, offline queue, reconciliation, answer diff |
| Present the output as B's contestable proof | P0.2 `contest`; the Reconciliation screen; the video's contest beat |
| End with one 30-second override→diff moment from B | P1.1, time-boxed to 75 minutes |
| Keep per-mother memory but demote it to substrate | The 14-week BP from facility memory makes the onset "new"; memory screen is supporting |
| Make missing and conflicting data first-class | "Missing is not normal" design principle; `unknown` blocks a rule |
| Rename away from "danger-sign checker" | Name **Mizani** ("scales"), tagline "Two witnesses, one referral" |
| Also from C: the offline-then-reconcile story | The Agent Without Borders option 2 is the platform problem we enter |

Note on the scenario numbers: the landscape sketch used facility 136/86 and a 14-week BP of 118/76; build.md's final Scenario A uses facility 138/88 (40 minutes after oral nifedipine), a repeat 148/96, dipstick 2+, and 116/74 at 14 weeks. The research sketch and the build scenario are both synthetic; build.md is authoritative for the demo.

### 6.10 Search Log (For Reproducibility)

- **Web searches:** PROMPTS/UlizaLlama, SMART ANC DAK, eCHIS, CHT, Living Goods, CommCare, OpenSRP, Safe Delivery, Safer Deliveries, mMitra/Kilkari, MomConnect, Babylon, Ada, Ubenwa, PeriGen, Google ultrasound, PIERS family, CRADLE, CLIP/POM, Penda AI Consult, iDeliver, LLM maternal chatbots, ObGynLongBench, interpretable CDSS review, neuro-symbolic guideline conflicts, contestable AI, override mining, BP variability, Hb trajectory, ISSHP, CHP kit, Confidential Enquiry, referral documentation audits, Deep Funding, MeTTa hackathons, Gemma 4 Good winners, Kenyan PPH hackathon.
- **`gh search repos` queries:** metta {maternal, health, medical, clinical, diagnosis, symptom, pregnancy}, hyperon {healthcare, medical}, maternal {triage, referral, danger signs, risk agent}, preeclampsia, antenatal, smart-anc.
- **Code inspected:** `WorldHealthOrganization/smart-anc` `input/cql/ANCDT01/04/17.cql` and `ANCContactDataElements.cql`; `medic/cht-core` `config/default/forms/app/pregnancy_home_visit.xml` and `pregnancy_danger_sign.xml`.

---

## 7. Alternatives Considered And The Decision

A time-boxed scan on 2 October 2026, about 09:30 to 09:50 EAT, asked whether any other idea beat the maternal two-witness referral. Method: `gh search repos` (2026-created filters), `gh search code` for MeTTa files, web search, and a live API probe. Breadth over depth; anything load-bearing was flagged for re-verification.

### 7.1 Saturation Snapshot (GitHub, 2026-Created Repos)

| Area | Finding | Repos |
|---|---|---|
| "Two Agents One Truth" clones | Generic "two agents argue" is crowded; domain specificity matters | [harsha-glitchedout/two-agents-one-truth](https://github.com/harsha-glitchedout/two-agents-one-truth) (WhatsApp scam-message checker, 2026-09-27); [yuxufjameel-cmd/subzero-two-agents-one-truth](https://github.com/yuxufjameel-cmd/subzero-two-agents-one-truth) (generic, 2026-09-27); [vishnuv41/Two-Agents-One-Truth](https://github.com/vishnuv41/Two-Agents-One-Truth) (2026-09-29); [celstro/Med-Verdict-Two-agents-One-truth](https://github.com/celstro/Med-Verdict-Two-agents-One-truth) (2026-09-30) |
| "Agent Without Borders" | **Zero repos found by name. Still open.** | |
| BASIX | [katelyn-signa/courtlens.BASIX.MARKET](https://github.com/katelyn-signa/courtlens.BASIX.MARKET) (2026-09-30); fractional NFT repos exist but none Omega-based | [kameswarar/FractionalNFT](https://github.com/kameswarar/FractionalNFT) (a TechCrush capstone) |
| Kenyan MeTTa competitor to watch | MeTTa/Hyperon reasoning for "agriculture, weather, infrastructure resilience", Swahili naming; overlaps flood/agri, not maternal | [dgithinjibit/Tina-X](https://github.com/dgithinjibit/Tina-X) |
| Other Omega hackathon repos | Google AI Studio boilerplate; low bar for technical execution if you actually run MeTTa on PeTTa | [Dhrubojyoti07/Omega](https://github.com/Dhrubojyoti07/Omega); [2528017-spandan-off/omega-hackathon](https://github.com/2528017-spandan-off/omega-hackathon) |
| Zero hits | MeTTa + flood, MeTTa + crop, chama + agent, livestock disease agent, land dispute agent, offline-first agent reconcile, "phigital" | |

### 7.2 Each Alternative

| # | Idea | Pitch | Fit | Need (evidence) | Saturation | Data | Judge appeal | Risks |
|---|---|---|---|---|---|---|---|---|
| 1 | **Mafuriko Two-Witness** (flood evacuation) | A village DRR volunteer's offline Omega agent decides "prepare / move livestock / evacuate" from a small MeTTa rule pack over community observations (river mark, rain hours, upstream calls); the county agent reconciles with GloFAS discharge and rainfall forecasts and explains the change in Swahili | Agent Without Borders 02 + 01; Two Agents One Truth (community witness vs model witness); solo "two agents resolving one conflicting claim" and "one auditable decision"; strongest fit to the 20% Sustainability Impact (climate adaptation) | OND 2026 El Niño >90% probability; 18 counties flagged high-risk (Tana River, Kisumu, Busia, Nairobi and others); Kenya Red Cross anticipatory action saved families in Tana River (May 2026) ([Kenyans.co.ke](https://www.kenyans.co.ke/news/126050-interior-ministry-identifies-high-risk-counties-ahead-el-nino-2026); [Dawan Africa](https://www.dawan.africa/news/early-warnings-save-lives-as-flood-threat-grows-in-tana-river); [Save the Children](https://resourcecentre.savethechildren.net/document/lessons-in-anticipatory-action-an-operational-pilot-for-flooding-in-kenya)) | Many generic 2026 flood apps (Egypt, Sri Lanka, India); none on MeTTa/Omega; none framed as community-vs-sensor reconciliation; Tina-X adjacent | Excellent: Open-Meteo Flood API (GloFAS) and forecast API free and keyless, probed live for Tana Delta. Caveat: the chosen grid cell returned 0 m3/s, so pick the river cell carefully or replay a 2023/2024 flood window | High for Sustainability Impact and timeliness; Wanjiru relevance; Goertzel: PLN revision of testimony vs forecast | Life-safety claim; reconciliation mostly numeric; memory is about a place, not a person; video less emotional |
| 2 | **Homa ya Bonde** (Rift Valley Fever, One Health) | A community animal health worker's offline agent flags suspected RVF (abortion storms, sudden lamb deaths, nearby flooding) with a MeTTa case-definition pack; the county vet agent reconciles with rainfall anomalies and lab results and explains (Swahili / Maa) the upgrade or downgrade | Agent Without Borders 02 + 01; Two Agents One Truth; "one agent learning/updating a rule" (case definition tightens after a lab negative) | Explicit 2026 El Niño RVF warning; DVS enhanced surveillance; ILRI found unreported RVF circulation in 2023/24 El Niño ([Dawan Africa](https://www.dawan.africa/news/el-nino-raises-fresh-rift-valley-fever-threat-across-east-africa); [ILRI](https://www.ilri.org/index.php/knowledge/publications/unreported-rift-valley-fever-virus-circulation-during-2023-2024-el-nino); [Citizen Digital](https://citizen.digital/article/veterinary-association-calls-for-urgent-action-to-shield-livestock-from-el-nino-n384049)) | Only academic RVF modelling repos (Uganda SDM, Cameroon risk maps); no agent entries | Public case definitions (FAO/CDC); rainfall from Open-Meteo; herd data synthetic | Medium-high: One Health + climate is very "sustainability"; less intuitive for video judges | Niche; must learn RVF clinical signs fast; health-adjacent; synthetic herd data |
| 3 | **Dawa Halisi** (pharmacy dispensing check) | A rural chemist's offline agent checks a pack against a cached recall pack; on reconnect it receives new PPB recalls and shows why yesterday's "safe to dispense" became "quarantine and return" | Agent Without Borders 02 (very clean "answer changed because new evidence arrived" story); "one auditable decision" | PPB ran 58 recalls and 14 rapid alerts since Jan 2025, closed 200 outlets; falsified Augmentin; multi-agency crackdown ([Eastleigh Voice](https://eastleighvoice.co.ke/health/374181/kenya-unveils-multi-agency-team-to-crack-down-on-fake-and-substandard-medicines); [Capital FM](https://www.capitalfm.co.ke/business/2025/04/govt-recalls-substandard-batches-of-paracetamol-augmentin)) | Many 2026 "drug verification" repos (NAFDAC-style, Flask dashboards); none MeTTa | Good (public PPB recalls) | Medium; Goertzel/iCog may see a database lookup | Thin reasoning; crowded; health overlap with MED-VERDICT and MedTriage |
| 4 | **Chama Mizani** (savings-group loan decision) | A chama treasurer agent with persistent member memory decides a loan with a contestable proof; a second member's agent disputes a contribution record (M-Pesa SMS vs paper book) and they reconcile | "One auditable decision", "one NPC with persistent memory", Two Agents One Truth; BASIX workflow tie-in | Defaults rising (16.6% of borrowers in 2024); fivefold rise in digital-lending complaints ([Capital FM](https://www.capitalfm.co.ke/business/2025/07/106877/)); chama dispute data not found | Direct overlap with basix-trustgate; several 2026 chama/ajo repos on Stellar ([CIRCLEUP-AJO/CIRCLEUP](https://github.com/CIRCLEUP-AJO/CIRCLEUP); [presidoclintonbased-alt/ajo](https://github.com/presidoclintonbased-alt/ajo); [SiroDevs/e-chama](https://github.com/SiroDevs/e-chama); [kim214/zetu](https://github.com/kim214/zetu)) | Synthetic, easy | Medium; relatable to Kenyan judges; weaker Sustainability Impact | Head-on with trustgate; credit-scoring fairness questions |
| 5 | **Sanaa Halisi** (BASIX phigital listing for Kenyan artists) | An onboarding agent remembers a Nairobi artist across sessions, reconciles provenance claims (gallery receipt vs artist statement vs photo metadata) before a phigital listing, tracks fractional co-ownership by a collective | BASIX.Market Mature Build; "one BASIX workflow" | Kenyan artists lose 40 to 50% to galleries; Kenyan NFT Club "Mbogi Onboarding Fund"; Kasuku NFT marketplace; mostly 2021 to 2023 evidence ([Right Click Save](https://rightclicksave.com/article/what-nft-community-means-for-kenya-and-nigeria); [Standard](https://www.standardmedia.co.ke/evewoman/living/article/2001445695/kasuku-firm-bets-on-nfts-to-disrupt-art-economy)) | CourtLens on BASIX; generic fractional-NFT repos | Synthetic; BASIX API access unknown | XR execs may like it; Goertzel/iCog less; weak Sustainability Impact | Solo must build on Omega anyway; NFT narrative dated; BASIX integration risk by 21:00 |
| 6 | **Ardhi Mbili** (land record reconciliation) | Two agents hold conflicting beliefs about a parcel (Ardhisasa title vs elder testimony vs survey beacon photos) and reconcile with provenance-weighted PLN, explained in Swahili | Two Agents One Truth; "one auditable decision" | Double titling at the Coast; land cases dominate courts; Ardhisasa mandatory since March 2025 ([People Daily](https://peopledaily.digital/news/surveyors-urge-speedy-digitisation-of-land-records-to-curb-fraud/amp); [Kenyans.co.ke](https://www.kenyans.co.ke/news/125050-court-explains-why-many-kenyans-lose-their-land-cases)) | No agent repos; conceptually overlaps CourtLens | Hard; all synthetic | Medium; politically sensitive; weak Sustainability Impact | Legal overclaim; looks like CourtLens; hard to make vivid |

**Considered and dropped:**
- **Crop disease / extension advisory.** Real need (1 extension officer per about 5,000 farmers vs FAO 1:400, [AGRA](https://agra.org/partnerships-aim-to-rebuild-kenyas-agriculture-extension-services/)), but saturated: PlantVillage Nuru already works offline in Swahili ([Self Help Africa](https://selfhelpafrica.org/uk/ai-agriculture/)); Zindi crop-pest hackathons; Farmlingua BGI Nexus grant; Tina-X MeTTa agri.
- **Ambulance/emergency referral.** Overlaps MedTriage and the maternal referral itself.
- **KU student support.** The KU MOU is a nice hook, but need evidence is thin and "student mental health agent" is a crowded generic category with safety risk.

### 7.3 Ranked Comparison (Qualitative)

| Rank | Idea | Tech fit (MeTTa/PLN/memory) | Video clarity | Sustainability | Uncontested | Data for demo | Overall |
|---|---|---|---|---|---|---|---|
| 1 | Mizani maternal referral | High (longitudinal memory, provenance, revision) | Very high | Medium-high (SDG 3, UHC) | Yes | Synthetic but credible (MOH and WHO guidelines) | **Best** |
| 2 | Mafuriko flood two-witness | High | High | Very high (climate, timely) | Mostly (Tina-X adjacent) | Live free API | Close second |
| 3 | RVF One Health | High (rule update after lab) | Medium | High | Yes | Synthetic herd plus live rain | Strong dark horse |
| 4 | Dawa Halisi pharmacy | Medium-low (lookup-ish) | High | Medium | No (generic verifiers) | Good (PPB recalls) | Mid |
| 5 | Chama loan audit | Medium | Medium | Low-medium | No (trustgate) | Synthetic | Mid-low |
| 6 | BASIX phigital artist | Low-medium | Medium | Low | No (CourtLens on BASIX) | Synthetic, API risk | Low |
| 7 | Ardhi land reconciliation | Medium | Low-medium | Low | Partly (CourtLens) | Hard | Low |
| 8 | Crop disease advisory | Medium | Medium | High | No (Nuru, Farmlingua) | Good | Dropped |

### 7.4 Jev Rubric Scoring Of The Four Finalists

**Method (VERIFIED, `jev-test/score_ideas.py`, raw output `jev-test/idea_scores.json`).** One live request to `POST https://api.typesafe.ai/v1/systemone`, model pinned `jev-1.13.0`, state `{"ideas": {...}}` holding one paragraph per candidate, and 24 **Score** questions (4 ideas × 6 criteria). Each Score has five ordered levels: very weak (0), weak (1), moderate (2), strong (3), very strong (4). Jev returns a probability-weighted level index (fractional) and a confidence derived from the distribution's concentration (section 8.4).

**Criteria (as written in the request):**

| Key | Definition sent to Jev | Weight we applied |
|---|---|---|
| `technical_showcase` | How well the idea lets a solo builder show real Omega/MeTTa features (stateful memory that changes the answer, auditable truth-valued reasoning, reconciliation) as the core feature rather than decoration | 0.30 |
| `video_story` | How compelling and clear a 3-minute demo video would be for a mixed panel of AGI researchers, media producers and business executives | 0.25 |
| `track_fit` | How precisely the idea matches "The Agent Without Borders" (offline-first decision reconciled with a fuller Omega agent, local-language reasoning) or "Two Agents, One Truth" | 0.25 |
| `sustainability_impact` | Size and credibility of real-world social impact in East Africa, and a realistic adoption path with institutions | 0.10 |
| `novelty` | Uniqueness compared with typical 2026 hackathon entries and existing products | 0.05 |
| `buildability` | How realistic it is for one developer to build a polished working alpha in about 8 hours | 0.05 |

The weights are **ours**, chosen to mirror the all-track rubric (30% technical, 25% video, 25% fit) with the remaining 20% split across impact, novelty and buildability. They are not an official rubric.

**Results (score on 0 to 4, with Jev confidence in brackets):**

| Idea | Technical showcase | Video story | Track fit | Sustainability impact | Novelty | Buildability | **Weighted (0 to 4)** |
|---|---|---|---|---|---|---|---|
| **Mizani maternal** | 3.93 (0.94) | 3.28 (0.68) | 3.99 (0.99) | 3.28 (0.66) | 3.46 (0.58) | **0.74 (0.66)** | **3.53** |
| Mafuriko flood | 2.81 (0.73) | 2.43 (0.52) | 3.57 (0.64) | 2.64 (0.66) | 1.75 (0.62) | 1.54 (0.47) | **2.77** |
| RVF One Health | 2.71 (0.65) | 1.67 (0.59) | 3.15 (0.67) | 2.06 (0.64) | 2.58 (0.59) | 1.21 (0.68) | **2.41** |
| Chama loan | 2.58 (0.50) | 1.72 (0.60) | 1.65 (0.31) | 2.02 (0.58) | 1.05 (0.78) | 1.76 (0.32) | **1.96** |

Weighted score = 0.30 × technical + 0.25 × video + 0.25 × fit + 0.10 × impact + 0.05 × novelty + 0.05 × buildability (COMPUTED from the raw scores; re-computed during this write-up and matching the script output: 3.53, 2.77, 2.41, 1.96).

Selected probability distributions (from `idea_scores.json`):
- Mizani buildability: P(very weak) 0.33, P(weak) 0.60, P(moderate) 0.07. The only criterion where Mizani was below every other idea.
- Mizani track fit: P(very strong) 1.00.
- Mizani technical showcase: P(strong) 0.06, P(very strong) 0.94.
- Flood novelty: P(weak) 0.34, P(moderate) 0.55 (reflecting the Tina-X adjacency stated in its paragraph).

### 7.5 Caveats Of The Scoring

1. **Our own descriptions drove the scores.** The four paragraphs were written by us and were not symmetric. The Mizani paragraph was longer and stated strengths ("No one else in the hackathon is doing maternal health or 'Agent Without Borders'"); the flood, RVF and chama paragraphs stated their weaknesses ("Memory is about places, reconciliation mostly numeric", "Niche audience, synthetic herd data", "Competes head to head..."). Jev reads text literally (section 8.5), so this framing biases the result toward Mizani. The ranking agrees with the qualitative table in section 7.3, but it is not independent evidence.
2. **The Mizani paragraph contained "92% of maternal deaths in Kenya's confidential enquiry had poor care".** That is the press figure we decided not to use (section 5.7). It may have nudged the impact score; it does not change any published number.
3. **One run, non-deterministic.** Jev is not bit-for-bit deterministic (section 8.16). The request id was printed but not persisted in the JSON.
4. **Score confidence is not correctness.** Several confidences were low (chama track fit 0.31, chama buildability 0.32, flood buildability 0.47).
5. **The weights are a judgement call.** Under the Omega rubric (30/30/20/20 with Sustainability Impact at 20%), flood's impact advantage would count more. Mizani still leads on every criterion except buildability, so the conclusion is robust to reasonable weightings.
6. **Follow-up runs (after this section was first written).** (a) Re-run with the 92% figure corrected to "sub-optimal care in 81 to 98%" (request `req_01a0fb6a5c0e7ff883c136d87b7b2de8`): Mizani 3.54, flood 2.79, RVF 2.43, chama 1.90, ranking unchanged. (b) **Balanced re-run**, all four descriptions rewritten at similar length with one strength and one weakness each (`score_ideas_balanced.py`, request `req_01a0fb6ae331767da44f3c8332c90c63`): Mizani **3.12**, flood 2.74, RVF 2.66, chama 2.30. Mizani still first, but its **novelty fell to 1.42** when the description admitted that many maternal danger-sign apps exist. Conclusion: novelty depends on pitching the two-witness reconciliation and contestable proof, not "a maternal app". See problem.md section 7.

### 7.6 How The Decision Was Made

1. **No alternative clearly beats Mizani.** Flood is the only real challenger: it wins on timeliness (El Niño rains begin this month) and has live free data. It loses on what carries more weight: the memory is about a place, not a person, so the persistent-memory angle is weaker; the reconciliation is mostly numeric, so "how and why the answer changed" is less legible to media and business judges; and a Kenyan MeTTa project (Tina-X) already works in weather and agriculture.
2. **Take flood's strength without switching.** Set the Mizani scenario during the OND 2026 El Niño rains: a flooded road is why the CHP is offline and the referral is delayed. That makes the offline-first premise concrete and earns Sustainability Impact (climate-resilient primary care) for one scene's worth of work. build.md's demo does exactly this (Kilifi County, flooded road, mobile data cut).
3. **Fallback.** Keep RVF as a fallback only if the maternal clinical content could not be made safe enough by about 13:00 EAT. (Not triggered.)
4. **Act on the weak criterion.** Jev rated Mizani's **buildability at 0.74 of 4**, its only weak criterion. That led us to cut scope hard (build.md section 1): one loop as P0 (offline decide, sync, reconcile, contest, explain); override-to-patch and the full Omega chat as time-boxed P1; USSD, Android on-device PeTTa, FHIR/eCHIS, county dashboard, DAS memory and BASIX IP registration as P2 "What's Next" only; and an explicit cut list (no auth, no real data, no native app, no maps, no machine-learned risk score, no LLM making clinical decisions).

---
## 8. Jev (TypeSafe) Findings

Research date 2 October 2026. Model answering every call: `jev-1.13.0` (alias `jev-latest`). Python SDK `typesafe-sdk` 0.7.2. Sources: [docs index](https://docs.typesafe.ai/llms.txt) and the linked pages (API, models, primitives Choice, Noul and Score, confidence, Python SDK usage, retries, exceptions and constants, JavaScript SDK, model jaggedness for jev-1.13, and the cookbooks: pre-parsed value extraction, citation check, SDE cascade, parallel questions). Copies of the pages used are in `scratchpad/jev-test/docs/`. All test code is in `scratchpad/jev-test/`. The API key was read from the shell environment only and never written to disk.

### 8.1 What Jev Is And How Mizani Uses It

Jev is TypeSafe's "System One" judgement model: it turns natural language and application state into typed judgements (Choice, Noul, Score) with probabilities. It is **not a text generator**. In Mizani, **Jev reads; Omega decides**: Jev pre-fills danger-sign toggles from a CHP's Swahili, Sheng or English note and picks today's BP from candidate spans; the CHP confirms; only confirmed observations enter MeTTa. Jev never produces a number, a threshold or a decision (build.md section 9).

### 8.2 The API

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
Content-Type: application/json
```

Also `GET /v1/models` (lists aliases). The response header `x-typesafe-request-id` (for example `req_01a0fb3e...`) identifies each call; log it.

**Request body:**

```json
{
  "model": "jev-latest",
  "state": { "visit_note": "Mama analalamika kichwa kinauma sana ..." },
  "questions": {
    "sign__severe_headache": {
      "type": "choice",
      "instructions": { "danger_sign": {"...": "..."}, "question": "According to `visit_note`, what is the status of `danger_sign` for the mother?" },
      "criteria": { "present": "...", "absent": "...", "not_mentioned": "..." }
    },
    "any_danger": { "type": "noul", "instructions": "...", "criteria": { "true": "...", "false": "..." } },
    "urgency":    { "type": "score", "instructions": "...", "criteria": ["level 0 text", "level 1 text", "level 2 text"] }
  }
}
```

Notes: `model` can be pinned to `jev-1.13.0`; `state` may be a string, object or array; question ids are **not** sent to the model; Choice allows up to 255 options and an option's value may be null; Noul criteria are optional; Score takes 2 to 10 ordered levels. `instructions` and `criteria` accept string, object or array. Reference state fields with backticks (`` `visit_note` ``).

**Multiple independent questions go in one request** (more keys in `questions`). Jev reads the state once and evaluates every question in parallel; questions cannot see each other's answers. The parallel-questions cookbook measured batching 13 questions as **12.2× cheaper and 10× faster** than 13 calls. In our test, 10 to 12 questions per note took the same about 380 ms as a 1-question call.

**Response body (a real response captured in `followup.log`):**

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "severe_headache": { "type": "choice", "choice": "present", "confidence": 1.0,
                         "probabilities": { "present": 1.0, "absent": 0.0, "not_mentioned": 0.0 } },
    "any_danger_sign": { "type": "noul", "noul": 0.97 }
  },
  "usage": { "input_tokens": 422, "output_tokens": 66 }
}
```

### 8.3 Question Types

| Type | Use for | Returns |
|---|---|---|
| **Choice** | One of a defined set | `choice` (argmax), `probabilities` per option (sum to 1), `confidence` |
| **Noul** | Is a condition true? | `noul` = P(yes) in [0, 1]; no confidence field |
| **Score** | Position on ordered levels | `score` (probability-weighted level index, can be fractional), `legend`, `probabilities` per level, `confidence` |

### 8.4 Confidence Semantics

From the docs' own explorer code: Choice `confidence = (n × p_max - 1) / (n - 1)`; Score `confidence = 1 - spread_around_peak / spread_of_uniform`. It is derived only from the distribution's concentration. **It is not a correctness guarantee**, and a Noul of 0.5 means "equally likely yes or no", not "medium". The docs warn that structural identities do not hold across questions (a Noul and a yes/no Choice on the same text, or a question and its negation, need not agree), so thresholds must be tuned per question type.

Example (COMPUTED): with 3 options and p_max = 0.88, confidence = (3 × 0.88 - 1) / 2 = 0.82, which matches the strict-convulsion result in section 8.11 (E2).

### 8.5 Limits, Pricing And Behaviour (Models Page, jev-1.13)

| Property | Value |
|---|---|
| Price | **$0.042 per million input tokens; output tokens free** |
| Cost per note (COMPUTED) | A 10-sign note request is about 2,430 (plain) to 2,980 (glossary) input tokens, so 2,870 × 0.042 / 1,000,000 = **about $0.00012 per note**, roughly **8,000 notes per US dollar** |
| Rate limits | 100K tokens/s and 40 requests/s ("adjusting dynamically"); 429 when exceeded |
| Context | 64k tokens per request total; 32k for `state` plus the single longest question |
| Modality | Text only |
| Languages | English is the primary training language; "other languages are handled but not equally well; test on your own content" |
| Data | Not trained on customer data; ZDR for enterprise customers |
| Determinism | Not perfectly deterministic (section 8.16) |
| Known jaggedness | Literal reading; **unreliable numbers, counting and date arithmetic** (do these in code); multi-hop indirection; distractor-heavy state; adversarial text; not a text generator |

### 8.6 Errors (VERIFIED Live)

| Status | Body observed or documented | SDK exception |
|---|---|---|
| 401 | `{"detail":{"error_type":"authentication_error","message":"Cannot authenticate with the server. Please check your API key and try again."}}` | `TypeSafeAuthenticationError` |
| 422 | `{"detail":[{"type":"missing","loc":["body","questions","q","choice","criteria"],"msg":"Field required",...}]}` | `TypeSafeUnprocessableEntityError` |
| 429 / 529 | Rate limit / overloaded; `retry-after` may be set | `TypeSafeRateLimitError` (`retry_after_ms`) / `TypeSafeInternalServerError` |
| No response | DNS, connection or timeout | `TypeSafeAPIConnectionError` / `TypeSafeAPITimeoutError` |

All derive from `TypeSafeError`. SDK defaults: per-HTTP-operation timeout 10 s; `RetryPolicy(max_retries=2, backoff_initial=0.5, backoff_max=5.0, backoff_jitter=0.25, http_statuses={408,429,5xx}, respect_retry_after=True, timeout=30.0)`.

### 8.7 SDKs And Gateways

- **Python:** `pip install typesafe-sdk` (or `uv add`). `TypeSafeClient` / `AsyncTypeSafeClient`; question classes `Choice`, `Noul`, `Score`; `client.system_one(state, questions, model=..., retry=..., timeout=...)`; accessors `resp.choices[id]`, `resp.nouls[id]`, `resp.scores[id]`, `resp.request_id`, `resp.raw_http_response`. Env: `TYPESAFE_API_KEY`, `TYPESAFE_BASE_URL`, `TYPESAFE_DEFAULT_MODEL`, `TYPESAFE_LOG_LEVEL` (**debug logs request bodies unredacted**, so never enable debug logging with patient notes).
- **JS/TS:** `pnpm add @typesafe-ai/sdk` (Node 20+): `new TypeSafeClient().systemOne({ state, questions: { x: choice("...", {a: null}) } })`, helpers `choice()`, `noul()`, `score()`. Server side only; never ship the key to the browser.
- Also reachable via OpenRouter (`~typesafe/jev-latest`), Vercel AI Gateway and Pydantic AI Gateway through `base_url`.

### 8.8 Live Test Design: 12 CHP Notes × 10 WHO Danger Signs

One request per note, `state = {"visit_note": note}`, one **Choice per danger sign** with three options, plus a BP selection Choice:

```python
STATUS_CRITERIA = {
    "present": "The note says the mother has this sign now (reported by her, a relative, or observed by the CHP).",
    "absent": "The note explicitly says the mother does NOT have this sign.",
    "not_mentioned": "The note says nothing about this sign either way.",
}

def sign_choice(sign: dict, with_glossary: bool) -> Choice:
    definition = {"sign": sign["name"], "definition": sign["en"]}
    if with_glossary:
        definition["swahili_and_sheng_phrases"] = sign["sw"]     # e.g. "kifafa, degedege, ..."
    return Choice(
        instructions={
            "danger_sign": definition,
            "context": "`visit_note` is a Community Health Promoter's note about a pregnant "
                       "or recently delivered mother in Kenya. It may be in English, Swahili, or Sheng.",
            "question": "According to `visit_note`, what is the status of `danger_sign` for the mother?",
        },
        criteria=STATUS_CRITERIA,
    )
```

Definitions carried the clinical boundary cases, for example swelling: "Swelling of only the feet or legs does NOT count"; convulsions: "Shivering or chills from fever are NOT convulsions". The ten signs: severe headache, blurred vision, convulsions, vaginal bleeding, fever, severe abdominal pain, reduced fetal movement, swelling of face and hands, difficulty breathing, water breaking early.

**Numbers (BP) are never generated by Jev.** Following the pre-parsed value extraction cookbook, a regex `\b(\d{2,3})\s*/\s*(\d{2,3})\b` finds every candidate span; Jev picks which one is today's BP (or `none`); code splits it into systolic and diastolic. Jev cannot invent or transpose a digit this way.

```python
cands = list(dict.fromkeys(f"{a}/{b}" for a, b in BP_RE.findall(note)))
questions["bp_today"] = Choice(
    instructions="Which value in `visit_note` is the mother's blood pressure measured at TODAY's visit? "
                 "(Ignore readings from earlier visits.)",
    criteria={c: None for c in cands} | {"none": "No blood pressure was measured today."},
)
```

### 8.9 Test Set

Set A (6 typical notes) and set B (6 adversarial notes). Ground truth labelled by us; where wording is genuinely ambiguous (for example "mild backache only" for severe abdominal pain) either `absent` or `not_mentioned` is accepted.

| Id | Language | Note (abridged) | Key truths |
|---|---|---|---|
| n1 | Swahili | "kichwa kinauma sana na anaona giza, miguu imevimba. BP 160/110. wiki 34" | Headache present, vision present; face/hands swelling NOT (feet only) |
| n2 | English | "No bleeding, no fever. baby not kicking since yesterday. Mild backache. BP today 118/76 (last visit 130/85)" | RFM present; bleeding and fever absent; BP distractor |
| n3 | Sheng | "manzi ako na homa kali, anatetemeka, tumbo inamuuma vibaya sana. Hakuna damu. Mtoto anacheza poa" | Fever present, abdominal pain present, bleeding absent, RFM absent; shivering is not convulsion |
| n4 | Swahili | "alipata kifafa ... kutetemeka mwili mzima. Uso na mikono imevimba. Hana homa. Presha 170/115" | Convulsions present, face/hands present, fever absent |
| n5 | Swahili/English | "Maji yamevunja leo, mimba wiki 32 tu. Hakuna uchungu. Anapumua vizuri, no headache" | PROM present, breathing absent, headache absent |
| n6 | Sheng/English | "Ameanza kubleed kiasi ... anashindwa kupumua akipanda stairs. Hakuna headache. BP 100/60, pulse 112" | Bleeding present, breathing present, headache absent |
| h1 | Swahili | Past fever now recovered; **her 3-year-old** has high fever; mild headache; "if she sees blood go to hospital" | Fever not present; bleeding not mentioned (hypothetical) |
| h2 | Swahili | "hajisikii mtoto akicheza kama zamani", "spotting kidogo", asked about darkness: "hapana" | RFM present (hedged), bleeding present (spotting), vision absent |
| h3 | Clinical shorthand | "G3P2 @ 36/40. c/o PV bleed ++, FM reduced. Oedema face ++. Afebrile. No SOB. Visit date 12/10. BP 150/100" | Bleeding, RFM, face present; fever and SOB absent; BP among 36/40 and 12/10 |
| h4 | Heavy Sheng | "headache mbaya mbaya, macho inaona blur, ameanza kuchizi akiongea, hajaanguka ama kutetemeka. Mguu imefura tu" | Headache and vision present; **convulsions absent** (confusion is not a fit) |
| h5 | Swahili/English | "Wiki 39. Maji yamevunja ... ameanza uchungu vizuri. Wiki jana BP 150/100, leo ni 138/88. Pulse 98" | Waters broke **at term in labour**, so not "early"; BP = 138/88 |
| h6 | Swahili | Postpartum day 3, "damu nyingi ... pedi 4 kwa saa moja", "anapumua haraka haraka", "mwili unachemka" | Bleeding, breathing and fever present |

### 8.10 Results

Each cell is 60 sign judgements over 6 notes (raw logs `run1.log`, `run_hard.log`; answers `results.json`, `results_hard.json`).

| Variant | Set A accuracy | Set B accuracy | Combined | Latency per note (median; min to max), set A / set B |
|---|---|---|---|---|
| Choice, English definitions only | 60/60 | 58/60 | **118/120** | 385 ms (368 to 418) / 387 ms (378 to 411) |
| Choice, + Swahili/Sheng phrase glossary (+ BP + Score) | 60/60 | 58/60 | **118/120** | 390 ms (372 to 465) / 384 ms (375 to 424) |
| Noul per sign (threshold 0.5, binary present vs not) | 60/60 | 59/60 | 119/120 | 398 ms (364 to 423) / 382 ms (369 to 405) |

- **BP selection: 6/6 correct, confidence 0.99 to 1.00**, including the hard distractors (`130/85` last visit, `150/100` last week, `36/40` gestation, `12/10` date).
- **No true-positive danger sign was missed** in any variant (0 false negatives on 24 "present" labels per variant).
- Latency: warm-up first call 549 to 586 ms (TLS setup), then 360 to 465 ms per request; 6 notes fired concurrently finished in 615 ms and 1,007 ms wall (two runs).
- Usage: about 2,430 input tokens (plain), 2,870 to 2,980 (glossary), 1,740 (Noul); Noul responses reported 224 output tokens for 10 questions.

### 8.11 Errors And What They Teach

| # | Note | What happened | Lesson and fix |
|---|---|---|---|
| E1 | h5 (waters broken at 39 weeks, in active labour) | Labelled "water breaking early = present": P = 0.79 (plain), 0.92 (glossary), Noul 0.69 | The docs' "literal reading / indirection" failure: "early" is a **rule** (pre-labour or <37 weeks), not an observation. **Fix VERIFIED:** ask literal facts (membranes ruptured: Choice; labour started: Choice; gestational weeks: regex candidates plus Choice) and apply the rule in code or MeTTa. Result: n5 (32 weeks, no labour, 582 ms) gives `water_breaking_early=yes`; h5 (39 weeks, in labour, 370 ms) gives `no`. **Jev extracts, MeTTa decides** (build.md rule `r_prom`) |
| E2 | h4 ("ameanza kuchizi akiongea", talking confusedly) | Read as convulsions with the plain definition (P(present) = 0.64, confidence 0.46); with the glossary flipped to absent at 0.51 vs 0.47 (confidence 0.27) | A sharper definition ("NOT convulsions: shivering, confusion, talking strangely, dizziness") gave **absent 0.88, confidence 0.82** (P present 0.11), while true eclampsia (n4) stayed **present 1.00** and the shivering case (n3) stayed not convulsions (not_mentioned 0.58, confidence 0.37). **Put clinical exclusion criteria into the definition** |
| E3 | h4, reduced fetal movement | Present with P = 0.41 and confidence 0.11 (glossary variant), a near-uniform distribution on a sign not in the note | Wrong, but confidence is extremely low, so a gate catches it |

### 8.12 Confidence Gating

Rule: status becomes `needs_review` if confidence < **0.60**, or if the answer is not "present" but P(present) > **0.15**. Applied post hoc to all 120 Choice judgements per variant: 2 errors, 1 caught (the other is the h5 over-call, fixed by decomposition), and **6 to 7 correct answers flagged for CHP confirmation (5 to 6%)**. In the end-to-end FastAPI test on the h4 note, the gate turned both doubtful answers (convulsions confidence 0.38, RFM confidence 0.21) into `needs_review`. Mizani's fail-safe: an unconfirmed `needs_review` sign is treated as present for referral rules, and the explanation says so (build.md section 6.1 principle 7).

### 8.13 Choice Versus Noul, Glossary, And Score

- **Choice vs Noul.** Noul was equally accurate on presence but loses the `absent` vs `not_mentioned` distinction, which matters clinically (an explicit "hakuna damu" denial is information; silence is not) and for the audit trail. Noul probabilities also compress toward 0.03 for both. **Recommendation: Choice with three options per sign.**
- **Glossary.** No measurable difference on these notes (Jev already understood "kichwa kinauma sana", "anaona giza", "kifafa", "kubleed", "homa") at about 20% more tokens. Keep a glossary only for terms it misses; put boundary rules (feet vs face, shivering vs fits, confusion vs fits) in the definitions, because those rules fixed the errors.
- **Score (`note_specificity`).** Values 1.34 to 1.89 with confidence 0.23 to 0.83: not discriminative. Do not use a Score as a "confidence" signal; per-Choice `confidence` and `probabilities` are the right uncertainty signals.

### 8.14 Explanation-Faithfulness Check (VERIFIED)

State = the MeTTa rule trace; one Choice per explanation **sentence** (`supported` / `contradicted` / `not_in_trace`). This is the docs' citation-check pattern.

| Sentence | Jev |
|---|---|
| "The mother has a severe headache and blurred vision." | supported, 1.00 |
| "Her blood pressure is 160/110, which meets the severe hypertension threshold." | supported, 0.99 |
| "Together these match the danger rule for pre-eclampsia, so she must be referred urgently." | supported, 1.00 |
| "Her blood pressure is normal." (injected) | **contradicted, 1.00** |
| "Give magnesium sulfate 4 g before the referral." (injected) | **not_in_trace, 1.00** |
| "She should be referred urgently." | supported, 1.00 |

360 to 372 ms per explanation; 892 and 1,025 input tokens. Use: any sentence not `supported` at or above the threshold is dropped, or the explanation falls back to a template rendered from the trace. In build.md this is P1.3, because Mizani's P0 explanations are deterministic templates that cannot add content.

```python
def faithfulness_questions(sentences: list[str]) -> dict:
    return {f"s{i}": Choice(
        instructions={"claim": s,
                      "question": "Compare `claim` with `rule_trace`, the record of what the decision rules "
                                  "observed and concluded. Is `claim` supported by `rule_trace`?"},
        criteria={"supported": "Everything `claim` states is in `rule_trace` or follows directly from it.",
                  "contradicted": "`claim` conflicts with something in `rule_trace`.",
                  "not_in_trace": "`claim` adds a fact, drug, dose, or action that `rule_trace` does not contain."})
        for i, s in enumerate(sentences)}
# state = {"rule_trace": ["(observation severe_headache present)", ..., "(action refer-urgently-to-facility)"]}
```

### 8.15 Raw HTTP And Error Probes (VERIFIED, `followup.log`)

- Raw `httpx` call: `200`, 590 ms, request id `req_01a0fb3efb7571b3b1a81acb2fd76b9f`, 422 input tokens, 66 output tokens.
- Invalid request (Choice without criteria): 422 with the `missing` detail shown in section 8.6.
- Bad key: 401 with `authentication_error`.

### 8.16 Determinism

The same request three times gave P(absent) = **0.89, 0.88, 0.94** (latencies 380, 404, 388 ms). **Store the response; do not expect to re-derive it.** Pin the model version and record the question-set hash.

### 8.17 Integration Pattern (Tested End To End)

**Call pattern.**
- Async, one shared `AsyncTypeSafeClient` per process created in the FastAPI `lifespan` (connection pooling avoids about 150 ms TLS warm-up per call). Never use the sync client inside an `async def` route.
- One request per visit note with all 10 sign Choices plus BP pick (plus gestational-age pick and the PROM sub-facts). The faithfulness check is a second request because it needs the MeTTa output.
- **Pin `model="jev-1.13.0"`** so tuned thresholds do not shift when `jev-latest` moves; log `response.model` anyway.
- Timeouts: p50 about 390 ms observed. Use `timeout=3.0` per HTTP operation and `RetryPolicy(max_retries=1, backoff_initial=0.3, backoff_max=1.0, timeout=4.0)`, so the user waits at most about 4 s before the fallback form appears.
- Key: `TYPESAFE_API_KEY` from env or a git-ignored `.env`, server only. Keep `TYPESAFE_LOG_LEVEL` at `info` or lower.
- PHI minimisation: send only the note text; strip names and phone numbers first (for example "Visited Akinyi" becomes "Visited [mother]"). Jev does not train on customer data; ZDR is enterprise-only, so ask TypeSafe before using real patient data (and see DPA s.48 to 49, section 5.20.1).

**Offline and failure fallback.** Manual checkbox entry is the primary data contract; Jev is a pre-filler, not a dependency:
1. The UI always renders the 10 danger-sign toggles (present / absent / not asked) plus BP fields.
2. Online: the note goes to `/visits/extract`; Jev's answers pre-fill the toggles; `needs_review` items are highlighted and must be tapped by the CHP before submission.
3. Offline, timeout, 429/5xx or 401: return `mode="offline_manual"` immediately; the CHP fills toggles by hand. The note can be re-extracted later for audit comparison only, never to change an already-made decision silently.
4. MeTTa only consumes CHP-confirmed observations (source `jev` confirmed, or `chp_manual`).

**Working module (abridged from `jev_service.py`):**

```python
Status = Literal["present", "absent", "not_mentioned", "needs_review"]
CONFIDENCE_FLOOR = 0.60          # tune on labelled CHP notes
PRESENT_REVIEW_FLOOR = 0.15      # P(present) above this on a non-"present" answer -> review
BP_RE = re.compile(r"\b(\d{2,3})\s*/\s*(\d{2,3})\b")

def _gate(a: dict) -> Status:
    if a["confidence"] < CONFIDENCE_FLOOR:
        return "needs_review"
    if a["choice"] != "present" and a["probabilities"].get("present", 0) > PRESENT_REVIEW_FLOOR:
        return "needs_review"
    return a["choice"]

async def extract(client: AsyncTypeSafeClient, note: str) -> ExtractionRecord:
    questions = _questions(note)
    q_hash = hashlib.sha256(json.dumps({k: v.model_dump() for k, v in questions.items()},
                                       sort_keys=True).encode()).hexdigest()[:16]
    t0 = time.perf_counter()
    try:
        resp = await client.system_one({"visit_note": note}, questions)
    except (TypeSafeAPIConnectionError, TypeSafeAPIError, TypeSafeError) as exc:
        return ExtractionRecord(mode="offline_manual", observations=[], error=type(exc).__name__)
    raw = resp.raw_http_response.json()
    ...   # gate each sign, record model, request_id, usage, latency_ms, question_set_hash, answers
    bp = raw["answers"].get("bp_today")
    if bp and bp["choice"] != "none" and bp["confidence"] >= CONFIDENCE_FLOOR:
        s, d = bp["choice"].split("/")          # verbatim span from the note, parsed in code
    ...

def make_client() -> AsyncTypeSafeClient:
    return AsyncTypeSafeClient(model="jev-1.13.0", timeout=3.0,
                               retry=RetryPolicy(max_retries=1, backoff_initial=0.3,
                                                 backoff_max=1.0, timeout=4.0))
```

Observed in `app_test.py`: an h4-style note with BP returned `200 jev 150/100 jev-1.13.0 545 ms`, with convulsions and RFM `needs_review`; pointing the client at an unreachable host returned `mode="offline_manual", error="TypeSafeAPIConnectionError"` within 1 s. Production code should catch exceptions more narrowly than `TypeSafeError` and log the error, never the note body.

**Making extraction auditable.** Store one immutable extraction event per note, linked to the MeTTa trace:

```json
{
  "event": "neural_extraction",
  "visit_id": "v_123",
  "note_sha256": "…",
  "model": "jev-1.13.0", "request_id": "req_01a0fb3e…", "latency_ms": 390,
  "question_set_hash": "5cd294809d06c3b2",
  "thresholds": {"confidence_floor": 0.60, "present_review_floor": 0.15},
  "signs": {
    "convulsions": {"jev_choice": "present", "p": {"present": 0.47, "absent": 0.51, "not_mentioned": 0.02},
                    "confidence": 0.27, "gate": "needs_review",
                    "chp_final": "absent", "confirmed_by": "chp_42", "confirmed_at": "2026-10-02T09:14Z"}
  },
  "bp": {"candidates": ["150/100", "12/10", "36/40"], "picked": "150/100", "p": 1.0, "systolic": 150, "diastolic": 100}
}
```

UI: per sign, a small bar with the three probabilities, the confidence, and a badge for who made the final call ("Jev 1.00, confirmed by CHP", "CHP changed Jev's answer", "entered manually, offline"). For BP, highlight the selected span so the reviewer sees Jev selected text rather than invented it. In MeTTa, observations carry provenance, for example `(observation convulsions absent (source chp_override (jev present 0.47)))`. Disagreements between Jev and the CHP are a free labelled dataset for tuning thresholds.

### 8.18 Design Rules Distilled

1. One Choice per sign with `present / absent / not_mentioned`; definitions include exclusion criteria.
2. Never ask Jev for numbers, dates or thresholds: regex candidates, Choice pick, code parsing (BP, gestational weeks).
3. Never ask Jev a derived or rule question ("early", "severe pre-eclampsia", "refer?"). Ask literal facts; MeTTa decides.
4. Batch every independent question for a note into one request; a second request only for things that depend on MeTTa output (faithfulness).
5. Gate on `confidence` and residual P(present); route to CHP confirmation; fail safe toward referral.
6. Pin the model version; store raw answers, request id and question-set hash; the model is not bit-for-bit deterministic.

### 8.19 Where Jev Should Not Be Used Here

Free-text generation of the explanation (Jev cannot generate; use a template from the MeTTa trace, then optionally verify with the faithfulness check); arithmetic (MAP, gestational age from LMP, shock index); anything that should be a hard clinical rule.

### 8.20 Honest Caveats

12 notes written by us (not by CHPs), one labeller, no inter-rater check. Notes are short; real notes will have spelling variation, denser code-switching and lengths not covered. English remains Jev's primary language per the docs. **This is a plausibility check, not a validation.** Before any field claim, label 100 to 200 real de-identified CHP notes and measure per-sign sensitivity, especially for convulsions, bleeding and reduced fetal movement, where a false negative is the costly error.

### 8.21 Files

All in `scratchpad/jev-test/`: `cases.py` (10 danger-sign definitions with Swahili/Sheng phrases; 12 notes with ground truth); `run_extraction.py`, `run_hard.py` (three variants, latency, scoring; logs `run1.log`, `run_hard.log`; raw `results.json`, `results_hard.json`); `followup.py` (PROM decomposition, strict convulsion definition, determinism, faithfulness, raw HTTP and 422/401 probes; log `followup.log`; raw `results_followup.json`); `jev_service.py`, `app_test.py` (FastAPI module, end-to-end and offline-fallback test); `score_ideas.py`, `idea_scores.json` (section 7.4); `docs/` (downloaded TypeSafe pages). Run: `cd jev-test && uv venv .venv && uv pip install --python .venv/bin/python typesafe-sdk httpx fastapi && zsh -lc '.venv/bin/python run_extraction.py'`.

---

## 9. Design Research Summary

Research date 2 October 2026, for a maternal-health decision-support web app using only shadcn/ui components plus Tailwind utilities. Verification: shadcn docs pulled as raw markdown (`https://ui.shadcn.com/docs/<page>.md`); the CLI run with pnpm; a default project scaffolded (`pnpm dlx shadcn@latest init -t next -d`); Stripe's production CSS bundles downloaded and tokens extracted; every contrast ratio computed with a WCAG 2.x relative-luminance script (`scratchpad/tokens/check3.py`). **The applied version lives in [build.md](build.md) sections 11 to 13.**

### 9.1 Decisions

| Decision | Recommendation | Why |
|---|---|---|
| Component base | **Base UI** (`-b base`, default since 2026-07-02); Radix still supported (`-b radix`) | Docs, blocks and new components ship for Base UI first |
| Style | `base-nova` (default, "reduced padding and margins for compact layouts"); consider `mira` (dense) or `rhea` (compact Luma) for dense clinician screens | Nova density is close to Stripe Dashboard density; style is fixed at init |
| Base colour | `neutral` at init, then **replace the tokens** with the Stripe-navy set (section 9.5) | `baseColor` cannot change after init; token overrides are the supported way |
| Font | **Inter** (sans) and **Geist Mono** or JetBrains Mono (mono) | Söhne (Stripe, Klim) is commercial; Inter is in the shadcn font registry (`@shadcn/font-inter`) |
| Icons | `lucide` (`lucide-react ^1.49`) | Default, wired into every component |
| Charts | shadcn `chart` (Recharts **v3**) | Uses `var(--chart-N)` directly, no `hsl()` wrapper |
| Forms | `Field` family + react-hook-form `Controller` + zod | The legacy `Form` page redirects to `/docs/forms` |
| Toasts | `sonner` (used by `dashboard-01`); a Base UI `toast` exists (July 2026) | Pick one; sonner has the simpler API |
| Package manager | pnpm (`pnpm dlx shadcn@latest ...`) | Docs show `npx`; the CLI detects pnpm and writes `pnpm-workspace.yaml` |

### 9.2 shadcn/ui: State Of Play (October 2026, VERIFIED By Scaffolding)

- **CLI:** `shadcn` **4.21.1** is npm `latest` (published 2026-10-01); `pnpm dlx` resolved 4.21.0 from cache during the probe. CLI v4 (2026-03-06) added presets, `--dry-run`, `--diff`, `--view`, templates, `--base`, `info`, `docs`, `registry:base` and `registry:font`.
- **Scaffold output** (`init -t next -d -n probe-app`): `components.json` with `"style": "base-nova"`, `"baseColor": "neutral"`, `"cssVariables": true`, `"iconLibrary": "lucide"`, `"rtl": false`, `"menuColor": "default"`, `"menuAccent": "subtle"`, `"tailwind.config": ""` (Tailwind v4 has no config file). Dependencies: `next 16.3.6`, `react 19.2.8`, `@base-ui/react ^1.8.0`, `class-variance-authority ^0.7.1`, **`cn ^0.4.0`**, `lucide-react ^1.49.0`, `next-themes ^0.4.6`, `shadcn ^4.21.0`, `tw-animate-css ^1.4.0`, `tailwindcss ^4`, `@tailwindcss/postcss ^4`, `prettier-plugin-tailwindcss`. Fonts: Geist (`--font-sans`) and Geist Mono (`--font-mono`) via `next/font/google`. `components/theme-provider.tsx`: next-themes with `attribute="class"`, `defaultTheme="system"`, `enableSystem`, `disableTransitionOnChange`, plus a built-in **"d" hotkey** for dark mode. `lib/utils.ts` and components use `import { cn } from "cn"`; the `cn` package (September 2026) replaces `clsx` + `tailwind-merge` (`shadcn migrate cn`).
- Preset `--defaults` = `--template=next --preset=nova`. A decoded preset example (`b27GcrRo` = Rhea): style rhea, baseColor neutral, theme neutral, chartColor neutral, iconLibrary lucide, font inter, fontHeading inherit, radius default, menuAccent subtle, menuColor default.
- **Eight styles:** Vega, Nova, Maia, Lyra, Mira, Luma, Rhea, Sera. **Three bases:** `base` (Base UI), `radix`, `aria` (React Aria).
- **Base UI API difference that bites agents:** Radix `asChild` is replaced by the `render` prop, for example `<DropdownMenuTrigger render={<Button variant="outline" size="icon" />} />` or `<SidebarMenuButton render={<Link href="/patients" />}>`. The dark-mode doc's `ModeToggle` still shows `asChild` (Radix flavour); adapt it.
- **Cannot change after init:** `style`, `tailwind.baseColor`, `tailwind.cssVariables`. Base colours: `neutral | stone | zinc | mauve | olive | mist | taupe`; **Slate and Gray are no longer listed** (though `/r/colors/slate.json` is still served).
- **Chart token caveat:** the actual CLI output for the default preset (`chartColor: neutral`) sets chart tokens to greyscale in both modes (`--chart-1: oklch(0.87 0 0)` to `--chart-5: oklch(0.269 0 0)`); the colourful values appear only in the docs.
- No built-in Timeline, Stepper, Code Block, Diff or Stat component: compose them (build.md section 13).

Sources: [shadcn llms.txt](https://ui.shadcn.com/llms.txt), [theming](https://ui.shadcn.com/docs/theming), [components.json](https://ui.shadcn.com/docs/components-json), [schema](https://ui.shadcn.com/schema.json), [installation (Next)](https://ui.shadcn.com/docs/installation/next), [CLI](https://ui.shadcn.com/docs/cli), [dark mode (Next)](https://ui.shadcn.com/docs/dark-mode/next), [chart](https://ui.shadcn.com/docs/components/chart), [forms (RHF)](https://ui.shadcn.com/docs/forms/react-hook-form), [registry](https://ui.shadcn.com/docs/registry), [blocks](https://ui.shadcn.com/blocks), [charts gallery](https://ui.shadcn.com/charts), [create](https://ui.shadcn.com/create).

### 9.3 shadcn Changelog Items That Matter (2025 To 2026)

Source: [shadcn changelog](https://ui.shadcn.com/docs/changelog).

| Date | Change |
|---|---|
| 2025-02 | Tailwind v4 support (`@theme inline`, OKLCH tokens, `tw-animate-css` replaces `tailwindcss-animate`) |
| 2025-06 | Unified `radix-ui` package; Calendar rebuilt |
| 2025-08 | CLI 3.0 and MCP server |
| 2025-10 | New components: Spinner, Kbd, Button Group, Input Group, Field, Item, Empty |
| 2025-12 | `shadcn create`; five styles (Vega, Nova, Maia, Lyra, Mira); choice of Radix or Base UI |
| 2026-01 | Base UI docs, RTL support |
| 2026-02 | All blocks available for both Radix and Base UI |
| 2026-03 | CLI v4, presets, shadcn/skills; Luma style |
| 2026-04 | `shadcn apply <preset>`, preset decode/resolve/url/open, `--pointer`, Sera style |
| 2026-05 | Rhea style, `shadcn eject`, package imports (`#components/*`), registry include/validate |
| 2026-06 | Chat components: MessageScroller, Message, Bubble, Attachment, Marker; `scroll-fade`, `shimmer` utilities; GitHub registries |
| 2026-07-02 | **Base UI is the default**; migration skill `npx skills add shadcn/ui`; **`asChild` becomes `render`** |
| 2026-07 | `shadcn/typeset`, `@shadcn/helpers` (AI SDK), React Aria base (`--base aria`), Base UI Toast |
| 2026-08 | Questionnaire (multi-step question flows), private GitHub registries, human-in-the-loop helpers |
| 2026-09 | `cn` package |

### 9.4 Stripe: Visual Language Teardown

Sources: [stripe.com](https://stripe.com), [payments](https://stripe.com/payments), [pricing](https://stripe.com/pricing), [Stripe Sessions](https://stripesessions.com), CSS bundles at `https://b.stripecdn.com/mkt-ssr-statics/assets/_next/static/css/*.css` and `https://b.stripecdn.com/docs-statics-srv/assets/{docs,frontend,sail}.*.css`, [docs](https://docs.stripe.com), [payments quickstart](https://docs.stripe.com/payments/quickstart), [dashboard basics](https://docs.stripe.com/dashboard/basics), [Stripe Apps style](https://docs.stripe.com/stripe-apps/style), [Badge](https://docs.stripe.com/stripe-apps/components/badge), [Radar risk evaluation](https://docs.stripe.com/radar/risk-evaluation), [Radar risk insights](https://docs.stripe.com/radar/reviews/risk-insights). Marketing uses an internal token system prefixed `--hds-*`; docs and Dashboard use **Sail** (`--sail-*`).

| Aspect | Findings |
|---|---|
| Typography | Marketing `--hds-font-family: "sohne-var", "SF Pro Display", sans-serif` (variable, weights 1 to 1000); code `"SourceCodePro"` weight 500. **Weights are light:** `--hds-font-weight-normal: 300`, `--hds-font-weight-bold: 400`; headings xxl to sm at 300. Heading scale (desktop / tablet / mobile rem): xxl 3.5 / 3 / 2.125; xl 3 / 2.125 / 1.75; lg 2 / 1.75 / 1.375; md 1.625 / 1.375 / 1.25; sm 1.375 / 1.25 / 1.125; xs 1; xxs 0.875. Line-height headings 1.03 to 1.12, body about 1.4. Letter-spacing xxl -0.025em to -0.02em; most frequent `-.01em`. Features `"ss01"` and `"tnum"`. Sail uses the system stack at 14px base |
| Colour | Brand blurple 600 `#533afd` (primary action, about `oklch(0.521 0.268 277)`); neutral 990 `#061b31` (text, about `oklch(0.219 0.051 252)`); full ramps for brand, neutral, dark, success (`#00b261`, `#006f3a`), error (`#f3432a`, `#a01400`). Legacy `#635BFF`, `#0A2540`, `#F6F9FC`. Semantic mapping: `text-solid = neutral-990`, `text-soft = neutral-600`, `action-bg-solid = brand-600`, `input-border = neutral-100` (hover/focus `brand-500`). Gradients `linear-gradient(270deg, #ffd601, #ee30fb, #635bff)` and a conic gradient; hero wave is WebGL; `backdrop-filter: blur(12px)` on the sticky nav |
| Spacing | 8px core grid (`space-core-100 = 8px` up to `2000 = 160px`); content max width 1264px; 12 / 8 / 4 columns; gap 16px; breakpoints 640, 940, 1264px. Sail: header 48px, sidebar 250 to 280px, right pane 250px, content max 1175px. Stripe Apps tokens xxsmall 2 to xxlarge 48 |
| Radius, elevation, motion | Radius xs 2, sm 4, **md 6px (most used, 106 rules)**, lg 16, xl 32. Two-layer navy-tinted shadows; classic card shadow `0 50px 100px -20px rgba(50,50,93,.25), 0 30px 60px -30px rgba(0,0,0,.3)`. Dominant easing `cubic-bezier(.25,1,.5,1)` (41 uses), typical 300ms, gated behind `prefers-reduced-motion: no-preference` (70 blocks) |
| Page patterns | Sticky blurred nav with mega-menu; light-weight hero; logo wall; eyebrow + H2 + body sections; stats band with tabular numerals; dark navy developer sections; docs with left nav, content and sticky right TOC; Dashboard with sidebar, shortcuts, dense tables, status badges |
| **Status badges (Stripe Apps)** | neutral, info, positive, negative, **warning** (needs action, optional), **urgent** (needs immediate action, must resolve): maps closely to clinical triage |
| **Radar risk UI** | Risk level Normal / Elevated / High (`risk_level: normal \| elevated \| highest`, plus `not_assessed`, `unknown`); score 0 to 99 (65+ elevated, 75+ high); a "Risk insights" card listing factors that raise or lower risk. **Direct model for the reasoning trail** |

### 9.5 Recommended Token Set ("Stripe Clinical")

> **Cross-reference.** build.md section 12.2 refers to this block as "research.md section 3.1" (its numbering in the original design workstream). This is that block, verbatim.

Design intent: neutrals from Stripe's navy-tinted slate (hue about 250 to 262), ink `#071b31`; primary Stripe blurple `oklch(0.52 0.25 277)` (`#5142f3`) in light and a lifted `#8394ff` in dark; surfaces white on cool off-white; dark mode deep navy (`#070e1b` background, `#0e1727` cards), not black; **inputs get a 3:1 boundary** (WCAG 1.4.11) in both modes (shadcn's default `--input` does not meet this); a four-level risk palette (teal-green 180, amber 78, orange 45, deep red 22) chosen to separate under deuteranopia and protanopia simulation (minimum OKLab distance under CVD simulation 0.092, vs 0.037 for a stock green/orange/red option); chart hues (277, 235, 340, 255, 265) avoid the risk hues; radius `0.5rem`.

```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);
  --font-heading: var(--font-sans);

  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);

  --color-risk-normal: var(--risk-normal);
  --color-risk-normal-foreground: var(--risk-normal-foreground);
  --color-risk-normal-subtle: var(--risk-normal-subtle);
  --color-risk-normal-subtle-foreground: var(--risk-normal-subtle-foreground);
  --color-risk-watch: var(--risk-watch);
  --color-risk-watch-foreground: var(--risk-watch-foreground);
  --color-risk-watch-subtle: var(--risk-watch-subtle);
  --color-risk-watch-subtle-foreground: var(--risk-watch-subtle-foreground);
  --color-risk-urgent: var(--risk-urgent);
  --color-risk-urgent-foreground: var(--risk-urgent-foreground);
  --color-risk-urgent-subtle: var(--risk-urgent-subtle);
  --color-risk-urgent-subtle-foreground: var(--risk-urgent-subtle-foreground);
  --color-risk-emergency: var(--risk-emergency);
  --color-risk-emergency-foreground: var(--risk-emergency-foreground);
  --color-risk-emergency-subtle: var(--risk-emergency-subtle);
  --color-risk-emergency-subtle-foreground: var(--risk-emergency-subtle-foreground);

  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) * 1.4);
  --radius-2xl: calc(var(--radius) * 1.8);
  --radius-3xl: calc(var(--radius) * 2.2);
  --radius-4xl: calc(var(--radius) * 2.6);

  --shadow-xs: 0 1px 2px 0 var(--shadow-color-1);
  --shadow-sm: 0 2px 5px -1px var(--shadow-color-1), 0 1px 3px -1px var(--shadow-color-2);
  --shadow-md: 0 6px 12px -2px var(--shadow-color-1), 0 3px 7px -3px var(--shadow-color-2);
  --shadow-lg: 0 13px 27px -5px var(--shadow-color-1), 0 8px 16px -8px var(--shadow-color-2);
  --shadow-xl: 0 30px 60px -12px var(--shadow-color-1), 0 18px 36px -18px var(--shadow-color-2);

  --ease-stripe: cubic-bezier(0.25, 1, 0.5, 1);
}

:root {
  --radius: 0.5rem;

  --background: oklch(1 0 0);                       /* #ffffff */
  --foreground: oklch(0.22 0.05 252);               /* #071b31 ink (Stripe #061b31) */
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.22 0.05 252);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.22 0.05 252);
  --primary: oklch(0.52 0.25 277);                  /* #5142f3 blurple */
  --primary-foreground: oklch(0.99 0.005 277);
  --secondary: oklch(0.955 0.012 250);              /* #eaf1f8 */
  --secondary-foreground: oklch(0.29 0.05 255);     /* #1a2c44 */
  --muted: oklch(0.975 0.006 250);                  /* #f4f7fb (Stripe #f6f9fc) */
  --muted-foreground: oklch(0.49 0.045 257);        /* #50627a (Stripe neutral-600) */
  --accent: oklch(0.962 0.018 275);                 /* #eff2ff blurple tint (hover/selected) */
  --accent-foreground: oklch(0.42 0.2 277);         /* #3b30b6 */
  --destructive: oklch(0.5 0.19 25);                /* #b71824 */
  --border: oklch(0.925 0.013 250);                 /* #e0e7ef hairline (decorative) */
  --input: oklch(0.64 0.03 255);                    /* #808d9f control boundary, 3.36:1 */
  --ring: oklch(0.58 0.22 277);                     /* #6061f8 */

  --chart-1: oklch(0.52 0.25 277);                  /* #5142f3 blurple   */
  --chart-2: oklch(0.6 0.12 235);                   /* #1b8abd sky       */
  --chart-3: oklch(0.58 0.2 340);                   /* #c13b9f magenta   */
  --chart-4: oklch(0.5 0.04 255);                   /* #54657a slate     */
  --chart-5: oklch(0.38 0.1 265);                   /* #283f77 navy      */

  --sidebar: oklch(0.985 0.004 250);                /* #f8fafd */
  --sidebar-foreground: oklch(0.22 0.05 252);
  --sidebar-primary: oklch(0.52 0.25 277);
  --sidebar-primary-foreground: oklch(0.99 0.005 277);
  --sidebar-accent: oklch(0.955 0.014 260);         /* #ebf1fa */
  --sidebar-accent-foreground: oklch(0.22 0.05 252);
  --sidebar-border: oklch(0.925 0.013 250);
  --sidebar-ring: oklch(0.58 0.22 277);

  /* Risk: Normal (teal-green) */
  --risk-normal: oklch(0.54 0.098 180);                    /* #008171 */
  --risk-normal-foreground: oklch(0.99 0.005 180);
  --risk-normal-subtle: oklch(0.965 0.03 180);             /* #dffbf4 */
  --risk-normal-subtle-foreground: oklch(0.42 0.076 180);  /* #015a4f */
  /* Risk: Watch (amber) */
  --risk-watch: oklch(0.67 0.135 78);                      /* #c28914 */
  --risk-watch-foreground: oklch(0.25 0.058 60);           /* #351a00 */
  --risk-watch-subtle: oklch(0.975 0.04 95);               /* #fff7d9 */
  --risk-watch-subtle-foreground: oklch(0.45 0.1 65);      /* #7a4702 */
  /* Risk: Urgent (orange) */
  --risk-urgent: oklch(0.575 0.163 45);                    /* #c35104 */
  --risk-urgent-foreground: oklch(0.99 0.004 45);
  --risk-urgent-subtle: oklch(0.965 0.02 55);              /* #fff0e7 */
  --risk-urgent-subtle-foreground: oklch(0.47 0.14 42);    /* #983803 */
  /* Risk: Emergency (deep red) */
  --risk-emergency: oklch(0.45 0.175 22);                  /* #a00c24 */
  --risk-emergency-foreground: oklch(0.99 0.004 22);
  --risk-emergency-subtle: oklch(0.955 0.021 20);          /* #feebea */
  --risk-emergency-subtle-foreground: oklch(0.44 0.17 22); /* #9b0d23 */

  --shadow-color-1: oklch(0.3 0.08 265 / 0.1);
  --shadow-color-2: oklch(0 0 0 / 0.06);
}

.dark {
  --background: oklch(0.165 0.03 262);              /* #070e1b deep navy */
  --foreground: oklch(0.965 0.01 255);              /* #eff4fa */
  --card: oklch(0.205 0.035 262);                   /* #0e1727 */
  --card-foreground: oklch(0.965 0.01 255);
  --popover: oklch(0.205 0.035 262);
  --popover-foreground: oklch(0.965 0.01 255);
  --primary: oklch(0.7 0.158 275);                  /* #8394ff */
  --primary-foreground: oklch(0.18 0.05 275);       /* #0c0f27 */
  --secondary: oklch(0.265 0.04 262);               /* #1a2539 */
  --secondary-foreground: oklch(0.965 0.01 255);
  --muted: oklch(0.245 0.035 262);                  /* #172031 */
  --muted-foreground: oklch(0.74 0.035 257);        /* #9dacc1 */
  --accent: oklch(0.28 0.06 275);                   /* #202646 */
  --accent-foreground: oklch(0.9 0.048 275);        /* #d4dcff */
  --destructive: oklch(0.7 0.17 25);                /* #f66d67 */
  --border: oklch(1 0 0 / 10%);
  --input: oklch(0.52 0.03 260);                    /* #5f6a7b, 3.5:1 on bg (opaque on purpose) */
  --ring: oklch(0.7 0.158 275);

  --chart-1: oklch(0.7 0.158 275);                  /* #8394ff */
  --chart-2: oklch(0.76 0.11 230);                  /* #5dbee9 */
  --chart-3: oklch(0.72 0.17 345);                  /* #ed74bd */
  --chart-4: oklch(0.72 0.03 255);                  /* #98a6b8 */
  --chart-5: oklch(0.84 0.07 285);                  /* #c5c5f7 */

  --sidebar: oklch(0.185 0.032 262);                /* #0b1321 */
  --sidebar-foreground: oklch(0.965 0.01 255);
  --sidebar-primary: oklch(0.7 0.158 275);
  --sidebar-primary-foreground: oklch(0.18 0.05 275);
  --sidebar-accent: oklch(0.255 0.04 262);          /* #182336 */
  --sidebar-accent-foreground: oklch(0.965 0.01 255);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.7 0.158 275);

  --risk-normal: oklch(0.76 0.12 178);                     /* #45cab1 */
  --risk-normal-foreground: oklch(0.2 0.036 180);
  --risk-normal-subtle: oklch(0.28 0.05 180);              /* #01312a */
  --risk-normal-subtle-foreground: oklch(0.87 0.09 178);   /* #90e8d4 */
  --risk-watch: oklch(0.86 0.14 88);                       /* #f7cb58 */
  --risk-watch-foreground: oklch(0.25 0.058 60);
  --risk-watch-subtle: oklch(0.3 0.06 75);                 /* #3f2903 */
  --risk-watch-subtle-foreground: oklch(0.9 0.12 90);      /* #fddb7c */
  --risk-urgent: oklch(0.76 0.14 55);                      /* #f49752 */
  --risk-urgent-foreground: oklch(0.2 0.05 45);
  --risk-urgent-subtle: oklch(0.3 0.07 45);                /* #4a200c */
  --risk-urgent-subtle-foreground: oklch(0.86 0.088 55);   /* #ffc29a */
  --risk-emergency: oklch(0.58 0.2 25);                    /* #d73337 */
  --risk-emergency-foreground: oklch(0.99 0.004 25);
  --risk-emergency-subtle: oklch(0.3 0.1 25);              /* #551112 */
  --risk-emergency-subtle-foreground: oklch(0.87 0.068 25);/* #fec4be */

  --shadow-color-1: oklch(0 0 0 / 0.45);
  --shadow-color-2: oklch(0 0 0 / 0.3);
}

@layer base {
  * { @apply border-border outline-ring/50; }
  html { @apply font-sans; }
  body {
    @apply bg-background text-foreground antialiased;
    font-feature-settings: "cv11";
  }
  table, [data-slot="chart"], .tabular { font-variant-numeric: tabular-nums; }
  button:not(:disabled), [role="button"]:not(:disabled) { cursor: pointer; }
}
```

Font wiring: `Inter({ subsets: ["latin"], variable: "--font-sans" })` and `Geist_Mono({ subsets: ["latin"], variable: "--font-mono" })` from `next/font/google`, or `pnpm dlx shadcn@latest add @shadcn/font-inter`. Type ramp (avoid weight 300 below 40px): marketing display `text-5xl md:text-6xl font-light tracking-[-0.025em] leading-[1.03]`; page title `text-2xl font-semibold tracking-[-0.015em]`; section title `text-lg font-semibold`; card title `text-sm font-medium`; body `text-sm leading-6`; meta `text-xs text-muted-foreground`; vitals and KPIs `text-3xl font-medium tabular-nums tracking-tight`.

### 9.6 Verified Contrast (WCAG 2.x)

Thresholds: text 4.5:1; non-text and UI boundaries 3:1. All pairs pass. "Risk X" means the fill or indicator.

| Pair | Light | Dark |
|---|---|---|
| foreground / background | 17.31 | 17.43 |
| foreground / card | 17.31 | 16.21 |
| muted-foreground / background | 6.26 | 8.37 |
| muted-foreground / muted | 5.82 | 7.05 |
| primary-foreground / primary | 5.95 | 6.85 |
| primary / background (link text) | 6.12 | 6.99 |
| accent-foreground / accent | 8.22 | 10.89 |
| secondary-foreground / secondary | 12.39 | 13.86 |
| destructive / background | 6.63 | 6.69 |
| input / background (3:1) | 3.36 | 3.50 |
| ring / background (3:1) | 4.61 | 6.99 |
| sidebar-accent-fg / sidebar-accent | 15.19 | 14.28 |
| chart-1..5 / card (3:1) | 6.12, 3.86, 4.78, 5.99, 10.16 | 6.50, 8.55, 6.66, 7.24, 10.84 |
| risk-normal-foreground / risk-normal | 4.68 | 8.81 |
| risk-normal-subtle-fg / subtle, / bg | 7.42, 8.12 | 10.00, 13.49 |
| risk-normal / bg, / card (3:1) | 4.81 | 9.47, 8.81 |
| risk-watch-foreground / risk-watch | 5.31 | 10.53 |
| risk-watch-subtle-fg / subtle, / bg | 7.13, 7.64 | 10.20, 14.30 |
| risk-watch / bg (3:1) | 3.05 | 12.55 |
| risk-urgent-foreground / risk-urgent | 4.54 | 8.19 |
| risk-urgent-subtle-fg / subtle, / bg | 6.54, 7.27 | 8.94, 12.35 |
| risk-urgent / bg | 4.68 | 8.64 |
| risk-emergency-foreground / risk-emergency | 7.93 | 4.60 |
| risk-emergency-subtle-fg / subtle, / bg | 7.40, 8.50 | 9.36, 12.70 |
| risk-emergency / bg, / card | 8.17 | 4.07, 3.79 |

All tokens are inside the sRGB gamut, so the ratios hold on non-P3 screens. Two cautions: `risk-watch` on white is 3.05:1 (fine for fills, **never as text**; use `risk-watch-subtle-foreground` for amber text); `border` is intentionally below 3:1 and may never be the sole boundary of an input (inputs use `border-input`).

### 9.7 Risk Semantics (Colour + Icon + Label + Weight)

| Level | Clinical meaning (to be confirmed by a clinical lead) | Badge style | lucide icon | Extra |
|---|---|---|---|---|
| Normal | Routine care, continue schedule | subtle `bg-risk-normal-subtle text-risk-normal-subtle-foreground` | `CircleCheck` | none |
| Watch | Monitor closely, recheck soon | subtle + `border-risk-watch/40` | `Eye` | none |
| Urgent | Same-day clinician review or referral | solid `bg-risk-urgent text-risk-urgent-foreground` | `TriangleAlert` | Card `border-l-4 border-l-risk-urgent` |
| Emergency | Immediate action or emergency referral | solid `bg-risk-emergency text-risk-emergency-foreground font-semibold` | `Siren` (or `OctagonAlert`) | Page-level `Alert` banner + `AlertDialog` acknowledgement |

Visual weight increases with severity (subtle, subtle with border, solid, solid with banner), mirroring Stripe Badge semantics and Radar's Normal / Elevated / High. **Never rely on colour alone.** Diffs must **not** use risk red and green (they collide with clinical meaning): added lines use `bg-accent text-accent-foreground` with a "+" gutter; removed lines use `bg-muted text-muted-foreground line-through` with a "-" gutter.

### 9.8 Component Mapping (Condensed)

| Need | shadcn composition |
|---|---|
| App shell | `dashboard-01` / `sidebar-07` / `sidebar-16` (SidebarProvider, `Sidebar variant="inset" collapsible="icon"`, SidebarInset, Breadcrumb, Command search); ⌘B toggles; sidebar becomes a Sheet on mobile |
| Patient or referral list | `Table` + TanStack; faceted filters (Popover + Command); sort by risk severity first; row opens a right `Sheet` quick view |
| Visit entry form | `FieldSet` / `Field` / `InputGroup` with unit addons; `ToggleGroup` or `Checkbox` grid for danger signs; zod ranges with soft warnings; live risk preview card; sticky footer action bar |
| Reasoning trail | Ordered `Item` list with icon, rule name, evidence, direction badge; `Collapsible` "Show All Factors"; `HoverCard` on guideline citations; `Marker` separators ("Inputs", "Rules Fired", "Recommendation"); modelled on Radar risk insights |
| Diff view | `Tabs` (Side By Side / Unified), `ResizablePanelGroup`, monospace lines, `Badge` counts; field-level rows with the old value struck through, `ArrowRight`, new value |
| Vitals chart | `ChartContainer` + Recharts `LineChart`; `ReferenceArea` bands; `ReferenceLine` at 140 and 160 mmHg; `accessibilityLayer`; a hidden table for screen readers |
| Emergencies | Persistent `Alert` + `AlertDialog` acknowledgement; **never a toast** |
| Empty, loading | `Empty` variants (no data, no matches, offline, all clear); `Skeleton` matching final layout |
| Mobile | Offcanvas Sheet sidebar; bottom tab bar; table becomes `Item` cards; Dialogs become `Drawer`; 44px touch targets (`max-md:h-11`); test at 360px |

Stripe-feel checklist: navy ink with one blurple primary action per view; hairlines over boxes; 14px body, `h-8` controls; tabular numerals; 150 to 300ms motion with `ease-(--ease-stripe)` inside `motion-safe:`; Title Case for titles and buttons; no em or en dashes in UI copy; deep navy dark mode with every risk badge tested in both modes.

### 9.9 Pointers To build.md

| Topic | build.md section |
|---|---|
| Frontend rules (pure shadcn, Base UI `render`, Title Case, no dashes, light/dark, 360px) | 11.1 |
| Setup commands (`init -t next -b base --pointer`, component list, pnpm) | 11.2 |
| Look and feel, tokens, risk semantics, diff colours | 12 |
| Screens (Welcome, Community Visit, Facility Inbox, Reconciliation, Mother Memory, Audit) and component inventory | 13 |

---
## 10. Open Questions And Unverified Items

Everything below is either unanswered or rests on a source we could not check ourselves. None of it should be stated as fact in the README, the video or the submission form without the caveat shown.

### 10.1 Hackathon And Organisers

| # | Item | Status | Where to resolve |
|---|---|---|---|
| H1 | Which deadline staff enforce (deck 21:29 EAT vs platform 02:59 EAT) | Open; we submit by 21:00 EAT regardless | Help Desk, t.me/metta_omniversity |
| H2 | Exact submission form field list | **UNVERIFIED** (inferred from a competitor's issue) | Platform after login |
| H3 | Whether a hidden "Solo" flag exists, or Omega plus a stated solo challenge is enough | Open | Help Desk |
| H4 | Whether a GitHub account must be invited as collaborator (no BASIX/XRA org found) | Open; public repo assumed sufficient | Help Desk |
| H5 | Prize split across the 5 winners; whether prizes are credited to an on-platform balance | **UNVERIFIED** | Help Desk; privacy policy wording only |
| H6 | Results of the Aug 2025 Nairobi MeTTa hackathon and SJIT cohorts | NOT FOUND | |
| H7 | Public footprints for Derese, Choudhary, Wondimagegnehu, Darwajawala, Shukla | **UNVERIFIED** beyond the deck | |
| H8 | Logan Golema family office focus ("fiscal, organic, and agentic longevity") | **UNVERIFIED** (search snippet) | |
| H9 | Rafael Presa's Deep Funding role | **UNVERIFIED** (search snippet) | |
| H10 | CodeSlayer 2K26 details | NOT FOUND | |
| H11 | Any page or theme for the 24 to 25 October follow-on | NOT FOUND; theme inferred | |
| H12 | In-event Telegram announcements (private group) | Not read | Join the group |
| H13 | Whether the submission can be edited after the deadline | Open | Help Desk |
| H14 | HackIndia project of Prateek Choudhary; Team Hackstreet's win | **UNVERIFIED** (snippet) | |
| H15 | Cognify, Atelier OS and MintCondition wins | **UNVERIFIED** (search snippet) | |

### 10.2 Omega And MeTTa

| # | Item | Status |
|---|---|---|
| T1 | The full Omega agent loop (Docker `singularitynet/omega:v0.1.19` or native with torch and ChromaDB) | Not run (no Docker daemon; needs an LLM key) |
| T2 | Whether `lib_omega.metta`'s import of the missing `./src/context` breaks HEAD or only the native path | Open |
| T3 | Whether the v0.1.19 Docker image predates the rename and the missing file | Open |
| T4 | MettaWamJam as an HTTP alternative to FastAPI | **UNVERIFIED** |
| T5 | DAS and MORK backends | Not tested (too heavy) |
| T6 | Omega docs' figures "LLM premise formulation errors (up to ~16.6%)" and "about 10% confidence decay per hop" | Read in docs; the per-hop decay is consistent with our hand checks, the 16.6% is the docs' own claim |
| T7 | Secondary coverage (MindStudio, openclawdatabase, Fetch.ai Innovation Lab OmegaClaw example) | **UNVERIFIED** |
| T8 | Surafel Fikru's link to Omega beyond the deck and commits | **UNVERIFIED** |

### 10.3 Maternal Evidence

| # | Item | Status |
|---|---|---|
| M1 | World Bank WDI MMR **149** (2023) vs MMEIG/GHO **379** | **CONFLICT**, unresolved; use 379 |
| M2 | CEMD 2015 to 2018 figures (38% / 19% / 18%; 66% postpartum; 61% within 24 hours; 75% and 72% delays; 53% anaemia; 342 MMR) | **UNVERIFIED** (press; primary PDF not obtained) |
| M3 | 2017 and 2015/16 CEMD primary reports | Not accessible (GHDx 403; Harvard-hosted PDF removed); figures from the LSTM abstract |
| M4 | Nation Newsplex "92% poor care, 81% substandard, 72% out of hours, obstetrician in 1 in 9" | **UNVERIFIED** press; 92% not used (section 5.7) |
| M5 | County MMRs from the 2009 census (Mandera 3,795 and others); "15 counties contribute 98%" | Dated, highly uncertain; do not reuse |
| M6 | 2019 census MMR 355 and county range 67 to 641 | **UNVERIFIED** (search summary) |
| M7 | ICRHK 2026 data (delays 30 / 25 / 45%; commodity shortages; SBA decline 69.8% to 65.5%) | **UNVERIFIED** (press report of a presentation) |
| M8 | KHIS counts 2,851 and 2,656; neonatal 6,909 to 5,777 | **UNVERIFIED** (paywalled) |
| M9 | "594" MMR (CS Duale) and "2,600 abortion deaths per year" | Unsourced or implausible; do not use |
| M10 | "62.4% preventable" | South African, not Kenyan |
| M11 | PPB MDSW guideline details (categories, fees, data localisation) | **UNVERIFIED** (press); read the PPB document |
| M12 | Digital Health regulations 2025 certification requirement | **UNVERIFIED** (press and law-firm summaries) |
| M13 | AI Bill 2026 status; draft AI policy; HELINA guidelines | **UNVERIFIED**; fast-moving |
| M14 | MEOWS thresholds; omqSOFA | **UNVERIFIED** (secondary summaries) |
| M15 | SHA / Linda Jamii tariffs; home-birth trends | **UNVERIFIED** (press) |
| M16 | CHP kit BP device model and its validation for pre-eclampsia | Unknown |
| M17 | CHP count: about 107,800 (MOH) vs about 95k (Medic) | **CONFLICT** (definitions differ) |
| M18 | PROMPTS PNC effect: +7.4 pp (18% relative, paper) vs "+17% relative" (IPA) | Minor **CONFLICT** in rounding or definition; cite the paper |
| M19 | CLIP pooled primary composite (24% vs 22%, aOR 1.17) vs per-country aORs (India 0.92, Mozambique 1.31) | Both reported; cite each with its source |
| M20 | KDHS facility birth 82.3% (KIR) vs 88% (final); PNC within 2 days 72.5% vs 78% | **CONFLICT**; prefer the final Summary Report |
| M21 | Mobile WACh effect sizes; Rongo CHW knowledge finding; Sheng comprehension | **UNVERIFIED** (summaries) |
| M22 | Rural internet and phone ownership by county | **UNVERIFIED** (secondary, likely 2019 census) |
| M23 | No RCT found of digital closed-loop maternal referral, or of AI clinical decision support for maternal outcomes in Kenya | Evidence gap (NOT FOUND) |
| M24 | WHO SMART ANC CQL transcription errors | VERIFIED as present; correct values must be re-derived from the narrative DAK |
| M25 | Swahili clinical phrasing in Mizani's templates (for example "kifafa cha mimba") | Needs review by a fluent Kenyan speaker |

### 10.4 Landscape, Alternatives, Jev And Design

| # | Item | Status |
|---|---|---|
| L1 | "Not found" novelty claims (sections 6.5, 6.7) | Search-bounded; not proof of absence |
| L2 | PROMPTS "about 15k messages a day" and "about 7% urgent, 18 nurses" | Press (NPR/WUSF) |
| L3 | Ubenwa ">95% accuracy" | Company claim via press |
| L4 | Flood idea: the right GloFAS river cell for Tana Delta | Open (probe returned 0 m3/s) |
| L5 | Chama dispute data | NOT FOUND |
| J1 | Jev accuracy on real CHP notes | Not tested; label 100 to 200 de-identified notes before any field claim |
| J2 | ZDR availability and data-transfer terms for Kenyan health data | Ask TypeSafe; DPA s.48 to 49 applies |
| J3 | Jev idea-scoring request id | Printed, not persisted |
| D1 | Clinical meaning of the four risk labels | To be confirmed by a clinical lead |
| D2 | Söhne licensing | Not used (Inter instead) |

---

## 11. Bibliography

Every URL from the seven research workstreams, deduplicated and numbered, grouped by topic. Where a repository was named in a source by owner and name only (from `gh search` output), the URL is the standard `https://github.com/<owner>/<name>` form and is marked "(named in search output)". Local sources are listed first.

### 11.1 Local And Organiser Sources

1. Official deck: `docs/source/260924_SingularityNET-Omega-BASIX-Hackathon_SJIT-KU-2026_24HR+TEAM.pptx.pdf` (35 slides; text in `scratchpad/deck.txt`).
2. Hackathon platform page. https://basix.market/lms/hackathon/1
3. Hackathons list (451 registered, 5 entries). https://basix.market/lms/hackathons
4. BASIX homepage. https://basix.market/
5. BASIX terms (dated 28 September 2026). https://basix.market/terms
6. BASIX privacy policy. https://basix.market/privacy
7. BASIX curriculum. https://basix.market/curriculum
8. BASIX ecosystem. https://basix.market/ecosystem
9. BASIX partners. https://basix.market/partners
10. BASIX join. https://basix.market/join
11. BASIX channels. https://basix.market/channels
12. BASIX ops. https://basix.market/ops
13. Platform JS chunk with tracks, problems and validation limits. https://basix.market/_next/static/chunks/7031-3142d4b527d0f389.js
14. Competitor issue copying the submission form fields. https://github.com/simpleHacker0893/basix-venture-route/issues/150
15. Official Telegram hub. https://t.me/metta_omniversity
16. SingularityNET announcements channel (public preview). https://t.me/s/snetann

### 11.2 Organisers, Partners, People And Media

17. XR Agency home. https://xragency.org/
18. XR Agency about (leadership). https://xragency.org/about.html
19. XR Agency MeTTa case study. https://xragency.org/case-study.html
20. XR Agency institutional practice (KU MOU, Ownership Schedule). https://xragency.org/institutional-practice.html
21. Ben Goertzel, "How Omega Lost Its Claw" (2026-09-15). https://bengoertzel.substack.com/p/how-omega-lost-its-claw
22. BGI Commons HyperSprint. https://bgicommons.org/hypersprint
23. BGI Nexus Grant Round 01 awardees. https://singularitynet.io/announcing-the-bgi-nexus-grant-round-01-awardees/
24. iCog Labs about. https://icog-labs.com/about-us/
25. iCog Labs AI internship (Geez Jobs). https://geezjobs.com/job-detail/ai-internship-program-icog-labs-1
26. BeyondTheCode.ai. https://www.beyondthecode.ai/
27. EIN Presswire on XR Agency and BeyondTheCode. https://www.einpresswire.com/article/697493862/xr-agency-revolutionizing-immersive-experiences-and-web-3-0-solutions-with-groundbreaking-docuseries-beyondthecode-ai
28. BeyondTheCode YouTube channel. https://www.youtube.com/@BeyondTheCode_AI_
29. Blockwee. https://blockwee.com
30. Logan Golema (theorg). https://theorg.com/org/heir-es/org-chart/logan-golema
31. Logan Golema (MarketScreener, snippet). https://in.marketscreener.com/insider/LOGAN-GOLEMA-A46EDM/
32. Logan Golema (LinkedIn). https://www.linkedin.com/in/logan-ryan-golema-115b59249/
33. Cognitive Sprints. https://cognitive-sprints.in
34. DevSphereIndia (LinkedIn). https://www.linkedin.com/company/devsphereindia-community
35. NIT Delhi "Code Slayer" gallery. https://nitdelhi.ac.in/campus/clubs/uba-cell/gallery/Code%20Slayer
36. Rejuve.bio. https://www.rejuve.bio
37. Expand Health. https://www.expandhealth.io
38. Haley Lowy bio (Lifeboat). https://lifeboat.com/ex/bios.haley.lowy
39. Haley Lowy commits to singnet/Omega. https://github.com/singnet/Omega/commits?author=HWLowy
40. Surafel Fikru commits to singnet/Omega. https://github.com/singnet/Omega/commits?author=surafelfikru
41. Cardano forum thread (Rafael Presa snippet). https://forum.cardano.org/t/decentralising-artificial-intelligence/118468
42. Sheila Wanjiru (LinkedIn; blocked from fetch). https://www.linkedin.com/in/sheila-wanjiru-925bb7177/
43. SingularityNET on X: OmegaClaw. https://x.com/SingularityNET/status/2049126570699174296
44. SingularityNET on X: Omega rename. https://x.com/SingularityNET/status/2098133734839276013

### 11.3 History And Analogous Events

45. MeTTa Training/Hackathon 2025, Nairobi (Luma). https://luma.com/y5jblri6
46. GDG on Campus Kenyatta University co-host page. https://gdg.community.dev/events/details/google-gdg-on-campus-kenyatta-university-nairobi-kenya-presents-metta-training-amp-hackathon-the-developer-pathway-to-agi/cohost-gdg-on-campus-kenyatta-university-nairobi-kenya/
47. MeTTa LLM Security Guard (2025 entry). https://github.com/snjiraini/MeTTa_AI_Hackathon2025
48. Locally adapted AI education (2025 entry). https://github.com/eunice-mwicigi/LOCALLY-ADAPTED-AI-and-TECH-EDUCATION-SCHOOL
49. MeTTa Omniversity Launch @ SJIT (video). https://www.youtube.com/watch?v=heM5EOJdnQ4
50. BASIX Omniversity Cohort 2 @ SJIT (video). https://www.youtube.com/watch?v=i4hwXoC6iD0
51. BGI Sprint I. https://bgicommons.org/hackathons/bgi-sprint-i
52. HyperSprint #1: OmegaClaw. https://bgicommons.org/hackathons/hypersprint-1-omegaclaw
53. HyperSprint #2: Build What's Next for Omega. https://bgicommons.org/hackathons/hypersprint-2-omega
54. SingularityNET ecosystem updates, March 2025 (HackIndia). https://singularitynet.io/singularitynet-latest-ecosystem-updates-march-2025/
55. ETHGlobal NYC winners (Superintelligence Alliance). https://superintelligence.io/ethglobal-nyc-winners/

### 11.4 Same-Hackathon And Omega-Track Repositories

56. MED-VERDICT. https://github.com/celstro/Med-Verdict-Two-agents-One-truth
57. MedTriage. https://github.com/Balaji150508/Medtriage
58. Venture Route. https://github.com/simpleHacker0893/basix-venture-route
59. basix-trustgate. https://github.com/kaniska-praba007/basix-trustgate
60. CourtLens. https://github.com/katelyn-signa/courtlens.BASIX.MARKET
61. TruthBridge. https://github.com/Brian20264/TruthBridge
62. glassbox-agent. https://github.com/Gitika2008/glassbox-agent
63. omega-real-formal-ablation-v1 (named in search output). https://github.com/fanz23-cell/omega-real-formal-ablation-v1
64. omegaclaw-deontic (named in search output). https://github.com/MesTTo/omegaclaw-deontic
65. omegaclaw-launchpad (named in search output). https://github.com/marcelosite/omegaclaw-launchpad
66. two-agents-one-truth (named in search output). https://github.com/harsha-glitchedout/two-agents-one-truth
67. subzero-two-agents-one-truth (named in search output). https://github.com/yuxufjameel-cmd/subzero-two-agents-one-truth
68. Two-Agents-One-Truth (named in search output). https://github.com/vishnuv41/Two-Agents-One-Truth
69. Omega boilerplate (named in search output). https://github.com/Dhrubojyoti07/Omega
70. omega-hackathon boilerplate (named in search output). https://github.com/2528017-spandan-off/omega-hackathon
71. Tina-X (Kenyan MeTTa agri/weather, named in search output). https://github.com/dgithinjibit/Tina-X
72. FractionalNFT (named in search output). https://github.com/kameswarar/FractionalNFT

### 11.5 Omega And SingularityNET Stack

73. singnet/Omega repository. https://github.com/singnet/Omega (clone URL https://github.com/singnet/Omega.git)
74. Omega README. https://github.com/singnet/Omega/blob/main/README.md
75. Omega release v0.1.20 (rename, PR #331). https://github.com/singnet/Omega/releases/tag/v0.1.20
76. Omega release v0.1.19. https://github.com/singnet/Omega/releases/tag/v0.1.19
77. Omega Dockerfile. https://github.com/singnet/Omega/blob/main/Dockerfile
78. Omega run.metta. https://github.com/singnet/Omega/blob/main/run.metta
79. Omega agent loop. https://github.com/singnet/Omega/blob/main/src/loop.metta
80. Omega memory. https://github.com/singnet/Omega/blob/main/src/memory.metta
81. Omega memory store internals. https://github.com/singnet/Omega/blob/main/docs/reference-internals-memory-store.md
82. Omega lib_nal.metta. https://github.com/singnet/Omega/blob/main/lib_nal.metta
83. Omega introduction (ACT/HYPOTHESIZE thresholds). https://github.com/singnet/Omega/blob/main/docs/introduction.md
84. Omega tutorial 05: reasoning with NAL and PLN. https://github.com/singnet/Omega/blob/main/docs/tutorial-05-reasoning-with-nal-pln.md
85. Omega plugin API. https://github.com/singnet/Omega/blob/main/docs/reference-plugin-api.md
86. Omega wschat channel. https://github.com/singnet/Omega/blob/main/channels/wschat.py
87. Omega Docker install script (v0.1.19). https://github.com/singnet/Omega/raw/refs/tags/v0.1.19/scripts/omegaclaw
88. Previous home (redirects to singnet/Omega; named in API output). https://github.com/asi-alliance/OmegaClaw-Core
89. MeTTaClaw origin. https://github.com/patham9/mettaclaw
90. Docker Hub singularitynet/omegaclaw. https://hub.docker.com/r/singularitynet/omegaclaw
91. MindStudio on OmegaClaw (secondary). https://www.mindstudio.ai/blog/omegaclaw-symbolic-ai-agent
92. openclawdatabase Docker test (secondary). https://openclawdatabase.com/news/videos/2026-09-06-omegaclaw-symbolic-agent-docker-test/
93. Fetch.ai Innovation Lab: OmegaClaw Agentverse skills. https://innovationlab.fetch.ai/resources/docs/examples/openclaw/omegaclaw-agentverse-skills
94. Fetch.ai Innovation Lab: Medical Agent with MeTTa. https://innovationlab.fetch.ai/resources/docs/examples/singularityNet/medical-agent-metta
95. Fetch.ai innovation-lab-examples code. https://github.com/fetchai/innovation-lab-examples
96. Hyperon framework paper. https://arxiv.org/pdf/2310.18318
97. Icog-metta_lang_practice. https://github.com/Kalkidan-Amare/Icog-metta_lang_practice
98. MeTTa stdlib documentation. https://github.com/eyuuab/MeTTa-lang-stdlib-documentation
99. SingularityNET Deep Funding. https://deepfunding.ai/

### 11.6 MeTTa Runtimes

100. PeTTa (clone URL https://github.com/trueagi-io/PeTTa.git). https://github.com/trueagi-io/PeTTa
101. hyperon on PyPI. https://pypi.org/project/hyperon/
102. hyperon-experimental. https://github.com/trueagi-io/hyperon-experimental
103. MeTTa-WAM (named in search output). https://github.com/trueagi-io/metta-wam
104. MettaWamJam (named in search output). https://github.com/trueagi-io/MettaWamJam
105. MORK (named in search output). https://github.com/trueagi-io/MORK
106. DAS (Distributed AtomSpace). https://github.com/singnet/das
107. PLN (named in search output). https://github.com/trueagi-io/PLN
108. pln-experimental (named in search output). https://github.com/trueagi-io/pln-experimental

### 11.7 Maternal Burden And Statistics

109. WHO maternal mortality fact sheet. https://www.who.int/news-room/fact-sheets/detail/maternal-mortality
110. WHO, Trends in maternal mortality 2000 to 2023. https://www.who.int/publications/i/item/9789240108462
111. UNFPA, Trends in maternal mortality 2000 to 2023. https://www.unfpa.org/publications/trends-maternal-mortality-2000-2023
112. UNICEF Data, Trends in maternal mortality. https://data.unicef.org/resources/trends-in-maternal-mortality-2000-to-2023/
113. WHO GHO API, MMR (MDG_0000000026), Kenya. https://ghoapi.azureedge.net/api/MDG_0000000026?$filter=SpatialDim%20eq%20'KEN'
114. WHO GHO API, maternal deaths (MORT_MATERNALNUM), Kenya. https://ghoapi.azureedge.net/api/MORT_MATERNALNUM?$filter=SpatialDim%20eq%20'KEN'
115. WHO GHO API, stillbirth rate (WHOSIS_000014), Kenya. https://ghoapi.azureedge.net/api/WHOSIS_000014?$filter=SpatialDim%20eq%20'KEN'
116. WHO GHO API, anaemia in pregnancy, Kenya. https://ghoapi.azureedge.net/api/NUTRITION_ANAEMIA_PREGNANT_PREV?$filter=SpatialDim%20eq%20'KEN'
117. World Bank WDI API, MMR, Kenya. https://api.worldbank.org/v2/country/KEN/indicator/SH.STA.MMRT?format=json
118. World Bank WDI API, neonatal mortality, Kenya. https://api.worldbank.org/v2/country/KEN/indicator/SH.DYN.NMRT?format=json
119. UN IGME, Standing up for Stillbirth. https://data.unicef.org/resources/standing-up-for-stillbirth-report/
120. Business Daily, Kenya off track on MMR target. https://www.businessdailyafrica.com/bd/corporate/health/un-says-kenya-off-track-to-meet-maternal-mortality-target-4998378
121. KDHS 2022 Key Indicators Report. https://dhsprogram.com/pubs/pdf/PR143/PR143.pdf
122. KDHS 2022 Summary Report. https://dhsprogram.com/pubs/pdf/SR277/SR277.pdf
123. KNBS KDHS 2022 page. https://www.knbs.or.ke/kenya-demographic-and-health-survey-kdhs-2022/
124. KNBS 2019 KPHC Analytical Report on Population Dynamics. https://new.knbs.or.ke/wp-content/uploads/2023/09/2019-Kenya-population-and-Housing-Census-Analytical-Report-on-Population-Dynamics.pdf
125. Muthee et al., county facility maternal mortality 2011 to 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC12427102
126. UNFPA Kenya county MMR ranking. https://kenya.unfpa.org/en/node/45574
127. The Star (2017), worst counties to give birth in. https://www.the-star.co.ke/news/realtime/2017-06-20-how-to-reduce-maternal-deaths-in-the-worst-counties-to-give-birth-in
128. Ziraba et al., Nairobi informal settlements. https://doaj.org/article/f412d783c0234a75b70fa2fae701805f
129. The Star, Duale "No woman should die giving life". https://www.the-star.co.ke/news/2025-09-28-duale-no-woman-should-die-giving-life
130. The Standard, Amoth: 5,000 mothers. https://www.standardmedia.co.ke/business/health-science/article/2001543638/amoth-how-kenya-loses-5000-mothers-to-preventable-childbirth-failures
131. Kenyans.co.ke, Nairobi tops counties for childbirth deaths. https://www.kenyans.co.ke/news/120705-nairobi-tops-list-counties-highest-childbirth-deaths
132. Capital FM, drop in skilled birth attendance (ICRHK data). https://capitalfm.africa/kenya-records-drop-in-skilled-birth-attendance-as-maternal-health-gaps-persist/
133. Daily Nation, maternal deaths drop 6.8% but home births surge. https://nation.africa/kenya/health/maternal-deaths-drop-by-6-8pc-but-home-births-surge-as-sha-replaces-linda-mama-5553740

### 11.8 Causes, CEMD And Near-Miss

134. Cresswell et al., global causes of maternal death 2009 to 2020. https://pubmed.ncbi.nlm.nih.gov/40064189/
135. Oxford summary of global causes update. https://www.demography.ox.ac.uk/news/global-update-reveals-haemorrhage-leading-cause-maternal-death
136. WHO news, complications undetected and untreated (8 March 2025). https://www.who.int/news/item/08-03-2025-many-pregnancy-related-complications-going-undetected-and-untreated--who
137. Say et al., global causes 2003 to 2009. https://doaj.org/article/9af5e06aeb694cf0b7baf2267a3ba4bf
138. Ameh, Godia, Ogutu, first vs second Kenya CEMD (RCOG 2019 abstract). https://research.lstmed.ac.uk/en/publications/improving-the-quality-of-maternal-and-newborn-health-care-in-keny/
139. GHDx, Saving Mothers' Lives 2017. https://ghdx.healthdata.org/node/541794
140. GHDx, Saving Mothers' Lives 2015 to 2016. https://ghdx.healthdata.org/node/541795
141. LSTM news on the CEMD report. https://www.lstmed.ac.uk/node/9013
142. The Standard, bleeding a leading cause (CEMD 2015 to 2018). https://www.standardmedia.co.ke/health/health-science/article/2001468321/bleeding-a-leading-cause-of-maternal-death-report
143. Daily Nation Newsplex, most maternal deaths out of office hours (92% figure, not used). https://nation.africa/kenya/newsplex/most-maternal-deaths-occur-out-of-office-hours-says-study-17060
144. Owolabi et al., maternal near-miss in Kenya 2018. https://pmc.ncbi.nlm.nih.gov/articles/PMC7495416/
145. Mohamed et al., induced abortion in Kenya. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4546129/
146. Hb trajectory and PPH (IJWH). https://www.dovepress.com/hemoglobin-trajectory-during-pregnancy-and-postpartum-hemorrhage-a-ret-peer-reviewed-fulltext-article-IJWH
147. LSHTM on severe anaemia and PPH risk. https://www.lshtm.ac.uk/node/383046

### 11.9 Kenya Health System: CHPs, eCHIS, Referral, Financing

148. Amref, 107,000 CHPs (June 2025). https://newsroom.amref.org/blog/2025/06/built-from-the-ground-up-how-107000-community-health-promoters-are-changing-the-face-of-health-care-in-kenya/
149. Amref, generative AI lessons from Machakos. https://newsroom.amref.org/blog/2025/10/harnessing-generative-ai-to-transform-community-health-lessons-from-machakos-county-2/
150. The Standard, CHP programme yet to fully take off (2024). https://www.standardmedia.co.ke/health/health-science/article/2001496277/seven-months-later-chp-programme-yet-to-fully-take-off
151. Kenya News Agency, Nyeri CHP kits. https://www.kenyanews.go.ke/nyeri-governor-flags-off-chp-kits/
152. Deputy President, Community Health Stipends speech (kit list). https://deputypresident.go.ke/sites/default/files/2024-05/Community%20Health%20Stipends%20Speech%20Formatted.pdf
153. The Standard, eCHIS roll-out (July 2024). https://www.standardmedia.co.ke/health/health-science/article/2001498549/health-ministry-rolls-out-electronic-system-to-boost-services
154. Muriithi et al., eCHIS implementation and acceptability (2026). https://chwcentral.org/wp-content/uploads/Implementation-Process-and-Acceptability-of-the-electronic-Community-Health-Information-System-among-Community-Health-Workers-in-Kenya.pdf
155. People Daily, new smartphones and stipend for CHPs. https://peopledaily.digital/news/ruto-promises-new-smartphones-and-stipend-increase-for-community-health-promoters (AMP: https://peopledaily.digital/news/ruto-promises-new-smartphones-and-stipend-increase-for-community-health-promoters/amp)
156. The Star, Ruto slams counties over unpaid CHPs. https://www.the-star.co.ke/news/2025-09-04-ruto-slams-counties-over-unpaid-health-promoters
157. Capital FM, permanent and pensionable CHP jobs. https://capitalfm.africa/community-health-promoters-to-get-permanent-pensionable-jobs-ruto/
158. The Standard, CHPs protest 13-month stipend delay. https://www.thestandard.ke/business/amp/coast/article/2001519721/over-1400-chps-protest-over-13-month-stipend-delay
159. Medic, partnership with the Kenyan government. https://medic.org/stories/medic-partners-with-kenyan-government-to-transform-community-health/
160. Medic Q2 2024 impact report. https://medic.org/q2-2024-impact-report/
161. Medic Community Roundup listing (eCHIS to TaifaCare closed loop). https://unjobs.org/channels/TCrYgB812EXuz7Y0yLTGGNsXLi03/GPHorre4g-0
162. KEMRI-Wellcome, PCN implementation. https://kemri-wellcome.org/policy-briefs/examining-the-implementation-experience-of-primary-care-networks-in-kenya-2
163. Kenya News Agency, PCNs (January 2026). https://www.kenyanews.go.ke/?p=167549
164. People Daily, Linda Mama to Linda Jamii. https://peopledaily.digital/news/duale-announces-transition-from-linda-mama-to-linda-jamii-for-maternal-care/amp
165. Kenyans.co.ke, Linda Jamii cover. https://www.kenyans.co.ke/news/113366-duale-lauds-expanded-linda-jamii-cover-full-maternity-care-and-family-benefits
166. Citizen Digital, RUPHA survey on SHA claims. https://citizen.digital/news/majority-of-health-facilities-unpaid-for-sha-claims-rupha-survey-reveals-n355378
167. The Star, governors on SHA challenges. https://www.the-star.co.ke/news/2026-01-21-governors-raise-alarm-over-sha-challenges
168. MEASURE Evaluation PIMA, referral system building in Kenya. https://measureevaluation.cpc.unc.edu/pima/meval-pima-news/referral-system-building-in-kenya.html
169. MOH 100 Community Referral Form. https://tciurbanhealth.org/wp-content/uploads/2018/04/Community-Referral-form-MOH-100.pdf
170. Transaid/AFCAP, linking rural communities with health services. https://www.transaid.org/wp-content/uploads/2015/09/AFCAP-Linking-Rural-Communities-to-Health-Services.pdf
171. Kenya MOH Mother and Child Health Handbook (2020). https://www.kenyapaediatric.org/ecd/wp-content/uploads/2021/04/Mother-Child-Health-Handbook-MOH-NEW-LAYOUT-10th-Sep-2020.pdf

### 11.10 Clinical Guidelines And Thresholds

172. WHO Digital Adaptation Kit for Antenatal Care (2021). https://www.who.int/publications/i/item/9789240020306
173. WHO SMART ANC repository. https://github.com/WorldHealthOrganization/smart-anc
174. SMART ANC PlanDefinitions (ANCDT01 to ANCDT28). https://github.com/WorldHealthOrganization/smart-anc/tree/master/bundles/plandefinition
175. SMART ANC CQL. https://github.com/WorldHealthOrganization/smart-anc/tree/master/input/cql
176. SMART ANC ANCDT17 PlanDefinition JSON. https://raw.githubusercontent.com/WorldHealthOrganization/smart-anc/master/bundles/plandefinition/ANCDT17/ANCDT17-files/plandefinition-ANCDT17.json
177. SMART ANC implementation guide. https://build.fhir.org/ig/costateixeira/smart-anc/documentation.html
178. WHO SMART L3 starter-kit checklist. https://smart.who.int/ig-starter-kit/v1.0.0/checklist.html
179. Tunçalp et al., WHO 2016 ANC model. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5487083/
180. ANC schedule briefer (MCSP). https://www.mcsprogram.org/wp-content/uploads/2018/03/ANC-OverviewBriefer-A4-1.pdf
181. WHO 2024 Hb cut-offs (DHS Program blog). https://blog.dhsprogram.com/hemoglobin-collection-at-the-dhs-program-impact-of-updated-who-guidelines-on-dhs-program-anemia-data/
182. WHO 2024 Hb cut-offs (Guideline Central). https://www.guidelinecentral.com/guideline/3534081/
183. NICE NG133 hypertension in pregnancy. https://www.nice.org.uk/guidance/ng133
184. NICE QS35 statement 4. https://www.nice.org.uk/guidance/QS35/chapter/quality-statement-4-assessing-women-with-severe-hypertension-in-pregnancy
185. ISSHP classification summary. https://pmc.ncbi.nlm.nih.gov/articles/PMC11588921/
186. Brown et al. 1999, evaluation of a definition of pre-eclampsia. https://read.qxmd.com/read/10453825/evaluation-of-a-definition-of-pre-eclampsia
187. Magee et al. 2021, BP variability in CLIP. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8284372/
188. BP trajectory parameterisation (LSTM repository). https://research.lstmed.ac.uk/en/publications/parameterization-of-the-mid-trimester-drop-in-blood-pressure-traj-5/
189. Gestational weight gain and HDP. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3807791/
190. Home vs clinic BP (UCT GHI). https://journals.uct.ac.za/index.php/GHI/article/download/836/672
191. WHO news, new PPH recommendations (5 October 2025). https://www.who.int/news/item/05-10-2025-global-health-agencies-issue-new-recommendations-to-help-end-deaths-from-postpartum-haemorrhage
192. FIGO press release on PPH recommendations. https://www.figo.org/press-releases/global-health-agencies-issue-new-recommendations-help-end-deaths-postpartum-haemorrhage
193. Nathan et al. 2015, shock index in PPH. https://safemotherhood.ucsf.edu/sites/g/files/tkssra10096/f/wysiwyg/Shock-index-an-effective-predictor-of-outcome-in-postpartum-haemorrhage-.pdf
194. El Ayadi et al. 2016, shock index in hypovolaemic shock. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4762936/
195. Nathan et al. 2019, shock index in haemorrhage and sepsis. https://scholar.sun.ac.za/items/3edc628a-0b87-4d89-ab4a-0ff715b17502
196. WHO statement on maternal sepsis. https://www.worldsepsisday.org/news/2018/1/9/who-statement-on-maternal-sepsis
197. Bonet et al., consensus definition of maternal sepsis. https://pmc.ncbi.nlm.nih.gov/articles/PMC5450299/
198. O&G Magazine, sepsis redefined (omqSOFA). https://www.ogmagazine.org.au/?p=9898
199. Singh et al., MEOWS validation. https://portaldeboaspraticas.iff.fiocruz.br/biblioteca/a-validation-study-of-the-cemach-recommended-modified-early/
200. RCOG GTG 57 summary, reduced fetal movements. https://opqic.org/bjog-reduced-fetal-movements-green-top-guideline-no-57/
201. WHO 2016 ANC fetal movement recommendation. https://bigg-rec.bvsalud.org/en/recommendations/33ead605397e1d6ea990c2aed0f3995ed0f52a12

### 11.11 Trials And Programme Evidence

202. Vousden et al., CRADLE-3 feasibility (CRADLE VSA). https://pmc.ncbi.nlm.nih.gov/articles/PMC5924508/
203. Vousden et al., CRADLE-3 trial. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6379820/
204. CRADLE referrals for obstetric haemorrhage (UTS repository). https://opus.cloud1.lib.uts.edu.au/bitstream/10453/155169/2/Effect%20of%20the%20CRADLE%20vital%20signs%20alert%20device%20intervention%20on%20referrals%20for%20obstetric%20haemorrhage%20in%20low-middle%20income%20count.pdf
205. KCL news, CRADLE-5 in Sierra Leone. https://www.kcl.ac.uk/news/use-of-blood-pressure-and-pulse-monitoring-device-shows-promise-for-maternal-health-in-sierra-leone
206. CLIP cluster RCTs (Lancet 2020). https://scholars.aku.edu/en/publications/the-community-level-interventions-for-pre-eclampsia-clip-cluster-/
207. CLIP India. https://ecommons.aku.edu/pakistan_fhs_mc_women_childhealth_wc/115
208. CLIP Mozambique. https://scholars.aku.edu/en/publications/community-level-interventions-for-pre-eclampsia-clip-in-mozambiqu/
209. KCL news, CHWs reduce maternal, fetal and newborn deaths (CLIP). https://www.kcl.ac.uk/news/community-health-workers-reduce-maternal-foetal-new-born-deaths
210. PIERS on the Move. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4123040/
211. E-MOTIVE (Oxford WRH). https://www.wrh.ox.ac.uk/publications/publication_modal/2390339
212. WHO news on E-MOTIVE (9 May 2023). https://www.who.int/news/item/09-05-2023-lifesaving-solution-dramatically-reduces-severe-bleeding-after-childbirth
213. 2 Minute Medicine on E-MOTIVE. https://www.2minutemedicine.com/early-detection-and-treatment-of-postpartum-hemorrhage-reduces-associated-complications/
214. Semrau et al., BetterBirth (NEJM 2017). https://www.hsph.harvard.edu/global-health-research-partnership/wp-content/uploads/sites/2448/2023/09/nejmoa1701075.pdf
215. Vatsa et al., PROMPTS (PLoS Med 2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC11835334/
216. IPA summary of PROMPTS. https://poverty-action.org/impact-digital-health-platform-maternal-and-newborn-care-kenya
217. AI4D, Jacaranda UlizaLlama/UlizaMama. https://www.ai4d.ai/blog/revolutionizing-maternal-healthcare-with-ai
218. AWS, Jacaranda Health. https://aws.amazon.com/blogs/publicsector/jacaranda-health-advances-maternal-infant-health-across-kenya-beyond-aws/
219. Korom et al., Penda Health AI Consult (arXiv 2507.16947). https://arxiv.org/abs/2507.16947
220. OpenAI, AI clinical copilot with Penda Health. https://openai.com/index/ai-clinical-copilot-penda-health
221. Citizen Digital, AI tool cuts diagnostic errors by 16%. https://citizen.digital/news/ai-tool-cuts-diagnostic-errors-by-16-in-kenyan-clinics-study-finds-n367615
222. Barron et al., MomConnect (BMJ Glob Health 2018). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5922497/
223. MomConnect helpdesk paper. https://www.measureevaluation.org/resources/publications/ja-18-252
224. Unger et al., Mobile WACh. https://pmc.ncbi.nlm.nih.gov/articles/PMC6179930
225. Mobile WACh registry (NCT01894126). https://clinicaltrials.gov/study/NCT01894126
226. Trinity College Dublin, Living Goods/BRAC Uganda RCT. https://www.tcd.ie/news_events/articles/new-community-health-programme-linked-to-decreased-child-mortality-in-uganda
227. Agarwal et al., Cochrane CD012944.pub2. https://cochranelibrary.com/cdsr/doi/10.1002/14651858.CD012944.pub2/information
228. Amoakoh-Coleman et al., mHealth for health workers in pregnancy (JMIR 2016). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5010646/
229. Adepoju et al., mCDSS in sub-Saharan Africa (JMIR mHealth 2017). https://mhealth.jmir.org/2017/3/e38
230. van der Sijs et al., overriding of drug safety alerts (JAMIA 2006). https://textbookofdigitalhealth.com/references/h2006overriding.html
231. Textbook of Digital Health, alert fatigue. https://www.textbookofdigitalhealth.com/glossary/alert-fatigue.html

### 11.12 Law And Regulation

232. Data Protection Act 2019 (No. 24; Cap. 411C). https://new.kenyalaw.org/akn/ke/act/2019/24/eng@2022-12-31
233. Data Protection (General) Regulations 2021. https://www.odpc.go.ke/wp-content/uploads/2024/03/THE-DATA-PROTECTION-GENERAL-REGULATIONS-2021-1.pdf
234. Primary Health Care Act 2023 (No. 13). https://new.kenyalaw.org/akn/ke/act/2023/13/eng@2023-11-24
235. Facilities Improvement Financing Act 2023 (No. 14). https://new.kenyalaw.org/akn/ke/act/2023/14/eng@2023-11-24
236. Digital Health Act 2023 (No. 15). https://new.kenyalaw.org/akn/ke/act/2023/15/eng@2023-11-24
237. AllAfrica, SHA digital health rules deadline (September 2026). https://allafrica.com/stories/202609010210.html
238. Clyde & Co, health data protection in Kenya (March 2026). https://www.clydeco.com/en/insights/2026/03/health-data-protection-in-kenya-strategic-complian
239. The Star, new rules for health apps and medical software (22 April 2026). https://www.the-star.co.ke/news/2026-04-22-new-rules-set-for-health-apps-medical-software
240. Health Business, Kenya tightens oversight of medical device software. https://healthbusiness.co.ke/10137/kenya-tightens-oversight-of-medical-device-software/
241. The Standard, what the AI Bill and PPB rules mean. https://www.standardmedia.co.ke/business/opinion/article/2001551793/what-ai-bill-and-ppb-software-device-rules-mean-for-healthcare-businesses
242. KMPDC, virtual medical services provider application. https://kmpdc.go.ke/resources/Application%20for%20Registration%20as%20a%20Virtual%20Medical%20Services%20Provider.pdf
243. Bowmans, draft AI and Emerging Technologies Policy 2026. https://bowmanslaw.com/insights/kenya-ai-governance-framework-continues-to-take-shape-draft-artificial-intelligence-and-emerging-technologies-policy-2026/
244. HELINA, health sector AI regulation press release (May 2026). https://helina.africa/wp-content/uploads/2026/05/Kenya-Health-Sector-AI-Regulation-Press-Release.pdf
245. HL7 FHIR CRMI artifact lifecycle. https://hl7.org/fhir/uv/crmi/en/artifact-lifecycle.html

### 11.13 Language And Access

246. Translators without Borders, Words of Relief impact study. https://translatorswithoutborders.org/wp-content/uploads/2016/08/TWB_WoR_ImpactStudy_FINAL.pdf
247. CLEAR Global, Words of Relief study. https://clearglobal.org/resources/words-of-relief-impact-study-of-rural-and-urban-kenyans/
248. Kiswahili video messaging on COVID-19 (IGI Global). https://igi-global.com/chapter/kiswahili-video-messaging-on-covid-19-awareness-in-kenya/345946
249. CHW knowledge in Rongo (Frontiers Public Health 2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10173767
250. Khusoko, Kenya ICT statistics Q2 2025/2026. https://khusoko.com/2026/04/08/kenya-ict-sector-statistics-q2-2025-2026/
251. Ecofin Agency, rural connectivity spectrum reform. https://www.ecofinagency.com/news-digital/1602-52943-kenya-moves-to-strengthen-rural-connectivity-through-spectrum-reform

### 11.14 Landscape: Production Systems And Programmes

252. WUSF/NPR, Kenyan moms turn to an AI chatbot (17 September 2026). https://www.wusf.org/2026-09-17/to-prevent-deaths-in-childbirth-kenyan-moms-turn-to-an-ai-powered-chatbot
253. The Standard, AI in maternal healthcare in Murang'a. https://www.standardmedia.co.ke/health/amp/health-science/article/2001515393/how-ai-is-transforming-maternal-healthcare-in-muranga-county
254. CHT core default forms (high_blood_pressure flag). https://github.com/medic/cht-core/tree/master/config/default/forms/app
255. CHT Maternal & Newborn reference app. https://docs.communityhealthtoolkit.org/reference-apps/maternal-newborn/
256. CHT offline-first concepts (sync conflicts). https://docs.communityhealthtoolkit.org/technical-overview/concepts/offline-first/
257. CHT offline-first overview. https://docs.communityhealthtoolkit.org/core/overview/offline-first
258. JMIR 2020 on SMART ANC / OpenSRP. https://jmir.org/2020/10/e16355
259. Living Goods, closed-loop referrals. https://livinggoods.org/media/closed-loop-for-referrals-follow-up-of-maternal-neonatal-and-child-health-integrated-community-case-management/
260. Dimagi, maternal and newborn health. https://dimagi.com/sectors/maternal-and-newborn-health/
261. CommCare Nigeria ANC pre/post study. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4420494/
262. GCGH, mHealth Safer Deliveries. https://gcgh.grandchallenges.org/grant/mhealth-safer-deliveries
263. D-tree Safer Deliveries results. https://www.d-tree.org/?p=1880
264. Safer Deliveries visits study. https://pmc.ncbi.nlm.nih.gov/articles/PMC10921749
265. PRE-EMPT miniPIERS. https://pre-empt.obgyn.ubc.ca/evidence/minipiers
266. PIERS-ML in Nairobi (Strathclyde). https://strathprints.strath.ac.uk/88885/7/MontgomeryCsoban-etal-LDH-2024-Machine-learning-enabled-maternal-risk-assessment.pdf
267. Consecutive prediction of adverse maternal outcomes (Strathclyde). https://pureportal.strath.ac.uk/en/publications/consecutive-prediction-of-adverse-maternal-outcomes-of-preeclamps/
268. MIT Solve, Safe Delivery App. https://solve.mit.edu/solutions/19533
269. Population Medicine, AI personalisation at scale (MomConnect). https://www.populationmedicine.eu/AI-Powered-Personalisation-at-Scale-Bridging-the-Equity-Gap-in-Maternal-and-Child,227345,0,2.html
270. Kilkari RCT (BMJ Global Health). https://gh.bmj.com/content/6/Suppl_5/e008838.full
271. Digital Health, Lancet review of Babylon. https://www.digitalhealth.net/2018/11/lancet-review-babylons-ai/
272. MedCity News, Babylon in the UK. https://medcitynews.com/2023/09/babylon-healthcare-ai-uk/
273. Ada Health AFYA. https://about.ada.com/?p=10952
274. Ada accuracy study (BMJ Open 2022). https://doaj.org/article/ef2ac35795214766a36535328d1bfe75
275. Ubenwa paper (arXiv 1711.06405). https://ar5iv.labs.arxiv.org/html/1711.06405
276. Quartz on Ubenwa. https://qz.com/africa/1158185/nigerian-ai-health-startup-ubenwa-hopes-to-save-thousands-of-babies-lives-every-year
277. PeriGen PeriWatch Vigilance. https://perigen.com/periwatch-vigilance/
278. Google Health AI ultrasound. https://health.google/caregivers/ultrasound
279. Blind-sweep ultrasound AI (arXiv 2203.10139). https://arxiv.org/pdf/2203.10139
280. Business Daily, Google tests AI ultrasound. https://www.businessdailyafrica.com/bd/corporate/technology/google-tests-handheld-ai-assisted-ultrasound-machines-4768212
281. iDeliver (JMIR Formative Research 2022). https://formative.jmir.org/2022/6/e34741

### 11.15 Landscape: Research Literature

282. Scoping review of interpretable CDSS in high-risk pregnancy (Jan 2026). https://pmc.ncbi.nlm.nih.gov/articles/PMC12870301/
283. SK-MOEFS fuzzy-rule pre-eclampsia classifier. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12190940/
284. Hybrid fuzzy-XGBoost, Bangladesh (arXiv 2601.07866). https://arxiv.org/pdf/2601.07866
285. Graph-neurosymbolic CDS (PMLR v319). https://proceedings.mlr.press/v319/akande26a.html
286. TrustKG (L3S). https://www.l3s.de/trustkg-reliable-ai-for-medical-decision-making/
287. Neuro-symbolic guideline conflict resolution (arXiv 2604.17340). https://arxiv.org/pdf/2604.17340
288. ASPIC-G argumentation for conflicting guidelines (Argument & Computation 2021). https://journals.sagepub.com/doi/full/10.3233/AAC-200523
289. ASPIC-G preprint (arXiv 1902.07526). https://arxiv.org/pdf/1902.07526
290. India maternal chatbot (arXiv 2603.13168). https://arxiv.org/pdf/2603.13168
291. ObGynLongBench (arXiv 2609.07601). https://arxiv.org/pdf/2609.07601
292. RAG over Colombian maternal guidelines (Biomédica 2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12931962/
293. Systematic review of GPT maternal agents. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12862967/
294. MedAgents (arXiv 2311.10537). https://arxiv.org/abs/2311.10537v4
295. Multi-agent debate benchmark (NeurIPS 2023). https://neurips.cc/virtual/2023/75421
296. ConGaIT, Contest & Justify (arXiv 2507.22300). https://arxiv.org/html/2507.22300v1
297. FAU glaucoma referral explanation study (over-reliance). https://open.fau.de/handle/openfau/38109
298. Healthcare IT News, "cranky comments" and CDS alert errors. https://www.healthcareitnews.com/news/how-cranky-comments-can-help-spot-cds-alert-errors
299. Mindbowser, alert fatigue summary. https://www.mindbowser.com/alert-fatigue-healthcare/

### 11.16 Landscape: Maternal Hackathon Clones And Pain Points

300. Eastleigh Voice, Kenyan students win inaugural PPH hackathon. https://eastleighvoice.co.ke/health/382799/kenyan-students-win-inaugural-pph-hackathon-with-live-saving-maternal-health-tool
301. Prime Progress, MediBora. https://primeprogressng.com/spotlight/when-pregnancy-is-not-a-risk-african-students-build-ai-system-for-danger-warning/
302. mamaalert. https://github.com/Code-blize/mamaalert
303. mamacare-ai-danger-sign-assistant. https://github.com/helenmenim/mamacare-ai-danger-sign-assistant
304. MamaAlert (voice). https://github.com/MehGerald/MamaAlert
305. MamaAlert-HW. https://github.com/Najeev-lab/MamaAlert-HW
306. SafeMother-CDSS. https://github.com/zinthooz/SafeMother-CDSS
307. Maitri. https://github.com/mlvpatel/maitri
308. MaTriX. https://github.com/Mangalasridharan/MaTriX-AI-Maternal-Triage-Escalation-Intelligence
309. mamacord-gemma4. https://github.com/uthy4r/mamacord-gemma4
310. maternal-triage-system. https://github.com/Davidic-02/maternal-triage-system
311. Haven-AI. https://github.com/samruddhikhade/Haven-AI-
312. My-baby. https://github.com/Tech-sis123/My-baby
313. safepass. https://github.com/WeCODE22/safepass
314. maternal-health-risk-alert. https://github.com/mljadama/maternal-health-risk-alert
315. who-anc-skill. https://github.com/rubayatkhan/who-anc-skill
316. Ghana maternity referral form audit. https://pmc.ncbi.nlm.nih.gov/articles/PMC8925182/
317. Community-facility linkage in Busia and Migori (CHW Central). https://chwcentral.org/resources/factors-influencing-community-facility-linkage-for-case-management-of-possible-serious-bacterial-infections-among-young-infants-in-kenya/
318. CHW mHealth scoping review (CHW Central). https://chwcentral.org/resources/mobile-health-mhealth-applications-for-community-health-workers-in-low-and-middle-income-countries-a-scoping-review/
319. JMIR mHealth 2026, frontline workers and clinical autonomy. https://mhealth.jmir.org/2026/1/e81829

### 11.17 Alternatives Considered

320. Kenyans.co.ke, high-risk counties ahead of El Niño 2026. https://www.kenyans.co.ke/news/126050-interior-ministry-identifies-high-risk-counties-ahead-el-nino-2026
321. Dawan Africa, early warnings in Tana River. https://www.dawan.africa/news/early-warnings-save-lives-as-flood-threat-grows-in-tana-river
322. Save the Children, anticipatory action for flooding in Kenya. https://resourcecentre.savethechildren.net/document/lessons-in-anticipatory-action-an-operational-pilot-for-flooding-in-kenya
323. Dawan Africa, El Niño and Rift Valley Fever. https://www.dawan.africa/news/el-nino-raises-fresh-rift-valley-fever-threat-across-east-africa
324. ILRI, unreported RVF circulation 2023 to 2024. https://www.ilri.org/index.php/knowledge/publications/unreported-rift-valley-fever-virus-circulation-during-2023-2024-el-nino
325. Citizen Digital, veterinary association on El Niño. https://citizen.digital/article/veterinary-association-calls-for-urgent-action-to-shield-livestock-from-el-nino-n384049
326. Eastleigh Voice, multi-agency crackdown on fake medicines. https://eastleighvoice.co.ke/health/374181/kenya-unveils-multi-agency-team-to-crack-down-on-fake-and-substandard-medicines
327. Capital FM, recalls of substandard paracetamol and Augmentin. https://www.capitalfm.co.ke/business/2025/04/govt-recalls-substandard-batches-of-paracetamol-augmentin
328. Capital FM, loan defaults and digital-lending complaints. https://www.capitalfm.co.ke/business/2025/07/106877/
329. CIRCLEUP (named in search output). https://github.com/CIRCLEUP-AJO/CIRCLEUP
330. ajo (named in search output). https://github.com/presidoclintonbased-alt/ajo
331. e-chama (named in search output). https://github.com/SiroDevs/e-chama
332. zetu (named in search output). https://github.com/kim214/zetu
333. Right Click Save, NFT community in Kenya and Nigeria. https://rightclicksave.com/article/what-nft-community-means-for-kenya-and-nigeria
334. The Standard, Kasuku NFTs. https://www.standardmedia.co.ke/evewoman/living/article/2001445695/kasuku-firm-bets-on-nfts-to-disrupt-art-economy
335. People Daily, digitisation of land records. https://peopledaily.digital/news/surveyors-urge-speedy-digitisation-of-land-records-to-curb-fraud/amp
336. Kenyans.co.ke, why Kenyans lose land cases. https://www.kenyans.co.ke/news/125050-court-explains-why-many-kenyans-lose-their-land-cases
337. AGRA, rebuilding agricultural extension. https://agra.org/partnerships-aim-to-rebuild-kenyas-agriculture-extension-services/
338. Self Help Africa, AI in agriculture (PlantVillage Nuru). https://selfhelpafrica.org/uk/ai-agriculture/

### 11.18 Jev (TypeSafe)

339. TypeSafe docs index. https://docs.typesafe.ai/llms.txt
340. TypeSafe System One endpoint. https://api.typesafe.ai/v1/systemone

### 11.19 Design: shadcn/ui

341. shadcn llms.txt. https://ui.shadcn.com/llms.txt
342. shadcn docs (raw markdown pattern `https://ui.shadcn.com/docs/<page>.md`). https://ui.shadcn.com/docs/theming
343. shadcn components.json. https://ui.shadcn.com/docs/components-json
344. shadcn schema. https://ui.shadcn.com/schema.json
345. shadcn installation (Next.js). https://ui.shadcn.com/docs/installation/next
346. shadcn CLI. https://ui.shadcn.com/docs/cli
347. shadcn dark mode (Next.js). https://ui.shadcn.com/docs/dark-mode/next
348. shadcn chart. https://ui.shadcn.com/docs/components/chart
349. shadcn forms (react-hook-form). https://ui.shadcn.com/docs/forms/react-hook-form
350. shadcn registry. https://ui.shadcn.com/docs/registry
351. shadcn blocks. https://ui.shadcn.com/blocks
352. shadcn charts gallery. https://ui.shadcn.com/charts
353. shadcn create and presets. https://ui.shadcn.com/create
354. shadcn changelog. https://ui.shadcn.com/docs/changelog
355. shadcn colour registry (zinc, slate, stone). https://ui.shadcn.com/r/colors/zinc.json (also `/r/colors/slate.json`, `/r/colors/stone.json`)

### 11.20 Design: Stripe

356. Stripe home. https://stripe.com
357. Stripe Payments. https://stripe.com/payments
358. Stripe Pricing. https://stripe.com/pricing
359. Stripe Sessions. https://stripesessions.com
360. Stripe marketing CSS bundles. https://b.stripecdn.com/mkt-ssr-statics/assets/_next/static/css/*.css
361. Stripe docs CSS bundles (docs, frontend, sail). https://b.stripecdn.com/docs-statics-srv/assets/{docs,frontend,sail}.*.css
362. Stripe docs. https://docs.stripe.com
363. Stripe payments quickstart. https://docs.stripe.com/payments/quickstart
364. Stripe Dashboard basics. https://docs.stripe.com/dashboard/basics
365. Stripe Apps style. https://docs.stripe.com/stripe-apps/style
366. Stripe Apps Badge. https://docs.stripe.com/stripe-apps/components/badge
367. Stripe Radar risk evaluation. https://docs.stripe.com/radar/risk-evaluation
368. Stripe Radar risk insights. https://docs.stripe.com/radar/reviews/risk-insights

---

*End of research log. For the event rules in full see [info.md](info.md); for what we build from this evidence see [build.md](build.md).*
