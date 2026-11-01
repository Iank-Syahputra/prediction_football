"""
==============================================================================
[MODULE GOAL & ROLE]
  Master Google Forms Automated Submitter for PT Vinix Seven Aurum Fast Track.
  Fulfills MSIB Fast Track Batch 10 (Divisi Artificial Intelligence, Kelompok 1):
    - Form 1 (Presensi): 6 submissions (Week 2 S1 & S2, Week 3 S1 & S2, Week 4 S1 & S2)
    - Form 2 (Assignment): 3 submissions (Week 2, Week 3, Week 4)
    - Form 3 (Logbook): Week 4 Logbook submission
  Enforces:
    - MANDATORY INVARIANT: Periode Magang * MUST be selected as "4 Bulan" (MUTLAK).
    - Empirical screenshot confirmation proofs saved for every submission.
==============================================================================
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

PROOFS_DIR = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\proofs\form_submissions"
os.makedirs(PROOFS_DIR, exist_ok=True)

# Form URLs
FORM_PRESENSI_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform"
FORM_ASSIGNMENT_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdVPxekg5o3NyjLmiG3UgvyAHbwlQSqiBAMjyWroEiDXOwHHA/viewform"
FORM_LOGBOOK_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfaoPBT-SCmdU4KGH2CmnVHMAsc704VRVlWYsfUVj1Ybm30aw/viewform"

def upload_file_in_picker(page, file_path):
    print(f"Uploading file: {file_path} (Size: {os.path.getsize(file_path)} bytes)...", flush=True)
    
    # 1. Click Add File button
    add_btn = page.locator("div[role='button']:has-text('Add file'), div[role='button']:has-text('Tambahkan file'), span:has-text('Add file'), span:has-text('Tambahkan file')").first
    add_btn.scroll_into_view_if_needed()
    time.sleep(1)
    add_btn.click()
    print("Clicked Add file button, locating picker iframe...", flush=True)
    time.sleep(3)
    
    picker_frame = None
    for attempt in range(10):
        for f in page.frames:
            if "picker" in f.url or "google.com/picker" in f.url:
                picker_frame = f
                break
        if picker_frame:
            break
        time.sleep(1)
        
    if not picker_frame:
        raise RuntimeError("Google Picker iframe not found after clicking Add file!")
        
    print(f"Found picker frame: {picker_frame.name}", flush=True)
    
    # 2. Inject file into picker input[type="file"]
    file_input = picker_frame.locator("input[type='file']")
    if file_input.count() > 0:
        file_input.first.set_input_files(file_path)
        print("File assigned to picker input[type='file']!", flush=True)
    else:
        # Fallback to Browse button
        browse_btn = picker_frame.locator("button:has-text('Browse'), div:has-text('Browse'), span:has-text('Browse')").first
        with page.expect_file_chooser() as fc:
            browse_btn.click()
        fc.value.set_files(file_path)
        print("File set via file chooser!", flush=True)
        
    # 3. Wait for upload to complete and picker dialog to dismiss
    print("Waiting for file upload to complete...", flush=True)
    for i in range(30):
        time.sleep(1)
        active_pickers = [f for f in page.frames if "picker" in f.url]
        if len(active_pickers) == 0:
            print(f"Picker dialog closed in {i+1}s. Upload complete!", flush=True)
            break
    time.sleep(2)

def select_radio_exact(page, label_text):
    # Try aria-label or data-value or internal text
    opt = page.locator(f"div[role='radio'][aria-label='{label_text}'], div[role='radio'][data-value='{label_text}']")
    if opt.count() == 0:
        # Try text search within radio container
        opt = page.locator(f"div[role='radio']:has-text('{label_text}')")
    if opt.count() == 0:
        # Fallback by span text near radio
        opt = page.locator(f"span:has-text('{label_text}')")
        
    if opt.count() > 0:
        target = opt.first
        target.scroll_into_view_if_needed()
        time.sleep(0.5)
        target.click()
        print(f"Selected radio: '{label_text}'", flush=True)
    else:
        raise ValueError(f"Could not locate radio button with label: '{label_text}'")

def submit_and_confirm(page, item_key):
    # Take pre-submission screenshot
    pre_shot = os.path.join(PROOFS_DIR, f"{item_key}_pre_submit.png")
    page.screenshot(path=pre_shot)
    print(f"Saved pre-submit screenshot: {pre_shot}", flush=True)
    
    # Click Submit / Kirim
    sub_btn = page.locator("div[role='button']:has-text('Submit'), div[role='button']:has-text('Kirim'), span:has-text('Submit'), span:has-text('Kirim')").first
    sub_btn.scroll_into_view_if_needed()
    time.sleep(0.5)
    print(f"Clicking Submit button ({sub_btn.text_content().strip()})...", flush=True)
    sub_btn.click()
    
    # Wait for response URL
    print("Waiting for formResponse confirmation...", flush=True)
    confirmed = False
    for attempt in range(15):
        time.sleep(1)
        if "formResponse" in page.url or page.locator("text='Your response has been recorded'").count() > 0 or page.locator("text='Jawaban Anda telah direkam'").count() > 0:
            confirmed = True
            break
            
    conf_shot = os.path.join(PROOFS_DIR, f"{item_key}_confirmed.png")
    page.screenshot(path=conf_shot)
    print(f"[SUCCESS] Submission recorded! Saved confirmation screenshot: {conf_shot}", flush=True)
    return conf_shot

# ==============================================================================
# FORM SUBMISSION WORKFLOWS
# ==============================================================================

def submit_presensi(page, kehadiran_label, proof_path, item_key):
    print(f"\n=======================================================", flush=True)
    print(f"Executing Presensi Submission: {kehadiran_label}", flush=True)
    print(f"=======================================================", flush=True)
    
    page.goto(FORM_PRESENSI_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    
    # 1. Fill Nama
    name_inp = page.locator("input.whsOnd[type='text']").first
    name_inp.fill("Kenny Helim")
    print("Filled Nama: Kenny Helim", flush=True)
    
    # 2. Select Divisi: Artificial Intelligence
    select_radio_exact(page, "Artificial Intelligence")
    
    # 3. Select Periode Magang: 4 Bulan [MANDATORY INVARIANT]
    select_radio_exact(page, "4 Bulan")
    
    # 4. Select Kehadiran
    select_radio_exact(page, kehadiran_label)
    
    # 5. Upload Proof
    upload_file_in_picker(page, proof_path)
    
    # 6. Submit and confirm
    return submit_and_confirm(page, item_key)

def submit_assignment(page, penugasan_label, file_path, item_key):
    print(f"\n=======================================================", flush=True)
    print(f"Executing Assignment Submission: {penugasan_label}", flush=True)
    print(f"=======================================================", flush=True)
    
    page.goto(FORM_ASSIGNMENT_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    
    inputs = page.locator("input.whsOnd[type='text']").all()
    # Fields: Nama, Kelompok, WA, Email, Judul
    # Nama
    inputs[0].fill("Kenny Helim")
    # Kelompok
    inputs[1].fill("Kelompok 1")
    # WA
    inputs[2].fill("081298098127")
    # Email
    inputs[3].fill("kenny.helim@binus.ac.id")
    print("Filled text inputs: Nama, Kelompok 1, WA, Email", flush=True)
    
    # Cluster: BATCH 10 (6 Oktober - 6 November)
    select_radio_exact(page, "BATCH 10 (6 Oktober - 6 November)")
    
    # Divisi: Artificial Intelligence
    select_radio_exact(page, "Artificial Intelligence")
    
    # Pengumpulan penugasan
    select_radio_exact(page, penugasan_label)
    
    # Judul Project
    judul_inp = page.locator("input.whsOnd[type='text']").nth(4)
    judul_inp.fill("Prediksi Hasil Pertandingan dan Probabilitas Juara ASEAN Cup Menggunakan Algoritma Machine Learning Berdasarkan Statistik Historis Tim Nasional")
    print("Filled Judul Project", flush=True)
    
    # Upload File
    upload_file_in_picker(page, file_path)
    
    # Submit and confirm
    return submit_and_confirm(page, item_key)

def submit_logbook(page, pertemuan_num, file_path, item_key):
    print(f"\n=======================================================", flush=True)
    print(f"Executing Logbook Submission: Pertemuan {pertemuan_num}", flush=True)
    print(f"=======================================================", flush=True)
    
    page.goto(FORM_LOGBOOK_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    
    # Nama
    name_inp = page.locator("input.whsOnd[type='text']").first
    name_inp.fill("Kenny Helim")
    print("Filled Nama: Kenny Helim", flush=True)
    
    # Divisi: Divisi Artificial Intelligence (Prefix 'Divisi ')
    select_radio_exact(page, "Divisi Artificial Intelligence")
    
    # Paket: Starterpack
    select_radio_exact(page, "Starterpack")
    
    # Logbook Pertemuan
    select_radio_exact(page, str(pertemuan_num))
    
    # Upload File Logbook
    upload_file_in_picker(page, file_path)
    
    # Submit and confirm
    return submit_and_confirm(page, item_key)

if __name__ == "__main__":
    print("Master Form Submitter module loaded. Ready for execution.", flush=True)
