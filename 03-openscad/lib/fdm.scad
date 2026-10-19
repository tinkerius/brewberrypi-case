// Printer-agnostic FDM helpers (see docs/fdm-design-rules.md).
// No printer or slicer settings here, only geometry.

// Default clearance per side between mating parts (mm). Override in the entry file.
fit_clearance_default = 0.2;

// 2D teardrop: circle of radius r with a 45° point towards +Y.
module teardrop2d(r) {
    union() {
        circle(r = r);
        polygon([[-r / sqrt(2), r / sqrt(2)], [0, r * sqrt(2)], [r / sqrt(2), r / sqrt(2)]]);
    }
}

// Horizontal hole along Y with the teardrop point facing +Z (up). Subtract from a wall.
module teardrop_hole(d, length, center = true) {
    rotate([90, 0, 0])
        linear_extrude(height = length, center = center)
            teardrop2d(d / 2);
}

// Cube from [0,0,0] to size, with 45° chamfered bottom edges (printable, unlike a bottom fillet).
module bottom_chamfer_cube(size, chamfer) {
    hull() {
        translate([chamfer, chamfer, 0])
            cube([size.x - 2 * chamfer, size.y - 2 * chamfer, chamfer]);
        translate([0, 0, chamfer])
            cube([size.x, size.y, size.z - chamfer]);
    }
}

// Row of rounded vent slots, running along X, spaced along Y, cut through Z from 0 to depth.
module vent_slots(count, length, width, pitch, depth) {
    for (i = [0 : count - 1])
        translate([0, i * pitch, 0])
            hull() {
                translate([width / 2, 0, 0]) cylinder(d = width, h = depth, $fn = 24);
                translate([length - width / 2, 0, 0]) cylinder(d = width, h = depth, $fn = 24);
            }
}
