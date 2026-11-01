from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform')
    page.wait_for_timeout(3000)
    radios = page.locator('div[role="radio"]').all_text_contents()
    print("All radio options:")
    for r in radios:
        print(" -", r)
    browser.close()
