import os
import sys
from playwright.sync_api import sync_playwright

user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data'
print("Using Edge User Data Dir:", user_data_dir)

url_presensi = "https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            channel="msedge",
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        print("Navigating to Presensi form...")
        page.goto(url_presensi, wait_until="networkidle")
        print("Title:", page.title())
        print("URL:", page.url)
        
        # Check if form questions are visible
        headings = page.locator("div[role='heading'], div[role='listitem'] span, .freebirdFormviewerComponentsQuestionBaseTitle").all_text_contents()
        clean = [h.strip() for h in headings if h.strip() and len(h.strip()) < 100]
        print(f"Found {len(clean)} questions/headings:")
        for c in clean[:20]:
            print("  *", c)
            
        page.screenshot(path="C:/Users/Kenny/.gemini/antigravity-ide/scratch/school_football_prediction/data/presensi_loaded.png")
        print("Saved screenshot to data/presensi_loaded.png")
        browser.close()
except Exception as e:
    print("Error:", e)
