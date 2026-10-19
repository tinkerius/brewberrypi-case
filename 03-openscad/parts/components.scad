// Bought components as simple envelopes (not printed): assembly view and collision check (AC3, AC10).
// Included by brewberrypi-case.scad. Dimensions from 01-requirements/inputs/components.md (C1–C8).

// ---- envelopes --------------------------------------------------------------
module pi_envelope() {                            // C8 + F11: brass standoffs, board, components / GPIO wires
    for (p = pi_hole_positions()) translate([p.x, p.y, z_div_top + 0.02]) cylinder(d = 5, h = pi_standoff - 0.02, $fn = 6);
    translate([pi_pos.x, pi_pos.y, z_div_top + pi_standoff]) cube([pi_board.x, pi_board.y, 1.6]);
    translate([pi_pos.x, pi_pos.y, z_div_top + pi_standoff + 1.6]) cube([pi_board.x, pi_board.y, 17]);
}

module relay_envelope() {                         // C1 + F12: PCB on the standoffs, relays hanging below
    z_pcb = hv_h - relay_standoff_h - 1.6 - 0.01;  // 0.01 off the standoff tips: touching is not a collision
    translate([relay_pos.x, relay_pos.y, z_pcb]) cube([relay_board.x, relay_board.y, 1.6]);
    translate([relay_pos.x + 3, relay_pos.y + 3, z_pcb - 16]) cube([relay_board.x - 6, relay_board.y - 6, 16]);
}

module adapter_envelope() {                       // C2 + F14: adapter against the plate, USB-C plug + cable below
    translate([adapter_pos.x, adapter_pos.y, hv_h - adapter.z]) cube([adapter.x, adapter.y, adapter.z - 0.01]);
    translate([adapter_pos.x + adapter.x / 2 - 4.5, adapter_pos.y + adapter.y / 2 - 4.5, hv_h - adapter.z - 30])
        cube([9, 9, 30]);
}

module switch_envelope(i) {                       // C6 / C7 + F3: bezel outside, body + connectors inside
    s = switches[i];
    main = i == 0;
    bezel = main ? [29, 35.3] : [26.7, 35];
    body_ = main ? [21.7, 26] : [21, 28];
    depth = main ? 37 : 48;                       // from the outer face, incl. spade connectors
    translate([s[1] - bezel.x / 2, -4, switch_z - bezel.y / 2]) cube([bezel.x, 4 - 0.01, bezel.y]);
    translate([s[1] - body_.x / 2, 0.01, switch_z - body_.y / 2]) cube([body_.x, depth, body_.y]);
}

module socket_envelope(i) {                       // C5 + F7: body Ø43 behind the panel, flange + hinged cover outside
    x = sockets[i][1];
    translate([x, case_d - 26, back_z]) rotate([-90, 0, 0]) cylinder(d = socket_d, h = 26 - 0.01);
    translate([x - 25, case_d + 0.01, back_z - 25]) cube([50, 21, 62]);
}

module iec_envelope() {                           // C4 + F6: body behind the panel, flange outside
    translate([iec_x, case_d - 27.6, back_z]) rotate([-90, 0, 0])
        linear_extrude(27.6 - 0.01) rounded_rect([27, 31], 1);
    translate([iec_x - 21.9, case_d + 0.01, back_z - 16.4]) cube([43.8, 3.1, 32.8]);
}

module jack_envelope() {                          // C3 + F8: body + hex nut inside, thread in the hole, front nut outside
    translate([jack_pos.x, 0, jack_pos.y]) rotate([-90, 0, 0]) {
        translate([0, 0, case_d - 15]) cylinder(d = 9, h = 13);                       // body
        translate([0, 0, case_d - 3.99]) cylinder(d = 12, h = 1.98, $fn = 6);         // hex nut, in the pocket
        translate([0, 0, case_d - jack_panel_t - 0.5]) cylinder(d = jack_d, h = 3);   // thread
        translate([0, 0, case_d + 0.01]) cylinder(d = 10, h = 3);                     // front nut
    }
}

// ---- grouping ---------------------------------------------------------------
module components_on_divider() {
    color("#2e7d32", 0.9) pi_envelope();
    color("#c62828", 0.9) relay_envelope();
    color("#212121", 0.9) adapter_envelope();
}

module components_in_body() {
    for (i = [0 : len(switches) - 1]) color("#43a047", 0.9) switch_envelope(i);
    for (i = [0 : len(sockets) - 1]) color("#424242", 0.9) socket_envelope(i);
    color("#424242", 0.9) iec_envelope();
    color("#b8860b", 0.9) jack_envelope();
}

// Component i of the collision list.
n_components = 10;
module component(i) {
    if (i == 0) pi_envelope();
    else if (i == 1) relay_envelope();
    else if (i == 2) adapter_envelope();
    else if (i <= 5) switch_envelope(i - 3);
    else if (i <= 7) socket_envelope(i - 6);
    else if (i == 8) iec_envelope();
    else jack_envelope();
}

// AC3 + AC10: every intersection below must be empty, so a clean model renders nothing.
// Parts that rest on each other (lids on the body, divider on the pads) are lifted 0.01 mm apart,
// because touching faces are intended and are not a collision.
module collision_check() {
    for (i = [0 : n_components - 1]) intersection() { printed_parts(); component(i); }      // component ↔ print
    for (i = [0 : n_components - 2], j = [i + 1 : n_components - 1])
        intersection() { component(i); component(j); }                                   // component ↔ component
    intersection() { body(); translate([0, 0, 0.01]) top_lid(); }                        // AC10 joints
    intersection() { body(); translate([0, 0, -0.01]) bottom_lid(); }
    intersection() { body(); translate([0, 0, 0.01]) divider(); }
}

module printed_parts() {     // as assembled, resting parts 0.01 mm apart (see collision_check)
    body();
    translate([0, 0, 0.01]) divider();
    translate([0, 0, 0.01]) top_lid();
    translate([0, 0, -0.01]) bottom_lid();
}
