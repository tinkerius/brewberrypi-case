#!/usr/bin/env python3
"""Converts the brand logo (B2, an SVG with masks) into OpenSCAD outlines: 03-openscad/lib/brand-logo.scad (F21).

OpenSCAD's SVG import ignores masks, so the dial ring, needle and berry dots would come out solid. This script
flattens the SVG itself: curves become polylines, transforms are applied, and every masked shape becomes a
difference(). Coordinates stay in brand units, with Y flipped so the logo reads the right way up in OpenSCAD.
Only the SVG features the brand files use are supported (rect, circle, path with absolute M L H V C Q A Z, g,
translate / scale / rotate, masks in user space). Anything else stops the script.

Usage: python3 tools/make_logo.py
"""
import math
import pathlib
import re
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "01-requirements" / "inputs" / "brand-logo-stacked.svg"   # B2
OUT = ROOT / "03-openscad" / "lib" / "brand-logo.scad"
NS = "{http://www.w3.org/2000/svg}"
STEPS = 16          # segments per Bézier curve
SEG = 96            # segments per full circle
CLOSE = 0.01        # closing (grow, then shrink) in brand units: shapes that only touch at a point (the two leaf
                    # lobes) get a tiny neck, so the extruded logo is a closed mesh. Smallest real gap: 0.79
IDENT = (1, 0, 0, 1, 0, 0)


# --- transforms (SVG matrix a b c d e f) ----------------------------------------
def mul(m, n):
    return (m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3],
            m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5])


def transform(s):
    m = IDENT
    for name, args in re.findall(r"(\w+)\(([^)]*)\)", s or ""):
        v = [float(x) for x in re.split(r"[\s,]+", args.strip())]
        if name == "translate":
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            c, s_ = math.cos(math.radians(v[0])), math.sin(math.radians(v[0]))
            t = (c, s_, -s_, c, 0, 0)
            if len(v) == 3:
                t = mul(mul((1, 0, 0, 1, v[1], v[2]), t), (1, 0, 0, 1, -v[1], -v[2]))
        else:
            raise SystemExit(f"make_logo: unsupported transform {name}()")
        m = mul(m, t)
    return m


def apply(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


# --- shapes → rings (closed point lists) ------------------------------------------
def bezier(*ctrl):
    """Points of a quadratic or cubic Bézier after its start point."""
    n = len(ctrl) - 1
    return [tuple(sum(math.comb(n, i) * (1 - t) ** (n - i) * t ** i * c[k] for i, c in enumerate(ctrl)) for k in (0, 1))
            for t in (j / STEPS for j in range(1, STEPS + 1))]


def arc(p0, r, large, sweep, p1):
    """Circular SVG arc (rx = ry, no rotation): centre from SVG 1.1 F.6.5."""
    mx, my = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    d2 = mx * mx + my * my
    r = max(r, math.sqrt(d2))
    k = math.sqrt(max(r * r - d2, 0) / d2) * (-1 if large == sweep else 1)
    cx, cy = (p0[0] + p1[0]) / 2 + k * my, (p0[1] + p1[1]) / 2 - k * mx
    a0 = math.atan2(p0[1] - cy, p0[0] - cx)
    da = math.atan2(p1[1] - cy, p1[0] - cx) - a0
    da += 2 * math.pi if sweep and da < 0 else -2 * math.pi if not sweep and da > 0 else 0
    n = max(4, round(abs(da) / (2 * math.pi) * SEG))
    return [(cx + r * math.cos(a0 + da * i / n), cy + r * math.sin(a0 + da * i / n)) for i in range(1, n + 1)]


def path(d):
    toks = re.findall(r"[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:[eE]-?\d+)?", d)
    rings, ring, cur, i, cmd = [], [], (0.0, 0.0), 0, None

    def nums(n):
        nonlocal i
        i += n
        return [float(t) for t in toks[i - n:i]]

    while i < len(toks):
        if toks[i].isalpha():
            cmd, i = toks[i], i + 1
        if cmd not in "MLHVCQAZ":
            raise SystemExit(f"make_logo: unsupported path command {cmd}")
        if cmd == "M":
            if ring:
                rings.append(ring)
            cur = tuple(nums(2))
            ring, cmd = [cur], "L"          # further pairs after M are line-tos
        elif cmd == "L":
            cur = tuple(nums(2))
            ring.append(cur)
        elif cmd in "HV":
            v = nums(1)[0]
            cur = (v, cur[1]) if cmd == "H" else (cur[0], v)
            ring.append(cur)
        elif cmd in "CQ":
            v = nums(6 if cmd == "C" else 4)
            ctrl = [cur] + [tuple(v[j:j + 2]) for j in range(0, len(v), 2)]
            ring += bezier(*ctrl)
            cur = ctrl[-1]
        elif cmd == "A":
            rx, ry, rot, large, sweep, x, y = nums(7)
            if rx != ry or rot:
                raise SystemExit("make_logo: only circular arcs are supported")
            ring += arc(cur, rx, int(large), int(sweep), (x, y))
            cur = (x, y)
        else:   # Z
            if ring:
                rings.append(ring)
            ring = []
    if ring:
        rings.append(ring)
    return rings


def rounded_rect(x, y, w, h, r):
    if r <= 0:
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    r, q = min(r, w / 2, h / 2), SEG // 4
    corners = ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180))
    return [(cx + r * math.cos(math.radians(a + 90 * j / q)), cy + r * math.sin(math.radians(a + 90 * j / q)))
            for cx, cy, a in corners for j in range(q + 1)]


def rings_of(el, m):
    """Rings of a rect, circle or path element in the coordinates of matrix m (parent transforms)."""
    tag, f = el.tag.removeprefix(NS), lambda k: float(el.get(k, 0))
    if tag == "rect":
        rings = [rounded_rect(f("x"), f("y"), f("width"), f("height"), float(el.get("rx", el.get("ry", 0))))]
    elif tag == "circle":
        rings = [[(f("cx") + f("r") * math.cos(2 * math.pi * j / SEG), f("cy") + f("r") * math.sin(2 * math.pi * j / SEG))
                  for j in range(SEG)]]
    elif tag == "path":
        rings = path(el.get("d"))
    else:
        raise SystemExit(f"make_logo: unsupported element <{tag}>")
    m = mul(m, transform(el.get("transform")))
    return [clean([apply(m, p) for p in r]) for r in rings]


def clean(r):
    out = []
    for p in r:
        if not out or math.dist(p, out[-1]) > 1e-6:
            out.append(p)
    while len(out) > 1 and math.dist(out[0], out[-1]) < 1e-6:
        out.pop()
    return out


# --- fill rule ----------------------------------------------------------------------
def area(r):
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(r, r[1:] + r[:1])) / 2


def inside(p, r):
    c = False
    for a, b in zip(r, r[1:] + r[:1]):
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1]):
            c = not c
    return c


def shapes(rings):
    """Nonzero fill as fonts use it: outer contours run one way, their holes the other way and lie inside them.
    Each glyph becomes its own polygon, so touching or overlapping glyphs can't punch holes into each other."""
    sign = math.copysign(1, area(max(rings, key=lambda r: abs(area(r)))))
    outer = [(r, []) for r in rings if math.copysign(1, area(r)) == sign]
    for h in (r for r in rings if math.copysign(1, area(r)) != sign):
        min((o for o in outer if inside(h[0], o[0])), key=lambda o: abs(area(o[0])))[1].append(h)
    return outer


def polygon(outer, holes=()):
    pts, paths = [], []
    for r in (outer, *holes):
        paths.append(list(range(len(pts), len(pts) + len(r))))
        pts += r
    p = ",".join(f"[{x:.3f},{-y:.3f}]" for x, y in pts)        # flip Y: SVG down → OpenSCAD up
    return f"polygon([{p}], {paths});" if holes else f"polygon([{p}]);"


# --- main ---------------------------------------------------------------------------
def main():
    root = ET.parse(SRC).getroot()
    masks = {m.get("id"): [c for g in m.iter(NS + "g") for c in g] for m in root.iter(NS + "mask")}

    def walk(node, m):
        for el in node:
            tag = el.tag.removeprefix(NS)
            if tag == "g":
                yield from walk(el, mul(m, transform(el.get("transform"))))
            elif tag in ("rect", "circle", "path"):
                yield el, m
            elif tag not in ("title", "style", "mask", "desc"):
                raise SystemExit(f"make_logo: unsupported element <{tag}>")

    body, pts = [], []
    for el, m in walk(root, IDENT):
        rings = rings_of(el, m)
        pts += [p for r in rings for p in r]
        solid = " ".join(polygon(o, h) for o, h in shapes(rings))
        ref = re.fullmatch(r"url\(#(.+)\)", el.get("mask", ""))
        if ref:   # maskUnits="userSpaceOnUse": the mask shapes live in the masked element's coordinates
            user = mul(m, transform(el.get("transform")))
            cut = " ".join(polygon(r) for c in masks[ref.group(1)] for r in rings_of(c, user))
            body.append(f"difference() {{ union() {{ {solid} }} {cut} }}")
        else:
            body.append(solid)
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = -max(p[1] for p in pts), -min(p[1] for p in pts)
    rel = SRC.relative_to(ROOT).as_posix()
    OUT.write_text(
        f"// Generated by tools/make_logo.py from {rel} (B2). Do not edit: change the script and rerun it.\n"
        "// Brand logo (stacked), one colour, in brand units (1 unit = 1 mm before scaling), Y up.\n"
        "// The SVG masks (dial ring, needle, berry dots) are cut out with difference().\n"
        f"// offset() closes by {CLOSE} so shapes that only touch at a point don't leave a non-manifold pinch.\n\n"
        f"// Drawn area [[x0, y0], [x1, y1]]: {x1 - x0:.2f} x {y1 - y0:.2f}\n"
        f"function brand_logo_box() = [[{x0:.3f}, {y0:.3f}], [{x1:.3f}, {y1:.3f}]];\n\n"
        f"module brand_logo_2d() {{\n    offset(r = -{CLOSE}, $fn = 16) offset(delta = {CLOSE}) union() {{\n"
        + "".join(f"        {b}\n" for b in body) + "    }\n}\n")
    print(f"wrote {OUT} ({x1 - x0:.2f} x {y1 - y0:.2f} brand units)")


if __name__ == "__main__":
    main()
