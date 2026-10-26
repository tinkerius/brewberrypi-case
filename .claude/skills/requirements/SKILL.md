---
name: requirements
description: Stage 1 of the case pipeline. Interview the user and consolidate requirements in 01-requirements/. Use when `make status` shows requirements as needs-you, or the user brings new inputs (photos, sketches, datasheets, measurements).
---

# Stage 1: Requirements

Interactive. Needs the user's answers, so never run it headless.

**Inputs:** the user's answers; photos, sketches, screenshots, links, datasheets they provide.
**Outputs:** `01-requirements/interview.md`, `01-requirements/inputs/` + `inputs/README.md`, `01-requirements/requirements.md`.

## Steps
1. Interview the user in rounds of focused questions. Log every round (questions + answers verbatim or closely paraphrased) in `interview.md`.
2. Store every input the user provides in `inputs/` and index it in `inputs/README.md`.
   Describe what each image shows and which dimensions can be read from it.
3. Consolidate into `requirements.md`: each requirement gets an ID (`R1`, `R2`, …) and a source (interview round / input file).
4. Keep the **Assumptions** and **Open questions** sections current. When nothing is open, the section reads `- None.`

## Exit gate
`make status` → `requirements  done`. That means no blocking open questions, or the user explicitly accepts the listed assumptions
(then record that and set Open questions to `- None.`).

**Commit prefix:** `req:` · update the Requirements row of the `README.md` status table.
