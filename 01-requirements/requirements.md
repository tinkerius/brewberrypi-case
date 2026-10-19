# Requirements

Status: **draft (round 2 pending)**. Sources: interview round `I1`, sketches `S1–S3`, components `C1–C8` (see `inputs/`).

## Purpose
| ID | Requirement | Source |
|---|---|---|
| R1 | Enclosure for the BrewberryPi brewing controller: Raspberry Pi, relay board, USB-C power adapter, mains switches, mains inlet and mains sockets for **boiler** and **pump**. | S1–S3 |

## Layout
| ID | Requirement | Source |
|---|---|---|
| R2 | Two compartments stacked vertically, separated by a horizontal **divider**: upper **RPI part** (low voltage), lower **MAINS part**. | S1, S2, S3 |
| R3 | The Pi sits on standoffs **on top of** the divider. The relay board hangs on standoffs **under** the divider. | S1 |
| R4 | A **cable feed-through** in the divider for the Pi ↔ relay-board wiring (GPIO jumper cable) and the Pi power cable. | S1 |
| R5 | The USB-C power adapter (C2) is mounted in the MAINS part. | S1, C2 |

## Openings
| ID | Requirement | Source |
|---|---|---|
| R6 | **Front, MAINS part:** 1 × main switch (C6, I/0) + 2 × switches boiler/pump (C7, I/0/II), side by side. | S2, C6, C7 |
| R7 | **Back, MAINS part:** 1 × IEC C14 inlet with fuse (C4) + 2 × panel sockets boiler/pump (C5), each with its screw holes. | S3, C4, C5 |
| R8 | **Back, RPI part:** 1 × 3.5 mm jack socket for the temperature sensor (C3). | S3, C3 |

## Hardware & replaceability
| ID | Requirement | Source |
|---|---|---|
| R9 | Fits a **Raspberry Pi 3** now. A **Pi 4 or Pi 5** must be fittable as a replacement (same 58 × 49 mm M2.5 hole pattern). | I1, C8 |
| R10 | Component cutouts and mounting patterns are **parameters** with the values from C1–C7 as defaults, so other parts can be swapped in. | I1 |

## Construction
| ID | Requirement | Source |
|---|---|---|
| R11 | The **top lid** opens for access to the RPI part. The **bottom** opens for access to the MAINS part. | I1, S1 |
| R12 | Screw joints use **brass heat-set inserts + screws**, with as few different sizes as possible. | I1 |
| R13 | **Easily FDM-printable**: no tiny details, **single filament/colour**, **minimum number of printed parts**. | I1 |
| R14 | **Parametric**: every uncertain dimension is a named parameter with a documented default. | I1 |

## Safety
| ID | Requirement | Source |
|---|---|---|
| R15 | Mains (230 V~) is present: inlet, switches, sockets, relays, power adapter. The design must keep mains and low voltage separated by the divider, allow PE (earth) wiring to the sockets, and provide strain relief/fixing for internal wiring. **A printed enclosure is not mains insulation on its own.** Wiring must be done by a qualified person. | S1, C4, C5, CLAUDE.md |

## Constraints
- Printable on a typical FDM printer without printer-specific tuning (see `docs/fdm-design-rules.md`).
- No printer or slicer settings are part of the design.

## Assumptions (apply unless the user says otherwise)
- **A1** Relay board ≈ 75 × 55 mm, holes ≈ 69 × 49 mm Ø3.1, height ≈ 19 mm (C1, to be measured). Parameters.
- **A2** Jack socket needs a Ø6 mm hole, max 3 mm panel → the wall is locally thinned around it (C3).
- **A3** Rocker switches snap into a panel of ≈ 1.5–2 mm → the front wall is locally thinned around the cutouts (C6, C7).
- **A4** Fastener set: **M3** inserts + screws for everything (lids, divider, relay board, power adapter, IEC inlet, sockets via M3 + washer in their Ø4.5 holes). **M2.5** only for the Pi, because its holes (Ø2.75) do not take M3.
- **A5** No Pi ports are exposed. Network via Wi-Fi, and Pi access by opening the top lid.
- **A6** The Pi is powered from the USB-C adapter (C2) through the divider feed-through (Pi 3 needs a USB-C → micro-USB cable).
- **A7** Passive ventilation slots in the RPI part. Optional 30 mm or 40 mm fan mount as a parameter (for a Pi 5).
- **A8** Freestanding on a table, with no wall mount.

## Open questions (round 2)
- **Q1 Part split / how the MAINS part opens** (key question, see chat).
- **Q2** Relay board: real size and hole spacing (or "don't know" → A1).
- **Q3** Power of boiler and pump (W). The relays and the IEC inlet are rated 10 A.
- **Q4** Pi ports: does anything need to be reachable from outside (USB, Ethernet, HDMI, SD)? (→ A5)
- **Q5** Pi 4/5 swap: must the same print fit all models, or is reprinting one part OK? Fan for Pi 5? (→ A7)
- **Q6** Environment: where does it stand (steam, splashes, heat)? Table or wall? (→ A8)
- **Q7** Labels (I/0/II, "Boiler", "Pump", logo) embossed in the case? Single colour → only debossed/embossed text.
- **Q8** Rough size limits, if any (max width/depth/height).
