import subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\chrome_debug_profile"
PORT = 9222
URL = "https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform"

# Launch Chrome
cmd = [
    CHROME,
    f"--remote-debugging-port={PORT}",
    f"--user-data-dir={PROFILE_DIR}",
    "--profile-directory=Profile 8",
    "--no-first-run",
    "--no-default-browser-check",
    URL
]

print("Launching Chrome on port 9222...")
proc = subprocess.Popen(cmd)

connected = False
for _ in range(15):
    time.sleep(1)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
            if resp.status == 200:
                connected = True
                break
    except:
        pass

print("Connected to port 9222:", connected)

if connected:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        time.sleep(3)
        print("Page URL:", page.url)
        print("Page Title:", page.title())
        page.screenshot(path=r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\proofs\form_submissions\test_p8_screen.png")
        browser.close()

proc.terminate()
print("Cleaned up proc.")
