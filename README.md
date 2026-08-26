# Automotive Frontend RP2040 — KiCad Research Project

## IMPORTANT — V0.1 is deprecated

The original V0.1 files in this repository used a generated legacy Eeschema `.sch`, did not contain a real `.kicad_pcb`, and the `.kicad_pro` file was only a stub. **Do not use V0.1 for layout, routing, fabrication, or HV testing.**

A corrected **V0.2 native KiCad 8 project** has been generated with:

- `frontend_rp2040.kicad_sch` native schematic.
- `frontend_rp2040.kicad_pcb` 2-layer routed prototype.
- Through-hole / DIP-focused footprints for hand soldering.
- Physical HK19F relay pin mapping in the prototype footprint.
- 3 ranges: approximately ±30 V / ±300 V / ±600 V.
- MCP6024-I/P DIP-14, relay drivers, primary/secondary clamps and RP2040 bench header.

The V0.2 package has passed generator-side structural and routing geometry checks, but **KiCad ERC/DRC has not yet been run**, because `kicad-cli` is unavailable in the generation environment. Open the V0.2 project in KiCad and run ERC/DRC before fabrication.

## Electrical concept retained

- RP2040/Pico is used temporarily as ADC/controller.
- Three passive divider paths are permanently connected in parallel.
- K1/K2 only select range; relays are **not** a protection mechanism.
- Relay default state is HIGH range.
- Passive resistor attenuation + Schottky clamps protect the low-voltage stages.
- MCP6024 runs at 3.3 V.
- ADC filter starts at 330 Ω + 1.5 nF.
- 1N5711 through-hole Schottky diodes are used for the hand-solder prototype.

## Range starting values

| Range | High-side resistor chain | Low-side | Initial compensation |
|---|---|---|---|
| LOW ~±30 V | 6 × 180 kΩ | 47 kΩ to VBIAS | 4.7 pF HV + 2.2 kΩ; 100 pF low-side |
| MID ~±300 V | 4 × 2.7 MΩ | 47 kΩ to VBIAS | 4.7 pF HV + 2.2 kΩ; 1 nF low-side |
| HIGH ~±600 V | 8 × 2.7 MΩ | 47 kΩ to VBIAS | 4.7 pF HV + 2.2 kΩ; 2.2 nF low-side |

Compensation values are starting values only and must be tuned on the physical prototype.

## HV prototype rules

- Do not build the 300/600 V section on solderless breadboard.
- Use soldered FR4, current-limited sources and verified resistor working-voltage ratings.
- Do not connect directly to secondary ignition.
- This design is not CAT-rated or mains-rated.
- Do not claim a 600 V product rating until pulse/continuous limits, creepage/clearance and protection tests are validated.

## Repository history

V0.1 is retained in Git history only for traceability. It should not be treated as the current KiCad implementation.
