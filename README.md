# Mizani

**Two witnesses, one referral.** Two SingularityNET Omega agents reconcile a pregnant woman's referral between the community health promoter who saw her at home and the nurse who receives her, and show their working in English and Swahili.

| | |
|---|---|
| **Hackathon** | SingularityNET x Omega x BASIX.Market Hackathon (BASIX Omniversity), 30 Sept to 2 Oct 2026 |
| **Track** | Omega (Solo Track) |
| **Omega problem** | The Agent Without Borders (challenge 02: offline-first decision with a small MeTTa rule set, reconciled with a fuller Omega agent, showing how and why the answer changed; challenge 01: reasoning explained in a local language) |
| **Solo challenge** | 01: One agent producing an auditable decision |
| **Team** | Technetians (Eugene Mutembei, solo) |
| **Demo video** | _Link added at submission_ |
| **Status** | Docs complete; alpha in build (see [docs/build.md](docs/build.md)) |

> **Decision support, not diagnosis.** Mizani is a hackathon prototype. It is not a certified medical device and must not be used for real patients. All data in this repository is synthetic.

---

## The Problem

When a pregnant woman in rural Kenya shows danger signs, the **first witness** is usually a Community Health Promoter (CHP) at her home, often with no network. The **second witness** is a nurse at a facility hours later, who sees different numbers (often after treatment given on the way), does not see what the CHP saw, and does not see the mother's earlier history. The two witnesses disagree and nobody reconciles them.

- Kenya: about **5,700 maternal deaths** in 2023 (MMR **379** per 100,000 live births, UN MMEIG via WHO GHO).
- Kenya's confidential enquiry: sub-standard care in **81.4% (2014) to 98.1% (2015/16)** of maternal deaths; delay in treatment in **41%**.
- Kenya's national near-miss study: **64%** of severe maternal outcomes were already present on arrival at the referral hospital; **58%** of those had been referred from lower facilities.

Full evidence: [docs/problem.md](docs/problem.md).

## The Solution

1. **Community agent (offline).** The CHP records the visit (Swahili, English or Sheng note; danger signs; BP repeated after rest). An Omega agent with a small MeTTa rule pack decides on the phone side, with no network, and queues the referral.
2. **Facility agent (remembers the mother).** When the network returns, the packet syncs. The facility's Omega agent holds the mother's earlier visits and the full rule pack, and **reconciles both witnesses** with Omega's own NAL reasoning:
   - **revises** agreeing evidence (confidence goes up);
   - **defeats** evidence the protocol says to discount (a lower BP taken after nifedipine is not reassurance);
   - uses **memory** (a normal BP at 14 weeks makes today's hypertension new-onset, so pre-eclampsia, not chronic hypertension).
3. **Contestable referral proof.** The nurse sees the level and action, every premise with its source and truth value, and a diff of what changed from the community decision and why, in English and Swahili. The nurse can **contest any premise** and watch the decision recompute.

Full solution: [docs/solution.md](docs/solution.md).

## How It Uses Omega

Omega's stateful, auditable-reasoning architecture is the feature, not decoration:

| Omega piece | Use in Mizani |
|---|---|
| `lib_nal.metta` from [singnet/Omega](https://github.com/singnet/Omega) (pinned commit, unmodified) | Every rule firing (NAL deduction) and every merge of witnesses (NAL revision), with `(stv frequency confidence)` truth values |
| PeTTa (Omega's runtime, v1.0.4 on SWI-Prolog 10.0.2) | Runs both agents |
| Persistent memory (append-only atom log, like Omega's `history.metta`) | Each agent remembers across restarts; the facility agent's memory of the mother changes the answer |
| Self-modification (`add-atom` / `remove-atom` on `&self`) | Rule packs are atoms; rule updates produce literal before/after diffs |
| Plugin API (`loadOmegaPlugin`, `add-skill`) | Mizani ships as an Omega plugin (`assess`, `reconcile`, `why`, `contest`) |
| Omega's action thresholds (act: f ≥ 0.6 and c ≥ 0.5) | Decision bands: act, confirm first, none |

**Jev reads, Omega decides, the human confirms.** TypeSafe Jev (`jev-1.13.0`) only turns free-text notes into typed danger-sign observations that the CHP confirms. No LLM makes or explains a clinical decision; explanations are rendered from the proof.

## Architecture

```
Next.js + shadcn/ui  ──▶  Community agent :8101 (edge pack, outbox)  ──sync──▶  Facility agent :8102 (full pack, memory)
                              FastAPI + PeTTa + Omega lib_nal                       FastAPI + PeTTa + Omega lib_nal
```

Details, endpoints, atoms and rules: [docs/build.md](docs/build.md).

## Run It

> The commands below are the target interface defined in [docs/build.md](docs/build.md) section 16. They become runnable as the build lands.

Prerequisites (macOS): Homebrew, then `brew install swi-prolog uv pnpm`, and Node 20+.

```bash
git clone --recurse-submodules https://github.com/CodeWithEugene/Basix-Hackathon.git
cd Basix-Hackathon
cp .env.example .env
make setup
make seed
make dev
```

`TYPESAFE_API_KEY` in `.env` is optional. Without it, notes fall back to manual danger-sign toggles, which is also how the offline community agent works.

## Repository Map

| Path | What |
|---|---|
| [docs/info.md](docs/info.md) | Everything about the hackathon: rules, tracks, judging, judges, history, deadlines |
| [docs/problem.md](docs/problem.md) | Problems considered, evidence, scoring, the chosen problem |
| [docs/solution.md](docs/solution.md) | The full solution end to end |
| [docs/build.md](docs/build.md) | The build spec: architecture, MeTTa design, API, UI, tests, video plan |
| [docs/research.md](docs/research.md) | Research log and full bibliography |
| `agent/` | Omega agents (FastAPI + PeTTa + MeTTa plugin) |
| `web/` | Next.js app with pure shadcn/ui |

## AI Disclosure

This disclosure is mandatory for the Solo Track and is kept honest and current.

- **Claude Code (Anthropic, Claude Opus 5.5)** was used for research (web and GitHub research, verifying the Omega and PeTTa install, reading sources), planning, writing documentation, and writing and reviewing code. The author reviewed every change.
- **TypeSafe Jev (`jev-1.13.0`)** is used inside the product only to read visit notes into typed danger-sign observations that the health worker confirms. During research it was also used once to score candidate ideas against the judging rubric. It never makes or explains a clinical decision.
- **SingularityNET Omega's own inference** (`lib_nal.metta` on PeTTa) does all of the agent's reasoning, over rules written by hand from WHO and Kenya Ministry of Health guidance.
- No LLM generates clinical text. Explanations are templates filled from the proof.

## What's Next

Governed rule learning from clinician overrides (override, proposed MeTTa patch, human review, versioned rule, replay of past decisions); an Omega chat channel so a nurse can ask "why?" in plain language; integration behind Kenya's eCHIS so Mizani reasons inside the tools CHPs already use; a county pilot with KU incubation and a BGI Nexus proposal. See [docs/solution.md](docs/solution.md) section 15.

## Limitations

Not validated with CHPs or clinicians; Swahili strings need native clinical review; the community agent runs as a separate process in the demo rather than on a phone; Jev was tested on 12 synthetic notes only; a real deployment would likely be regulated as Software as a Medical Device in Kenya.

## Credits

- [singnet/Omega](https://github.com/singnet/Omega) (Apache-2.0), SingularityNET and contributors
- [trueagi-io/PeTTa](https://github.com/trueagi-io/PeTTa), TrueAGI and contributors
- [shadcn/ui](https://ui.shadcn.com) (MIT)
- WHO SMART Guidelines ANC decision tables; Kenya Ministry of Health Mother and Child Health Handbook
- [TypeSafe](https://docs.typesafe.ai) Jev

## License

[MIT](LICENSE.md). See [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE-OF-CONDUCT.md](CODE-OF-CONDUCT.md).
