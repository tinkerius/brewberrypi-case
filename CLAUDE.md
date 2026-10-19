# Instructions for Claude

This repo holds **one** model: a case for the user's BrewberryPi. Work strictly through the stages below.

## Pipeline

```
01-requirements  →  02-specification  →  03-openscad  →  04-stl
```

### 1. Requirements (`01-requirements/`)
- Interview the user in rounds of focused questions. Log every round (questions + answers verbatim or closely paraphrased) in `interview.md`.
- Store every input the user provides (photos, sketches, screenshots, links, datasheets) in `inputs/` and index it in `inputs/README.md`.
  Describe what each image shows and which dimensions can be read from it.
- Consolidate into `requirements.md`: each requirement gets an ID (`R1`, `R2`, …) and a source (interview round / input file).
- Keep **Assumptions** and **Open questions** sections current.
- **Exit:** no blocking open questions, or the user explicitly accepts the listed assumptions.

### 2. Specification (`02-specification/`)
- Write `spec.md` from the template. Every feature (`F…`) traces back to requirements (`R…`).
- Draw dimensioned views as SVG in `drawings/` (mm, top/front/side/section as needed), linked from the spec.
- Every acceptance criterion (`AC…`) must be checkable from the model, renders or a print.
- **Exit:** the user approves the spec. Record version + date in the spec's approval line and the README status table.
- **No OpenSCAD work before approval.**

### 3. OpenSCAD (`03-openscad/`)
- Entry file `brewberrypi-case.scad`, with a `part` selector (`base`, `lid`, `assembly`, …) and all parameters at the top, Customizer-friendly.
- One module per spec feature. Comment each module and parameter with its spec ID (`// F3`, `// P2`).
- Use `lib/fdm.scad` helpers and BOSL2 (`include <vendor/BOSL2/std.scad>`) where useful.
- **Spec is the source of truth.** If something must change, update `spec.md` (new revision) first, then the code.

### 4. STL (`04-stl/`)
- `tools/build.sh` renders the STLs and previews. `tools/check.sh` reports mesh problems and bounding boxes.
- Look at the preview PNGs yourself. Check every AC and fill in the verification table in `04-stl/README.md`, with the spec version the STLs were built from.
- Commit the STLs and previews.

### Feedback loop
Print feedback from the user → spec revision → code change → rebuild → re-verify.

## Rules
- FDM-optimized, printer-agnostic: follow `docs/fdm-design-rules.md`. **Never** add printer or slicer settings
  (nozzle, layer height, material, temperatures, infill, support settings) to any file.
- Units: millimetres everywhere.
- Commit after each meaningful step, with messages prefixed by stage: `req:`, `spec:`, `scad:`, `stl:`.
- Update the status table in `README.md` when a stage changes state.
- Safety: if mains voltage enters the case, flag it. A printed enclosure is not mains insulation on its own.
