// BrewberryPi Case. Entry file.
// Built from spec version: 0.10 (02-specification/spec.md). The spec is the source of truth.
// Every parameter (P…) and module (F…) is tagged with its spec ID.
// Units: mm. Origin: front-left-bottom outer corner of the body, +X right, +Y back, +Z up.
// Exported parts are placed in their print orientation, the assembly in its use position.

use <lib/fdm.scad>

/* [Part] */
// Which part to render
part = "assembly"; // [assembly, body, divider, top_lid, bottom_lid, collision_check]
// Assembly only: pull the lids and the divider module apart (mm)
explode = 0; // [0:5:80]
// Assembly only: show the bought components (Pi, relay board, adapter, switches, sockets, inlet, jack)
show_components = true;
// Assembly only: cut open like the spec sections (A-A at x = 40.5 seen from +X, C-C at y = 85 seen from the front)
section_cut = "none"; // [none, A-A, C-C]

/* [Case] */
// P1 outer width (X)
case_w = 190;
// P2 outer depth (Y)
case_d = 160;
// P3 high-voltage part: body bottom -> divider underside
hv_h = 70;
// P4 low-voltage part: divider top -> top lid underside
lv_h = 47;
// P5 wall thickness
wall = 3; // [2.4:0.1:4]
// P6 lid thickness (also the rim height)
lid_t = 3; // [2.4:0.1:4]
// P7 divider plate thickness
divider_t = 3; // [2.4:0.1:4]
// P8 outer vertical edge radius
corner_r = 4;
// P9 clearance per side for every cutout and mating fit
fit_clearance = 0.2; // [0.1:0.05:0.5]
// P10 local wall thickness at the rocker switches [MAIN, HEATER/PUMP] = measured clip gap - 0.3 (> wall: inside frame, < wall: inside pocket)
switch_panel_t = [3.7, 2.7];
// P31 rim above the lid seat (top rebate)
rim_t = 1.5; // [1.2:0.1:2]
// P32 bottom lid locating lip [thickness, height]
lip = [2, 4];

/* [Fasteners] */
// P11 M3 heat-set insert hole [diameter, depth] for inserts 3 x 6 x 4.5 (6 long, Ø4.5): case, lids, divider, panel parts
insert_m3 = [4.0, 7.0];
// P12 M2.5 heat-set insert hole [diameter, depth] for inserts 2.5 x 5 x 3.5 (5 long, Ø3.5): circuit boards (Pi, relay board)
insert_m25 = [3.2, 6.0];

/* [Raspberry Pi] */
// P13 Pi board corner (x, y); board rotated with the GPIO edge to the front
pi_pos = [17, 55];
// P14 Pi hole pattern (same for Pi 3/4/5)
pi_holes = [58, 49];

/* [Relay board] */
// P15 relay board size (measured)
relay_board = [75, 52];
// P16 relay board hole pattern, centre to centre (measured, holes Ø3)
relay_holes = [70, 46];
// P17 relay board corner (x, y), directly under the Pi
relay_pos = [17, 58];
// P18 gap between divider and relay PCB
relay_standoff_h = 10;

/* [USB-C adapter] */
// P19 adapter size [x (cable side), y, height] (measured)
adapter = [51, 49, 27];
// P29 adapter corner (x, y)
adapter_pos = [123, 61];
// P30 adapter mounting hole [x, y] relative to the adapter corner (measured); [] = none
adapter_screw = [43, 45.5];

/* [Top lid] */
// P20 fan mount in the top lid: 0 = none
fan = 0; // [0, 30, 40]

/* [Labels] */
// P21 raised labels and logo
labels = true;
// P22 label height above the surface
label_raise = 0.6;
// Label font (any installed font; OpenSCAD ships Liberation Sans)
font = "Liberation Sans:style=Bold";

/* [Panel components] */
// P23 main switch cutout, portrait [w, h]
switch_main = [22, 27];
// P24 3-position switch cutout, portrait [w, h]
switch_3pos = [21.5, 28.5];
// P25 IEC inlet cutout [w, h, corner radius]
iec_cutout = [27.5, 31.5, 1];
// P25 IEC inlet screw spacing
iec_screw_spacing = 36;
// P26 socket cutout diameter
socket_d = 43;
// P26 socket screw square
socket_holes = 38;
// P27 jack thread diameter (measured: M8)
jack_d = 8;
// P28 local wall thickness at the jack: nut 2 + wall <= 4 mm usable thread (>= wall: no thinning)
jack_panel_t = 1.6;

/* [Hidden] */
// ---- derived levels -------------------------------------------------------
H = hv_h + divider_t + lv_h;              // lid seat (z = 120)
body_h = H + lid_t;                       // body incl. rim (z = 123)
z_div_top = hv_h + divider_t;             // divider top (z = 73)
bottom_chamfer = 0.6;                     // F1

// ---- fixed feature positions from the spec (§5) ---------------------------
col_inset = 7;  col_d = 10;               // F2 corner columns
pad_size = [10, 14];  pad_block = 8;      // F4 divider pads (x into the room, y along the wall), solid block above the chamfer
pad_y = [40, 120];                        // F4
divider_gap = 0.3;                        // F10 divider plate <-> inner walls
notch = 12;                               // F10 corner notch, measured from the plate corner
rib = [2, 6];  rib_x = [15, 175];         // F10 stiffening ribs [thickness, height], x range
pi_board = [85, 56];  pi_hole_inset = 3.5;   // F11
pi_boss = [7, 3.5];                       // F11 insert boss [diameter, protrusion under the plate]
pi_standoff = 10;                         // F11 bought brass standoffs
relay_standoff_d = 8;                     // F12
relay_h = 17;  relay_pins = 3;            // C1 measured: PCB underside → relay tops, solder pins (envelope only)
slot = [111, 85, 14, 46];                 // F13 feed-through [cx, cy, w, l]
bracket = [12, 2, 10];  adapter_clear = 0.5;  // F14 L-brackets [leg, thickness, height]
tie_slot = [5.5, 2.5];  tie_x = [15, 35];     // F14 tie slots, adapter-local x positions
switch_z = 40;                            // F3
switches = [["MAIN", 40, switch_main, switch_panel_t[0]], ["HEATER", 115, switch_3pos, switch_panel_t[1]],
            ["PUMP", 150, switch_3pos, switch_panel_t[1]]];   // name, x, cutout, wall at the clips
pocket_margin = 8;                        // F3 frame / pocket margin around each cutout
back_z = 38;                              // F6, F7
iec_x = 35;                              // F6
sockets = [["HEATER", 90], ["PUMP", 145]];   // F7
socket_flat = 24;                         // F7 flat-top teardrop
panel_boss = [8, 6];                      // F6/F7 insert bosses behind the back wall [diameter, length]
jack_pos = [35, 98];  jack_pocket_d = 16;   // F8
jack_flat = 4.7;                          // F8 flat-top teardrop: flat 4.7 above the centre (under the Ø10 nose)
vent = [11, 3, 30, 8, 40, 80];            // F9 [count, width, length, pitch, first y, bottom z]
pry_w = 12;                               // F16
label_size = 6.4;                         // F5, F8: OpenSCAD text size 6.4 → capitals ≥ 6 mm
front_label_z = 12;  back_label_z = 4;  temp_label_z = 82;   // F5, F8 baselines
logo = "BrewberryPi";  logo_size = 12.6;  // F21: OpenSCAD text size 12.6 → capitals ≥ 12 mm
logo_raise = 0.8;  logo_pos = [95, 30];   // F21
fan_pos = [72, 79];                       // F22
m3_clear = 3.4;                           // screw through-holes

$fa = 4;  $fs = 0.4;

// ---- shared geometry ------------------------------------------------------
// Case outline (2D), inset by `inset` from the outer faces, corners concentric with the outer R.
module outline2d(inset = 0) {
    offset(r = max(corner_r - inset, 0.01)) offset(delta = -corner_r) square([case_w, case_d]);
}

function col_centres() = [[col_inset, col_inset], [case_w - col_inset, col_inset],
                          [col_inset, case_d - col_inset], [case_w - col_inset, case_d - col_inset]];
function pad_centres() = [for (y = pad_y) for (x = [wall + pad_size.x / 2, case_w - wall - pad_size.x / 2]) [x, y]];
function pi_hole_positions() =       // Pi rotated 180°: SD-card end at +X, GPIO edge at the front
    [for (dx = [0, pi_holes.x]) for (dy = [0, pi_holes.y])
        [pi_pos.x + pi_board.x - pi_hole_inset - dx, pi_pos.y + pi_hole_inset + dy]];
function relay_hole_positions() =
    [for (dx = [0, relay_holes.x]) for (dy = [0, relay_holes.y])
        [relay_pos.x + (relay_board.x - relay_holes.x) / 2 + dx, relay_pos.y + (relay_board.y - relay_holes.y) / 2 + dy]];

include <parts/body.scad>
include <parts/divider.scad>
include <parts/lids.scad>
include <parts/components.scad>

// ---- part selector (print orientation for single parts) -------------------
if (part == "body") {
    body();
} else if (part == "divider") {
    translate([0, case_d, z_div_top]) rotate([180, 0, 0]) divider();      // upside down: top face on the bed
} else if (part == "top_lid") {
    translate([0, 0, -H]) top_lid();                                      // outer face (logo) up
} else if (part == "bottom_lid") {
    translate([0, 0, lid_t]) bottom_lid();                                // outer face down, lip up
} else if (part == "collision_check") {
    collision_check();                                                    // AC3/AC10: renders nothing if all clear
} else {
    assembly();
}

// AC4/AC5 report: key dimensions as modelled (checked in the STL stage).
if (part != "collision_check") {
    c2 = 2 * [fit_clearance, fit_clearance];
    echo(str("REPORT F1 body ", case_w, " x ", case_d, " x ", body_h, ", lid seat z = ", H, ", divider ", hv_h, "…", z_div_top));
    for (s = switches) echo(str("REPORT F3 ", s[0], " cutout ", s[2] + c2, " at x = ", s[1], ", z = ", switch_z, ", wall at the clips ", s[3]));
    echo(str("REPORT F6 IEC cutout ", [iec_cutout.x, iec_cutout.y] + c2, " r", iec_cutout[2], " at x = ", iec_x, ", z = ", back_z, ", screws ", iec_screw_spacing, " apart"));
    for (s = sockets) echo(str("REPORT F7 ", s[0], " socket Ø", socket_d + 2 * fit_clearance, " flat top at ", socket_flat, ", at x = ", s[1], ", z = ", back_z, ", holes □", socket_holes));
    echo(str("REPORT F8 jack Ø", jack_d + 2 * fit_clearance, " flat top at ", jack_flat, ", wall ", jack_panel_t, ", at x = ", jack_pos.x, ", z = ", jack_pos.y));
    echo(str("REPORT F14 adapter ", adapter, " at ", adapter_pos, ", screw hole at ", adapter_pos + adapter_screw));
    echo(str("REPORT inserts: M3 hole ", insert_m3, " (case), M2.5 hole ", insert_m25, " (Pi, relay board)"));
    echo(str("REPORT F11 Pi holes ", pi_hole_positions()));
    echo(str("REPORT F12 relay holes ", relay_hole_positions()));
}

module assembly() {
    difference() {
        assembly_parts();
        if (section_cut == "A-A") translate([40.5, -50, -50]) cube([case_w, case_d + 100, body_h + 100]);
        if (section_cut == "C-C") translate([-50, -50, -50]) cube([case_w + 100, 85 + 50, body_h + 100]);
    }
}

module assembly_parts() {
    color("#d9d9d9") body();
    color("#f2f2f2") translate([0, 0, explode]) divider();
    color("#bfbfbf") translate([0, 0, 2 * explode]) top_lid();
    color("#bfbfbf") translate([0, 0, -explode]) bottom_lid();
    if (show_components) translate([0, 0, explode]) components_on_divider();
    if (show_components) components_in_body();
}
