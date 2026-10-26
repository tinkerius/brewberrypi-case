---
name: stl
description: Stage 4 of the case pipeline. Render the STLs and previews, run the checks, look at the previews and fill in the verification table in 04-stl/README.md. Use when `make status` shows stl as stale. Can run headless via `make claude-stl`.
---

# Stage 4: STL

Runs without the user: `make claude-stl` calls it with `claude -p "/stl"`.

**Inputs:** `03-openscad/` at the approved spec version; the ACs in `02-specification/spec.md`.
**Outputs:** `04-stl/*.stl`, `04-stl/previews/*.png`, `04-stl/check-report.txt`, `04-stl/.source-hash`, `04-stl/README.md`.

**Precondition:** `python3 tools/status.py --require scad` succeeds. If it fails, stop and report why.

## Steps
1. `make build` renders the STLs and previews and writes `04-stl/.source-hash`.
2. `make test` (`tools/check.sh`) reports mesh problems, overhangs, label sizes, collisions and bounding boxes. Save its output to `04-stl/check-report.txt`.
3. Look at the preview PNGs yourself (Read them).
4. Check every AC and fill in the verification table in `04-stl/README.md`: `✅ pass` / `❌ fail` / `⏳ open` with evidence.
   Set `Built from spec version: **X**` to the spec version the STLs were built from.
5. An AC that needs a print stays `⏳ open`. That is the user's part (`/feedback`).

## Exit gate
`make status` → `stl  done`; `make test` exits 0.

**Commit prefix:** `stl:`. Commit the STLs and previews, and update the STL row of the `README.md` status table. Never push.
