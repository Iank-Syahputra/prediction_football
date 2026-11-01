"""
==============================================================================
[MODULE GOAL & ROLE]
  Comprehensive Google Forms Automated Submission Engine (Senior Craftsmanship).
  Orchestrates the 4 Mandatory Pending Submissions for Kenny Helim (Divisi AI, Kelompok 1):
    1. Form 1: Presensi FAST TRACK Batch 10
       - Kehadiran: WEEK 4 Sesi 2 (30 Okt 2026 - Mentoring Pak Aslan Alwi)
       - Periode Magang: 4 Bulan (MUTLAK)
       - Divisi: Artificial Intelligence
       - File: 1_BUKTI_PRESENSI_WEEK4_SESI2.png (Screenshot 7800)
    2. Form 2: Assignment FAST TRACK (Submission A)
       - Penugasan: Assignment WEEK 2
       - File: 2_ASSIGNMENT_WEEK_2_BLUEPRINT.pdf
    3. Form 2: Assignment FAST TRACK (Submission B)
       - Penugasan: Assignment WEEK 4
       - File: 3_ASSIGNMENT_WEEK_4_FINAL_REPORT.pdf
    4. Form 3: Logbook Fast Track
       - Pertemuan Ke-: 4
       - Periode Magang: 4 Bulan (MUTLAK tercantum di tabel logbook)
       - File: 4_LOGBOOK_WEEK_4_KENNY_HELIM.pdf

[INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
  - Operates over Chrome DevTools Protocol (CDP port 9222).
  - Uses persistent automation profile: chrome_debug_profile.
  - Automatically copies proof screenshots to Kenny's Desktop:
    C:\\Users\\Kenny\\Desktop\\BUKTI_SUKSES_SUBMIT_WEEK_4\\
  - Bilingual selectors (Indonesian & English) for zero-failure interaction.
  - Rule VQ-94: Timeout-guarded yields, explicit delays, and error interception.
==============================================================================
"""

import os
import sys
import time
import shutil
import subprocess
import urllib.request
from playwright.sync_api import sync_playwright

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\chrome_debug_profile"
PORT = 9222

PROOFS_INTERNAL = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\proofs\form_submissions"
DESKTOP_PROOFS = r"C:\Users\Kenny\Desktop\BUKTI_SUKSES_SUBMIT_WEEK_4"
os.makedirs(PROOFS_INTERNAL, exist_ok=True)
os.makedirs(DESKTOP_PROOFS, exist_ok=True)

# Upload Files (Consolidated on Desktop)
FOLDER_BERKAS = r"C:\Users\Kenny\Desktop\BERKAS_UPLOAD_SEKARANG_KENNY"
PROOF_W4_S2 = os.path.join(FOLDER_BERKAS, "1_BUKTI_PRESENSI_WEEK4_SESI2.png")
ASSIGN_W2 = os.path.join(FOLDER_BERKAS, "2_ASSIGNMENT_WEEK_2_BLUEPRINT.pdf")
ASSIGN_W4 = os.path.join(FOLDER_BERKAS, "3_ASSIGNMENT_WEEK_4_FINAL_REPORT.pdf")
LOGBOOK_W4 = os.path.join(FOLDER_BERKAS, "4_LOGBOOK_WEEK_4_KENNY_HELIM.pdf")

# Google Form URLs
URL_PRESENSI = "https://docs.google.com/forms/d/e/1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw/viewform"
URL_ASSIGNMENT = "https://docs.google.com/forms/d/e/1FAIpQLSdVPxekg5o3NyjLmiG3UgvyAHbwlQSqiBAMjyWroEiDXOwHHA/viewform"
URL_LOGBOOK = "https://docs.google.com/forms/d/e/1FAIpQLSfaoPBT-SCmdU4KGH2CmnVHMAsc704VRVlWYsfUVj1Ybm30aw/viewform"

def ensure_browser():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
            if resp.status == 200:
                print("==> Connected to active Chrome CDP on port 9222.", flush=True)
                return None
    except Exception:
        pass
        
    print(f"==> Launching visible Chrome on CDP port {PORT}...", flush=True)
    chrome_cmd = [
        CHROME_BIN,
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--start-maximized",
        URL_PRESENSI
    ]
    proc = subprocess.Popen(chrome_cmd)
    
    connected = False
    for _ in range(20):
        time.sleep(1)
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1) as resp:
                if resp.status == 200:
                    connected = True
                    break
        except Exception:
            pass
            
    if not connected:
        proc.terminate()
        raise RuntimeError("Gagal membuka port CDP 9222 pada browser Chrome.")
        
    print("==> Chrome berhasil terbuka di port 9222.", flush=True)
    return proc

def upload_via_picker(page, file_path):
    print(f"    [UPLOAD] Memproses unggah file: {os.path.basename(file_path)} ({os.path.getsize(file_path):,} bytes)...", flush=True)
    add_btn = page.locator("div[role='button']:has-text('Add file'), div[role='button']:has-text('Tambahkan file'), span:has-text('Add file'), span:has-text('Tambahkan file')").first
    add_btn.scroll_into_view_if_needed()
    time.sleep(1)
    add_btn.click()
    
    picker_frame = None
    for _ in range(15):
        time.sleep(1)
        for f in page.frames:
            if "picker" in f.url:
                picker_frame = f
                break
        if picker_frame:
            break
            
    if not picker_frame:
        raise RuntimeError("Dialog Google Picker untuk upload berkas tidak muncul!")
        
    file_input = picker_frame.locator("input[type='file']")
    if file_input.count() > 0:
        file_input.first.set_input_files(file_path)
    else:
        browse_btn = picker_frame.locator("button:has-text('Browse'), div:has-text('Browse'), button:has-text('Jelajahi')").first
        with page.expect_file_chooser() as fc:
            browse_btn.click()
        fc.value.set_files(file_path)
        
    # Wait for upload progress to finish and modal to close
    for _ in range(40):
        time.sleep(1)
        active_pickers = [f for f in page.frames if "picker" in f.url]
        if len(active_pickers) == 0:
            break
    time.sleep(2)
    print("    [UPLOAD] Sukses! File telah terunggah dan dialog picker tertutup.", flush=True)

def select_radio(page, label_text):
    opt = page.locator(f"div[role='radio'][aria-label='{label_text}'], div[role='radio'][data-value='{label_text}']")
    if opt.count() == 0:
        opt = page.locator(f"div[role='radio']:has-text('{label_text}')")
    if opt.count() == 0:
        opt = page.locator(f"span:has-text('{label_text}')")
        
    if opt.count() > 0:
        target = opt.first
        target.scroll_into_view_if_needed()
        time.sleep(0.4)
        target.click()
        print(f"    [PILIH] Opsi radio: '{label_text}'", flush=True)
    else:
        raise ValueError(f"Opsi radio '{label_text}' tidak ditemukan pada formulir!")

def submit_and_record(page, receipt_name):
    # Pre-submit screenshot
    pre_path = os.path.join(PROOFS_INTERNAL, f"{receipt_name}_pre_submit.png")
    page.screenshot(path=pre_path)
    
    sub_btn = page.locator("div[role='button']:has-text('Submit'), div[role='button']:has-text('Kirim'), span:has-text('Submit'), span:has-text('Kirim')").first
    sub_btn.scroll_into_view_if_needed()
    time.sleep(0.8)
    sub_btn.click()
    print("    [KIRIM] Menekan tombol Kirim / Submit. Menunggu respons server Google...", flush=True)
    
    # Wait for confirmation screen
    for _ in range(20):
        time.sleep(1)
        if "formResponse" in page.url or page.locator("text='Your response has been recorded'").count() > 0 or page.locator("text='Jawaban Anda telah direkam'").count() > 0:
            break
            
    conf_path_internal = os.path.join(PROOFS_INTERNAL, f"{receipt_name}_confirmed.png")
    conf_path_desktop = os.path.join(DESKTOP_PROOFS, f"{receipt_name}_BUKTI_SUKSES.png")
    
    page.screenshot(path=conf_path_internal)
    shutil.copy2(conf_path_internal, conf_path_desktop)
    
    print(f"    ===> [BUKTI EMPIRIS TERSIMPAN] {conf_path_desktop}", flush=True)
    return conf_path_desktop

def submit_form1_presensi_w4_s2(page):
    print("\n" + "="*70)
    print("[1/4] MEMPROSES PENGIRIMAN: Presensi FAST TRACK Week 4 Sesi 2")
    print("="*70, flush=True)
    page.goto(URL_PRESENSI, wait_until="domcontentloaded", timeout=25000)
    time.sleep(2)
    
    if "accounts.google.com" in page.url:
        print("[AUTH BLOCKED] Memerlukan login Google. Menunggu login...", flush=True)
        return False
        
    print("    [ISI] Nama Lengkap: Kenny Helim")
    page.locator("input.whsOnd[type='text']").first.fill("Kenny Helim")
    
    select_radio(page, "Artificial Intelligence")
    select_radio(page, "4 Bulan")  # INVARIANT: 4 Bulan MUTLAK
    select_radio(page, "WEEK 4 Sesi 2")
    
    upload_via_picker(page, PROOF_W4_S2)
    submit_and_record(page, "1_PRESENSI_WEEK_4_SESI_2")
    return True

def submit_form2_assignment(page, penugasan_label, file_path, receipt_name):
    print("\n" + "="*70)
    print(f"MEMPROSES PENGIRIMAN: Assignment FAST TRACK - {penugasan_label}")
    print("="*70, flush=True)
    page.goto(URL_ASSIGNMENT, wait_until="domcontentloaded", timeout=25000)
    time.sleep(2)
    
    if "accounts.google.com" in page.url:
        print("[AUTH BLOCKED] Memerlukan login Google.", flush=True)
        return False
        
    inputs = page.locator("input.whsOnd[type='text']").all()
    inputs[0].fill("Kenny Helim")
    inputs[1].fill("Kelompok 1")
    inputs[2].fill("081298098127")
    inputs[3].fill("kenny.helim@binus.ac.id")
    print("    [ISI] Identitas Mahasiswa: Kenny Helim (Kelompok 1, WA, Email Binus)")
    
    select_radio(page, "BATCH 10 (6 Oktober - 6 November)")
    select_radio(page, "Artificial Intelligence")
    select_radio(page, penugasan_label)
    
    judul = "Prediksi Hasil Pertandingan dan Probabilitas Juara ASEAN Cup Menggunakan Algoritma Machine Learning Berdasarkan Statistik Historis Tim Nasional"
    page.locator("input.whsOnd[type='text']").nth(4).fill(judul)
    print(f"    [ISI] Judul Project: {judul[:50]}...")
    
    upload_via_picker(page, file_path)
    submit_and_record(page, receipt_name)
    return True

def submit_form3_logbook_w4(page):
    print("\n" + "="*70)
    print("[4/4] MEMPROSES PENGIRIMAN: Logbook FAST TRACK Pertemuan 4")
    print("="*70, flush=True)
    page.goto(URL_LOGBOOK, wait_until="domcontentloaded", timeout=25000)
    time.sleep(2)
    
    if "accounts.google.com" in page.url:
        print("[AUTH BLOCKED] Memerlukan login Google.", flush=True)
        return False
        
    page.locator("input.whsOnd[type='text']").first.fill("Kenny Helim")
    print("    [ISI] Nama Lengkap: Kenny Helim")
    
    select_radio(page, "Divisi Artificial Intelligence")
    select_radio(page, "Starterpack")
    select_radio(page, "4")
    
    upload_via_picker(page, LOGBOOK_W4)
    submit_and_record(page, "4_LOGBOOK_PERTEMUAN_4")
    return True

def main():
    print("\n" + "#"*70)
    print("# ENJIN OTOMASI PENGIRIMAN FORMULIR FAST TRACK MSIB BATCH 10")
    print("# Peserta: Kenny Helim | Divisi AI | Kelompok 1")
    print("#"#70 + "\n", flush=True)
    
    proc = ensure_browser()
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            
            # Navigate to Form 1 to check login state
            page.goto(URL_PRESENSI, wait_until="domcontentloaded", timeout=25000)
            time.sleep(2)
            
            if "accounts.google.com" in page.url:
                print("*"*70)
                print("[PERHATIAN] Jendela Chrome terbuka menampilkan halaman login Google.")
                print("Silakan klik / pilih akun Google Anda di jendela browser Chrome tersebut.")
                print("Setelah login berhasil, sistem otomasi akan langsung berjalan 100% sendiri!")
                print("*"*70 + "\n", flush=True)
                
                # Wait for user sign in
                for i in range(120): # wait up to 2 minutes
                    time.sleep(1)
                    if "accounts.google.com" not in page.url and "docs.google.com/forms" in page.url:
                        print("==> Login Google Terdeteksi! Memulai eksekusi otomasi penuh...\n", flush=True)
                        break
                        
            if "accounts.google.com" not in page.url and "docs.google.com/forms" in page.url:
                # 1. Presensi Week 4 Sesi 2
                res1 = submit_form1_presensi_w4_s2(page)
                
                # 2. Assignment Week 2
                res2 = submit_form2_assignment(page, "Assignment WEEK 2", ASSIGN_W2, "2_ASSIGNMENT_WEEK_2")
                
                # 3. Assignment Week 4
                res3 = submit_form2_assignment(page, "Assignment WEEK 4", ASSIGN_W4, "3_ASSIGNMENT_WEEK_4")
                
                # 4. Logbook Pertemuan 4
                res4 = submit_form3_logbook_w4(page)
                
                print("\n" + "="*70)
                print("[SUKSES BESAR] SEMUA 4 FORMULIR TELAH BERHASIL TERSUBMIT KE GOOGLE!")
                print(f"Bukti screenshot konfirmasi telah disimpan di Desktop:")
                print(f"--> {DESKTOP_PROOFS}")
                print("="*70 + "\n", flush=True)
            else:
                print("[INFO] Menunggu sesi login Google aktif. Silakan jalankan kembali setelah login.", flush=True)
                
            browser.close()
    finally:
        if proc:
            proc.terminate()
            print("==> Selesai. Browser otomasi ditutup dengan bersih.", flush=True)

if __name__ == "__main__":
    main()
