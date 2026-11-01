"""
Adversarial Compliance and Invariant Test Suite.
Author: Challenger 2 (Data Invariant & Compliance Challenger)
Validates:
1. Invariant & Metadata ("Periode Magang: 4 Bulan (MUTLAK)", UN SDG 9 alignment).
2. Presentation Deck Rigor (11 slides, no blank textboxes, Slides 5/6/7/10 content).
3. Attendance and Deliverable Evidence (Screenshot (7800).png, 6 proofs, 3 assignments, 1 logbook).
4. Rule VQ-472 Compliance (Zero lingering tasks).
"""

import os
import unittest
from PIL import Image
from pptx import Presentation

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestInstitutionalComplianceAndInvariants(unittest.TestCase):

    def test_01_screenshot_7800_integrity(self):
        """Verify Screenshot (7800).png exists, dimensions 1920x1080, genuine mentoring proof."""
        screenshot_path = r"C:\Users\Kenny\Downloads\Screenshot (7800).png"
        self.assertTrue(os.path.exists(screenshot_path), "Screenshot (7800).png does not exist in Downloads.")
        with Image.open(screenshot_path) as im:
            self.assertEqual(im.size, (1920, 1080), f"Expected (1920, 1080), got {im.size}")
            self.assertEqual(im.format, "PNG", "Expected PNG format")

    def test_02_all_6_attendance_proofs_exist(self):
        """Verify all 6 required attendance proof screenshots exist on disk."""
        proof_files = [
            os.path.join(PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_3", "Bukti_Presensi_Senin_12_Okt_2026.png"),
            os.path.join(PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_3", "Bukti_Presensi_Jumat_16_Okt_2026.png"),
            os.path.join(PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_3", "Bukti_Presensi_Senin_19_Okt_2026.png"),
            os.path.join(PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_3", "Bukti_Presensi_Jumat_23_Okt_2026.png"),
            os.path.join(PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_3", "Bukti_Presensi_Real_Zoom_Senin_26_Okt_2026_1947.png"),
            r"C:\Users\Kenny\Downloads\Screenshot (7800).png",
        ]
        for pf in proof_files:
            self.assertTrue(os.path.exists(pf), f"Attendance proof missing: {pf}")
            with Image.open(pf) as im:
                self.assertGreater(im.size[0], 0)
                self.assertGreater(im.size[1], 0)

    def test_03_all_3_assignment_pdfs_exist(self):
        """Verify all 3 assignment PDFs exist on disk."""
        assignments = [
            r"C:\Users\Kenny\Downloads\AI_Football_Prediction_Blueprint_compressed - Muh ihram Syahputra (2).pdf",
            os.path.join(PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_3", "Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pdf"),
            r"C:\Users\Kenny\Desktop\DESKTOP_ORGANIZED_HUB\06_Folders_And_Packages\Divisi Artificial Intelligence Starterpack kelompok 1\FINAL_PROJECT_WEEK_4_JUMAT\FINAL_PROJECT_REPORT_KELOMPOK_1_AI.pdf",
        ]
        for af in assignments:
            self.assertTrue(os.path.exists(af), f"Assignment PDF missing: {af}")
            self.assertGreater(os.path.getsize(af), 1000, f"Assignment PDF file size too small: {af}")

    def test_04_week4_logbook_pdf_exists(self):
        """Verify Week 4 Logbook PDF exists on disk."""
        logbook_path = os.path.join(
            PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_4",
            "LOGBOOK (Minggu 4) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf"
        )
        self.assertTrue(os.path.exists(logbook_path), "Week 4 Logbook PDF missing.")
        self.assertGreater(os.path.getsize(logbook_path), 1000)

    def test_05_pptx_deck_rigor(self):
        """Verify PPTX deck has exactly 11 slides with rich content and specific requirements."""
        pptx_path = os.path.join(PROJECT_ROOT, "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx")
        self.assertTrue(os.path.exists(pptx_path), "Presentation PPTX not found.")
        prs = Presentation(pptx_path)
        self.assertEqual(len(prs.slides), 11, f"Expected exactly 11 slides, got {len(prs.slides)}")

        # Collect text per slide
        slide_texts = []
        for idx, slide in enumerate(prs.slides):
            texts = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    t = shape.text_frame.text.strip()
                    if t:
                        texts.append(t)
            combined = "\n".join(texts)
            slide_texts.append(combined)
            self.assertGreater(len(combined), 100, f"Slide {idx+1} has insufficient text content ({len(combined)} chars)")

        # Slide 1: Must contain 4 Bulan (MUTLAK)
        self.assertIn("4 Bulan MUTLAK", slide_texts[0], "Slide 1 missing '4 Bulan MUTLAK'")

        # Slide 5: Must contrast Tabular Forecasting vs YOLO11 Road Damage
        s5 = slide_texts[4].lower()
        self.assertTrue("yolo11" in s5 and "road damage" in s5, "Slide 5 does not contrast Tabular with YOLO11 Road Damage")

        # Slide 6: Must document Log Loss 0.5966 (<= 0.8198) on 52 AFF matches
        s6 = slide_texts[5]
        self.assertIn("0.5966", s6, "Slide 6 missing Log Loss 0.5966")
        self.assertIn("0.8198", s6, "Slide 6 missing threshold 0.8198")
        self.assertIn("52", s6, "Slide 6 missing 52 AFF matches")

        # Slide 7: Must document Monte Carlo probabilities
        s7 = slide_texts[6]
        self.assertIn("31.26%", s7, "Slide 7 missing Thailand 31.26%")
        self.assertIn("27.99%", s7, "Slide 7 missing Indonesia 27.99%")
        self.assertIn("22.79%", s7, "Slide 7 missing Vietnam 22.79%")
        self.assertIn("15.08%", s7, "Slide 7 missing Malaysia 15.08%")

        # Slide 10: Must provide actionable counter-strategies for underdogs
        s10 = slide_texts[9].lower()
        self.assertTrue("underdog" in s10 or "kuda hitam" in s10, "Slide 10 missing underdog counter-strategies")

    def test_06_defense_script_invariants(self):
        """Verify docs/DEFENSE_PRESENTATION_SCRIPT.md maintains invariants and active SDG 9 explanation."""
        script_path = os.path.join(PROJECT_ROOT, "docs", "DEFENSE_PRESENTATION_SCRIPT.md")
        self.assertTrue(os.path.exists(script_path))
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("4 Bulan MUTLAK", content)
        self.assertIn("SDG 9", content)
        self.assertIn("Infrastruktur Komputasi Terbuka", content)
        self.assertIn("Inovasi Riset Berbasis Bukti", content)

    def test_07_form_submission_scripts_invariants(self):
        """Verify form submission scripts explicitly select '4 Bulan'."""
        submit_script = os.path.join(PROJECT_ROOT, "scripts", "master_form_submitter.py")
        self.assertTrue(os.path.exists(submit_script))
        with open(submit_script, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('"4 Bulan"', content)

    def test_08_logbook_week4_pdf_and_docx_contains_periode_magang_invariant(self):
        """Verify Week 4 Logbook DOCX and PDF contain 'Periode Magang: 4 Bulan (MUTLAK)'."""
        import docx
        from pypdf import PdfReader
        
        # Check DOCX
        docx_path = os.path.join(
            PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_4",
            "Logbook_Minggu_4_Kenny_Helim_AI.docx"
        )
        self.assertTrue(os.path.exists(docx_path), "Week 4 Logbook DOCX missing.")
        doc = docx.Document(docx_path)
        docx_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
        self.assertIn("periode magang", docx_text.lower(), "DOCX missing 'Periode Magang'")
        self.assertIn("4 bulan (mutlak)", docx_text.lower(), "DOCX missing '4 Bulan (MUTLAK)'")

        # Check PDF
        pdf_path = os.path.join(
            PROJECT_ROOT, "UPLOAD_BERKAS_FORM_MINGGU_4",
            "LOGBOOK (Minggu 4) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf"
        )
        self.assertTrue(os.path.exists(pdf_path), "Week 4 Logbook PDF missing.")
        reader = PdfReader(pdf_path)
        pdf_text = " ".join([page.extract_text() for page in reader.pages])
        self.assertIn("periode magang", pdf_text.lower(), "PDF missing 'Periode Magang'")
        self.assertIn("4 bulan (mutlak)", pdf_text.lower(), "PDF missing '4 Bulan (MUTLAK)'")

    def test_09_streamlit_app_contains_periode_magang_invariant(self):
        """Verify app/streamlit_app.py explicitly displays 'Periode Magang: 4 Bulan (MUTLAK)'."""
        app_path = os.path.join(PROJECT_ROOT, "app", "streamlit_app.py")
        self.assertTrue(os.path.exists(app_path))
        with open(app_path, "r", encoding="utf-8") as f:
            app_content = f.read()
        self.assertIn("Periode Magang:</b> 4 Bulan (MUTLAK)", app_content, "Streamlit header missing Periode Magang")
        self.assertIn("**Periode Magang:** 4 Bulan (MUTLAK)", app_content, "Streamlit sidebar missing Periode Magang")

    def test_10_starterpack_mirror_logbook_contains_invariant(self):
        """Verify starterpack mirror files contain '4 Bulan (MUTLAK)'."""
        import docx
        from pypdf import PdfReader
        
        mirror_dir = r"C:\Users\Kenny\Desktop\DESKTOP_ORGANIZED_HUB\06_Folders_And_Packages\Divisi Artificial Intelligence Starterpack kelompok 1"
        if os.path.exists(mirror_dir):
            docx_mirror = os.path.join(mirror_dir, "Logbook_Minggu_4_Kenny_Helim_AI.docx")
            pdf_mirror = os.path.join(mirror_dir, "LOGBOOK (Minggu 4) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf")
            self.assertTrue(os.path.exists(docx_mirror), "Mirror DOCX missing")
            self.assertTrue(os.path.exists(pdf_mirror), "Mirror PDF missing")
            
            doc = docx.Document(docx_mirror)
            docx_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
            self.assertIn("4 bulan (mutlak)", docx_text.lower())
            
            reader = PdfReader(pdf_mirror)
            pdf_text = " ".join([page.extract_text() for page in reader.pages])
            self.assertIn("4 bulan (mutlak)", pdf_text.lower())


if __name__ == "__main__":
    unittest.main()
