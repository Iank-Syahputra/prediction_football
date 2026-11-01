import time, os
from playwright.sync_api import sync_playwright

PROOF_FILE = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png"
print("Uploading file:", PROOF_FILE, "Size:", os.path.getsize(PROOF_FILE))

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    target_page = [pg for pg in context.pages if "1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw" in pg.url][0]
    target_page.bring_to_front()

    picker_frame = None
    for f in target_page.frames:
        if "picker" in f.url:
            picker_frame = f
            break

    if not picker_frame:
        print("Picker frame not found! Opening file picker...")
        add_btn = target_page.locator("div[role='button']:has-text('Add file'), div[role='button']:has-text('Tambahkan file')").first
        add_btn.click()
        time.sleep(2)
        for f in target_page.frames:
            if "picker" in f.url:
                picker_frame = f
                break

    print("Found picker frame:", picker_frame.name)
    file_input = picker_frame.locator("input[type='file']")
    print("Setting input files...")
    file_input.set_input_files(PROOF_FILE)
    print("File assigned to input!")

    # Wait for upload progress to complete and modal to dismiss
    print("Waiting for file upload to finish...")
    for i in range(20):
        time.sleep(1)
        frames = [f for f in target_page.frames if "picker" in f.url]
        print(f"Sec {i+1}: picker frames remaining = {len(frames)}")
        if len(frames) == 0:
            print("Picker dialog has closed! Upload complete.")
            break

    time.sleep(2)
    shot_attached = r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\week4_file_attached.png"
    target_page.screenshot(path=shot_attached)
    print("Saved file attached screenshot:", shot_attached)

    # Click Submit button
    submit_btn = target_page.locator("div[role='button']:has-text('Submit'), div[role='button']:has-text('Kirim')").first
    print("Submit button found:", submit_btn.text_content())
    submit_btn.click()
    print("Clicked Submit button! Waiting for confirmation...")
    
    time.sleep(5)
    shot_confirm = r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\week4_presensi_confirmed.png"
    target_page.screenshot(path=shot_confirm)
    print("Saved confirmation screenshot:", shot_confirm)

    browser.close()
    print("ALL DONE SUCCESSFULLY!")
