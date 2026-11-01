import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    for idx, page in enumerate(context.pages):
        print(f"Page {idx}: title='{page.title()}' url='{page.url}'")
        if "1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw" in page.url:
            page.screenshot(path=r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\real_current_state.png")
            print("Took screenshot of form page!")
            # Check if submit button is visible
            sub = page.locator("div[role='button']:has-text('Submit'), span:has-text('Submit')")
            print("Submit button count:", sub.count())
            if sub.count() > 0:
                print("Clicking submit button again to ensure submission...")
                sub.first.click()
                print("Clicked! Waiting 8 seconds...")
                time.sleep(8)
                page.screenshot(path=r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\after_reclick_submit.png")
                print("New URL:", page.url)
                print("New Title:", page.title())
    browser.close()
