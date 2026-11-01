import os
import sys
import subprocess
import time
import urllib.request

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9222

print("Killing chrome...")
subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
time.sleep(2)

print("Launching Chrome with port 9222...")
cmd = [
    CHROME_BIN,
    f"--remote-debugging-port={PORT}",
]
proc = subprocess.Popen(cmd)

success = False
for i in range(10):
    time.sleep(1)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
            data = resp.read().decode()
            print("SUCCESS! CDP connected:", data)
            success = True
            break
    except Exception as e:
        print(f"Waiting ({i+1}/10)... {e}")

if not success:
    print("FAILED to enable CDP on default profile.")
