from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    print("Connected to CDP!")
    for ctx in browser.contexts:
        print("Context:", ctx)
        for page in ctx.pages:
            print("  Page:", page.title(), "| URL:", page.url)
    browser.close()
