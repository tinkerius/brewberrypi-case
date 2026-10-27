# BrewberryPi Case

A 3D-printable (FDM) case for the BrewberryPi, designed like a small software project:

```
requirements, interview, drawings, screenshots, …  →  specification (text, sketches, …)  →  OpenSCAD  →  STL
   01-requirements/                                   02-specification/                  03-openscad/  04-stl/
```

Each stage has its own folder, and a stage only starts once the previous one is done (see [CLAUDE.md](CLAUDE.md)).
The model is designed for FDM printing, but **contains no printer or slicer settings**. Layer height, material, infill, supports etc. are chosen in your slicer.

## Status

| Stage | State | Notes |
|---|---|---|
| 1. Requirements | done | 2026-10-19, all parts measured 2026-10-23 (round 10), new brand 2026-10-27 (round 19, R24) |
| 2. Specification | done | **v0.19 approved** 2026-10-27 (new brand: Zilla Slab Bold labels, stacked brand logo centred on the top lid), no open questions |
| 3. OpenSCAD | done | from spec v0.19: 4 parts, all manifold, collision check empty; labels in Zilla Slab Bold (font in `03-openscad/fonts/`), brand logo from `tools/make_logo.py` |
| 4. STL | done | 4 STLs from spec v0.18, AC1–AC8 + AC10 pass, **AC9 print test open** |

## Folders

| Folder | Contents |
|---|---|
| `01-requirements/inputs/` | your photos, hand sketches, screenshots, datasheets |
| `01-requirements/interview.md` | question/answer log, in rounds |
| `01-requirements/requirements.md` | consolidated requirements, assumptions, open questions |
| `02-specification/spec.md` | the specification: features, dimensions, parameters, acceptance criteria |
| `02-specification/drawings/` | dimensioned SVG views |
| `03-openscad/` | `brewberrypi-case.scad` (entry file), `lib/fdm.scad`, `lib/brand-logo.scad` (generated brand logo), `fonts/` (Zilla Slab Bold, SIL OFL), `vendor/BOSL2` |
| `04-stl/` | generated STLs + PNG previews + verification table |
| `docs/fdm-design-rules.md` | printer-agnostic FDM design rules the model follows |
| `tools/` | `setup.sh`, `build.sh`, `check.sh`, `status.py`, `make_drawings.py`, `make_logo.py` (brand logo SVG → OpenSCAD) |
| `.claude/skills/` | one skill per pipeline stage, used by Claude |

## Pipeline

Each stage is a Claude skill with fixed inputs, outputs and an exit gate. `make status` checks the gates
from the spec version stamps each stage leaves behind, and names the next skill to run.

| Stage | Skill | Gate (`make status`) | Who |
|---|---|---|---|
| 1. Requirements | `/requirements` | no open questions in `requirements.md` | you answer, Claude logs |
| 2. Specification | `/spec` | top version in `spec.md` approved, drawings at that version | you approve |
| 3. OpenSCAD | `/scad` | scad header at the approved version, no OpenSCAD warnings | headless: `make claude-scad` |
| 4. STL | `/stl` | `04-stl/README.md` at that version, STLs built from the current sources, no failed AC | headless: `make claude-stl` |
| Print feedback | `/feedback` | open ACs (print test) | you print, Claude revises the spec |

`make pipeline` runs whichever headless stage is stale. It commits locally and never pushes.

## Build

```sh
git clone --recurse-submodules <repo-url>
make setup     # installs openscad, xvfb, admesh (Debian/Ubuntu) and BOSL2
make build     # renders 04-stl/*.stl and 04-stl/previews/*.png
make lint      # shellcheck, ruff, OpenSCAD warnings, drawings and version stamps up to date
make test      # mesh, overhang, label, collision and dimension checks
make ci        # lint + build + test, what GitHub Actions runs
make status    # where the pipeline stands
```

The Makefile is the single source of truth: `.vscode/tasks.json` and `.github/workflows/ci.yml` only call its targets.
CI runs `make ci` inside the devcontainer (`.devcontainer/`), so VS Code "Reopen in Container" gives the same toolchain.

You can also open `03-openscad/brewberrypi-case.scad` in OpenSCAD and use the Customizer:
pick `part` (assembly / body / divider / top_lid / bottom_lid / collision_check), and in the assembly use
`explode` and `section_cut` to look inside. Single parts are shown in their print orientation.
