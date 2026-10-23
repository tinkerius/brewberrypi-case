#!/usr/bin/env python3
"""Generates the dimensioned spec drawings in 02-specification/drawings/ (SVG, mm).

The numbers below mirror the tables in 02-specification/spec.md. Change the spec first, then here.
Usage: python3 tools/make_drawings.py
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "02-specification" / "drawings"
SPEC_VERSION = "0.9"

# --- spec values (mm) -------------------------------------------------------
W, D = 190, 160                    # P1, P2 outer width (X) / depth (Y)
WALL = 3                           # P5
LID_T = 3                          # P6
DIV_T = 3                          # P7
HV_H = 70                          # P3 high-voltage part: body bottom -> divider underside
LV_H = 47                          # P4 low-voltage part: divider top -> top lid underside
H = HV_H + DIV_T + LV_H            # 120 lid seat
Z_DIV_TOP = HV_H + DIV_T           # 73
RIM = 1.5                          # P31 rim above the lid seat (top rebate)
H_BODY = H + LID_T                 # 123 body height incl. rim (lid flush with rim)
CLR = 0.2                          # P9 fit clearance
LIP_T, LIP_H = 2, 4                # P32 bottom lid locating lip
NOTCH_W = 12                       # F16 pry notch, centred on the back wall
COL_C, COL_R = 7, 5                # corner columns: centre inset, radius
PADS = [(8, 40), (8, 120), (182, 40), (182, 120)]   # divider pads (centre x, y), 10 x 14
PI = dict(x=17, y=55, w=85, d=56, standoff=10, boss=2.2, boss_d=8,
          holes=[(40.5, 58.5), (98.5, 58.5), (40.5, 107.5), (98.5, 107.5)])  # F11
GPIO = (43.9, 56, 51, 5)           # header footprint (x, y, w, d)
RELAY = dict(x=17, y=58, w=75, d=52, standoff=10, pcb=1.6, relays=15.4,
             holes=[(19.5, 61), (89.5, 61), (19.5, 107), (89.5, 107)])       # F12 (measured)
SLOT = dict(cx=111, cy=85, w=14, h=46)                                       # F13
ADAPTER = dict(x=123, y=61, w=51, d=49, h=27, fence=10, screw=(43, 45.5))                      # F14
Z_PANEL = 40                       # front switch centre height
SWITCHES = [  # name, x, cutout w, cutout h (portrait), bezel w, bezel h, depth behind panel incl. connectors
    ("MAIN", 40, 22, 27, 25.5, 34.5, 37),
    ("HEATER", 115, 21.5, 28.5, 25.7, 34.5, 48),
    ("PUMP", 150, 21.5, 28.5, 25.7, 34.5, 48),
]
Z_BACK = 38                        # back panel component centre height
IEC = dict(x=35, cw=27.5, ch=31.5, r=1, fw=43.8, fh=32.8, hole_dx=18, depth=27.6)
SOCKETS = [("HEATER", 90), ("PUMP", 145)]            # x centres; cutout Ø43 flat-top at r 24
SOCKET = dict(d=43, flat=24, flange=50, holes=38, depth=26, front=21)
JACK = dict(x=35, z=98, d=8, flat=4.7, nut=10, pocket=16)
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

    def poly(self, pts, stroke=INK, fill=CUT, sw=0.4):
        d = " ".join(f"{x:.2f},{y:.2f}" for x, y in (self.P(u, v) for u, v in pts))
        self.add(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

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


def case_outline(s, notch=False):
    s.rect(0, -LID_T, W, LID_T, fill="#f4f4f4")            # bottom lid
    s.rect(0, 0, W, H_BODY)                                 # body incl. rim
    s.line(RIM, H, W - RIM, H, HID, 0.3, "2 1.5")           # top lid seat (hidden behind the rim)
    if notch:                                               # F16: pry notch, top lid visible through it
        s.rect(W / 2 - NOTCH_W / 2, H, NOTCH_W, LID_T, INK, "#f4f4f4", 0.4)
        s.text(W / 2, H_BODY + 2, "pry notch", 2.6, HID)
    s.line(0, HV_H, W, HV_H, HID, 0.3, "2 1.5")             # divider (hidden)
    s.line(0, Z_DIV_TOP, W, Z_DIV_TOP, HID, 0.3, "2 1.5")
    s.text(3, Z_DIV_TOP + 3, "low-voltage part", 3, HID, "start")
    s.text(3, HV_H - 5, "high-voltage part", 3, HID, "start")


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
    s.dim_v(0, HV_H, W, 14, "70 (divider)")
    s.save("front-view.svg", [
        "Grey = cutout (clearance P9 added in the model), dashed pink = switch bezel. Labels raised 0.6 mm, 6 mm text.",
        "Wall at the switch clips (P10, clip gap − 0.3): MAIN 3.7 mm (0.7 mm frame inside), HEATER/PUMP 2.7 mm (0.3 mm pocket inside)."])


def back():
    s = Sheet("Back view (from +Y), mirrored X: u = 190 - x", -12, W + 30, -LID_T - 22, H + LID_T + 26)
    case_outline(s, notch=True)
    u = lambda x: W - x
    iu = u(IEC["x"])
    s.rect(iu - IEC["fw"] / 2, Z_BACK - IEC["fh"] / 2, IEC["fw"], IEC["fh"], PART, sw=0.35, dash="1.5 1")
    s.rect(iu - IEC["cw"] / 2, Z_BACK - IEC["ch"] / 2, IEC["cw"], IEC["ch"], fill=CUT, rx=IEC["r"])
    for dx in (-IEC["hole_dx"], IEC["hole_dx"]):
        s.circle(iu + dx, Z_BACK, 2, fill=CUT)
    s.text(iu, Z_BACK - 1, "27.5×31.5 r1", 2.6)
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
    s.teardrop(ju, JACK["z"], JACK["d"] / 2, JACK["flat"])
    s.text(ju, 82, "TEMP", 6, weight="bold")
    s.dim_h(0, W, -LID_T, -12)
    us = sorted([0, u(IEC["x"])] + [u(x) for _, x in SOCKETS])
    for a, b in zip(us, us[1:]):
        s.dim_h(a, b, H + LID_T, 8)
    s.dim_v(0, Z_BACK, W, 14)
    s.dim_v(0, JACK["z"], W, 22)
    s.save("back-view.svg", [
        "Sockets: Ø43 cutout with flat-top teardrop (top flat at r = 24, hidden by the 50 mm flange). Holes on 38 mm square.",
        "IEC: cutout 27.5×31.5 r1, screws 36 apart. All screw holes take M3 inserts pressed in from outside.",
        "Jack M8: Ø8 flat-top teardrop (flat 4.7 above the centre, hidden by the Ø10 nose). Grey dotted Ø16 = inside pocket, wall 1.6 mm (P28)."])


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
    s.text(r["x"] + r["w"] / 2, r["y"] + 18, "75×52, holes 70×46, 10 mm standoffs", 2.4, "#7b1fa2")
    a = ADAPTER
    s.rect(a["x"], a["y"], a["w"], a["d"], "#7b1fa2", sw=0.5, dash="3 1.5")
    for cx, cy, sx, sy in ((a["x"], a["y"], 1, 1), (a["x"] + a["w"], a["y"], -1, 1),
                           (a["x"], a["y"] + a["d"], 1, -1), (a["x"] + a["w"], a["y"] + a["d"], -1, -1)):
        ox, oy = cx - sx * 2.5, cy - sy * 2.5            # bracket outer corner (0.5 clearance + 2 wall)
        s.line(ox, oy, ox + sx * 12, oy, "#7b1fa2", 1.2)
        s.line(ox, oy, ox, oy + sy * 12, "#7b1fa2", 1.2)
    for lx in (a["x"] + 15, a["x"] + 35):                  # tie slots through the plate
        s.rect(lx - 2.75, a["y"] - 3, 5.5, 2.5, fill=CUT, sw=0.3)
        s.rect(lx - 2.75, a["y"] + a["d"] + 0.5, 5.5, 2.5, fill=CUT, sw=0.3)
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] / 2 + 3, "USB-C adapter (BELOW)", 2.8, "#7b1fa2", weight="bold")
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] / 2 - 1.5, "51×49, port faces down", 2.4, "#7b1fa2")
    s.text(a["x"] + a["w"] / 2, a["y"] + a["d"] / 2 - 5.5, "M3×30 screw + brackets (ties optional)", 2.4, "#7b1fa2")
    s.circle(a["x"] + a["screw"][0], a["y"] + a["screw"][1], 1.7, fill=CUT)   # adapter screw hole
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
    for m in (lambda u: u, lambda u: L - u):                # left and right wall: rim + lid seat
        s.poly([(m(0), 0), (m(WALL), 0), (m(WALL), H), (m(RIM), H), (m(RIM), H_BODY), (m(0), H_BODY)])
        s.rect(min(m(WALL + CLR), m(WALL + CLR + LIP_T)), 0, LIP_T, LIP_H, fill=CUT)   # bottom lid lip
    s.rect(0, -LID_T, L, LID_T, fill=CUT)
    s.rect(RIM + CLR, H, L - 2 * (RIM + CLR), LID_T, fill=CUT)
    if divider:
        s.rect(WALL + 0.3, HV_H, L - 2 * WALL - 0.6, DIV_T, fill=CUT)
    s.dim_v(-LID_T, 0, L, 8)
    s.dim_v(0, HV_H, L, 8)
    s.dim_v(HV_H + DIV_T, H, L, 8)
    s.dim_v(H, H + LID_T, L, 8)
    s.dim_v(-LID_T, H + LID_T, L, 18, "126")
    s.dim_h(0, L, -LID_T, -12)


def section_a():
    x_cut = PI["holes"][0][0]
    s = Sheet(f"Section A-A at x = {x_cut:g}: Pi / relay stack (viewed from +X, front left)",
              -20, D + 34, -LID_T - 20, H + LID_T + 18)
    section_frame(s)
    p, r = PI, RELAY
    z_pi = Z_DIV_TOP + p["standoff"]
    # Pi: standoffs (cut), bosses under the plate (cut), board (cut), components envelope
    for _, hy in p["holes"][::2]:
        s.rect(hy - 2.5, Z_DIV_TOP, 5, p["standoff"], BRASS, "#f3e5ab", 0.35)
        s.rect(hy - p["boss_d"] / 2, HV_H - p["boss"], p["boss_d"], p["boss"], fill=CUT, sw=0.3)
    s.rect(p["y"], z_pi, p["d"], 1.6, PART, "#f8bbd0", 0.4)
    s.rect(p["y"], z_pi + 1.6, p["d"], 17, PART, sw=0.3, dash="1 1")
    s.text(p["y"] + p["d"] / 2, z_pi + 9, "Pi components / GPIO wires", 2.6, PART)
    # relay: standoffs (beyond), PCB, relays
    z_pcb = HV_H - r["standoff"]
    for hy in sorted({h[1] for h in r["holes"]}):
        s.rect(hy - 4, z_pcb, 8, r["standoff"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(r["y"], z_pcb - r["pcb"], r["d"], r["pcb"], "#7b1fa2", "#e1bee7", 0.4)
    s.rect(r["y"] + 3, z_pcb - r["pcb"] - r["relays"], r["d"] - 6, r["relays"], "#7b1fa2", sw=0.35, dash="1.5 1")
    s.text(r["y"] + r["d"] / 2, z_pcb - 11, "relays (facing down)", 2.6, "#7b1fa2")
    # MAIN switch (front), IEC inlet (back)
    name, _, _, ch, _, bh, depth = SWITCHES[0]
    s.rect(-4, Z_PANEL - bh / 2, 4, bh, PART, sw=0.35, dash="1.5 1")
    s.rect(WALL, Z_PANEL - 13, depth - WALL, 26, PART, sw=0.35, dash="1.5 1")
    s.text(WALL + (depth - WALL) / 2, Z_PANEL, "MAIN switch", 2.6, PART)
    i = IEC
    s.rect(D - WALL - i["depth"], Z_BACK - i["ch"] / 2, i["depth"], i["ch"], SOFT, sw=0.35, dash="1.5 1")
    s.rect(D, Z_BACK - i["fh"] / 2, 3.1, i["fh"], SOFT, sw=0.35, dash="1.5 1")
    s.text(D - WALL - i["depth"] / 2, Z_BACK, "IEC inlet", 2.6, SOFT, rot=-90)
    s.dim_v(Z_DIV_TOP, z_pi, 0, -10, "10")
    s.dim_v(z_pcb, HV_H, 0, -10, "10")
    s.dim_v(z_pcb - r["pcb"] - r["relays"], HV_H, 0, -18, "27")
    s.dim_h(p["y"], p["y"] + p["d"], H, 6, "Pi 56")
    s.dim_h(r["y"], r["y"] + r["d"], z_pcb - r["pcb"] - r["relays"], -6, "relay 55")
    s.save("section-a-a.svg", [
        "Cut faces grey/filled. Dashed = beyond the cut or component envelopes. Brass = M2.5 hex standoffs (bought).",
        "Pi nut holders reach 2.2 mm under the plate → 4.8 mm above the relay board's 3 mm solder pins (10 mm relay standoffs).",
        "Relay board ↔ switch backs ≥ 3 mm (Y), ↔ IEC body ≥ 22 mm (Y). Free height above the Pi board ≈ 35 mm."])


def section_b():
    x_cut = ADAPTER["x"] + ADAPTER["w"] / 2
    s = Sheet(f"Section B-B at x = {x_cut:g}: USB-C adapter (viewed from +X, front left)",
              -20, D + 34, -LID_T - 20, H + LID_T + 18)
    section_frame(s)
    a = ADAPTER
    z_bot = HV_H - a["h"]
    s.rect(a["y"] - 2.5, HV_H - a["fence"], 2, a["fence"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(a["y"] + a["d"] + 0.5, HV_H - a["fence"], 2, a["fence"], "#7b1fa2", sw=0.3, dash="1 1")
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
    so = SOCKET
    s.rect(D - WALL - so["depth"], Z_BACK - so["d"] / 2, so["depth"], so["d"], SOFT, sw=0.35, dash="1.5 1")
    s.text(D - WALL - so["depth"] / 2, Z_BACK, "PUMP socket", 2.6, SOFT, rot=-90)
    s.dim_v(z_bot, HV_H, 0, -10, "27")
    s.dim_v(0, z_bot, 0, -10, "43 free")
    s.dim_h(a["y"], a["y"] + a["d"], H, 6, "adapter 49")
    s.dim_h(depth, a["y"] - 2.5, Z_PANEL + 20, 0)
    s.save("section-b-b.svg", [
        "Adapter hangs 27 mm under the divider in 4 corner brackets (10 high), held by 2 cable ties. Port faces down: 43 mm free for plug + cable.",
        "Adapter brackets ↔ switch backs ≥ 3 mm (Y), ↔ PUMP socket body ≥ 21 mm (Y). M3 × 30 screw from below, nut on top."])


def section_c():
    s = Sheet(f"Section C-C at y = {Y_CUT:g}: Pi / relay stack and adapter (viewed from the front, -Y)",
              -24, W + 34, -LID_T - 20, H + LID_T + 18)
    section_frame(s, W, divider=False)
    p, r, a, sl = PI, RELAY, ADAPTER, SLOT
    # divider plate (cut), interrupted by the feed-through
    s.rect(WALL + 0.3, HV_H, sl["cx"] - sl["w"] / 2 - WALL - 0.3, DIV_T, fill=CUT)
    s.rect(sl["cx"] + sl["w"] / 2, HV_H, W - WALL - 0.3 - sl["cx"] - sl["w"] / 2, DIV_T, fill=CUT)
    s.text(sl["cx"], Z_DIV_TOP + 2, "feed-through", 2.4, INK)
    # beyond the cut: back pads, corner columns, back-wall components
    for px, py in PADS[1::2]:
        s.rect(px - 5, HV_H - 10, 10, 10, HID, sw=0.3, dash="1 1")
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
        s.rect(hx - p["boss_d"] / 2, HV_H - p["boss"], p["boss_d"], p["boss"], HID, sw=0.3, dash="1 1")
    s.rect(p["x"], z_pi, p["w"], 1.6, PART, "#f8bbd0", 0.4)
    s.rect(p["x"], z_pi + 1.6, p["w"], 17, PART, sw=0.3, dash="1 1")
    s.text(p["x"] + p["w"] / 2, z_pi + 9, "Pi components (USB/Eth end left)", 2.6, PART)
    # relay board: standoffs beyond, PCB + relays cut
    z_pcb = HV_H - r["standoff"]
    for hx, _ in r["holes"][:2]:
        s.rect(hx - 4, z_pcb, 8, r["standoff"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(r["x"], z_pcb - r["pcb"], r["w"], r["pcb"], "#7b1fa2", "#e1bee7", 0.4)
    s.rect(r["x"] + 3, z_pcb - r["pcb"] - r["relays"], r["w"] - 6, r["relays"], "#7b1fa2", sw=0.35, dash="1.5 1")
    s.text(r["x"] + r["w"] / 2, z_pcb - 11, "relays (facing down)", 2.6, "#7b1fa2")
    # adapter: cut, brackets beyond, cable ties cut, plug envelope
    z_bot = HV_H - a["h"]
    for bx in (a["x"] - 2.5, a["x"] + a["w"] + 0.5):
        s.rect(bx, HV_H - a["fence"], 2, a["fence"], "#7b1fa2", sw=0.3, dash="1 1")
    s.rect(a["x"], z_bot, a["w"], a["h"], "#7b1fa2", "#e1bee7", 0.45)
    s.text(a["x"] + a["w"] / 2, z_bot + 15, "USB-C adapter", 3, "#7b1fa2", weight="bold")
    s.text(a["x"] + a["w"] / 2, z_bot + 10, "port faces down", 2.4, "#7b1fa2")
    for tx in (a["x"] + 15, a["x"] + 35):
        s.rect(tx - 2.5, z_bot - 1.5, 5, 1.5, "#7b1fa2", "#7b1fa2", 0.3)
    s.text(a["x"] + 15, z_bot - 5, "cable ties", 2.2, "#7b1fa2")
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
    s.dim_v(z_pcb, HV_H, 0, -10, "10")
    s.dim_v(z_pcb - r["pcb"] - r["relays"], HV_H, 0, -18, "27")
    s.dim_v(0, z_bot, a["x"] + a["w"] + 2.5, 6, "43 free")
    s.save("section-c-c.svg", [
        "Cut faces filled. Dashed = beyond the cut (back pads, corner columns, back-wall components) or component envelopes.",
        "The Pi sits directly above the relay board. Feed-through (14 wide) between the stack and the adapter carries GPIO wires and the USB-C cable.",
        "Relay board / adapter hang between the divider pads, so the whole divider module can be lowered in from the top."])


def detail_joints():
    K = 5                                                   # scale 5:1
    s = Sheet("Details X and Y: lid joints (section through a wall, scale 5:1)", -8, 232, -8, 92)
    s.text(55, 88, "Detail X: top lid in the rebate (F15, F20)", 3.6, weight="bold")
    s.text(175, 88, "Detail Y: bottom lid lip (F33)", 3.6, weight="bold")
    X = lambda u, v: (10 + K * u, K * (v - 110))            # detail X shows z 110…126
    Y = lambda u, v: (130 + K * u, K * (v + 5))             # detail Y shows z −5…11
    # --- X: wall with rim, top lid, column hint
    s.poly([X(0, 110), X(WALL, 110), X(WALL, H), X(RIM, H), X(RIM, H_BODY), X(0, H_BODY)])
    s.poly([X(RIM + CLR, H), X(16, H), X(16, H_BODY), X(RIM + CLR, H_BODY)], fill="#f4f4f4")
    s.line(*X(0, 110), *X(WALL, 110), HID, 0.3, "2 1")
    s.text(*X(-1.2, 114), "body wall", 3, HID, "end")
    s.text(*X(10, 121.1), "top lid", 3.2)
    s.text(*X(9, 112.5), "inside (low-voltage part)", 2.8, HID)
    s.text(*X(-1.2, 121), "rim", 3, HID, "end")
    x0, x15, x17, x3 = X(0, 0)[0], X(RIM, 0)[0], X(RIM + CLR, 0)[0], X(WALL, 0)[0]
    s.dim_h(x0, x15, X(0, H_BODY)[1], 14, "rim 1.5")
    s.dim_h(x15, x17, X(0, H_BODY)[1], 6, " ")
    s.text(x17 + 2, X(0, H_BODY)[1] + 6.6, "0.2 clearance", 3.2, DIM, "start")
    s.line(*X(2.4, H - 0.2), *X(6, 116.5), HID, 0.3)
    s.text(*X(6.2, 116), "lid seat 1.5 (+ column tops)", 3, HID, "start")
    s.dim_h(x0, x3, X(0, 110)[1], -6, "wall 3")
    s.dim_v(X(0, H)[1], X(0, H_BODY)[1], x0, -10, "3")
    s.dim_v(X(0, H)[1], X(0, H_BODY)[1], X(16, 0)[0], 6, "lid 3")
    # --- Y: wall with outer bottom chamfer, bottom lid with lip
    s.poly([Y(0, 0.6), Y(0.6, 0), Y(WALL, 0), Y(WALL, 11), Y(0, 11)])
    s.poly([Y(0, -LID_T), Y(16, -LID_T), Y(16, 0), Y(WALL + CLR + LIP_T, 0), Y(WALL + CLR + LIP_T, LIP_H),
            Y(WALL + CLR, LIP_H), Y(WALL + CLR, 0), Y(0, 0)], fill="#f4f4f4")
    s.line(*Y(0, 11), *Y(WALL, 11), HID, 0.3, "2 1")
    s.text(*Y(-1.2, 7), "body wall", 3, HID, "end")
    s.text(*Y(11, -1.9), "bottom lid", 3.2)
    s.text(*Y(12.5, 1.5), "inside (high-voltage part)", 2.8, HID)
    y0, y3, y32, y52 = Y(0, 0)[0], Y(WALL, 0)[0], Y(WALL + CLR, 0)[0], Y(WALL + CLR + LIP_T, 0)[0]
    s.dim_h(y0, y3, Y(0, 11)[1], 6, "wall 3")
    s.dim_h(y3, y32, Y(0, LIP_H)[1], 16, " ")
    s.text(y32 + 2, Y(0, LIP_H)[1] + 16.6, "0.2 clearance", 3.2, DIM, "start")
    s.dim_h(y32, y52, Y(0, LIP_H)[1], 6, "lip 2")
    s.dim_v(Y(0, 0)[1], Y(0, LIP_H)[1], y52, 14, "4")
    s.dim_v(Y(0, -LID_T)[1], Y(0, 0)[1], y0, -8, "3")
    s.save("detail-joints.svg", [
        "X: the outer 1.5 mm of the wall rises 3 mm above the lid seat (rim). The top lid drops in with 0.2 per side, sits on the 1.5 mm seat + column tops and is flush with the rim.",
        "Y: the bottom lid's 2 × 4 mm lip reaches inside the walls with 0.2 per side (skipping the corner columns). Lid edges flush with the body.",
        "Both: the lids cannot slide or twist. The 4 M3 screws per lid only clamp. Pry notch (F16) in the back rim to lift the top lid."])


if __name__ == "__main__":
    front(); back(); top(); section_a(); section_b(); section_c(); detail_joints()
