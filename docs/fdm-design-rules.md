# FDM design rules (printer-agnostic)

The model is shaped so it prints well on any reasonable FDM printer **without** support material where possible.
All tuning (nozzle, layer height, material, temperatures, infill, supports, brims) is left to the slicer.

## Geometry rules
1. **Flat build-plate face.** Every part has one large flat face that is the intended bottom.
2. **Overhangs ≤ 45°** from vertical, or short horizontal bridges between two supported edges.
3. **Horizontal holes** use a teardrop or flat-top profile (`teardrop_hole()` in `lib/fdm.scad`), so they print without support.
4. **Bottom edges are chamfered, not filleted.** A fillet on the build-plate edge creates an overhang, and a 45° chamfer does not (`bottom_chamfer_cube()`).
5. **No floating islands.** Every feature connects to geometry below it.
6. **Walls and ribs** have a named design parameter (`wall`). Thin features below it need a stated reason in the spec.
7. **Mating fits** use the named parameter `fit_clearance` (default 0.2 mm per side), which you can tune in the Customizer.
8. **Snap-fits** flex along the layer lines, not across them.
9. **Screw holes:** size them for the intended fastener (tap-in, heat-set insert, or through-hole + nut) as stated in the spec.
10. **Manifold output.** Every STL must pass `tools/check.sh` without errors.

## Explicitly out of scope
Nozzle diameter · layer height · material · temperatures · infill · slicer support settings · brim/raft · print speed.
