from playwright.sync_api import sync_playwright

url = "https://docs.google.com/forms/d/e/1FAIpQLSfaoPBT-SCmdU4KGH2CmnVHMAsc704VRVlWYsfUVj1Ybm30aw/viewform"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(3000)
    print("Page Title:", page.title())
    
    # Extract questions
    questions = page.locator("div[role='heading'], div[role='listitem'] span, .freebirdFormviewerComponentsQuestionBaseTitle").all_text_contents()
    print("Questions:", [q.strip() for q in questions if q.strip()][:20])
    
    # Extract all radio or dropdown options
    radios = page.locator("div[role='radio']").all_text_contents()
    print("Radios:", radios)
    
    browser.close()

