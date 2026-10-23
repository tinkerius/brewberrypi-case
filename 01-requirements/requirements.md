# Requirements

Status: **complete (2026-10-19)**, updated after the reviews (rounds 3, 4 and 6, `I3`, `I4`, `I6`). Exit criterion met: all questions answered. Q2 is covered by assumption A1 until the relay board arrives.
 Sources: interview round `I1`, sketches `S1–S3`, components `C1–C8` (see `inputs/`).

## Purpose
| ID | Requirement | Source |
|---|---|---|
| R1 | Enclosure for the BrewberryPi brewing controller: Raspberry Pi, relay board, USB-C power adapter, mains switches, mains inlet and mains sockets for **boiler** and **pump**. | S1–S3 |

## Layout
| ID | Requirement | Source |
|---|---|---|
| R2 | Two compartments stacked vertically, separated by a horizontal **divider**: upper **low-voltage part** (Pi), lower **high-voltage part** (mains). Called "RPI part" / "MAINS part" in sketch S1. | S1, S2, S3, I4 |
| R3 | The Pi sits on standoffs **on top of** the divider. The relay board hangs on standoffs **under** the divider, **directly below the Pi** (stacked). | S1, I3 |
| R4 | A **cable feed-through** in the divider for the Pi ↔ relay-board wiring (GPIO jumper cable) and the Pi power cable. | S1 |
| R5 | The USB-C power adapter (C2) is mounted **under the divider, next to the relay board**. The bottom lid carries no components. | S1, C2, I3 |

## Openings
| ID | Requirement | Source |
|---|---|---|
| R6 | **Front, high-voltage part:** 1 × main switch (C6, I/0) + 2 × switches boiler/pump (C7, I/0/II), side by side. Order seen from the top, left to right: **mains, boiler (heater), pump**. | S2, C6, C7, I6 |
| R7 | **Back, high-voltage part:** 1 × IEC C14 inlet with fuse (C4) + 2 × panel sockets boiler/pump (C5), each with its screw holes. Order seen from the top, left to right: **mains inlet, boiler (heater), pump**, the same as the switches at the front. | S3, C4, C5, I6 |
| R8 | **Back, low-voltage part:** 1 × 3.5 mm jack socket for the temperature sensor (C3), above the power inlet. | S3, C3, I6 |

## Hardware & replaceability
| ID | Requirement | Source |
|---|---|---|
| R9 | Fits a **Raspberry Pi 3** now. A **Pi 4 or Pi 5** must be fittable as a replacement (same 58 × 49 mm M2.5 hole pattern). | I1, C8 |
| R10 | Component cutouts and mounting patterns are **parameters** with the values from C1–C7 as defaults, so other parts can be swapped in. | I1 |

## Construction
| ID | Requirement | Source |
|---|---|---|
| R11 | The **top lid** opens for access to the low-voltage part. The **bottom** opens for access to the high-voltage part. | I1, S1 |
| R12 | Screw joints use **brass heat-set inserts + screws**: **M2.5 inserts 2.5 × 5 × 3.5 for the circuit boards** (Pi, relay board), **M3 inserts 3 × 6 × 4.5 for everything else**. | I1, I10, I11 |
| R13 | **Easily FDM-printable**: no tiny details, **single filament/colour**, **minimum number of printed parts**. | I1 |
| R14 | **Parametric**: every uncertain dimension is a named parameter with a documented default. | I1 |
| R16 | **Part split A**: body (walls only), separate **divider plate**, top lid, bottom lid. Pi and relay board mount on the divider plate. | I2-Q1 |
| R17 | No Pi port is reachable from outside. The Pi is accessed by opening the top lid. | I2-Q4 |
| R18 | Changing to a Pi 4/5 may require reprinting **only the divider plate**. Optional fan mount (off by default). | I2-Q5 |
| R19 | Freestanding on a table, on **adhesive rubber feet**. No markings on the bottom lid. | I2-Q6, I9 |
| R20 | **Raised labels** (switch and socket names, logo) that can be painted with a touch-up pen. The boiler switch and socket are labelled **HEATER**. | I2-Q7, I7 |
| R21 | Each printed part fits in **200 × 200 × 200 mm**. | I2-Q8 |
| R22 | Each lid ↔ wall connection has an **interlocking feature** (groove / notch / lip) so the joint is stronger than with screws alone. | I4 |
| R23 | The Pi's **USB and Ethernet ports** have free space in front of them (not blocked by a wall), so cables and sticks can be plugged in with the top lid open. | I16 |

## Safety
| ID | Requirement | Source |
|---|---|---|
| R15 | Mains (230 V~) is present. Mains and low voltage are separated by the divider. Electrical design (ratings, wiring, earthing) is **out of scope** and the user's responsibility (I2-Q3: "10 A is fine, don't worry about the electric part"). | S1, I2-Q3 |

## Constraints
- Printable on a typical FDM printer without printer-specific tuning (see `docs/fdm-design-rules.md`).
- No printer or slicer settings are part of the design.

## Assumptions (apply unless the user says otherwise)
- **A1** ~~Relay board size assumed~~ → **measured** (I10): 75 × 52, holes 70 × 46 Ø3, height 17 + 3 mm pins.
- **A2** ~~Jack hole assumed Ø6~~ → **measured** (I10): M8 thread, 4 mm usable, hex nut 2 mm / 11 mm, nose Ø10.
- **A3** Rocker switches snap into a panel of ≈ 1.5–2 mm → the front wall is locally thinned around the cutouts (C6, C7).
- **A4** Fastener set: **M3** inserts + screws for the case (lids, divider, IEC inlet, sockets via M3 + washer in their Ø4.5 holes), M3 × 30 + nut for the adapter. **M2.5** inserts + screws for the PCBs (Pi, relay board) (I11).
- **A5** No Pi ports are exposed. Network via Wi-Fi, and Pi access by opening the top lid.
- **A6** The Pi is powered from the USB-C adapter (C2) through the divider feed-through (Pi 3 needs a USB-C → micro-USB cable).
- **A7** Passive ventilation slots in the low-voltage part. Optional 30 mm or 40 mm fan mount as a parameter (for a Pi 5).
- **A8** Freestanding on a table, with no wall mount.
- **A9** ~~Adapter hole unknown~~ → **measured** (I10, I13, I14): **two** through-holes Ø3.5, diagonally opposite (top-right / bottom-left), centres **3.5 mm** from the top/bottom edge and **13 mm** from the side edge (25 × 42 mm apart, 48.5–48.9 mm diagonal), 5 mm recess; adapter 51 × 49 × 27.

## Open questions
- None. Adapter hole spacing re-measured (round 14): 13 mm from the sides, 3.5 mm from the top/bottom.

## Answered (round 2)
Q1 → R16 · Q2 → A1 · Q3 → R15 · Q4 → R17/A5 · Q5 → R18/A7 · Q6 → R19/A8 · Q7 → R20 · Q8 → R21 · round 4 → R2 (names), R22
