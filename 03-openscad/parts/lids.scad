// Top lid (part="top_lid"): spec §5.3, F20–F22.
// Bottom lid (part="bottom_lid"): spec §5.4, F30, F32, F33.
// Included by brewberrypi-case.scad. Modelled in use position; the part selector moves them to the bed.

// ---- top lid --------------------------------------------------------------
module top_lid() {
    difference() {
        union() {
            translate([0, 0, H]) linear_extrude(lid_t) outline2d(rim_t + fit_clearance);   // F20
            if (labels) logo();                                                             // F21
        }
        lid_screw_holes(H);                                                                 // F20
        if (fan > 0) fan_mount();                                                           // F22
    }
}

// F21 raised logo on the outer face.
module logo() {
    translate([logo_pos.x, logo_pos.y, body_h - 0.01])
        linear_extrude(logo_raise + 0.01)
            text(logo, size = logo_size, font = font, halign = "center", valign = "center");
}

// F22 optional fan mount over the Pi SoC (30 or 40 mm fan, M3 screws + nuts).
module fan_mount() {
    hole_sq = fan == 40 ? 32 : 24;
    translate([fan_pos.x, fan_pos.y, H - 1]) {
        cylinder(d = fan - 2, h = lid_t + 2);
        for (dx = [-1, 1], dy = [-1, 1])
            translate([dx * hole_sq / 2, dy * hole_sq / 2, 0]) cylinder(d = m3_clear, h = lid_t + 2);
    }
}

// F20 / F30 M3 through-holes over the corner columns.
module lid_screw_holes(z0) {
    for (p = col_centres()) translate([p.x, p.y, z0 - 1]) cylinder(d = m3_clear, h = lid_t + 2);
}

// ---- bottom lid -----------------------------------------------------------
// F32 feet positions (20, 20) … have no geometry.
module bottom_lid() {
    difference() {
        union() {
            translate([0, 0, -lid_t]) linear_extrude(lid_t) outline2d();                   // F30
            bottom_lid_lip();                                                               // F33
        }
        lid_screw_holes(-lid_t);                                                            // F30
    }
}

// F33 locating lip inside the walls, interrupted at the corner columns.
module bottom_lid_lip() {
    o = wall + fit_clearance;
    e = col_inset + col_d / 2 + 0.5;                       // 12.5: stop short of the columns
    translate([e, o, 0]) cube([case_w - 2 * e, lip.x, lip.y]);                        // front
    translate([e, case_d - o - lip.x, 0]) cube([case_w - 2 * e, lip.x, lip.y]);       // back
    translate([o, e, 0]) cube([lip.x, case_d - 2 * e, lip.y]);                        // left
    translate([case_w - o - lip.x, e, 0]) cube([lip.x, case_d - 2 * e, lip.y]);       // right
}
