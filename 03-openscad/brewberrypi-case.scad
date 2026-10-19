// BrewberryPi Case. Entry file.
// Built from spec version: none yet (no approved specification).
// Every module and parameter references its spec ID (F…, P…). The spec is the source of truth.

include <vendor/BOSL2/std.scad>
use <lib/fdm.scad>

/* [Part] */
// Which part to render
part = "assembly"; // [base, lid, assembly]

/* [Fit] */
// P? Clearance per side between mating parts (mm)
fit_clearance = 0.2; // [0.1:0.05:0.5]

/* [Hidden] */
$fn = 48;

// ---------------------------------------------------------------------------
// PLACEHOLDER: replaced once spec.md is approved.
// The cubes only exist so the build pipeline can be tested end to end.
// ---------------------------------------------------------------------------

module base() {
    echo("PLACEHOLDER: base not specified yet");
    cube([20, 20, 5]);
}

module lid() {
    echo("PLACEHOLDER: lid not specified yet");
    cube([20, 20, 2]);
}

module assembly() {
    base();
    translate([0, 0, 10]) lid();
}

if (part == "base") base();
else if (part == "lid") lid();
else assembly();
