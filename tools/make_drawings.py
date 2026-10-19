#!/usr/bin/env python3
"""Generates the dimensioned spec drawings in 02-specification/drawings/ (SVG, mm).

The numbers below mirror the tables in 02-specification/spec.md. Change the spec first, then here.
Usage: python3 tools/make_drawings.py
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "02-specification" / "drawings"

# --- spec values (mm) -------------------------------------------------------
W, D = 190, 160                    # P1, P2 outer width (X) / depth (Y)
WALL = 3                           # P5
LID_T = 3                          # P6
DIV_T = 3                          # P7
MAINS_H = 70                       # P3 body bottom -> divider underside
RPI_H = 47                         # P4 divider top -> body top
H = MAINS_H + DIV_T + RPI_H        # 120 body height
COL_C, COL_R = 7, 5                # corner columns: centre inset, radius
PADS = [(8, 40), (8, 120), (182, 40), (182, 120)]   # divider pads (centre x, y), 10 x 14
PI = dict(x=12, y=52, w=85, d=56, holes=[(35.5, 55.5), (93.5, 55.5), (35.5, 104.5), (93.5, 104.5)])
GPIO = (38.9, 53, 51, 5)           # header footprint (x, y, w, d)
RELAY = dict(x=102, y=55, w=75, d=55, holes=[(105, 58), (174, 58), (105, 107), (174, 107)])
SLOT = dict(cx=60, cy=38, w=50, h=14)                # feed-through
ADAPTER = dict(x=20, y=65, w=50, d=49, h=27)
Z_PANEL = 40                       # front switch centre height
SWITCHES = [  # name, x, cutout w, cutout h (portrait), bezel w, bezel h
    ("MAIN", 40, 22, 27, 29, 35.3),
    ("BOILER", 115, 21.5, 28.5, 26, 35),
    ("PUMP", 150, 21.5, 28.5, 26, 35),
]
Z_BACK = 38                        # back panel component centre height
IEC = dict(x=155, cw=27.5, ch=31.5, r=4, fw=43.8, fh=32.8, hole_dx=18)
SOCKETS = [("BOILER", 100), ("PUMP", 45)]            # x centres; cutout Ø43 flat-top at r 24
SOCKET = dict(d=43, flat=24, flange=50, holes=38)
JACK = dict(x=155, z=98, d=6)

# --- tiny SVG helper ----------------------------------------------------------
INK, HID, CUT, PART, DIM, SOFT = "#222", "#666", "#e6e6e6", "#c2185b", "#1565c0", "#999"


class Sheet:
    def __init__(self, title, umin, umax, vmin, vmax, margin=28):
        self.title, self.el = title, []
        self.ox, self.oy = margin - umin, margin + 10 + vmax
        self.w, self.h = umax - umin + 2 * margin, vmax - vmin + 2 * margin + 10

    def P(self, u, v):
        return self.ox + u, self.oy - v

    def add(self, s):
        self.el.append(s)

    def rect(self, u, v, w, h, stroke=INK, fill="none", sw=0.5, dash=None, rx=0):
        x, y = self.P(u, v + h)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, u, v, r, stroke=INK, fill="none", sw=0.4, dash=None):
        x, y = self.P(u, v)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, u1, v1, u2, v2, stroke=INK, sw=0.4, dash=None):
        (x1, y1), (x2, y2) = self.P(u1, v1), self.P(u2, v2)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, u, v, s, size=3.5, fill=INK, anchor="middle", weight="normal", rot=0):
        x, y = self.P(u, v)
        r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
                 f'font-weight="{weight}" font-family="Helvetica, Arial, sans-serif"{r}>{s}</text>')

    def teardrop(self, u, v, r, flat=None, fill=CUT):
        """Teardrop hole (point up), optionally truncated flat at height `flat` above the centre."""
        a = r / math.sqrt(2)
        apex = r * math.sqrt(2)
        top = [(-(apex - flat), flat), (apex - flat, flat)] if flat and flat < apex else [(0, apex)]
        pts = [(-a, a)] + top + [(a, a)]
        p = [self.P(u + du, v + dv) for du, dv in pts]
        path = f"M{p[0][0]:.2f},{p[0][1]:.2f} " + " ".join(f"L{x:.2f},{y:.2f}" for x, y in p[1:])
        path += f" A{r},{r} 0 1 1 {p[0][0]:.2f},{p[0][1]:.2f} Z"
        self.add(f'<path d="{path}" fill="{fill}" stroke="{INK}" stroke-width="0.4"/>')

    def dim_h(self, u1, u2, v, off, label=None):
        """Horizontal dimension between u1 and u2, measured at v, drawn `off` away."""
        vv = v + off
        self.line(u1, v, u1, vv + (1.5 if off > 0 else -1.5), DIM, 0.2)
        self.line(u2, v, u2, vv + (1.5 if off > 0 else -1.5), DIM, 0.2)
        self._arrow_line(self.P(u1, vv), self.P(u2, vv))
        self.text((u1 + u2) / 2, vv + 1.2, label or f"{abs(u2 - u1):g}", 3.2, DIM)

    def dim_v(self, v1, v2, u, off, label=None):
        uu = u + off
        self.line(u, v1, uu + (1.5 if off > 0 else -1.5), v1, DIM, 0.2)
        self.line(u, v2, uu + (1.5 if off > 0 else -1.5), v2, DIM, 0.2)
        self._arrow_line(self.P(uu, v1), self.P(uu, v2))
        self.text(uu - 1.2, (v1 + v2) / 2, label or f"{abs(v2 - v1):g}", 3.2, DIM, rot=-90)

    def _arrow_line(self, a, b):
        self.add(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{DIM}" '
                 f'stroke-width="0.25" marker-start="url(#a)" marker-end="url(#a)"/>')

    def save(self, name, notes=()):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w * 3:.0f}" height="{self.h * 3:.0f}" '
                f'viewBox="0 0 {self.w:.2f} {self.h:.2f}">'
                '<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" '
                f'orient="auto-start-reverse"><path d="M0,2 L5,5 L0,8" fill="none" stroke="{DIM}"/></marker></defs>'
                f'<rect width="100%" height="100%" fill="#fff"/>'
                f'<text x="6" y="9" font-size="5" font-weight="bold" font-family="Helvetica, Arial, sans-serif" '
                f'fill="{INK}">{self.title}</text>')
        foot = "".join(
            f'<text x="6" y="{self.h - 4 - 4.5 * i:.2f}" font-size="3" fill="{HID}" '
            f'font-family="Helvetica, Arial, sans-serif">{n}</text>' for i, n in enumerate(reversed(notes)))
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text(head + "".join(self.el) + foot + "</svg>\n")
        print("wrote", OUT / name)


def case_outline(s):
    s.rect(0, -LID_T, W, LID_T, fill="#f4f4f4")            # bottom lid
    s.rect(0, 0, W, H)                                      # body
    s.rect(0, H, W, LID_T, fill="#f4f4f4")                 # top lid
    s.line(0, MAINS_H, W, MAINS_H, HID, 0.3, "2 1.5")       # divider (hidden)
    s.line(0, MAINS_H + DIV_T, W, MAINS_H + DIV_T, HID, 0.3, "2 1.5")
    s.text(3, MAINS_H + DIV_T + 3, "RPI part", 3, HID, "start")
    s.text(3, MAINS_H - 5, "MAINS part", 3, HID, "start")


def front():
    s = Sheet("Front view (from -Y)", -12, W + 30, -LID_T - 22, H + LID_T + 26)
    case_outline(s)
    for name, x, cw, ch, bw, bh in SWITCHES:
        s.rect(x - bw / 2, Z_PANEL - bh / 2, bw, bh, PART, sw=0.35, dash="1.5 1")
        s.rect(x - cw / 2, Z_PANEL - ch / 2, cw, ch, fill=CUT)
        s.text(x, Z_PANEL - 1, f"{cw:g}×{ch:g}", 2.6, INK)
        s.text(x, 12, name, 6, INK, weight="bold")
    s.dim_h(0, W, -LID_T, -12)
    xs = [0] + [sw[1] for sw in SWITCHES]
    for a, b in zip(xs, xs[1:]):
        s.dim_h(a, b, H + LID_T, 8 if a == 0 else 15 if b == 115 else 8)
    s.dim_v(-LID_T, H + LID_T, 0, -10, "126")
    s.dim_v(0, Z_PANEL, W, 22)
    s.dim_v(0, MAINS_H, W, 14, "70 (divider)")
    s.save("front-view.svg", [
        "Grey = cutout (clearance P9 added in the model), dashed pink = switch bezel. Labels raised 0.6 mm, 6 mm text.",
        "Front wall is thinned to 2.0 mm (P10) from the inside around the switch cutouts for the snap-in clips."])


def back():
    s = Sheet("Back view (from +Y), mirrored X: u = 190 - x", -12, W + 30, -LID_T - 22, H + LID_T + 26)
    case_outline(s)
    u = lambda x: W - x
    # IEC inlet
    iu = u(IEC["x"])
    s.rect(iu - IEC["fw"] / 2, Z_BACK - IEC["fh"] / 2, IEC["fw"], IEC["fh"], PART, sw=0.35, dash="1.5 1")
    s.rect(iu - IEC["cw"] / 2, Z_BACK - IEC["ch"] / 2, IEC["cw"], IEC["ch"], fill=CUT, rx=IEC["r"])
    for dx in (-IEC["hole_dx"], IEC["hole_dx"]):
        s.circle(iu + dx, Z_BACK, 2, fill=CUT)
    s.text(iu, Z_BACK - 1, "27.5×31.5", 2.6)
    s.text(iu, 4, "POWER", 6, weight="bold")
    # sockets
    for name, x in SOCKETS:
        su, f, hp = u(x), SOCKET["flange"], SOCKET["holes"] / 2
        s.rect(su - f / 2, Z_BACK - f / 2, f, f, PART, sw=0.35, dash="1.5 1", rx=4)
        s.teardrop(su, Z_BACK, SOCKET["d"] / 2, SOCKET["flat"])
        for dx in (-hp, hp):
            for dz in (-hp, hp):
                s.circle(su + dx, Z_BACK + dz, 2, fill=CUT)
        s.text(su, Z_BACK - 1, "Ø43", 3)
        s.text(su, 4, name, 6, weight="bold")
    # jack
    s.teardrop(u(JACK["x"]), JACK["z"], JACK["d"] / 2)
    s.circle(u(JACK["x"]), JACK["z"], 5, PART, sw=0.35, dash="1.5 1")
    s.text(u(JACK["x"]), 86, "TEMP", 6, weight="bold")
    s.dim_h(0, W, -LID_T, -12)
    us = sorted([0, u(IEC["x"])] + [u(x) for _, x in SOCKETS])
    for a, b in zip(us, us[1:]):
        s.dim_h(a, b, H + LID_T, 8)
    s.dim_v(0, Z_BACK, W, 14)
    s.dim_v(0, JACK["z"], W, 22)
    s.save("back-view.svg", [
        "Sockets: Ø43 cutout with flat-top teardrop (top flat at r = 24, hidden by the 50 mm flange). Holes on 38 mm square.",
        "IEC: cutout 27.5×31.5 r4, screws 36 apart. Jack: Ø6 teardrop. All screw holes take M3 inserts pressed in from outside."])


def top():
    s = Sheet("Plan view at divider (from +Z, front at bottom)", -12, W + 12, -22, D + 26)
    s.rect(0, 0, W, D, rx=4)
    s.rect(WALL, WALL, W - 2 * WALL, D - 2 * WALL, SOFT, sw=0.3)
    for cx in (COL_C, W - COL_C):
        for cy in (COL_C, D - COL_C):
            s.circle(cx, cy, COL_R, fill="#f0f0f0")
            s.circle(cx, cy, 1.7)
    for px, py in PADS:
        s.rect(px - 5, py - 7, 10, 14, fill="#f0f0f0", sw=0.3)
        s.circle(px, py, 1.7)
    a = ADAPTER
    s.rect(a["x"], a["y"], a["w"], a["d"], SOFT, sw=0.35, dash="3 1.5")
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] + 1.5, "USB-C adapter 50×49 (on bottom lid)", 2.4, SOFT)
    r = RELAY
    s.rect(r["x"], r["y"], r["w"], r["d"], PART, sw=0.45, dash="3 1.5")
    for hx, hy in r["holes"]:
        s.circle(hx, hy, 4, PART, dash="1 1")
    s.text(r["x"] + r["w"] / 2, r["y"] + r["d"] / 2, "Relay board (BELOW divider)", 3, PART)
    s.text(r["x"] + r["w"] / 2, r["y"] + r["d"] / 2 - 4.5, "assumed 75×55, holes 69×49", 2.6, PART)
    p = PI
    s.rect(p["x"], p["y"], p["w"], p["d"], PART, "#fce4ec", 0.5)
    s.rect(*GPIO, PART, "#f8bbd0", 0.3)
    for hx, hy in p["holes"]:
        s.circle(hx, hy, 1.4, PART)
    s.text(p["x"] + p["w"] / 2, p["y"] + p["d"] / 2 + 2, "Raspberry Pi 3/4/5", 3.4, PART, weight="bold")
    s.text(p["x"] + p["w"] / 2, p["y"] + p["d"] / 2 - 3, "85×56, holes 58×49 M2.5", 2.6, PART)
    s.text(p["x"] + p["w"] / 2, p["y"] + 8, "GPIO header (front)", 2.4, PART)
    s.text(p["x"] + 4, p["y"] + p["d"] / 2, "USB/Eth end", 2.4, PART, rot=-90)
    sl = SLOT
    s.rect(sl["cx"] - sl["w"] / 2, sl["cy"] - sl["h"] / 2, sl["w"], sl["h"], fill=CUT, rx=7)
    s.text(sl["cx"], sl["cy"] - 1, "feed-through 50×14", 2.6)
    s.dim_h(0, W, 0, -12)
    s.dim_v(0, D, W, 10)
    s.dim_h(0, p["x"], D, 8)
    s.dim_h(p["x"], p["x"] + p["w"], D, 8)
    s.dim_h(r["x"], r["x"] + r["w"], D, 16)
    s.dim_v(0, p["y"], 0, -6)
    s.dim_v(r["y"], r["y"] + r["d"], r["x"] + r["w"], 4)
    s.save("plan-view.svg", [
        "Solid pink = on top of the divider. Dashed pink = hanging under the divider on 6 mm standoffs. Dashed grey = on the bottom lid.",
        "Divider plate rests on 4 pads (10×14, M3 inserts) and clears the Ø10 corner columns. Front = bottom edge of this sheet."])


def section():
    s = Sheet("Section A-A at x = 140 (viewed from -X, front left)", -18, D + 34, -LID_T - 20, H + LID_T + 18)
    # walls (cut)
    s.rect(0, 0, WALL, H, fill=CUT)
    s.rect(D - WALL, 0, WALL, H, fill=CUT)
    s.rect(0, -LID_T, D, LID_T, fill=CUT)
    s.rect(0, H, D, LID_T, fill=CUT)
    s.rect(WALL + 0.3, MAINS_H, D - 2 * WALL - 0.6, DIV_T, fill=CUT)
    s.text(D / 2, MAINS_H + 0.8, "divider plate", 2.2)
    # relay board hanging
    r = RELAY
    for hy in (58, 107):
        s.rect(hy - 4, MAINS_H - 6, 8, 6, fill=CUT, sw=0.3)
    s.rect(r["y"], MAINS_H - 7.6, r["d"], 1.6, PART, "#fce4ec")
    s.rect(r["y"] + 3, MAINS_H - 7.6 - 16, r["d"] - 6, 16, PART, sw=0.35, dash="1.5 1")
    s.text(r["y"] + r["d"] / 2, MAINS_H - 17, "relays", 3, PART)
    # Pi (beyond the cut)
    p = PI
    s.rect(p["y"], MAINS_H + DIV_T + 10, p["d"], 1.6, PART, sw=0.35, dash="1.5 1")
    s.rect(p["y"], MAINS_H + DIV_T + 11.6, p["d"], 17, PART, sw=0.3, dash="1 1")
    s.text(p["y"] + p["d"] / 2, MAINS_H + DIV_T + 20, "Pi (beyond), 10 mm standoffs", 2.6, PART)
    # adapter (beyond)
    a = ADAPTER
    s.rect(a["y"], 0, a["d"], a["h"], SOFT, sw=0.35, dash="3 1.5")
    s.text(a["y"] + a["d"] / 2, 12, "USB-C adapter (beyond)", 2.4, SOFT)
    # front switch envelope + back socket envelope
    s.rect(-4, Z_PANEL - 17.5, 4, 35, PART, sw=0.35, dash="1.5 1")
    s.rect(WALL, Z_PANEL - 13, 37, 26, PART, sw=0.35, dash="1.5 1")
    s.text(WALL + 18.5, Z_PANEL, "switch", 2.6, PART)
    s.rect(D - WALL - 26, Z_BACK - 21.5, 26, 43, SOFT, sw=0.35, dash="1.5 1")
    s.text(D - WALL - 13, Z_BACK, "socket/IEC", 2.6, SOFT)
    s.dim_v(-LID_T, 0, D, 8)
    s.dim_v(0, MAINS_H, D, 8)
    s.dim_v(MAINS_H + DIV_T, H, D, 8)
    s.dim_v(H, H + LID_T, D, 8)
    s.dim_v(-LID_T, H + LID_T, D, 18, "126")
    s.dim_v(MAINS_H - 7.6 - 16, MAINS_H, 0, -8, "≈24")
    s.dim_h(0, D, -LID_T, -12)
    s.dim_h(r["y"], r["y"] + r["d"], MAINS_H - 24, -6)
    s.save("section-a-a.svg", [
        "Cut faces grey. Dashed = components / envelopes. Free height above the Pi board ≈ 35 mm (GPIO jumper wires, Pi 5 cooler).",
        "Clearances checked: relay ↔ switch backs ≥ 3 mm (Y), relay ↔ socket bodies ≥ 20 mm (Y), relay ↔ adapter ≥ 19 mm (Z)."])


if __name__ == "__main__":
    front(); back(); top(); section()
