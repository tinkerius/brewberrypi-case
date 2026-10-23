// Divider plate (part="divider"): spec §5.2, F10–F14.
// Included by brewberrypi-case.scad. Modelled in use position (plate z = hv_h … z_div_top, standoffs
// pointing down). The part selector flips it upside down for printing.

module divider() {
    difference() {
        union() {
            translate([0, 0, hv_h]) linear_extrude(divider_t) divider_outline();   // F10
            divider_ribs();                                                         // F10
            pi_bosses();                                                            // F11
            relay_standoffs();                                                      // F12
            adapter_brackets();                                                     // F14
        }
        divider_screw_holes();                                                      // F10
        pi_nut_pockets();                                                           // F11
        relay_inserts();                                                            // F12
        feedthrough_slot();                                                         // F13
        tie_slots();                                                                // F14
        adapter_screw_hole();                                                       // F14 (P30)
    }
}

// F10 plate outline: inner body outline minus divider_gap, corners notched for the columns.
module divider_outline() {
    o = wall + divider_gap;
    difference() {
        outline2d(o);
        for (x = [0, case_w], y = [0, case_d])
            translate([x, y]) square(2 * (o + notch), center = true);
    }
}

// F10 stiffening ribs on the underside along the front and back edges.
module divider_ribs() {
    for (y = [wall + divider_gap, case_d - wall - divider_gap - rib.x])
        translate([rib_x[0], y, hv_h - rib.y]) cube([rib_x[1] - rib_x[0], rib.x, rib.y + 0.01]);
}

// F10 M3 through-holes over the pads.
module divider_screw_holes() {
    for (p = pad_centres()) translate([p.x, p.y, hv_h - 1]) cylinder(d = m3_clear, h = divider_t + 2);
}

// F11 Pi: nut holders under the plate; the M2.5 brass standoffs screw into nuts held in hex pockets.
module pi_bosses() {
    for (p = pi_hole_positions()) translate([p.x, p.y, hv_h - pi_boss.y]) cylinder(d = pi_boss.x, h = pi_boss.y + 0.01);
}

module pi_nut_pockets() {
    for (p = pi_hole_positions()) {
        translate([p.x, p.y, hv_h - pi_boss.y - 1]) cylinder(d = m25_clear, h = pi_boss.y + divider_t + 2);
        translate([p.x, p.y, hv_h - pi_boss.y - 0.01])
            cylinder(d = pi_nut.x / cos(30), h = pi_nut.y + 0.01, $fn = 6);     // nut sits against the plate
    }
}

// F12 relay board: printed standoffs Ø8 × relay_standoff_h, M3 inserts from the tip.
module relay_standoffs() {
    for (p = relay_hole_positions())
        translate([p.x, p.y, hv_h - relay_standoff_h]) cylinder(d = relay_standoff_d, h = relay_standoff_h + 0.01);
}

module relay_inserts() {
    for (p = relay_hole_positions())
        translate([p.x, p.y, hv_h - relay_standoff_h - 1]) cylinder(d = insert_m3[0], h = insert_m3[1] + 1);
}

// F13 cable feed-through: rounded slot 14 × 46.
module feedthrough_slot() {
    translate([slot[0], slot[1], hv_h - 1]) linear_extrude(divider_t + 2)
        hull() for (dy = [-1, 1]) translate([0, dy * (slot[3] - slot[2]) / 2]) circle(d = slot[2]);
}

// F14 adapter holder: 4 L-shaped corner brackets around the adapter footprint.
module adapter_brackets() {
    for (mx = [0, 1], my = [0, 1])
        translate([adapter_pos.x + mx * adapter.x, adapter_pos.y + my * adapter.y, hv_h - bracket.z])
            scale([mx ? -1 : 1, my ? -1 : 1, 1]) adapter_bracket();
}

module adapter_bracket() {       // lower-left corner, inner faces adapter_clear away from the adapter
    o = adapter_clear + bracket.y;
    translate([-o, -o, 0]) {
        cube([bracket.x, bracket.y, bracket.z + 0.01]);
        cube([bracket.y, bracket.x, bracket.z + 0.01]);
    }
}

// F14 tie slots through the plate, next to the adapter's front and back faces.
module tie_slots() {
    for (tx = tie_x, side = [0, 1]) {
        y = side == 0 ? adapter_pos.y - adapter_clear - tie_slot.y : adapter_pos.y + adapter.y + adapter_clear;
        translate([adapter_pos.x + tx - tie_slot.x / 2, y, hv_h - 1]) cube([tie_slot.x, tie_slot.y, divider_t + 2]);
    }
}

// F14 / P30 optional through-hole for an M3 screw through the adapter's own hole (nut on top).
module adapter_screw_hole() {
    if (len(adapter_screw) == 2)
        translate([adapter_pos.x + adapter_screw.x, adapter_pos.y + adapter_screw.y, hv_h - 1])
            cylinder(d = m3_clear, h = divider_t + 2);
}
