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
| 7 | Rocker switches: clip gap (bezel underside → clip tip), bezel outer size | Clip gap: I/O (MAIN) **4 mm**, I/O/II (HEATER, PUMP) **3 mm**. Bezel outer size (plastic frame below the rubber cap): I/O **25.5 × 34.5 mm**, I/O/II **25.7 × 34.5 mm** |
| 8 | Rocker switches: body size below the bezel | I/O: **21 × 25 mm** without clips, **34 mm** across the clips. I/O/II: **21.5 × 27 mm** without clips, **33 mm** across the clips |
| 9 | Inserts, Pi standoffs | M3 inserts **3 × 6 × 4.5** (M3, 6 mm long, Ø4.5 outside). **Only M3 inserts** shall be used. Brass standoffs for the Pi: **10 mm** |

**Decisions** (Claude, spec v0.9):
- Relay board 75 × 52, holes 70 × 46 (Ø3: M3 screws are a snug fit), height 17 + 3 mm pins → standoff positions updated; pins end 4.8 mm below the Pi nut holders.
- USB-C adapter 51 × 49 × 27, fixed with an **M3 × 30 screw** through its own hole (head in the 5 mm recess) and a nut on top of the divider; hole at adapter (43, 45.5) = (166, 106.5). Cable ties optional.
- Jack M8: hole Ø8 (+ clearance), **flat-top** teardrop cut at 4.7 mm (hidden under the Ø10 nose), wall 1.6 mm (nut 2 + wall 1.6 ≤ 4 mm thread).
- Switch walls = clip gap − 0.3: MAIN **3.7 mm** (inside frame), HEATER/PUMP **2.7 mm** (inside pocket). Cutouts confirmed by the body sizes.
- Insert holes Ø4.0 × 7 deep. **No M2.5 inserts**: the Pi's Ø2.75 holes only take M2.5, so the Pi standoffs go into **M2.5 nuts held in hex pockets** under the divider (or M2.5 screws from below for female-female standoffs).

## Round 11: inserts for the circuit boards (2026-10-23)

**User** (verbatim, on the M2.5 nut pockets for the Pi): *I don't like this. You convinced me. Use 2.5x5x3.5 for the PCBs and the 3x... for the rest. Does this separation make sense?*

**Claude:** yes. M2.5 for the PCBs (Pi: Ø2.75 holes only take M2.5; relay board: Ø3 holes, M2.5 fits easily where M3 is a tight fit), M3 for the case. → spec v0.10: M2.5 inserts 2.5 × 5 × 3.5 (M2.5, 5 long, Ø3.5) for the Pi and the relay board, M3 inserts 3 × 6 × 4.5 for everything else. Nut pockets removed. Pi standoffs need a male end (male-female).

## Round 12: confirmations (2026-10-23)

| Question | Answer (user) |
|---|---|
| Jack at x = 35, above the power inlet (spec v0.5)? | *Yes, sounds good* → confirmed |
| M3 inserts 3 × 6 × 4.5 = 6 mm long, Ø4.5 outside? | *3 × 6 × 4.5 is correct* → confirmed |

No open design questions left. Remaining: print test (AC9).

## Round 13: adapter mounting (2026-10-23)

**User** (verbatim, with a photo → `inputs/component-C2-usb-c-adapter-holes.png`):
- *That is not true. There are two screw holes top-right and bottom-left (completely symmetric).*
- *Can't we lift the adapter up a little? Similarly to the relay board?*

**Decision** (Claude, spec v0.11): the adapter sits on **2 printed standoffs** (Ø8 × 6) under its two diagonal holes, each with an **M3 insert**; **2 × M3 × 30** from below (22 mm through the adapter + 8 mm into the standoff). Two diagonal screws stop it turning → corner brackets and tie slots removed, no nut.

## Round 14: adapter holes (2026-10-23)

**User** (verbatim): *The holes for the USB-C power brick are completely off.*

**Claude:** cause found: the hole pattern was placed mirrored. Mounted port face down with the cable side towards −X, the port face's **top edge points to the front** (−Y), not the back. So the top-right hole (seen on the port face) is at front-right (166, 64.5) and the bottom-left hole at back-left (131, 106.5). v0.9–v0.11 had them on the other diagonal. → spec v0.12.

**User** (follow-up, verbatim): *The distance (center hole to center hole) is 55 mm. However, it should be 48.5 mm only.*

**Claude:** the edge distances (3.5 / 8 mm on a 51 × 49 face) give 35 × 42 → 54.7 mm diagonal, so they don't describe the hole pattern (probably measured on the smaller, chamfered port face). **Open:** centre-to-centre spacing across and up/down, and whether the pair is centred on the adapter. Until then the divider must not be printed.

**User** (re-measured, verbatim): *Holes are: 3.5 mm from the top/bottom; 13 mm from the left/right. Width of the device: 51 mm; height: 49 mm. Diagonal: center hole to center hole → 48.5.*

**Claude:** 13 / 3.5 mm give 25 × 42 mm → 48.9 mm diagonal, 0.4 mm from the measured 48.5: within measuring accuracy and within the ~0.5 mm play of an M3 screw in the Ø3.5 holes. The direct edge measurements are used. (The earlier "8 mm" was wrong.) → spec v0.13: standoffs at (161, 64.5) and (136, 106.5).

## Round 15: adapter support (2026-10-23)

**User** (verbatim): *Also only two inserts are needed, add two more dummy inserts (without holes for inserts) so the adapter is resting at 4 points (also only two have inserts).*

**Decision** (Claude, spec v0.14): 2 solid rest standoffs Ø8 × 6 at the other two corners of the hole rectangle, (136, 64.5) and (161, 106.5). The adapter rests on 4 points; only the 2 diagonal ones have M3 inserts and screws.

## Round 16: Pi orientation (2026-10-23)

**User** (verbatim): *Let's turn the RPi by 90 degree so that the USB and Ethernet ports are not blocked by the wall.*

**Decision** (Claude, spec v0.15): Pi turned 90° with the **USB/Ethernet end to the front**, 52 mm free in front of the ports. This puts the GPIO header on the right (next to the feed-through) and the power socket on the left (37 mm to the wall). Ports to the back was not chosen: the temperature jack sits there at the Pi's height. The **relay board turns too** (52 × 75 in plan), so it stays directly under the Pi (R3).

## Round 17: Pi position (2026-10-23)

**User** (verbatim): *On the opposite side of the USB/Ethernet is the SD card. Put the Pi in the middle, so SD card and USB/Ethernet have similar amount of space.*

**Decision** (Claude, spec v0.16): Pi centred front to back (y 37.5–122.5): 34.5 mm in front of the ports and behind the SD card. Relay board centred under it (y 42.5–117.5). The back relay standoffs merge with the Pi bosses above (inserts from opposite sides, holes 4.3 mm apart, 1 mm apart in height).

**User** (follow-up, verbatim): *Also, turn it around, so that the GPIOs are on the outside wall, not close to the passthrough hole.*

**Decision** (Claude, spec v0.17): Pi turned 180° (a board can only be turned, not mirrored): GPIO header along the left edge (outer wall), power socket facing the feed-through (short USB-C cable), **USB/Ethernet to the back, SD card to the front**, still centred with 34.5 mm at both ends.
