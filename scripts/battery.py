#!/usr/bin/env python3
import json

STATUS_FILE = "/tmp/battery_status.json"
HISTORY_FILE = "/tmp/battery_history.json"
CHART_WIDTH = 48
CHART_HEIGHT = 8

def render_chart(history):
    if not history:
        print("  No history yet — check back in 5 minutes!")
        return

    percents = [h["percent"] for h in history]
    
    # Sample down to CHART_WIDTH points if we have more
    if len(percents) > CHART_WIDTH:
        step = len(percents) / CHART_WIDTH
        percents = [percents[int(i * step)] for i in range(CHART_WIDTH)]

    print(f"  BATTERY HISTORY (LAST 24H)")
    print(f"  {'─' * (CHART_WIDTH + 6)}")

    for row in range(CHART_HEIGHT, 0, -1):
        threshold = (row / CHART_HEIGHT) * 100
        label = f"{int(threshold):3}% |"
        bar = ""
        for p in percents:
            if p >= threshold:
                bar += "█"
            elif p >= threshold - (100 / CHART_HEIGHT):
                bar += "▄"
            else:
                bar += " "
        print(f"  {label}{bar}")

    print(f"       └{'─' * CHART_WIDTH}")
    first_time = history[0]["time"]
    last_time = history[-1]["time"]
    print(f"        {first_time}{' ' * (CHART_WIDTH - 10)}{last_time}")

try:
    with open(STATUS_FILE, "r") as f:
        s = json.load(f)

    print(f"═══════════════════════════════════════════════════════")
    print(f"  MUTHR BATTERY STATUS")
    print(f"═══════════════════════════════════════════════════════")
    print(f"  Voltage : {s['voltage']}V")
    print(f"  Current : {s['current']}mA")
    print(f"  Power   : {s['power']}mW")
    print(f"  Battery : {s['percent']}%")
    print(f"  ETA     : {s['eta']}")
    print(f"───────────────────────────────────────────────────────")

    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        render_chart(history)
    except:
        print("  No history yet — check back in 5 minutes!")

    print(f"═══════════════════════════════════════════════════════")

except FileNotFoundError:
    print("Battery daemon not running.")

