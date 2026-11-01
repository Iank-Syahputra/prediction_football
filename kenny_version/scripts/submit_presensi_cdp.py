import os, time
from playwright.sync_api import sync_playwright

PROOF_FILE = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png"
if not os.path.exists(PROOF_FILE):
    PROOF_FILE = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Bukti_Presensi_Senin_26_Okt_2026_Malam.png"

print("Using proof file:", PROOF_FILE, "Exists:", os.path.exists(PROOF_FILE))

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    
    # Find the presensi form page
    target_page = None
    for page in context.pages:
        if "1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw" in page.url:
            target_page = page
            break
            
    if not target_page:
        print("Could not find presensi page, opening in first page...")
        target_page = context.pages[0]
        target_page.goto("https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform")
        target_page.wait_for_load_state("networkidle")
    else:
        print("Found active Presensi page:", target_page.title())

    # Bring to front
    target_page.bring_to_front()
    time.sleep(1)

    # 1. Fill Nama
    name_input = target_page.locator("input.whsOnd").first
    name_input.fill("Kenny Helim")
    print("Filled Nama: Kenny Helim")

    # 2. Select Divisi: Artificial Intelligence
    divisi_opt = target_page.locator("div[role='radio'][aria-label='Artificial Intelligence'], div[data-value='Artificial Intelligence']")
    if divisi_opt.count() > 0:
        divisi_opt.first.click()
        print("Selected Divisi: Artificial Intelligence")

    # 3. Select Periode Magang: 4 Bulan (MUTLAK 4 BULAN)
    periode_opt = target_page.locator("div[role='radio'][aria-label='4 Bulan'], div[data-value='4 Bulan']")
    if periode_opt.count() > 0:
        periode_opt.first.click()
        print("Selected Periode Magang: 4 Bulan")

    # 4. Select Kehadiran: WEEK 4 Sesi 1
    kehadiran_opt = target_page.locator("div[role='radio'][aria-label='WEEK 4 Sesi 1'], div[data-value='WEEK 4 Sesi 1']")
    if kehadiran_opt.count() > 0:
        kehadiran_opt.first.click()
        print("Selected Kehadiran: WEEK 4 Sesi 1")

    # 5. Take screenshot of form before upload
    shot1 = r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\cdp_presensi_pre_upload.png"
    target_page.screenshot(path=shot1)
    print("Saved pre-upload screenshot:", shot1)

    # 6. Click 'Add file' / 'Tambahkan file'
    add_file_btn = target_page.locator("div[role='button']:has-text('Add file'), div[role='button']:has-text('Tambahkan file'), span:has-text('Add file'), span:has-text('Tambahkan file')").first
    print("Add file button text:", add_file_btn.text_content())
    add_file_btn.click()
    print("Clicked Add file button, waiting for picker iframe...")
    time.sleep(3)

    # Inspect frames
    print("Frames count:", len(target_page.frames))
    for f in target_page.frames:
        print("Frame name:", f.name, "url:", f.url[:80])

    # Find the picker frame
    picker_frame = None
    for f in target_page.frames:
        if "picker" in f.url or "google.com/picker" in f.url:
            picker_frame = f
            break

    if picker_frame:
        print("Found picker frame:", picker_frame.url)
        # In picker frame, we look for file input or Browse button
        file_input = picker_frame.locator("input[type='file']")
        print("File inputs in picker frame:", file_input.count())
        if file_input.count() > 0:
            print("Setting file directly on picker input[type='file']...")
            file_input.first.set_input_files(PROOF_FILE)
            print("File set! Waiting for upload...")
        else:
            # Try clicking Browse button with file_chooser
            browse_btn = picker_frame.locator("button:has-text('Browse'), div:has-text('Browse'), span:has-text('Browse')").first
            if browse_btn.count() > 0:
                print("Clicking Browse with expect_file_chooser...")
                with target_page.expect_file_chooser() as fc:
                    browse_btn.click()
                fc.value.set_files(PROOF_FILE)
                print("File chooser set file!")
    else:
        print("Picker frame not found, looking in page frames...")
        # Check all frames for input[type='file']
        for idx, f in enumerate(target_page.frames):
            inp = f.locator("input[type='file']")
            if inp.count() > 0:
                print(f"Found input[type='file'] in frame {idx} ({f.name})")
                inp.first.set_input_files(PROOF_FILE)
                print("File set on frame input!")
                break

    # Wait for upload progress to finish
    print("Waiting 6 seconds for upload to finish...")
    time.sleep(6)

    shot2 = r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\cdp_presensi_post_upload.png"
    target_page.screenshot(path=shot2)
    print("Saved post-upload screenshot:", shot2)

    # Check submit button
    submit_btn = target_page.locator("div[role='button']:has-text('Submit'), div[role='button']:has-text('Kirim'), span:has-text('Submit'), span:has-text('Kirim')").first
    print("Submit button text:", submit_btn.text_content())
    submit_btn.click()
    print("Clicked Submit! Waiting for response...")
    time.sleep(4)

    shot3 = r"C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\cdp_presensi_confirmation.png"
    target_page.screenshot(path=shot3)
    print("Saved confirmation screenshot:", shot3)

    browser.close()
    print("Done!")
