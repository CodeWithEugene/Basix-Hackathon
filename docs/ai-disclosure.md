# AI Disclosure

> This disclosure is mandatory for the Solo Track and is kept honest and current.
> It also appears in summary form in the [README](../README.md).

## Tools used during the build

- **Claude Code (Anthropic, Claude Opus 5.5)** was used for research (web and
  GitHub research, verifying the Omega and PeTTa install, reading sources),
  planning, writing documentation, and writing and reviewing code. The author
  (Eugene Mutembei) reviewed every change, made the clinical and design
  decisions, and owns the result.
- **TypeSafe Jev (`jev-1.13.0`)** is used inside the product only to read
  visit notes into typed danger-sign observations that the health worker
  confirms. During research it was also used once to score candidate ideas
  against the judging rubric (see [research.md](research.md) section 7.4).
  **It never makes or explains a clinical decision, never produces a number,
  a threshold, a risk level, an action, or an explanation.**
- **SingularityNET Omega's own inference** (`lib_nal.metta` from
  `singnet/Omega` at commit `31ff0aad`, loaded unmodified, on PeTTa v1.0.4)
  does all of the agent's reasoning: every rule firing is a NAL deduction,
  every merge of the two witnesses is a NAL revision, over rules written by
  hand from WHO and Kenya Ministry of Health guidance.
- **No LLM generates clinical text.** Explanations in English and Swahili are
  deterministic templates filled from the proof, so they cannot claim anything
  the proof does not contain.

## What was built by hand

- All clinical rule packs (`agent/plugins/mizani/packs/`), with citations.
- The MeTTa evidence and reason layers (`agent/plugins/mizani/`).
- The synthetic scenarios and all test data. No real patient data exists in
  this repository.
