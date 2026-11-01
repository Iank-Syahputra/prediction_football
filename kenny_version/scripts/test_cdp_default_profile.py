import os
import sys
import subprocess
import time
import urllib.request

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9222

# First, check if port 9222 is listening
try:
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
        print("Port 9222 is ALREADY listening!", resp.read().decode())
        sys.exit(0)
except Exception as e:
    print("Port 9222 not listening yet:", e)

# Test launching Chrome with remote debugging on default profile
# We will check if it starts and opens port 9222
cmd = [
    CHROME_BIN,
    f"--remote-debugging-port={PORT}",
    "--restore-last-session"
]
print("Launching Chrome test...")
proc = subprocess.Popen(cmd)
time.sleep(3)

try:
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2) as resp:
        print("SUCCESS! Chrome CDP is active:", resp.read().decode())
except Exception as e:
    print("FAILED to connect to CDP:", e)
