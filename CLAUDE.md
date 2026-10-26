# Instructions for Claude

This repo holds **one** model: a case for the user's BrewberryPi. Work strictly through the stages below.

## Pipeline

```
01-requirements  →  02-specification  →  03-openscad  →  04-stl
   /requirements        /spec               /scad          /stl        ← print feedback: /feedback
   (needs user)         (needs approval)    (headless ok)  (headless ok)
```

Each stage is a skill in `.claude/skills/<stage>/SKILL.md` with its inputs, outputs, steps and exit gate. Follow it.

**Start with `make status`.** It reads the spec version stamps each stage leaves behind
(spec version table, `SPEC_VERSION` in `tools/make_drawings.py`, the scad header, `04-stl/README.md`, `04-stl/.source-hash`)
and shows, for each stage, done / stale / needs-you, plus the skill to run. Work on the first stage that is not done.

- `requirements` and `spec` need the user: interview answers, and the **spec approval**. Never mark a spec version approved yourself.
- `scad` and `stl` run headless as well: `make claude-scad`, `make claude-stl`, or `make pipeline` (runs whichever is stale).
- **No OpenSCAD work before the spec is approved.** **Spec is the source of truth.** A change goes into a new spec revision first, then the code.

Deterministic steps are `make` targets (see `make help`): `build`, `lint`, `test`, `status`, `ci`. CI runs `make ci`.

## Rules
- FDM-optimized, printer-agnostic: follow `docs/fdm-design-rules.md`. **Never** add printer or slicer settings
  (nozzle, layer height, material, temperatures, infill, support settings) to any file.
- Units: millimetres everywhere.
- Commit after each meaningful step, with messages prefixed by stage: `req:`, `spec:`, `scad:`, `stl:`.
- Update the status table in `README.md` when a stage changes state.
- Safety: if mains voltage enters the case, flag it. A printed enclosure is not mains insulation on its own.
