# Contributing To Mizani

Thank you for helping. Mizani is a maternal-health decision-support prototype built on SingularityNET Omega. Because it touches clinical reasoning, contributions are held to a few extra rules on top of the usual ones.

## Ground Rules

1. **Synthetic data only.** Never commit real patient data, real names, phone numbers, ID numbers or real visit notes. Use the synthetic scenarios in `agent/mizani/seed.py` or add new invented ones.
2. **Cite every clinical rule.** Any new or changed rule in `agent/plugins/mizani/packs/` must cite its source (for example WHO SMART ANC table id, ISSHP, WHO/FIGO/ICM 2025 PPH) in a comment, and must come with a golden test.
3. **No LLM decisions.** Language models (including Jev) may only read text into typed observations. They must never produce thresholds, risk levels, actions or clinical explanations.
4. **Omega stays unmodified.** `agent/vendor/omega` is a pinned submodule of `singnet/Omega`. Do not edit it. Shims go in `agent/plugins/mizani/shims.metta`.
5. **Copy rules for the UI.** Title Case for page titles, headings, card titles and buttons. Sentence case for body and helper text. No em dashes or en dashes in any user-facing text (`scripts/check-no-dashes.sh` enforces this).
6. **Pure shadcn/ui.** UI uses only shadcn/ui components, Tailwind utilities and lucide icons. Generated components live in `web/components/ui/` and are not hand-edited; compositions live in `web/components/mizani/`.

## Development Setup

Prerequisites: Homebrew (macOS), `brew install swi-prolog uv pnpm`, Node 20+.

```bash
git clone --recurse-submodules https://github.com/CodeWithEugene/Basix-Hackathon.git
cd Basix-Hackathon
cp .env.example .env
make setup
make seed
make dev
```

Package managers: **uv** for Python and **pnpm** for JavaScript. Do not use npm or yarn, and do not commit `package-lock.json` or `yarn.lock`.

## Tests

```bash
make test            # pytest (agent) + Playwright (web)
cd agent && uv run pytest --cov=mizani
cd web && pnpm lint && pnpm build
```

- Reasoning changes need golden tests in `agent/tests/test_reasoning.py` that pin the level, rule id, premise statuses and truth values.
- Aim for 80% or more coverage of `agent/mizani/`.
- New UI flows need a Playwright path in `web/tests/e2e/`.

## Commits And Pull Requests

- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`, `ci:`.
- One logical change per pull request, with a description of what changed, why, and how it was tested.
- For rule changes, paste the before/after MeTTa diff and the golden test output in the pull request.

## Reporting Problems

- Bugs and ideas: open a GitHub issue with steps to reproduce.
- Clinical safety concerns (a rule that could under-triage or over-triage): open an issue with the label `clinical-safety`, or use a private report if it involves anything sensitive (see [SECURITY.md](SECURITY.md)).
- Conduct: see [CODE-OF-CONDUCT.md](CODE-OF-CONDUCT.md).

## License

By contributing you agree that your contributions are licensed under the [MIT License](LICENSE.md).
