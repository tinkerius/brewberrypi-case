#!/usr/bin/env python3
"""Generates the dimensioned spec drawings in 02-specification/drawings/ (SVG, mm).

The numbers below mirror the tables in 02-specification/spec.md. Change the spec first, then here.
Usage: python3 tools/make_drawings.py
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "02-specification" / "drawings"
SPEC_VERSION = "0.2"

# --- spec values (mm) -------------------------------------------------------
W, D = 190, 160                    # P1, P2 outer width (X) / depth (Y)
WALL = 3                           # P5
LID_T = 3                          # P6
DIV_T = 3                          # P7
MAINS_H = 70                       # P3 body bottom -> divider underside
RPI_H = 47                         # P4 divider top -> body top
H = MAINS_H + DIV_T + RPI_H        # 120 body height
Z_DIV_TOP = MAINS_H + DIV_T        # 73
COL_C, COL_R = 7, 5                # corner columns: centre inset, radius
PADS = [(8, 40), (8, 120), (182, 40), (182, 120)]   # divider pads (centre x, y), 10 x 14
PI = dict(x=17, y=55, w=85, d=56, standoff=10, boss=4,
          holes=[(40.5, 58.5), (98.5, 58.5), (40.5, 107.5), (98.5, 107.5)])  # F11
GPIO = (43.9, 56, 51, 5)           # header footprint (x, y, w, d)
RELAY = dict(x=17, y=58, w=75, d=55, standoff=10, pcb=1.6, relays=16,
             holes=[(20, 61), (89, 61), (20, 110), (89, 110)])               # F12
SLOT = dict(cx=111, cy=85, w=14, h=46)                                       # F13
ADAPTER = dict(x=123, y=61, w=50, d=49, h=27, fence=10)                      # F14
Z_PANEL = 40                       # front switch centre height
SWITCHES = [  # name, x, cutout w, cutout h (portrait), bezel w, bezel h, depth behind panel incl. connectors
    ("MAIN", 40, 22, 27, 29, 35.3, 37),
    ("BOILER", 115, 21.5, 28.5, 26, 35, 48),
    ("PUMP", 150, 21.5, 28.5, 26, 35, 48),
]
Z_BACK = 38                        # back panel component centre height
IEC = dict(x=155, cw=27.5, ch=31.5, r=4, fw=43.8, fh=32.8, hole_dx=18, depth=27.6)
SOCKETS = [("BOILER", 100), ("PUMP", 45)]            # x centres; cutout Ø43 flat-top at r 24
SOCKET = dict(d=43, flat=24, flange=50, holes=38, depth=26, front=21)
JACK = dict(x=155, z=98, d=6, nut=10, pocket=16)
Y_CUT = 85                         # section C-C: through the Pi/relay stack, feed-through and adapter

# --- tiny SVG helper ----------------------------------------------------------
INK, HID, CUT, PART, DIM, SOFT, BRASS = "#222", "#666", "#e6e6e6", "#c2185b", "#1565c0", "#999", "#b8860b"


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
                f'fill="{INK}">{self.title}</text>'
                f'<text x="{self.w - 6:.2f}" y="9" font-size="3" text-anchor="end" fill="{HID}" '
                f'font-family="Helvetica, Arial, sans-serif">spec v{SPEC_VERSION} · mm</text>')
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
    s.line(0, Z_DIV_TOP, W, Z_DIV_TOP, HID, 0.3, "2 1.5")
    s.text(3, Z_DIV_TOP + 3, "RPI part", 3, HID, "start")
    s.text(3, MAINS_H - 5, "MAINS part", 3, HID, "start")


def front():
    s = Sheet("Front view (from -Y)", -12, W + 30, -LID_T - 22, H + LID_T + 26)
    case_outline(s)
    for name, x, cw, ch, bw, bh, _ in SWITCHES:
        s.rect(x - bw / 2, Z_PANEL - bh / 2, bw, bh, PART, sw=0.35, dash="1.5 1")
        s.rect(x - cw / 2, Z_PANEL - ch / 2, cw, ch, fill=CUT)
        s.text(x, Z_PANEL - 1, f"{cw:g}×{ch:g}", 2.6, INK)
        s.text(x, 12, name, 6, INK, weight="bold")
    s.dim_h(0, W, -LID_T, -12)
    xs = [0] + [sw[1] for sw in SWITCHES]
    for a, b in zip(xs, xs[1:]):
        s.dim_h(a, b, H + LID_T, 15 if b == 115 else 8)
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
    iu = u(IEC["x"])
    s.rect(iu - IEC["fw"] / 2, Z_BACK - IEC["fh"] / 2, IEC["fw"], IEC["fh"], PART, sw=0.35, dash="1.5 1")
    s.rect(iu - IEC["cw"] / 2, Z_BACK - IEC["ch"] / 2, IEC["cw"], IEC["ch"], fill=CUT, rx=IEC["r"])
    for dx in (-IEC["hole_dx"], IEC["hole_dx"]):
        s.circle(iu + dx, Z_BACK, 2, fill=CUT)
    s.text(iu, Z_BACK - 1, "27.5×31.5", 2.6)
    s.text(iu, 4, "POWER", 6, weight="bold")
    for name, x in SOCKETS:
        su, f, hp = u(x), SOCKET["flange"], SOCKET["holes"] / 2
        s.rect(su - f / 2, Z_BACK - f / 2, f, f, PART, sw=0.35, dash="1.5 1", rx=4)
        s.teardrop(su, Z_BACK, SOCKET["d"] / 2, SOCKET["flat"])
        for dx in (-hp, hp):
            for dz in (-hp, hp):
                s.circle(su + dx, Z_BACK + dz, 2, fill=CUT)
        s.text(su, Z_BACK - 1, "Ø43", 3)
        s.text(su, 4, name, 6, weight="bold")
    ju = u(JACK["x"])
    s.circle(ju, JACK["z"], JACK["pocket"] / 2, HID, sw=0.3, dash="1 1")
    s.circle(ju, JACK["z"], JACK["nut"] / 2, PART, sw=0.35, dash="1.5 1")
    s.teardrop(ju, JACK["z"], JACK["d"] / 2)
    s.text(ju, 82, "TEMP", 6, weight="bold")
    s.dim_h(0, W, -LID_T, -12)
    us = sorted([0, u(IEC["x"])] + [u(x) for _, x in SOCKETS])
    for a, b in zip(us, us[1:]):
        s.dim_h(a, b, H + LID_T, 8)
    s.dim_v(0, Z_BACK, W, 14)
    s.dim_v(0, JACK["z"], W, 22)
    s.save("back-view.svg", [
        "Sockets: Ø43 cutout with flat-top teardrop (top flat at r = 24, hidden by the 50 mm flange). Holes on 38 mm square.",
        "IEC: cutout 27.5×31.5 r4, screws 36 apart. All screw holes take M3 inserts pressed in from outside.",
        "Jack: Ø6 teardrop, point hidden by the Ø10 front nut. Grey dotted Ø16 = inside pocket, wall 2.0 mm (P28)."])


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
    # on top: Pi (solid)
    p = PI
    s.rect(p["x"], p["y"], p["w"], p["d"], PART, "#fce4ec", 0.5)
    s.rect(*GPIO, PART, "#f8bbd0", 0.3)
    for hx, hy in p["holes"]:
        s.circle(hx, hy, 1.4, PART)
    s.text(p["x"] + p["w"] / 2, p["y"] + 40, "Raspberry Pi 3/4/5 (on top)", 3.4, PART, weight="bold")
    s.text(p["x"] + p["w"] / 2, p["y"] + 35, "85×56, holes 58×49 M2.5, 10 mm brass standoffs", 2.4, PART)
    s.text(p["x"] + p["w"] / 2, p["y"] + 7.5, "GPIO header (front)", 2.4, PART)
    s.text(p["x"] + p["w"] / 2, p["y"] + p["d"] - 3, "power socket (back)", 2.4, PART)
    # below: relay board + adapter (dashed)
    r = RELAY
    s.rect(r["x"], r["y"], r["w"], r["d"], "#7b1fa2", sw=0.5, dash="3 1.5")
    for hx, hy in r["holes"]:
        s.circle(hx, hy, 4, "#7b1fa2", dash="1 1")
    s.text(r["x"] + r["w"] / 2, r["y"] + 22, "Relay board (BELOW, directly under the Pi)", 2.6, "#7b1fa2")
    s.text(r["x"] + r["w"] / 2, r["y"] + 18, "assumed 75×55, holes 69×49, 10 mm standoffs", 2.4, "#7b1fa2")
    a = ADAPTER
    s.rect(a["x"], a["y"], a["w"], a["d"], "#7b1fa2", sw=0.5, dash="3 1.5")
    for cx, cy, sx, sy in ((a["x"], a["y"], 1, 1), (a["x"] + a["w"], a["y"], -1, 1),
                           (a["x"], a["y"] + a["d"], 1, -1), (a["x"] + a["w"], a["y"] + a["d"], -1, -1)):
        ox, oy = cx - sx * 2.5, cy - sy * 2.5            # bracket outer corner (0.5 clearance + 2 wall)
        s.line(ox, oy, ox + sx * 12, oy, "#7b1fa2", 1.2)
        s.line(ox, oy, ox, oy + sy * 12, "#7b1fa2", 1.2)
    for lx in (a["x"] + 10, a["x"] + 40):
        s.rect(lx - 4, a["y"] - 5.5, 8, 3, "#7b1fa2", sw=0.3)
        s.rect(lx - 4, a["y"] + a["d"] + 2.5, 8, 3, "#7b1fa2", sw=0.3)
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] / 2 + 3, "USB-C adapter (BELOW)", 2.8, "#7b1fa2", weight="bold")
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] / 2 - 1.5, "50×49, port faces down", 2.4, "#7b1fa2")
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] / 2 - 5.5, "brackets + 2 cable ties", 2.4, "#7b1fa2")
    sl = SLOT
    s.rect(sl["cx"] - sl["w"] / 2, sl["cy"] - sl["h"] / 2, sl["w"], sl["h"], fill=CUT, rx=7)
    s.text(sl["cx"] + 1, sl["cy"], "feed-through 14×46", 2.4, rot=-90)
    for name, x in (("A", PI["holes"][0][0]), ("B", ADAPTER["x"] + ADAPTER["w"] / 2)):
        s.line(x, -4, x, D + 3, DIM, 0.35, "6 1.5 1 1.5")
        s.text(x, -7.5, f"{name}–{name}", 3.4, DIM, weight="bold")
    s.line(-3, Y_CUT, W + 3, Y_CUT, DIM, 0.35, "6 1.5 1 1.5")
    s.text(WALL + 1.5, Y_CUT + 1.5, "C–C", 3.4, DIM, "start", "bold")
    s.text(W - WALL - 1.5, Y_CUT + 1.5, "C–C", 3.4, DIM, "end", "bold")
    s.dim_h(0, W, 0, -12)
    s.dim_v(0, D, W, 10)
    s.dim_h(0, p["x"], D, 8)
    s.dim_h(p["x"], p["x"] + p["w"], D, 8)
    s.dim_h(a["x"], a["x"] + a["w"], D, 8)
    s.dim_h(sl["cx"] - sl["w"] / 2, sl["cx"] + sl["w"] / 2, D, 16)
    s.dim_v(0, p["y"], 0, -6)
    s.dim_v(r["y"], r["y"] + r["d"], 0, -6)
    s.dim_v(a["y"], a["y"] + a["d"], a["x"] + a["w"], 5)
    s.save("plan-view.svg", [
        "Pink solid = on top of the divider. Purple dashed = hanging UNDER the divider (relay board on 10 mm standoffs, adapter in 4 corner brackets).",
        "Divider plate rests on 4 pads (10×14, M3 inserts) and clears the Ø10 corner columns. Front = bottom edge of this sheet.",
        "Blue dash-dot = section lines A–A, B–B (side sections) and C–C (front section)."])


def section_frame(s, L=D, divider=True):
    s.rect(0, 0, WALL, H, fill=CUT)
    s.rect(L - WALL, 0, WALL, H, fill=CUT)
    s.rect(0, -LID_T, L, LID_T, fill=CUT)
    s.rect(0, H, L, LID_T, fill=CUT)
    if divider:
        s.rect(WALL + 0.3, MAINS_H, L - 2 * WALL - 0.6, DIV_T, fill=CUT)
    s.dim_v(-LID_T, 0, L, 8)
    s.dim_v(0, MAINS_H, L, 8)
    s.dim_v(MAINS_H + DIV_T, H, L, 8)
    s.dim_v(H, H + LID_T, L, 8)
    s.dim_v(-LID_T, H + LID_T, L, 18, "126")
    s.dim_h(0, L, -LID_T, -12)


def section_a():
    x_cut = PI["holes"][0][0]
    s = Sheet(f"Section A-A at x = {x_cut:g}: Pi / relay stack (viewed from -X, front left)",
              -20, D + 34, -LID_T - 20, H + LID_T + 18)
    section_frame(s)
    p, r = PI, RELAY
    z_pi = Z_DIV_TOP + p["standoff"]
    # Pi: standoffs (cut), bosses under the plate (cut), board (cut), components envelope
    for _, hy in p["holes"][::2]:
        s.rect(hy - 2.5, Z_DIV_TOP, 5, p["standoff"], BRASS, "#f3e5ab", 0.35)
        s.rect(hy - 3.5, MAINS_H - p["boss"], 7, p["boss"], fill=CUT, sw=0.3)
    s.rect(p["y"], z_pi, p["d"], 1.6, PART, "#f8bbd0", 0.4)
    s.rect(p["y"], z_pi + 1.6, p["d"], 17, PART, sw=0.3, dash="1 1")
    s.text(p["y"] + p["d"] / 2, z_pi + 9, "Pi components / GPIO wires", 2.6, PART)
    # relay: standoffs (beyond), PCB, relays
    z_pcb = MAINS_H - r["standoff"]
    for hy in (61, 110):
        s.rect(hy - 4, z_pcb, 8, r["standoff"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(r["y"], z_pcb - r["pcb"], r["d"], r["pcb"], "#7b1fa2", "#e1bee7", 0.4)
    s.rect(r["y"] + 3, z_pcb - r["pcb"] - r["relays"], r["d"] - 6, r["relays"], "#7b1fa2", sw=0.35, dash="1.5 1")
    s.text(r["y"] + r["d"] / 2, z_pcb - 11, "relays (facing down)", 2.6, "#7b1fa2")
    # MAIN switch (front), PUMP socket (back)
    name, _, _, ch, _, bh, depth = SWITCHES[0]
    s.rect(-4, Z_PANEL - bh / 2, 4, bh, PART, sw=0.35, dash="1.5 1")
    s.rect(WALL, Z_PANEL - 13, depth - WALL, 26, PART, sw=0.35, dash="1.5 1")
    s.text(WALL + (depth - WALL) / 2, Z_PANEL, "MAIN switch", 2.6, PART)
    so = SOCKET
    s.rect(D - WALL - so["depth"], Z_BACK - so["d"] / 2, so["depth"], so["d"], SOFT, sw=0.35, dash="1.5 1")
    s.text(D - WALL - so["depth"] / 2, Z_BACK, "PUMP socket", 2.6, SOFT, rot=-90)
    s.dim_v(Z_DIV_TOP, z_pi, 0, -10, "10")
    s.dim_v(z_pcb, MAINS_H, 0, -10, "10")
    s.dim_v(z_pcb - r["pcb"] - r["relays"], MAINS_H, 0, -18, "≈28")
    s.dim_h(p["y"], p["y"] + p["d"], H, 6, "Pi 56")
    s.dim_h(r["y"], r["y"] + r["d"], z_pcb - r["pcb"] - r["relays"], -6, "relay 55")
    s.save("section-a-a.svg", [
        "Cut faces grey/filled. Dashed = beyond the cut or component envelopes. Brass = M2.5 hex standoffs (bought).",
        "Pi bosses reach 4 mm under the plate → ≥ 4 mm above the relay board's solder side (10 mm relay standoffs).",
        "Relay board ↔ switch backs ≥ 3 mm (Y), ↔ socket bodies ≥ 18 mm (Y). Free height above the Pi board ≈ 35 mm."])


def section_b():
    x_cut = ADAPTER["x"] + ADAPTER["w"] / 2
    s = Sheet(f"Section B-B at x = {x_cut:g}: USB-C adapter (viewed from -X, front left)",
              -20, D + 34, -LID_T - 20, H + LID_T + 18)
    section_frame(s)
    a = ADAPTER
    z_bot = MAINS_H - a["h"]
    s.rect(a["y"] - 2.5, MAINS_H - a["fence"], 2, a["fence"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(a["y"] + a["d"] + 0.5, MAINS_H - a["fence"], 2, a["fence"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(a["y"], z_bot, a["d"], a["h"], "#7b1fa2", "#e1bee7", 0.45)
    s.text(a["y"] + a["d"] / 2, z_bot + 15, "USB-C adapter", 3, "#7b1fa2", weight="bold")
    s.text(a["y"] + a["d"] / 2, z_bot + 10, "back face against the plate", 2.4, "#7b1fa2")
    s.line(a["y"] - 1, z_bot - 1.5, a["y"] + a["d"] + 1, z_bot - 1.5, "#7b1fa2", 0.6, "2 1")
    s.text(a["y"] + 31, z_bot - 6, "2 cable ties", 2.4, "#7b1fa2", "start")
    s.rect(a["y"] + 20, z_bot - 30, 9, 30, SOFT, sw=0.35, dash="1.5 1")
    s.text(a["y"] + 31, z_bot - 16, "USB-C plug + cable", 2.4, SOFT, "start")
    _, _, _, ch, _, bh, depth = SWITCHES[2]
    s.rect(-4, Z_PANEL - bh / 2, 4, bh, PART, sw=0.35, dash="1.5 1")
    s.rect(WALL, Z_PANEL - ch / 2, depth - WALL, ch, PART, sw=0.35, dash="1.5 1")
    s.text(WALL + (depth - WALL) / 2, Z_PANEL, "PUMP switch", 2.6, PART)
    i = IEC
    s.rect(D - WALL - i["depth"], Z_BACK - i["ch"] / 2, i["depth"], i["ch"], SOFT, sw=0.35, dash="1.5 1")
    s.rect(D, Z_BACK - i["fh"] / 2, 3.1, i["fh"], SOFT, sw=0.35, dash="1.5 1")
    s.text(D - WALL - i["depth"] / 2, Z_BACK, "IEC inlet", 2.6, SOFT, rot=-90)
    s.dim_v(z_bot, MAINS_H, 0, -10, "27")
    s.dim_v(0, z_bot, 0, -10, "43 free")
    s.dim_h(a["y"], a["y"] + a["d"], H, 6, "adapter 49")
    s.dim_h(depth, a["y"] - 2.5, Z_PANEL + 20, 0)
    s.save("section-b-b.svg", [
        "Adapter hangs 27 mm under the divider in 4 corner brackets (10 high), held by 2 cable ties. Port faces down: 43 mm free for plug + cable.",
        "Adapter brackets ↔ switch backs ≥ 3 mm (Y), ↔ IEC body ≥ 16 mm (Y)."])


def section_c():
    s = Sheet(f"Section C-C at y = {Y_CUT:g}: Pi / relay stack and adapter (viewed from the front, -Y)",
              -24, W + 34, -LID_T - 20, H + LID_T + 18)
    section_frame(s, W, divider=False)
    p, r, a, sl = PI, RELAY, ADAPTER, SLOT
    # divider plate (cut), interrupted by the feed-through
    s.rect(WALL + 0.3, MAINS_H, sl["cx"] - sl["w"] / 2 - WALL - 0.3, DIV_T, fill=CUT)
    s.rect(sl["cx"] + sl["w"] / 2, MAINS_H, W - WALL - 0.3 - sl["cx"] - sl["w"] / 2, DIV_T, fill=CUT)
    s.text(sl["cx"], Z_DIV_TOP + 2, "feed-through", 2.4, INK)
    # beyond the cut: back pads, corner columns, back-wall components
    for px, py in PADS[1::2]:
        s.rect(px - 5, MAINS_H - 10, 10, 10, HID, sw=0.3, dash="1 1")
    for cx in (COL_C, W - COL_C):
        s.rect(cx - COL_R, 0, 2 * COL_R, H, HID, sw=0.25, dash="1 1")
    for name, x in SOCKETS:
        s.rect(x - SOCKET["d"] / 2, Z_BACK - SOCKET["d"] / 2, SOCKET["d"], SOCKET["d"], SOFT, sw=0.3, dash="1.5 1", rx=21.5)
        s.text(x, Z_BACK - 18, f"{name} socket (beyond)", 2.2, SOFT)
    i = IEC
    s.rect(i["x"] - i["cw"] / 2, Z_BACK - i["ch"] / 2, i["cw"], i["ch"], SOFT, sw=0.3, dash="1.5 1", rx=4)
    s.text(i["x"], Z_BACK - 14, "IEC (beyond)", 2.2, SOFT)
    s.circle(JACK["x"], JACK["z"], 4, SOFT, sw=0.3, dash="1.5 1")
    s.text(JACK["x"], JACK["z"] - 8, "jack (beyond)", 2.2, SOFT)
    # Pi: standoffs + bosses beyond (back row), board cut, components envelope
    z_pi = Z_DIV_TOP + p["standoff"]
    for hx, _ in p["holes"][:2]:
        s.rect(hx - 2.5, Z_DIV_TOP, 5, p["standoff"], BRASS, "#f3e5ab", 0.35, "1 0.6")
        s.rect(hx - 3.5, MAINS_H - p["boss"], 7, p["boss"], HID, sw=0.3, dash="1 1")
    s.rect(p["x"], z_pi, p["w"], 1.6, PART, "#f8bbd0", 0.4)
    s.rect(p["x"], z_pi + 1.6, p["w"], 17, PART, sw=0.3, dash="1 1")
    s.text(p["x"] + p["w"] / 2, z_pi + 9, "Pi components (USB/Eth end left)", 2.6, PART)
    # relay board: standoffs beyond, PCB + relays cut
    z_pcb = MAINS_H - r["standoff"]
    for hx, _ in r["holes"][:2]:
        s.rect(hx - 4, z_pcb, 8, r["standoff"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(r["x"], z_pcb - r["pcb"], r["w"], r["pcb"], "#7b1fa2", "#e1bee7", 0.4)
    s.rect(r["x"] + 3, z_pcb - r["pcb"] - r["relays"], r["w"] - 6, r["relays"], "#7b1fa2", sw=0.35, dash="1.5 1")
    s.text(r["x"] + r["w"] / 2, z_pcb - 11, "relays (facing down)", 2.6, "#7b1fa2")
    # adapter: cut, brackets beyond, cable ties cut, plug envelope
    z_bot = MAINS_H - a["h"]
    for bx in (a["x"] - 2.5, a["x"] + a["w"] + 0.5):
        s.rect(bx, MAINS_H - a["fence"], 2, a["fence"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(a["x"], z_bot, a["w"], a["h"], "#7b1fa2", "#e1bee7", 0.45)
    s.text(a["x"] + a["w"] / 2, z_bot + 15, "USB-C adapter", 3, "#7b1fa2", weight="bold")
    s.text(a["x"] + a["w"] / 2, z_bot + 10, "port faces down", 2.4, "#7b1fa2")
    for tx in (a["x"] + 10, a["x"] + 40):
        s.rect(tx - 2.5, z_bot - 1.5, 5, 1.5, "#7b1fa2", "#7b1fa2", 0.3)
    s.text(a["x"] + 10, z_bot - 5, "cable ties", 2.2, "#7b1fa2")
    px = a["x"] + a["w"] / 2
    s.rect(px - 4.5, z_bot - 30, 9, 30, SOFT, sw=0.35, dash="1.5 1")
    s.text(px - 6, z_bot - 18, "USB-C plug", 2.4, SOFT, "end")
    # dims
    s.dim_h(0, p["x"], H, 6)
    s.dim_h(p["x"], p["x"] + p["w"], H, 6, "Pi 85")
    s.dim_h(sl["cx"] - sl["w"] / 2, sl["cx"] + sl["w"] / 2, H, 6)
    s.dim_h(a["x"], a["x"] + a["w"], H, 6, "adapter 50")
    s.dim_h(r["x"], r["x"] + r["w"], z_pcb - r["pcb"] - r["relays"], -6, "relay 75")
    s.dim_v(Z_DIV_TOP, z_pi, 0, -10, "10")
    s.dim_v(z_pcb, MAINS_H, 0, -10, "10")
    s.dim_v(z_pcb - r["pcb"] - r["relays"], MAINS_H, 0, -18, "≈28")
    s.dim_v(0, z_bot, a["x"] + a["w"] + 2.5, 6, "43 free")
    s.save("section-c-c.svg", [
        "Cut faces filled. Dashed = beyond the cut (back pads, corner columns, back-wall components) or component envelopes.",
        "The Pi sits directly above the relay board. Feed-through (14 wide) between the stack and the adapter carries GPIO wires and the USB-C cable.",
        "Relay board / adapter hang between the divider pads, so the whole divider module can be lowered in from the top."])


if __name__ == "__main__":
    front(); back(); top(); section_a(); section_b(); section_c()
