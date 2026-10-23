# Interview log

## Round 1 (2026-10-19)

**Questions** (asked in chat): 1 contents · 2 connections, mains? · 3 user interface · 4 environment & mounting · 5 cooling · 6 construction / closure · 7 look · 8 project link.

**Answers** (user, close to verbatim):
- Look at the hand-drawn sketches for a rough idea of what the thing shall be. → S1, S2, S3
- The upper lid and the lower lid shall be detachable/openable to access the contents.
- Big fan of **brass inserts + screws**. Use them when needed. Stick to the same or a limited set of insert/screw sizes if possible.
- Must be **easily 3D printable**: avoid tiny details that cause printing problems, **one colour/filament**, **reduce the number of parts** to print.
- Details of switches/plugs are added when available. → C1–C7
- The Pi is a **Raspberry Pi 3**, but others may want a **Pi 4 or Pi 5**. Make it **replaceable**.
- Open questions are welcome, but expect "I don't know (yet)". Then make **good assumptions** and make the solution **parametric**.

**Still open from round 1:** 4 (environment, mounting), 5 (cooling), 7 (look), 8 (project link). Partly carried into round 2.

## Round 2 (2026-10-19)

Questions Q1–Q8 as listed in `requirements.md` (each with a default assumption).

**Answers** (user, verbatim):
- **Q1** Part split: **A**. Body (walls only) + separate divider plate + top lid + bottom lid.
- **Q2** Relay board size: *don't know (yet), still waiting for the shipment.* → assumption A1 stays, parametric.
- **Q3** Power: *10 A is fine. Don't worry about the electric part.*
- **Q4** Pi ports: *no, no port needs to be accessible from the outside.*
- **Q5** Pi 4/5 by reprinting the divider plate only + optional fan mount: *sounds perfect.*
- **Q6** Placement: *table + rubber feet.*
- **Q7** Labels: *yes, let's try this. If it's raised, one can easily paint it with a touch-up pen later.* → raised labels.
- **Q8** Size: *no limit, it just has to be printable. Try to make it not larger than 20 cm × 20 cm × 20 cm.*

## Round 3: review of spec draft v0.1 (2026-10-19)

**User questions / input** (verbatim):
- *Why are the RPI and the relay board not on top of each other but shifted on different levels?*
- *Why is the USB-C power adapter not next to the relay board on the divider panel?*
- *Additionally: the temp jack outlet looks like in the picture attached.* → C3 picture stored.

**Answers / decisions** (Claude, see chat):
- v0.1 shifted the boards because the Pi's insert bosses (4 mm under the plate) would have left only ≈ 0.5 mm above the relay board's solder joints with 6 mm relay standoffs. Fix: **10 mm relay standoffs** → boards **stacked** as in sketch S1.
- v0.1 put the adapter on the bottom lid because its mounting hole is unknown and a holder on a lid is easy. No hard reason. Moving it **under the divider next to the relay board** puts all electronics on one removable module, keeps the bottom lid a plain plate, and the adapter no longer hangs on its wires when the bottom is opened.
- Jack: clamped between a front nut and a hex nut → wall locally thinned to 2 mm (thread length unknown).

## Round 4: review of spec draft v0.2 (2026-10-19)

**User input** (verbatim):
- *Please also add another sectional cut, similar to A-A but looking at it from front/back.* → section C-C added (v0.2 drawings).
- *Add a groove/notch/... on the connection lid <-> outer wall to make the connection stronger (if not already planned, it's just not visible in the drawings).* → was not planned. New R22.
- *Rename the RPI part to 'low-voltage part' and the mains part to 'high-voltage part'.* → R2 and all documents renamed.

**Decisions** (Claude, spec v0.3):
- Top: **rebate**. The outer 1.5 mm of the wall rises 3 mm above the lid seat as a rim, and the lid drops in flush. This keeps the top lid printable outer-face-up with the raised logo.
- Bottom: **locating lip** (2 × 4 mm) on the bottom lid, reaching inside the walls. A rebate there would leave the corner columns starting in mid-air when the body is printed upright.

## Round 5: review of the OpenSCAD model (2026-10-19)

**User** (verbatim):
- *Why is the hole for the temp sensor jack in a drop shape?* → Claude: FDM rule 3 (teardrop holes in vertical walls print without support; the point is hidden under the Ø10 front nut). Offered a round hole as an option.
- *OpenSCAD models look fine to me. Go on with the generation.* → model accepted including the v0.4 corrections; teardrop jack hole kept.

## Round 6: change request after the STLs (2026-10-22)

**User** (verbatim): *Align the order of switches (front) and outlets/inputs (back). Looking from the top, the order shall be Mains, heater, pump (left to right).*

**Decisions** (Claude, spec v0.5):
- Front was already MAIN, BOILER, PUMP from the left. The back was reversed (PUMP, BOILER, POWER) → back panel mirrored: POWER x 155 → 35, BOILER 100 → 90, PUMP 45 → 145.
- The temperature jack moves with the inlet (x 155 → 35), so it stays above the power inlet as in sketch S3 and away from the PUMP socket's flip cover. To be confirmed.
- "Heater" = the boiler. Labels stay "BOILER".

## Round 7: label text (2026-10-22)

**Claude:** the labels still read "BOILER"; change to "HEATER"? **User** (verbatim): *yes, change to heater* → spec v0.6, labels HEATER front and back.

## Round 8: rubber feet (2026-10-22)

**User** (verbatim): *Add some markings for rubber feet to the bottom lid.*

**Decision** (Claude, spec v0.7): shallow round pockets Ø13 × 0.6 mm on the outer face at the four foot positions (F32). They mark and centre the feet. A pocket rather than a thin outline groove, because a fine groove on the bed face tends to close up in the first layer. Pocket size is a parameter (P33) for other feet.

## Round 9: rubber feet markings (2026-10-22)

**User** (verbatim): *I don't like them. Remove them again.* → spec v0.8: feet pockets (F32 geometry, P33) and the bottom view drawing removed; F32 is back to positions only.

## Round 10: measurements of the delivered parts (2026-10-23)

The user has all parts and measures what was assumed. Asked one question at a time.

| # | Question | Answer (user) |
|---|---|---|
| 1 | Relay board PCB outer size | **75 × 52 mm** |
| 2 | Relay board holes: spacing centre to centre, diameter | **70 × 46 mm**, **Ø3 mm** |
| 3 | Relay board height | **17 mm** from the PCB underside to the top of the relays; solder pins stick out **3 mm** on the underside |
| 4 | USB-C adapter: mounting hole, size | Hole goes **through** the 27 mm depth, with a **~5 mm recess** on the port side, so the screw is in the hole for 22 mm. Hole centre **3.5 mm** from the top edge and **8 mm** from the side edge (the side opposite the cable), **Ø3.5 mm**. Size **51 (cable side) × 49 × 27 mm**, measured at the bottom |
| 5 | Jack: thread diameter, usable thread length, hex nut | Thread **M8**, usable thread length **4 mm**, hex nut **2 mm** thick, **11 mm** at its widest |
| 6 | Jack: diameter of the black front nose | **Ø10 mm** |
