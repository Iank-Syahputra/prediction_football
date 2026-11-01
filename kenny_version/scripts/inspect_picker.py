from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    target_page = [pg for pg in context.pages if "1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw" in pg.url][0]
    
    picker_frame = None
    for f in target_page.frames:
        if "picker" in f.url:
            picker_frame = f
            break
            
    print("Picker frame:", picker_frame.name if picker_frame else "None")
    if picker_frame:
        inputs = picker_frame.locator("input").all()
        print(f"Total inputs in picker: {len(inputs)}")
        for inp in inputs:
            print("  type:", inp.get_attribute("type"), "id:", inp.get_attribute("id"), "class:", inp.get_attribute("class"))
        
        buttons = picker_frame.locator("button, div[role='button']").all()
        print(f"Total buttons in picker: {len(buttons)}")
        for b in buttons[:10]:
            print("  btn text:", b.text_content().strip())
    browser.close()
