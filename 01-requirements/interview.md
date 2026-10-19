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
