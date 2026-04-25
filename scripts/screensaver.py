#!/usr/bin/env python3
"""
MU/TH/UR 6000 — USCSS NOSTROMO STATUS DISPLAY
Weyland-Yutani Corp. // Deep Space Monitoring System
Density: HIGH // Priority: SPECIAL ORDER 937
"""

import time
import random
import sys
import tty
import termios
import threading

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════
W       = 79
INNER   = W - 2        
L_CELL  = 28           # Wider for more complex UIDs
R_CELL  = INNER - L_CELL - 1   
L_TEXT  = L_CELL - 2  
R_TEXT  = R_CELL - 2  

CHAR_DELAY = 0.002   # Ultrafast for high-density data
LINE_PAUSE = 0.03    

# ════════════════════════════════════════════════════════════════════════════
# ANSI & CORE ENGINE
# ════════════════════════════════════════════════════════════════════════════
GREEN   = "\033[32m"
RED     = "\033[31m"
YELLOW  = "\033[33m"
DIM     = "\033[2m"
INVERSE = "\033[7m"
RESET   = "\033[0m"
CLEAR   = "\033[2J\033[H"

running = True

def typewriter(text, delay=CHAR_DELAY):
    for char in text:
        if not running: break
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r\n")
    sys.stdout.flush()
    time.sleep(LINE_PAUSE)

def wait_for_key():
    global running
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        running = False

# ════════════════════════════════════════════════════════════════════════════
# TELEMETRY GENERATOR
# ════════════════════════════════════════════════════════════════════════════
def get_telemetry(category):
    roll = random.random()
    if roll < 0.85:
        status, color = "NOMINAL", GREEN
    elif roll < 0.97:
        status, color = random.choice(["WARNING", "DEGRADED", "OFFLINE", "FLUCT"]), YELLOW
    else:
        status, color = random.choice(["CRITICAL", "EMERGENCY", "BREACH", "OVERLOAD"]), RED + INVERSE

    # Specialized Data Generation
    if category == "TEMP":
        val = f"{random.uniform(-20, 1500):.1f}K"
    elif category == "PRESS":
        val = f"{random.uniform(0.5, 450.0):.2f} PSI"
    elif category == "POWER":
        val = f"{random.uniform(85, 104.5):.1f} MW"
    elif category == "ATMOS":
        val = f"{random.uniform(0.9, 1.1):.2f} ATM"
    elif category == "RAD":
        val = f"{random.uniform(0.01, 0.09):.3f} mSv/h"
    elif category == "NAV":
        val = f"{random.uniform(10.0, 999.9):.1f} AU"
    elif category == "MASS":
        val = f"{random.randint(100, 5000)} KG"
    else:
        val = f"{random.randint(10, 99)}%"

    return f"{val} {status}", color

# ════════════════════════════════════════════════════════════════════════════
# EQUIPMENT DATA
# ════════════════════════════════════════════════════════════════════════════
# Key format: (Sensor Name, Category)
DECK_DATA = {
    "REACTOR / ENGINEERING": [
        ("MAG-CONTAINMENT-{ID}", "POWER"), ("COOLANT-VALVE-{ID}", "PRESS"), ("CORE-TEMP-SENS-{ID}", "TEMP"),
        ("FUEL-INJECTOR-{ID}", "PRESS"), ("NEUTRON-FLUX-ID{ID}", "RAD"), ("TURBINE-GRID-{ID}", "POWER"),
        ("EMERGENCY-BATT-{ID}", "POWER"), ("PLASMA-CONDUIT-{ID}", "TEMP"), ("HEAT-EXCHANGER-B", "TEMP"),
        ("PRIMARY-VENT-S{ID}", "PRESS"), ("MHD-GENERATOR-A", "POWER"), ("FUEL-ROD-ASSY-{ID}", "RAD"),
        ("DAMPING-FIELD-{ID}", "OTHER"), ("COOLANT-PUMP-{ID}", "PRESS"), ("FUSION-CORE-STAB", "OTHER")
    ],
    "LIFE SUPPORT / ATMOS": [
        ("O2-SCRUBBER-U{ID}", "ATMOS"), ("CO2-LEVEL-SENS-{ID}", "ATMOS"), ("N2-RESERVE-T{ID}", "PRESS"),
        ("GRAV-PLATE-Z{ID}", "OTHER"), ("HUMIDITY-CTRL-{ID}", "OTHER"), ("ATMOS-PRESS-L3", "ATMOS"),
        ("WATER-RECYCLER-{ID}", "OTHER"), ("THERMAL-REG-{ID}", "TEMP"), ("HULL-EXT-TEMP", "TEMP"),
        ("O2-GEN-ELECTRO", "POWER"), ("AIR-FILTRATION-{ID}", "OTHER"), ("BIO-MONITOR-{ID}", "RAD"),
        ("WASTE-RECOVERY", "MASS"), ("CABIN-PRESSURE-A", "ATMOS"), ("EMERG-O2-TANK-{ID}", "PRESS")
    ],
    "BRIDGE / NAVIGATION": [
        ("INERTIAL-DAMPER-{ID}", "OTHER"), ("STAR-TRACKER-A{ID}", "NAV"), ("LONG-RANGE-LINK", "OTHER"),
        ("HEADING-COORD-X", "NAV"), ("HEADING-COORD-Y", "NAV"), ("HEADING-COORD-Z", "NAV"),
        ("GYRO-STAB-B", "OTHER"), ("AUTOPILOT-CPU-{ID}", "OTHER"), ("DOCKING-CLAMPS", "OTHER"),
        ("TELEMETRY-RELAY-{ID}", "NAV"), ("PROXIMITY-SENS-F", "NAV"), ("INTERSTELLAR-BCN", "NAV"),
        ("SENSOR-ARRAY-L{ID}", "OTHER"), ("THRUSTER-VECTOR-G", "OTHER"), ("COMMS-BUFFER-S{ID}", "OTHER")
    ],
    "CARGO / HOLD SECTORS": [
        ("MAG-LOCK-BAY-{ID}", "OTHER"), ("MOTION-TRACKER-{ID}", "NAV"), ("HULL-INTEG-S{ID}", "OTHER"),
        ("AIRLOCK-PRESS-A", "ATMOS"), ("CARGO-TETHER-{ID}", "MASS"), ("EXT-FLOOD-LIGHTS", "OTHER"),
        ("BIO-HAZARD-SEAL", "OTHER"), ("FIRE-SUPPR-B", "OTHER"), ("DECK-7-LATCH-{ID}", "OTHER"),
        ("LOAD-BEARING-S{ID}", "MASS"), ("STORAGE-UNIT-{ID}", "MASS"), ("ELEVATOR-WINCH-A", "OTHER"),
        ("CRANE-HYDRAULIC", "PRESS"), ("REFRIG-STORAGE-{ID}", "TEMP"), ("QUARANTINE-LOK", "OTHER")
    ]
}

# ════════════════════════════════════════════════════════════════════════════
# RENDER LOGIC
# ════════════════════════════════════════════════════════════════════════════
TOP_RULE    = "╔" + "═" * INNER      + "╗"
MID_RULE    = "╠" + "═" * INNER      + "╣"
BOT_RULE    = "╚" + "═" * INNER      + "╝"
SPLIT_OPEN  = "╠" + "─" * L_CELL + "╦" + "─" * R_CELL + "╣" 
INNER_SPLIT = "╠" + "─" * L_CELL + "╬" + "─" * R_CELL + "╣" 
SPLIT_CLOSE = "╠" + "═" * L_CELL + "╩" + "═" * R_CELL + "╣"

def _pad(text, width):
    return text[:width] + " " * (width - len(text))

def full_row(text):
    return "║ " + _pad(text, INNER - 2) + " ║"

def col_row(ltext, rtext, lcolor="", rcolor=""):
    lf = _pad(ltext, L_TEXT)
    rf = _pad(rtext, R_TEXT)
    lpart = f"{lcolor}{lf}{RESET}" if lcolor else lf
    rpart = f"{rcolor}{rf}{RESET}" if rcolor else rf
    return f"║ {lpart} ║ {rpart} ║"

def run_special_order():
    sys.stdout.write(CLEAR)
    typewriter(f"{RED}{INVERSE}{TOP_RULE}{RESET}")
    typewriter(f"{RED}{INVERSE}║ {'CLASSIFIED TOP SECRET':^{INNER-2}} ║{RESET}")
    typewriter(f"{RED}{INVERSE}{MID_RULE}{RESET}")
    orders = [
        "WEYLAND-YUTANI CORP // SPECIAL ORDER 937",
        "PRIORITY ONE",
        "INSURE RETURN OF ORGANISM",
        "ALL OTHER PRIORITIES RESCINDED",
        " ", "      CREW EXPENDABLE", " ",
        "AI UNIT 'ASH' MONITORING ACTIVE",
        "DIRECTIVE 0-1-0 OVERRIDE ENABLED"
    ]
    for line in orders: typewriter(f"{RED}║ {_pad(line, INNER-2)} ║{RESET}", delay=0.02)
    typewriter(f"{RED}{INVERSE}{BOT_RULE}{RESET}")
    time.sleep(6)
    sys.stdout.write(CLEAR)

def render_section(name, items):
    typewriter(SPLIT_OPEN)
    typewriter(col_row(name, f"DECK MONITOR  {time.strftime('%H:%M')}", lcolor=YELLOW, rcolor=DIM))
    typewriter(INNER_SPLIT)
    
    # RANDOM SIZE: 10 to 15 readouts
    count = random.randint(10, 15)
    
    # Shuffle and pick items (allowing repeats if list is shorter than count, but here it's 15)
    pool = random.sample(items, min(len(items), count))
    
    for item_template, category in pool:
        if not running: break
        uid = f"{random.randint(100, 999)}"
        label = item_template.replace("{ID}", uid)
        telemetry, color = get_telemetry(category)
        typewriter(col_row(label, telemetry, rcolor=color))
    
    typewriter(SPLIT_CLOSE)

# ════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ════════════════════════════════════════════════════════════════════════════
t = threading.Thread(target=wait_for_key, daemon=True)
t.start()

sys.stdout.write(CLEAR)
typewriter(TOP_RULE)
typewriter(full_row("MU/TH/UR 6000  //  USCSS NOSTROMO  //  MONITORING ACTIVE"))
typewriter(MID_RULE)

deck_names = list(DECK_DATA.keys())
idx = 0

while running:
    if random.random() < 0.02:
        run_special_order()
        typewriter(TOP_RULE)

    deck_key = deck_names[idx % len(deck_names)]
    render_section(deck_key, DECK_DATA[deck_key])
    
    time.sleep(random.uniform(0.6, 1.4))
    idx += 1
    
    if idx % 2 == 0 and running: # Footer every 2 sections now due to height
        typewriter(full_row(time.strftime("%Y.%m.%d // %H:%M:%S // WEYLAND-YUTANI")))
        typewriter(BOT_RULE)
        time.sleep(0.8)
        if running:
            typewriter(TOP_RULE)

sys.stdout.write(f"{RESET}{CLEAR}")
