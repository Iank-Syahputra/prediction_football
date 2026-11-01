import sys
from playwright.sync_api import sync_playwright

urls = [
    ("Form 1 (Assignment)", "https://docs.google.com/forms/d/e/1FAIpQLSdVPxekg5o3NyjLmiG3UgvyAHbwlQSqiBAMjyWroEiDXOwHHA/viewform"),
    ("Form 2 (Logbook)", "https://docs.google.com/forms/d/e/1FAIpQLSfaoPBT-SCmdU4KGH2CmnVHMAsc704VRVlWYsfUVj1Ybm30aw/viewform"),
    ("Form 3 (Presensi)", "https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for name, url in urls:
        print(f"=== Loading {name} ===")
        page.goto(url, wait_until="networkidle")
        print("Page Title:", page.title())
        print("Current URL:", page.url)
        content = page.content()
        # Look for question titles
        questions = page.locator("div[role='heading'], div[role='listitem'] span, .freebirdFormviewerComponentsQuestionBaseTitle").all_text_contents()
        clean_q = [q.strip() for q in questions if q.strip() and len(q.strip()) < 100]
        print(f"Extracted headings/questions ({len(clean_q)}):", clean_q[:15])
    browser.close()
