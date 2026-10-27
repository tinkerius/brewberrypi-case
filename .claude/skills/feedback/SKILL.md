---
name: feedback
description: Feedback loop of the case pipeline. Turn the user's print feedback (fit, photos, measurements) into a spec revision and drive it through scad and stl. Use when the user reports on a test print or `make status` shows the print test as needs-you.
---

# Feedback loop

Interactive. Starts from what the user saw on the print.

**Inputs:** the user's print feedback, photos and measurements.
**Outputs:** whatever the stages below change.

## Steps
1. Log the feedback as a new round in `01-requirements/interview.md`. Store photos in `inputs/` (`/requirements` rules).
   Update `requirements.md` if a requirement or assumption changes.
2. `/spec`: a new spec revision with the change. It needs the user's approval (human gate).
3. After approval: `/scad` then `/stl`, or `make pipeline`, which runs whichever of the two is stale headless.
4. Record the print result in the AC9 row of `04-stl/README.md` (pass / fail + what was printed).

## Exit gate
`make status` shows every stage `done`, and the print test `done` once the user confirms the fit.
