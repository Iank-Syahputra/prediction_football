from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    target_page = None
    for page in context.pages:
        if "1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw" in page.url:
            target_page = page
            break
    if target_page:
        target_page.screenshot(path=r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\current_page_open_dialog.png")
        print("Captured screenshot!")
        print("Frames:", len(target_page.frames))
        for f in target_page.frames:
            print("Frame:", f.name, f.url[:80])
    browser.close()
