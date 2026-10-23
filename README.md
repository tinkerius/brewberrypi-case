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
| 1. Requirements | done | 2026-10-19, all parts measured 2026-10-23 (round 10) |
| 2. Specification | done | **v0.11 approved** 2026-10-23, no open questions |
| 3. OpenSCAD | done | from spec v0.11: 4 parts, all manifold, collision check empty |
| 4. STL | done | 4 STLs from spec v0.11, AC1–AC8 + AC10 pass, **AC9 print test open** |

## Folders

| Folder | Contents |
|---|---|
| `01-requirements/inputs/` | your photos, hand sketches, screenshots, datasheets |
| `01-requirements/interview.md` | question/answer log, in rounds |
| `01-requirements/requirements.md` | consolidated requirements, assumptions, open questions |
| `02-specification/spec.md` | the specification: features, dimensions, parameters, acceptance criteria |
| `02-specification/drawings/` | dimensioned SVG views |
| `03-openscad/` | `brewberrypi-case.scad` (entry file), `lib/fdm.scad`, `vendor/BOSL2` |
| `04-stl/` | generated STLs + PNG previews + verification table |
| `docs/fdm-design-rules.md` | printer-agnostic FDM design rules the model follows |
| `tools/` | `setup.sh`, `build.sh`, `check.sh` |

## Build

```sh
git clone --recurse-submodules <repo-url>
tools/setup.sh     # installs openscad, xvfb, admesh (Debian/Ubuntu) and BOSL2
tools/build.sh     # renders 04-stl/*.stl and 04-stl/previews/*.png
tools/check.sh     # mesh sanity check + bounding boxes
```

You can also open `03-openscad/brewberrypi-case.scad` in OpenSCAD and use the Customizer:
pick `part` (assembly / body / divider / top_lid / bottom_lid / collision_check), and in the assembly use
`explode` and `section_cut` to look inside. Single parts are shown in their print orientation.
