# Specification: BrewberryPi Case

| Version | Status | Approved by / date |
|---|---|---|
| 0.0 | template, not started | |

## 1. Overview
<!-- what the case does, which parts it consists of -->

## 2. Coordinate system
- Units: mm.
- Origin: <!-- e.g. bottom-left-front corner of the base, on the build plate -->
- +X: <!-- e.g. towards the right (USB side) -->, +Y: <!-- … -->, +Z: up.
- Build-plate face of each part: <!-- … -->

## 3. Parts
| Part | `part=` value | Print orientation (design intent) | Notes |
|---|---|---|---|
| Base | `base` | | |
| Lid | `lid` | | |

## 4. Features
| ID | Part | Feature | Dimensions / position | Tolerance | Traces to |
|---|---|---|---|---|---|
| F1 | | | | | R… |

## 5. Parameters (Customizer)
| ID | Name | Default | Range | Used by |
|---|---|---|---|---|
| P1 | `wall` | | | |
| P2 | `fit_clearance` | 0.2 | 0.1–0.5 | all mating features |

## 6. Interfaces & clearances
<!-- PCB to standoffs, connectors to openings, lid to base, cables, fasteners -->

## 7. FDM design-rule check
| Rule (docs/fdm-design-rules.md) | How it is met |
|---|---|
| Flat build-plate face | |
| Overhangs ≤ 45° or bridged | |
| Horizontal holes teardrop / flat-top | |
| Bottom edges chamfered | |
| No floating islands | |

## 8. Drawings
<!-- links to drawings/*.svg -->

## 9. Acceptance criteria
| ID | Criterion | How checked |
|---|---|---|
| AC1 | | render / dimension / print |

## 10. Revision history
| Version | Date | Change |
|---|---|---|
| 0.0 | | template |
