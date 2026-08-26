# Wiring / perfboard notes

## Physical zoning

Arrange the hand-solder board from left to right:

```text
VIN / HV chains
    ->
LOW/MID/HIGH taps
    ->
K2 + K1 range relays
    ->
1k + primary Schottky clamp
    ->
MCP6024
    ->
330R + 1.5nF + secondary clamp
    ->
RP2040 ADC
```

Keep the high-value resistor chains along one edge of the board and keep all RP2040/3V3 wiring away from the HV end.

## Test points

Add pin loops for:

- VIN
- GND
- VBIAS_DIV
- VBIAS
- LOW_TAP
- MID_TAP
- HIGH_TAP
- SELECTED
- PROTECT
- BUF
- ADC_NODE
- +3V3
- +5V
- K1_COIL
- K2_COIL

## Relay physical pins

The schematic intentionally models only one SPDT pole per HK19F relay and does not assign the manufacturer's physical package pins.

Before soldering:
1. Check the exact HK19F-DC5V-SHG datasheet from your supplier.
2. Identify coil, COM, NC and NO using the bottom-view diagram.
3. Confirm coil resistance with a multimeter.
4. Confirm COM-NC continuity with the coil OFF.
5. Energize the coil with 5 V and confirm COM-NO continuity.

## First-power checklist

- RP2040 disconnected.
- Current-limited 3.3 V supply.
- Measure U1 pin 4 = 3.3 V and pin 11 = 0 V.
- Measure VBIAS around 1.65 V.
- Check BUF follows a 0–3.0 V lab input.
- Only then connect ADC_NODE to RP2040.
