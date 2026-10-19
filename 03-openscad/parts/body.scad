// Body (part="body"): spec §5.1, F1–F9, F15, F16.
// Included by brewberrypi-case.scad (uses its parameters). Built in use position = print orientation
// (upright, bottom edge on the bed).

module body() {
    difference() {
        union() {
            shell();                                  // F1, F15
            corner_columns();                         // F2
            divider_pads();                           // F4
            back_panel_bosses();                      // F6, F7
            if (labels) { front_labels(); back_labels(); }   // F5, F8
        }
        corner_column_inserts();                      // F2
        divider_pad_inserts();                        // F4
        switch_cutouts();                             // F3
        back_panel_inserts();                         // F6, F7
        iec_inlet_cutout();                           // F6
        socket_cutouts();                             // F7
        jack_cutout();                                // F8
        vent_slots_lv();                              // F9
        pry_notch();                                  // F16
    }
}

// F1 shell (190 × 160 × 123, wall 3, R4, bottom chamfer 0.6) + F15 top rebate:
// the inner part of the wall ends at the lid seat (z = H), the outer rim (rim_t) continues to body_h.
module shell() {
    difference() {
        hull() {
            linear_extrude(0.01) outline2d(bottom_chamfer);
            translate([0, 0, bottom_chamfer]) linear_extrude(body_h - bottom_chamfer) outline2d();
        }
        translate([0, 0, -1]) linear_extrude(H + 1.01) outline2d(wall);          // room below the lid seat
        translate([0, 0, H]) linear_extrude(lid_t + 1) outline2d(rim_t);          // F15 lid pocket inside the rim
    }
}

// F2 corner columns Ø10, z = 0 … lid seat.
module corner_columns() {
    for (p = col_centres()) translate([p.x, p.y, 0]) cylinder(d = col_d, h = H);
}

// F2 M3 inserts top (top lid) and bottom (bottom lid).
module corner_column_inserts() {
    for (p = col_centres()) {
        translate([p.x, p.y, H - insert_m3[1]]) cylinder(d = insert_m3[0], h = insert_m3[1] + 1);
        translate([p.x, p.y, -1]) cylinder(d = insert_m3[0], h = insert_m3[1] + 1);
    }
}

// F4 divider pads 10 × 14 on the left/right walls, top at hv_h, 45° chamfer underneath.
module divider_pads() {
    for (y = pad_y) {
        divider_pad_left(y);
        translate([case_w, 0, 0]) mirror([1, 0, 0]) divider_pad_left(y);
    }
}

module divider_pad_left(y) {
    hull() {
        translate([wall - 0.5, y - pad_size.y / 2, hv_h - pad_block]) cube([pad_size.x + 0.5, pad_size.y, pad_block]);
        translate([wall - 0.5, y - pad_size.y / 2, hv_h - pad_block - pad_size.x]) cube([0.5, pad_size.y, 0.01]);
    }
}

// F4 M3 inserts from the top.
module divider_pad_inserts() {
    for (p = pad_centres()) translate([p.x, p.y, hv_h - insert_m3[1]]) cylinder(d = insert_m3[0], h = insert_m3[1] + 1);
}

// F3 switch cutouts (portrait, + clearance) and the inside pocket that thins the wall to switch_panel_t.
module switch_cutouts() {
    for (s = switches) {
        x = s[1];  c = s[2] + 2 * [fit_clearance, fit_clearance];
        translate([x - c.x / 2, -1, switch_z - c.y / 2]) cube([c.x, wall + 2, c.y]);
        if (switch_panel_t < wall)
            translate([x - c.x / 2 - pocket_margin, switch_panel_t, switch_z - c.y / 2 - pocket_margin])
                cube([c.x + 2 * pocket_margin, wall - switch_panel_t + 1, c.y + 2 * pocket_margin]);
    }
}

// F6/F7 insert bosses on the inside of the back wall. Teardrop cross-section pointing down:
// 45° underside without a support wedge running down the wall (that would reach into the socket bodies).
module back_panel_bosses() {
    for (p = back_screw_positions()) panel_boss(p.x, p.y);
}

module panel_boss(x, z) {
    translate([x, case_d - wall - panel_boss.y, z]) rotate([-90, 0, 0])
        linear_extrude(panel_boss.y + 0.5) teardrop2d(panel_boss.x / 2);
}

function back_screw_positions() = concat(
    [for (dx = [-1, 1]) [iec_x + dx * iec_screw_spacing / 2, back_z]],                       // F6
    [for (s = sockets) for (dx = [-1, 1]) for (dz = [-1, 1])
        [s[1] + dx * socket_holes / 2, back_z + dz * socket_holes / 2]]);                     // F7

// M3 inserts pressed in from outside (teardrop holes), deep enough for M3 × 10 through a flange.
module back_panel_inserts() {
    for (p = back_screw_positions())
        translate([p.x, case_d + 1, p.y]) teardrop_hole(insert_m3[0], 1 + wall + panel_boss.y - 1);
}

// F6 IEC inlet: 27.5 × 31.5 r1 cutout.
module iec_inlet_cutout() {
    c = [iec_cutout.x, iec_cutout.y] + 2 * [fit_clearance, fit_clearance];
    translate([iec_x, case_d + 1, back_z]) rotate([90, 0, 0])
        linear_extrude(wall + 2) rounded_rect(c, iec_cutout[2]);
}

// F7 sockets: Ø43 flat-top teardrop (flat at r = 24, under the 50 mm flange).
module socket_cutouts() {
    for (s = sockets)
        translate([s[1], case_d + 1, back_z]) teardrop_hole(socket_d + 2 * fit_clearance, wall + 2, flat = socket_flat);
}

// F8 jack: Ø6 teardrop + inside pocket Ø16 that thins the wall to jack_panel_t.
module jack_cutout() {
    translate([jack_pos.x, case_d + 1, jack_pos.y]) teardrop_hole(jack_d + 2 * fit_clearance, wall + 2);
    if (jack_panel_t < wall)
        translate([jack_pos.x, case_d - wall - 1, jack_pos.y]) rotate([-90, 0, 0])
            cylinder(d = jack_pocket_d, h = 1 + wall - jack_panel_t);
}

// F9 vent slots 3 × 30 in the left and right walls, low-voltage part only.
module vent_slots_lv() {
    translate([case_w + 1, vent[4], vent[5]]) rotate([0, -90, 0])
        vent_slots(vent[0], vent[2], vent[1], vent[3], case_w + 2);
}

// F16 pry notch: rim cut down to the lid seat, centred on the back wall.
module pry_notch() {
    translate([case_w / 2 - pry_w / 2, case_d - rim_t - 0.5, H]) cube([pry_w, rim_t + 1, lid_t + 1]);
}

// F5 front labels, raised, readable from the front.
module front_labels() {
    for (s = switches)
        translate([s[1], 0.01, front_label_z]) rotate([90, 0, 0])
            linear_extrude(label_raise + 0.01) text(s[0], size = label_size, font = font, halign = "center");
}

// F8 back labels, raised, readable from the back (mirrored in X).
module back_labels() {
    back_label("POWER", iec_x, back_label_z);
    for (s = sockets) back_label(s[0], s[1], back_label_z);
    back_label("TEMP", jack_pos.x, temp_label_z);
}

module back_label(t, x, z) {
    translate([x, case_d - 0.01, z]) rotate([90, 0, 180])
        linear_extrude(label_raise + 0.01) text(t, size = label_size, font = font, halign = "center");
}
