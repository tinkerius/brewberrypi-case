#!/usr/bin/env python3
"""Label and logo sizes measured on the STLs (AC8): capital height and how far they are raised.

Usage: python3 tools/labels.py   (reads 04-stl/brewberrypi-case-body.stl and -top_lid.stl)
"""
import struct


def points(path):
    data = open(path, "rb").read()
    (n,) = struct.unpack_from("<I", data, 80)
    for i in range(n):
        v = struct.unpack_from("<12f", data, 84 + 50 * i)
        yield from (v[3:6], v[6:9], v[9:12])


def show(name, pts, axis_up, axis_out, base):
    if not pts:
        print(f"   {name:8s} not found")
        return
    up = [p[axis_up] for p in pts]
    out = [abs(p[axis_out] - base) for p in pts]
    print(f"   {name:8s} capitals {max(up) - min(up):5.2f} mm   raised {max(out):.2f} mm")


body = list(points("04-stl/brewberrypi-case-body.stl"))
front = [("MAIN", 40), ("BOILER", 115), ("PUMP", 150)]                 # x centres, F5 (keep in sync with the model)
back = [("POWER", 35, 20), ("BOILER", 90, 20), ("PUMP", 145, 20), ("TEMP", 35, 200)]   # F8 (keep in sync with the model)
for name, x in front:
    half = 10 if name == "MAIN" else 14
    show(name + " (front)", [p for p in body if p[1] < -0.05 and abs(p[0] - x) < half], 2, 1, 0)
for name, x, zmax in back:
    zmin = 70 if name == "TEMP" else 0
    show(name + " (back)", [p for p in body if p[1] > 160.05 and abs(p[0] - x) < 14 and zmin < p[2] < zmax], 2, 1, 160)
lid = [p for p in points("04-stl/brewberrypi-case-top_lid.stl") if p[2] > 3.05]
x0 = min(p[0] for p in lid)
show("logo 'B'", [p for p in lid if p[0] < x0 + 8], 1, 2, 3)
