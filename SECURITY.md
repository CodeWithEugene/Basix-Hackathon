# Security Policy

Mizani is a hackathon prototype for maternal-health decision support. It handles **synthetic data only**. This policy covers how to report problems and how the project protects data, secrets and patients.

## Supported Versions

| Version | Supported |
|---|---|
| `main` (hackathon alpha, October 2026) | Yes |
| Anything else | No |

## Reporting A Vulnerability

Please **do not open a public issue** for security problems.

1. Use GitHub's private vulnerability reporting on this repository (**Security** tab, then **Report a vulnerability**).
2. Include what you found, how to reproduce it, the impact you expect, and any suggested fix.
3. You will get an acknowledgement within 72 hours and a status update within 7 days.

Clinical safety issues (a rule or reconciliation path that could under-triage a mother) are treated with the same priority as security issues. Report them the same way if they are not already public.

## What We Protect And How

### Secrets

- The only secret is `TYPESAFE_API_KEY` (optional). It lives in a git-ignored `.env` or server environment variables, never in code, never in the browser, and never in logs.
- `.env.example` contains placeholders only.
- If a secret is ever committed, it is treated as exposed: rotate it immediately, then remove it from history.

### Data

- **No real patient data**, ever, in this repository, the demo, screenshots or the video.
- Names and phone-number-like strings are stripped from notes before any call to Jev. Request ids are logged; note bodies are not.
- In a real deployment, health data is **sensitive personal data** under Kenya's Data Protection Act 2019. Required before any real use: a Data Protection Impact Assessment (s.31), a licensed health care provider as controller (s.46), human decision-makers (s.35), Kenyan hosting or a Kenyan serving copy for primary care data (Data Protection (General) Regulations 2021, reg. 26), and audit trails (Digital Health Act 2023).

### Reasoning Engine Integrity

- User input never enters MeTTa as code. Ids are generated or validated against `^[A-Za-z0-9_-]{1,40}$`; readings are typed and range-checked; sign names and statuses are enums; free text is stored only as escaped strings or outside the atom space.
- Every mutation is written to an append-only atom log, so tampering is visible on replay.
- Omega (`singnet/Omega`) and PeTTa are pinned submodules; updates are reviewed changes, not automatic.

### Web App

- The browser talks only to Next.js route handlers, which proxy to the agents; agents are not exposed directly.
- No authentication in the hackathon alpha (roles are a labelled demo switcher). A real deployment needs authentication, role-based access and rate limiting before any real data is used.

### Clinical Safety

- Decision support, not diagnosis, stated on every screen.
- Uncertain or unconfirmed danger signs are treated as present for referral rules (fail safe).
- Every decision is contestable and overridable; rule changes require human review and are versioned.

## Scope

In scope: this repository's code (`agent/`, `web/`, `scripts/`) and configuration. Out of scope: vulnerabilities in upstream projects (report those to Omega, PeTTa, shadcn/ui or TypeSafe directly), and social engineering.
