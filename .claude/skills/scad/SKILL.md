---
name: scad
description: Stage 3 of the case pipeline. Bring 03-openscad/ in line with the approved spec. Use when `make status` shows scad as stale. Can run headless via `make claude-scad`.
---

# Stage 3: OpenSCAD

Runs without the user: `make claude-scad` calls it with `claude -p "/scad"`.

**Inputs:** the approved `02-specification/spec.md` (the version in the top row of its version table) and its drawings.
**Outputs:** `03-openscad/brewberrypi-case.scad`, `03-openscad/parts/*.scad`, `03-openscad/lib/fdm.scad`.

**Precondition:** `python3 tools/status.py --require spec` succeeds. If it fails, stop and report why. Do not touch the spec.

## Steps
1. Entry file `brewberrypi-case.scad`, with a `part` selector (`base`, `lid`, `assembly`, …) and all parameters at the top, Customizer-friendly.
2. One module per spec feature. Comment each module and parameter with its spec ID (`// F3`, `// P2`).
3. Use `lib/fdm.scad` helpers and BOSL2 (`include <vendor/BOSL2/std.scad>`) where useful.
4. Set `// Built from spec version: X` in the header of `brewberrypi-case.scad` to the approved version.
5. **Spec is the source of truth.** If the spec can't be implemented as written, stop and report it (in a headless run: as the final message, no commit).
   The spec revision itself is the `/spec` stage and needs the user.

## Exit gate
`make lint` passes (every part evaluates without OpenSCAD warnings, `make status` → `scad  done`), and
`openscad -D 'part="collision_check"'` renders empty.

**Commit prefix:** `scad:` · update the OpenSCAD row of the `README.md` status table. Never push.
