import os
import sys
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = Path(r"C:\Users\Kenny\Desktop")
UPLOAD_FOLDER = DESKTOP / "BERKAS_UPLOAD_SEKARANG_KENNY"
ZIP_DESKTOP = DESKTOP / "ASEAN_CUP_AI_PREDICTION_STUDIO_KENNY.zip"
ZIP_UPLOAD = UPLOAD_FOLDER / "ASEAN_CUP_AI_PREDICTION_STUDIO_KENNY.zip"

PPTX_SRC = DESKTOP / "FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pptx"
PDF_SRC = DESKTOP / "FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pdf"
VIDEO_SRC = DESKTOP / "DEMO_STREAMLIT_APP_FULL_WALKTHROUGH.mp4"

KENNY_DIR = ROOT / "kenny_version"

def package():
    print("[*] Starting packaging pipeline for Kenny's Application Studio...")
    
    # 1. Sync updated PPTX and PDF to docs/ and root in kenny_version and export folder
    targets_pptx = [
        KENNY_DIR / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx",
        KENNY_DIR / "docs" / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx",
        DESKTOP / "KENNY_VERSION_UNTUK_GITHUB" / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx",
        DESKTOP / "KENNY_VERSION_UNTUK_GITHUB" / "docs" / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx",
        ROOT / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx",
        UPLOAD_FOLDER / "5_FINAL_PROJECT_PRESENTATION_20_SLIDES_IAN_KENNY.pptx",
    ]
    for t in targets_pptx:
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PPTX_SRC, t)
        print(f"  [+] Synced PPTX -> {t}")

    targets_pdf = [
        KENNY_DIR / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pdf",
        KENNY_DIR / "docs" / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pdf",
        DESKTOP / "KENNY_VERSION_UNTUK_GITHUB" / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pdf",
        DESKTOP / "KENNY_VERSION_UNTUK_GITHUB" / "docs" / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pdf",
        ROOT / "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pdf",
        UPLOAD_FOLDER / "5_FINAL_PROJECT_PRESENTATION_20_SLIDES_IAN_KENNY.pdf",
    ]
    for t in targets_pdf:
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PDF_SRC, t)
        print(f"  [+] Synced PDF -> {t}")

    # 2. Ensure sample match ingestion CSV exists in data/
    sample_csv_dir = KENNY_DIR / "data"
    sample_csv_dir.mkdir(parents=True, exist_ok=True)
    sample_csv_file = sample_csv_dir / "sample_aff_match_ingestion.csv"
    if not sample_csv_file.exists():
        sample_csv_file.write_text(
            "date,home_team,away_team,home_score,away_score,neutral\n"
            "2026-11-01,Indonesia,Vietnam,2,1,0\n"
            "2026-11-02,Thailand,Malaysia,3,0,0\n"
            "2026-11-03,Singapore,Myanmar,1,1,0\n"
            "2026-11-04,Cambodia,Laos,2,0,0\n",
            encoding="utf-8"
        )
        print(f"  [+] Created sample CSV for Tab 2 -> {sample_csv_file}")

    # 3. Build standalone ZIP archive
    print(f"[*] Packaging standalone ZIP archive: {ZIP_DESKTOP}...")
    
    # Files to exclude
    exclude_dirs = {".venv", "__pycache__", ".git", ".pytest_cache", ".idea", ".vscode", "chrome_debug_profile"}
    exclude_exts = {".pyc", ".tmp", ".log"}
    
    with zipfile.ZipFile(ZIP_DESKTOP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        # Include entire kenny_version tree under ASEAN_Cup_AI_Prediction_Studio_Kenny/
        prefix = "ASEAN_Cup_AI_Prediction_Studio_Kenny"
        
        for root_dir, dirs, files in os.walk(KENNY_DIR):
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
            
            for file in files:
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                file_path = Path(root_dir) / file
                rel_path = file_path.relative_to(KENNY_DIR)
                arc_name = f"{prefix}/{rel_path.as_posix()}"
                zf.write(file_path, arc_name)

        # Include root presentations & video
        zf.write(PPTX_SRC, f"{prefix}/FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pptx")
        zf.write(PDF_SRC, f"{prefix}/FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pdf")
        if VIDEO_SRC.exists():
            zf.write(VIDEO_SRC, f"{prefix}/DEMO_STREAMLIT_APP_FULL_WALKTHROUGH.mp4")

    print(f"[+] ZIP generated successfully: {ZIP_DESKTOP} ({ZIP_DESKTOP.stat().st_size:,} bytes)")
    
    # Copy to upload folder
    shutil.copy2(ZIP_DESKTOP, ZIP_UPLOAD)
    print(f"[+] Mirrored ZIP to upload folder: {ZIP_UPLOAD}")

    # 4. Verification of ZIP contents
    print("[*] Verifying ZIP integrity...")
    with zipfile.ZipFile(ZIP_DESKTOP, 'r') as zf:
        names = zf.namelist()
        total_uncompressed = sum(info.file_size for info in zf.infolist())
        print(f"  [+] Total entries in ZIP: {len(names)}")
        print(f"  [+] Total uncompressed size: {total_uncompressed:,} bytes")
        
        critical_checks = [
            f"{prefix}/app/streamlit_app.py",
            f"{prefix}/models/football_model.pkl",
            f"{prefix}/FINAL_COMBINED_PRESENTATION_IAN_AND_KENNY.pdf",
            f"{prefix}/DEMO_STREAMLIT_APP_FULL_WALKTHROUGH.mp4",
            f"{prefix}/JALANKAN_STREAMLIT_DASHBOARD_BOLA.bat",
            f"{prefix}/README.md"
        ]
        for c in critical_checks:
            assert c in names, f"Critical file missing in ZIP: {c}"
            print(f"  [+] Verified present: {c}")

    print("\n[+] 100% COMPLETE: Application Studio packaged into clean ZIP on Desktop!")

if __name__ == "__main__":
    package()
