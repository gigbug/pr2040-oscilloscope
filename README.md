# Automotive Frontend RP2040 — KiCad Research Project

## Status

**V0.1 hand-solder research schematic. Not production-rated.**

This project captures the agreed 1-channel automotive analog frontend used to validate the high-risk analog sections before the STM32/production PCB is designed.

### Target architecture

- RP2040/Pico used temporarily as the ADC/controller.
- 3 ranges: approximately ±30 V / ±300 V / ±600 V.
- Three passive divider paths are always connected in parallel.
- Two 5 V signal relays select the active range.
- Relay default state selects HIGH range.
- Relays are **not** protection devices.
- Passive resistor chains + Schottky clamps protect downstream stages.
- MCP6024-I/P DIP-14 at 3.3 V:
  - A = VBIAS buffer.
  - B = signal buffer.
  - C/D = stable followers at VBIAS.
- ADC output filter: 330 Ω + 1.5 nF.
- Clamp diodes: 1N5711 through-hole for hand-solder prototype.

## Generate the KiCad schematic

The connected GitHub API used to publish this repository is optimized for text files, so the schematic is generated deterministically from source instead of committing an unverified long payload.

After cloning the repository, run:

```bash
python tools/generate_schematic.py
```

This creates:

```text
frontend_rp2040.sch
```

The generator is the source of truth for V0.1. Any schematic design changes should be made in `tools/generate_schematic.py` and the BOM/docs updated in the same commit.

## Open in KiCad

`frontend_rp2040.sch` is a legacy Eeschema schematic intentionally used because it is simple, self-contained and can be imported by modern KiCad.

Open it in KiCad 7/8/9:

1. Run `python tools/generate_schematic.py`.
2. Open KiCad / Schematic Editor.
3. Open `frontend_rp2040.sch`.
4. When KiCad offers conversion, save it as `frontend_rp2040.kicad_sch`.
5. Keep `frontend-cache.lib` and `sym-lib-table` in the project directory.

`frontend_rp2040.kicad_pro` is provided so the directory is recognized as a KiCad project. KiCad may add normal project settings when first saved.

## Symbol library

The project includes `frontend-cache.lib`, so it does not rely on non-standard symbols.

The MCP6024 symbol is drawn as its physical DIP-14 pin block, which is useful for hand soldering:

| Pin | Function |
|---:|---|
| 1 | OUTA |
| 2 | INA- |
| 3 | INA+ |
| 4 | VDD |
| 5 | INB+ |
| 6 | INB- |
| 7 | OUTB |
| 8 | OUTC |
| 9 | INC- |
| 10 | INC+ |
| 11 | VSS |
| 12 | IND+ |
| 13 | IND- |
| 14 | OUTD |

The HK19F relay symbol is **logical**, not a physical footprint. Verify the exact bottom-view pinout printed in the datasheet for the relay you buy before soldering.

## Range logic

- K1 OFF + K2 OFF -> HIGH / ~±600 V.
- K1 OFF + K2 ON -> MID / ~±300 V.
- K1 ON -> LOW / ~±30 V.

The firmware must lock range during a capture. If a transient clips the ADC, increase the range for the next capture.

## Divider starting values

### LOW

- RHI = 6 × 180 kΩ.
- RLOW = 47 kΩ.
- High-side compensation: 2.2 kΩ + 4.7 pF / >=1 kV.
- Low-side compensation: 100 pF C0G.

### MID

- RHI = 4 × 2.7 MΩ.
- RLOW = 47 kΩ.
- High-side compensation: 2.2 kΩ + 4.7 pF / >=1 kV.
- Low-side compensation: 1 nF C0G.

### HIGH

- RHI = 8 × 2.7 MΩ.
- RLOW = 47 kΩ.
- High-side compensation: 2.2 kΩ + 4.7 pF / >=1 kV.
- Low-side compensation: 2.2 nF C0G.

The compensation values are **starting values**, not production-final values.

## Recommended bench sequence

1. Assemble only MCP6024 power + VBIAS.
2. Verify VBIAS near 1.65 V.
3. Verify the signal buffer at 0–3.3 V.
4. Assemble LOW divider only and test from 0 to 30 V.
5. Add primary/secondary clamps and repeat low-voltage testing.
6. Add relay selector and drivers.
7. Add MID/HIGH resistor chains but validate ratios using <=30 V first.
8. Add compensation parts and tune with a square wave.
9. Only then increase voltage under current limit.
10. Perform wrong-range survival tests only after all earlier stages pass.

## HV safety / prototype constraints

- Do **not** build the 300/600 V resistor chains on solderless breadboard.
- Use soldered FR4/perfboard with spacing.
- Use current-limited HV sources.
- Resistor working-voltage rating matters, not only wattage.
- Do not connect directly to secondary ignition.
- This is not CAT-rated or mains-rated equipment.
- Do not claim 600 V product rating until pulse/continuous limits and PCB spacing are validated.

## Files

- `tools/generate_schematic.py` — source of truth for the generated schematic.
- `frontend-cache.lib` — self-contained legacy symbols.
- `sym-lib-table` — local symbol-library mapping.
- `frontend_rp2040.pro` — legacy project stub.
- `frontend_rp2040.kicad_pro` — modern project stub.
- `BOM.csv` — hand-solder research BOM.
- `docs/wiring_notes.md` — perfboard/test notes.
