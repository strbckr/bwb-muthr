#!/usr/bin/env python3
import subprocess
import time

TIMEOUT = 30
SCREENSAVER = "/home/starbuck/bee-write-back/Software/scripts/screensaver.py"
LOG = "/tmp/inactivity.log"

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")

log("Inactivity daemon started")

while True:
    tty_time = float(subprocess.check_output(
        ["stat", "-c", "%X", "/dev/tty1"]
    ).decode().strip())
    
    idle = time.time() - tty_time
    log(f"Idle time: {idle:.1f}s")
    
    if idle >= TIMEOUT:
        log("Launching screensaver")
        subprocess.call(["python3", SCREENSAVER])
        log("Screensaver exited")
    
    time.sleep(10)
