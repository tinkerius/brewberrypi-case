#!/usr/bin/env python3
"""Overhang report for STLs in print orientation (AC6).

Lists connected regions of facets that face downward more steeply than 45° and do not lie on the bed.
Flat regions (horizontal undersides) are bridges or ledges: judge them by their size in the report.
Usage: python3 tools/overhangs.py file.stl [...]
"""
import math
import struct
import sys

LIMIT = -math.cos(math.radians(45)) - 1e-3   # nz below this = steeper than 45°
BED = 0.05                                   # facets lower than this lie on the bed
TINY = 5.0                                   # mm², regions below this are only counted (text, small hole tops)


def facets(path):
    data = open(path, "rb").read()
    if data[:5] == b"solid" and b"facet" in data[:300]:
        tri = []
        for line in data.decode(errors="ignore").splitlines():
            parts = line.split()
            if parts[:1] == ["vertex"]:
                tri.append(tuple(map(float, parts[1:4])))
                if len(tri) == 3:
                    yield tri
                    tri = []
        return
    (n,) = struct.unpack_from("<I", data, 80)
    for i in range(n):
        v = struct.unpack_from("<12f", data, 84 + 50 * i)
        yield [v[3:6], v[6:9], v[9:12]]


def analyse(path):
    regions, parent = {}, {}

    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    down = []
    for a, b, c in facets(path):
        u = [b[i] - a[i] for i in range(3)]
        w = [c[i] - a[i] for i in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        ln = math.sqrt(sum(x * x for x in n)) or 1
        nz = n[2] / ln
        if nz < LIMIT and min(a[2], b[2], c[2]) > BED:
            keys = [tuple(round(x, 3) for x in p) for p in (a, b, c)]
            for k in keys[1:]:
                parent[find(k)] = find(keys[0])
            down.append((keys, ln / 2, nz))
    for keys, area, nz in down:
        r = regions.setdefault(find(keys[0]), {"area": 0, "pts": [], "flat": True})
        r["area"] += area
        r["pts"] += keys
        r["flat"] &= nz < -0.999
    return regions.values()


def main():
    for path in sys.argv[1:]:
        regs = sorted(analyse(path), key=lambda r: -r["area"])
        big = [r for r in regs if r["area"] >= TINY]
        tiny = [r for r in regs if r["area"] < TINY]
        print(f"== {path}: {len(big)} region(s) ≥ {TINY:g} mm², {len(tiny)} tiny "
              f"({sum(r['area'] for r in tiny):.1f} mm² in total)")
        for r in big:
            xs, ys, zs = zip(*r["pts"])
            kind = "flat (bridge/ledge)" if r["flat"] else "sloped"
            print(f"   {kind:20s} area {r['area']:7.1f} mm²  x {min(xs):6.1f}…{max(xs):6.1f}  "
                  f"y {min(ys):6.1f}…{max(ys):6.1f}  z {min(zs):6.1f}…{max(zs):6.1f}")


if __name__ == "__main__":
    main()
