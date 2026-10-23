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
            adapter_standoffs();                                                    // F14
        }
        divider_screw_holes();                                                      // F10
        pi_inserts();                                                               // F11
        relay_inserts();                                                            // F12
        feedthrough_slot();                                                         // F13
        adapter_inserts();                                                          // F14
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

// F11 Pi: Ø7 bosses protruding under the plate, M2.5 inserts pressed in from the top face.
module pi_bosses() {
    for (p = pi_hole_positions()) translate([p.x, p.y, hv_h - pi_boss.y]) cylinder(d = pi_boss.x, h = pi_boss.y + 0.01);
}

module pi_inserts() {
    for (p = pi_hole_positions()) translate([p.x, p.y, z_div_top - insert_m25[1]]) cylinder(d = insert_m25[0], h = insert_m25[1] + 1);
}

// F12 relay board: printed standoffs Ø8 × relay_standoff_h, M2.5 inserts from the tip.
module relay_standoffs() {
    for (p = relay_hole_positions())
        translate([p.x, p.y, hv_h - relay_standoff_h]) cylinder(d = relay_standoff_d, h = relay_standoff_h + 0.01);
}

module relay_inserts() {
    for (p = relay_hole_positions())
        translate([p.x, p.y, hv_h - relay_standoff_h - 1]) cylinder(d = insert_m25[0], h = insert_m25[1] + 1);
}

// F13 cable feed-through: rounded slot 14 × 46.
module feedthrough_slot() {
    translate([slot[0], slot[1], hv_h - 1]) linear_extrude(divider_t + 2)
        hull() for (dy = [-1, 1]) translate([0, dy * (slot[3] - slot[2]) / 2]) circle(d = slot[2]);
}

// F14 adapter: 4 printed standoffs; the 2 under its diagonal mounting holes get M3 inserts from the tip,
// the 2 at the other corners (adapter_rests) stay solid, so the adapter rests on 4 points.
module adapter_standoffs() {
    for (h = concat(adapter_holes, adapter_rests()))
        translate([adapter_pos.x + h.x, adapter_pos.y + h.y, hv_h - adapter_standoff_h])
            cylinder(d = adapter_standoff_d, h = adapter_standoff_h + 0.01);
}

module adapter_inserts() {
    for (h = adapter_holes)
        translate([adapter_pos.x + h.x, adapter_pos.y + h.y, hv_h - adapter_standoff_h - 1])
            cylinder(d = insert_m3[0], h = adapter_insert_depth + 1);
}
