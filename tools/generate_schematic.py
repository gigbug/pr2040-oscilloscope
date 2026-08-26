#!/usr/bin/env python3
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "frontend_rp2040.sch"
uid = 0x67000001


def comp(sym, ref, value, x, y):
    global uid
    u = uid
    uid += 1
    return f'''$Comp\nL {sym} {ref}\nU 1 1 {u:08X}\nP {x} {y}\nF 0 "{ref}" H {x} {y-180} 50 0000 C CNN\nF 1 "{value}" H {x} {y+180} 50 0000 C CNN\nF 2 "" H {x} {y} 50 0001 C CNN\nF 3 "" H {x} {y} 50 0001 C CNN\n\t1    {x} {y}\n\t1 0 0 -1\n$EndComp\n'''


def wire(x1, y1, x2, y2):
    return f"Wire Wire Line\n\t{x1} {y1} {x2} {y2}\n"


def label(x, y, name):
    return f"Text Label {x} {y} 0    45   ~ 0\n{name}\n"


def note(x, y, text, size=50):
    return f"Text Notes {x} {y} 0    {size}   ~ 12\n{text}\n"


s = '''EESchema Schematic File Version 4\nLIBS:frontend-cache\nEELAYER 29 0\nEELAYER END\n$Descr A4 11693 8268\nSheet 1 1\nTitle "Automotive Frontend 1CH - RP2040 Research"\nDate "2026-08-26"\nRev "V0.1-PROTOTYPE"\nComp "Automotive Repair Tools Project"\nComment1 "30V / 300V / 600V autorange frontend - hand solder research"\nComment2 "MCP6024 DIP14 + HK19F relays + Schottky clamps"\nComment3 "NOT production rated - validate HV/compensation before PCB"\nComment4 "Do not use solderless breadboard for 300/600V"\n$EndDescr\n'''

s += note(600, 500, "AUTOMOTIVE FRONTEND 1CH - RP2040 / HAND-SOLDER PROTOTYPE", 75)
s += note(600, 650, "HV TEST ONLY ON SOLDERED FR4 + CURRENT-LIMITED SOURCE. NO MAINS. NO DIRECT SECONDARY IGNITION.", 48)

# Input
s += comp("CONN_2", "J1", "ANALOG_INPUT", 800, 1050)
s += wire(1250,1000,1450,1000) + label(1450,1000,"VIN")
s += wire(1250,1100,1450,1100) + label(1450,1100,"GND")

# Divider generator: RHI chain + 47k low side + compensation network.
def divider(prefix, y, values, lowref, dampref, chiref, clowref, tap, clow):
    global s
    s += note(600, y-250, prefix, 52)
    xs = [1800 + 700*i for i in range(len(values))]
    refs = []
    for x, (ref, value) in zip(xs, values):
        s += comp("RESISTOR_THT", ref, value, x, y)
        refs.append(ref)
    for a,b in zip(xs[:-1], xs[1:]):
        s += wire(a+300,y,b-300,y)
    s += wire(xs[0]-300,y,1450,y) + label(1450,y,"VIN")
    end = xs[-1]+300
    tapx = end+300
    s += wire(end,y,tapx,y) + label(tapx,y,tap)
    s += comp("RESISTOR_THT", lowref, "47k 1%", tapx+400, y)
    s += label(tapx+700,y,"VBIAS")
    # high-side compensation branch is logically VIN -> 2.2k -> 4.7pF/1kV -> TAP
    s += comp("RESISTOR_THT", dampref, "2.2k", 2600, y+200)
    s += comp("CAP_THT", chiref, "4.7pF / >=1kV C0G", 3400, y+200)
    s += wire(2900,y+200,3100,y+200) + label(2300,y+200,"VIN") + label(3700,y+200,tap)
    s += comp("CAP_THT", clowref, clow, tapx+400, y+200)
    s += label(tapx+100,y+200,tap) + label(tapx+700,y+200,"VBIAS")

low_vals = [(f"R{i}", "180k 1%") for i in range(1,7)]
divider("LOW RANGE ~ +/-30V",1450,low_vals,"R7","R8","C1","C2","LOW_TAP","100pF C0G (TUNE)")
mid_vals = [(f"R{i}", "2.7M 1% HV") for i in range(9,13)]
divider("MID RANGE ~ +/-300V",2250,mid_vals,"R13","R14","C3","C4","MID_TAP","1nF C0G (TUNE)")
high_vals = [(f"R{i}", "2.7M 1% HV") for i in range(15,23)]
divider("HIGH RANGE ~ +/-600V",3050,high_vals,"R23","R24","C5","C6","HIGH_TAP","2.2nF C0G (TUNE)")

# Relay selector, logical pins only.
s += note(8200,1050,"AUTORANGE: OFF/OFF=HIGH; K2 ON=MID; K1 ON=LOW",48)
s += comp("RELAY_SPDT_LOGIC","K2","HK19F 5V - logical",8650,1500)
s += label(7950,1350,"+5V") + wire(7950,1350,8150,1350)
s += label(7950,1650,"K2_COIL") + wire(7950,1650,8150,1650)
s += wire(9150,1400,9400,1400)+label(9400,1400,"K2_COM")
s += wire(9150,1500,9400,1500)+label(9400,1500,"HIGH_TAP")
s += wire(9150,1600,9400,1600)+label(9400,1600,"MID_TAP")
s += comp("RELAY_SPDT_LOGIC","K1","HK19F 5V - logical",8650,2150)
s += label(7950,2000,"+5V") + wire(7950,2000,8150,2000)
s += label(7950,2300,"K1_COIL") + wire(7950,2300,8150,2300)
s += wire(9150,2050,9400,2050)+label(9400,2050,"SELECTED")
s += wire(9150,2150,9400,2150)+label(9400,2150,"K2_COM")
s += wire(9150,2250,9400,2250)+label(9400,2250,"LOW_TAP")
s += note(8200,2500,"VERIFY PHYSICAL HK19F BOTTOM-VIEW PINOUT BEFORE SOLDERING",42)

# Primary protection.
s += note(600,3900,"PRIMARY CLAMP + BUFFER",55)
s += comp("RESISTOR_THT","R25","1k",2200,4250)
s += label(1900,4250,"SELECTED") + label(2500,4250,"PROTECT")
s += comp("DIODE_THT","D1","1N5711",3400,4150)
s += label(3100,4150,"PROTECT") + label(3700,4150,"+3V3")
s += comp("DIODE_THT","D2","1N5711",3400,4350)
s += label(3100,4350,"GND") + label(3700,4350,"PROTECT")

# VBIAS.
s += note(600,4900,"VBIAS ~1.65V",52)
s += comp("RESISTOR_THT","R26","10k 1%",1800,5150) + label(1500,5150,"+3V3") + label(2100,5150,"VBIAS_DIV")
s += comp("RESISTOR_THT","R27","10k 1%",2600,5150) + label(2300,5150,"VBIAS_DIV") + label(2900,5150,"GND")
s += comp("CAP_THT","C7","100nF",1800,5350) + label(1500,5350,"VBIAS_DIV") + label(2100,5350,"GND")
s += comp("CAP_THT","C8","1uF",2600,5350) + label(2300,5350,"VBIAS_DIV") + label(2900,5350,"GND")

# MCP6024 physical DIP block. A = VBIAS buffer, B = signal buffer, C/D = stable followers.
s += comp("MCP6024_DIP14","U1","MCP6024-I/P DIP14",5600,5050)
s += wire(5000,4750,4800,4750)+label(4800,4750,"VBIAS")
s += wire(5000,4850,4700,4850)+wire(4700,4850,4700,4750)+wire(4700,4750,5000,4750)
s += wire(5000,4950,4800,4950)+label(4800,4950,"VBIAS_DIV")
s += wire(5000,5050,4800,5050)+label(4800,5050,"+3V3")
s += wire(5000,5150,4800,5150)+label(4800,5150,"PROTECT")
s += wire(5000,5250,4700,5250)+wire(4700,5250,4700,5350)+wire(4700,5350,5000,5350)
s += wire(5000,5350,4800,5350)+label(4800,5350,"BUF")
s += wire(6200,5050,6400,5050)+label(6400,5050,"GND")
s += wire(6200,5150,6400,5150)+label(6400,5150,"VBIAS")
s += wire(6200,5250,6500,5250)+wire(6500,5250,6500,5350)+wire(6500,5350,6200,5350)
s += wire(6200,4950,6400,4950)+label(6400,4950,"VBIAS")
s += wire(6200,4850,6500,4850)+wire(6500,4850,6500,4750)+wire(6500,4750,6200,4750)

# ADC filter + secondary clamp.
s += comp("RESISTOR_THT","R28","330R",7500,4850)+label(7200,4850,"BUF")+label(7800,4850,"ADC_NODE")
s += comp("CAP_THT","C9","1.5nF C0G",7500,5050)+label(7200,5050,"ADC_NODE")+label(7800,5050,"GND")
s += comp("DIODE_THT","D3","1N5711",8400,4750)+label(8100,4750,"ADC_NODE")+label(8700,4750,"+3V3")
s += comp("DIODE_THT","D4","1N5711",8400,4950)+label(8100,4950,"GND")+label(8700,4950,"ADC_NODE")
s += comp("CAP_THT","C10","100nF",7200,5350)+label(6900,5350,"+3V3")+label(7500,5350,"GND")
s += comp("CAP_THT","C11","4.7uF",8000,5350)+label(7700,5350,"+3V3")+label(8300,5350,"GND")

# RP2040 bench header.
s += comp("CONN_6","J2","RP2040/PICO BENCH HEADER",10100,5050)
for yy,name in [(4800,"+3V3"),(4900,"GND"),(5000,"ADC_NODE"),(5100,"GPIO_K1"),(5200,"GPIO_K2"),(5300,"+5V")]:
    s += wire(10550,yy,10800,yy)+label(10800,yy,name)

# Relay drivers.
s += note(600,6100,"RELAY LOW-SIDE DRIVERS",52)
for base_x, qref, rbase, rpd, diode, gpio, coil in [
    (1800,"Q1","R29","R30","D5","GPIO_K1","K1_COIL"),
    (5200,"Q2","R31","R32","D6","GPIO_K2","K2_COIL")]:
    s += comp("RESISTOR_THT",rbase,"1k",base_x,6400)+label(base_x-300,6400,gpio)+label(base_x+300,6400,f"BASE_{qref}")
    s += comp("RESISTOR_THT",rpd,"10k pulldown",base_x+800,6600)+label(base_x+500,6600,f"BASE_{qref}")+label(base_x+1100,6600,"GND")
    s += comp("NPN_THT",qref,"2N2222A / S8050 TO92",base_x+1700,6400)
    s += label(base_x+1200,6400,f"BASE_{qref}")+wire(base_x+1200,6400,base_x+1400,6400)
    s += wire(base_x+2000,6300,base_x+2250,6300)+label(base_x+2250,6300,coil)
    s += wire(base_x+2000,6500,base_x+2250,6500)+label(base_x+2250,6500,"GND")
    s += comp("DIODE_THT",diode,"1N4148 flyback",base_x+1700,6800)+label(base_x+1400,6800,coil)+label(base_x+2000,6800,"+5V")

s += note(600,7300,"TEST ORDER: VBIAS -> BUFFER -> LOW <=30V -> CLAMPS -> RELAYS -> MID/HIGH at low V -> COMPENSATION -> controlled HV.",46)
s += note(600,7450,"RELAY SWITCHING IS NOT PROTECTION. EVERY RANGE MUST SURVIVE +/-600V PEAK BY PASSIVE ATTENUATION + CLAMPS.",46)
s += "$EndSCHEMATC\n"

OUT.write_text(s, encoding="utf-8")
print(f"Generated: {OUT}")
