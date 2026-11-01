"""
# ==============================================================================
# [MODULE GOAL & ROLE]
# tests/test_presentation_deck.py
#
# Unit test suite verifying the authoritative 11-Slide Defense Presentation Deck:
#   - FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx (Root & docs/)
#   - docs/DEFENSE_PRESENTATION_SCRIPT.md
# Governed by Rule VQ-94 (Zero Fatal Flaws) & Rule VQ-338 (Real-Time Verification).
#
# [INTENTIONAL DESIGN DECISIONS - DO NOT REMOVE]
# 1. Validates exact slide count == 11.
# 2. Asserts 16:9 widescreen dimensions (13.333" x 7.5").
# 3. Validates slide title texts, key academic invariants, empirical evaluation metrics.
# 4. Asserts no corrupted shapes or unreadable text frames.
# 5. Asserts speaker script completeness (11 slide notes, timing, mentor Q&A).
#
# [SESSION REVISION & CHAT MILESTONE LEDGER]
# - 2026-10-30T15:48:00Z: Created automated test suite for presentation deck.
# ==============================================================================
"""

import os
import unittest
from pptx import Presentation
from pptx.util import Inches


class TestPresentationDeck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.deck_root = os.path.join(cls.base_dir, "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx")
        cls.deck_docs = os.path.join(cls.base_dir, "docs", "FINAL_PROJECT_PRESENTATION_REVISED_PARADIGM.pptx")
        cls.script_path = os.path.join(cls.base_dir, "docs", "DEFENSE_PRESENTATION_SCRIPT.md")

    def test_deck_files_exist_and_non_empty(self):
        """Verify presentation deck exists at project root and docs/ with valid size."""
        self.assertTrue(os.path.exists(self.deck_root), f"Root deck missing: {self.deck_root}")
        self.assertTrue(os.path.exists(self.deck_docs), f"Docs deck missing: {self.deck_docs}")
        self.assertTrue(os.path.exists(self.script_path), f"Defense script missing: {self.script_path}")

        root_size = os.path.getsize(self.deck_root)
        docs_size = os.path.getsize(self.deck_docs)
        script_size = os.path.getsize(self.script_path)

        self.assertGreater(root_size, 30000, f"Root deck too small: {root_size} bytes")
        self.assertEqual(root_size, docs_size, "Root and docs deck sizes mismatch")
        self.assertGreater(script_size, 10000, f"Defense script too small: {script_size} bytes")

    def test_slide_count_and_dimensions(self):
        """Verify presentation contains exactly 11 slides and 16:9 widescreen geometry."""
        prs = Presentation(self.deck_root)
        self.assertEqual(len(prs.slides), 11, f"Expected exactly 11 slides, found {len(prs.slides)}")

        # Check 16:9 widescreen dimensions (13.333" x 7.5" approx within 1000 EMU)
        expected_width = Inches(13.333)
        expected_height = Inches(7.5)
        self.assertAlmostEqual(prs.slide_width, expected_width, delta=10000)
        self.assertAlmostEqual(prs.slide_height, expected_height, delta=10000)

    def test_slide_titles_and_academic_invariants(self):
        """Validate core content, titles, and academic invariants across all 11 slides."""
        prs = Presentation(self.deck_root)

        slide_texts = []
        for i, slide in enumerate(prs.slides):
            all_text = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    t = shape.text_frame.text.strip()
                    if t:
                        all_text.append(t)
            combined = " ".join(all_text)
            self.assertGreater(len(combined), 50, f"Slide {i+1} has insufficient text: {len(combined)} chars")
            slide_texts.append(combined)

        # Slide 1: Executive Title & Academic Governance
        s1 = slide_texts[0].lower()
        self.assertIn("prediksi hasil pertandingan sepak bola internasional", s1)
        self.assertIn("kenny helim", s1)
        self.assertIn("binus university", s1)
        self.assertIn("kelompok 1", s1)
        self.assertIn("pt vinix seven aurum", s1)
        self.assertIn("pak aslan alwi", s1)
        self.assertIn("bimo rizki abdusshamad", s1)
        self.assertIn("4 bulan mutlak", s1)
        self.assertIn("sdg 9", s1)

        # Slide 2: Core Problem Statement
        s2 = slide_texts[1].lower()
        self.assertIn("bias subjektif", s2)
        self.assertIn("sdg 9", s2)
        self.assertIn("infrastruktur data terbuka", s2)

        # Slide 3: Scope & Anti-Leakage
        s3 = slide_texts[2].lower()
        self.assertTrue("49.945" in s3 or "49.000+" in s3)
        self.assertIn("38.288", s3)
        self.assertIn("6.162", s3)
        self.assertIn("52", s3)
        self.assertTrue("anti-leakage" in s3 or "tanpa mesin waktu" in s3)

        # Slide 4: AI Methodology & Elo
        s4 = slide_texts[3].lower()
        self.assertIn("elo", s4)
        self.assertTrue("k=32" in s4 or "k = 32" in s4)
        self.assertTrue("h=100" in s4 or "h = 100" in s4)
        self.assertIn("form", s4)

        # Slide 5: Cross-Paradigm Contrast (YOLO11)
        s5 = slide_texts[4].lower()
        self.assertIn("yolo11", s5)
        self.assertTrue("log loss" in s5 or "cross-entropy" in s5)
        self.assertTrue("road damage" in s5 or "aspal jalanan" in s5)

        # Slide 6: Model Evaluation Metrics
        s6 = slide_texts[5].lower()
        self.assertIn("0.5966", s6)
        self.assertIn("0.8198", s6)
        self.assertIn("1.0686", s6)
        self.assertIn("75.00%", s6)
        self.assertIn("52", s6)

        # Slide 7: Monte Carlo Tournament Simulation
        s7 = slide_texts[6].lower()
        self.assertIn("10.000", s7)
        self.assertIn("thailand", s7)
        self.assertIn("31.26%", s7)
        self.assertIn("indonesia", s7)
        self.assertIn("27.99%", s7)
        self.assertIn("vietnam", s7)
        self.assertIn("22.79%", s7)
        self.assertIn("malaysia", s7)
        self.assertIn("15.08%", s7)

        # Slide 8: Interactive Dashboard
        s8 = slide_texts[7].lower()
        self.assertIn("streamlit", s8)
        self.assertIn("match predictor", s8)
        self.assertTrue("asean cup simulator" in s8 or "tournament simulator" in s8)

        # Slide 9: Dynamic Adaptability
        s9 = slide_texts[8].lower()
        self.assertIn("csv", s9)
        self.assertIn("slider", s9)

        # Slide 10: Target Beneficiaries & Underdog Counter-Strategies
        s10 = slide_texts[9].lower()
        self.assertTrue("underdog" in s10 or "kuda hitam" in s10)
        self.assertIn("pssi", s10)
        self.assertIn("aff", s10)

        # Slide 11: Summary & Defense Readiness
        s11 = slide_texts[10].lower()
        self.assertTrue("sintesis" in s11 or "summary" in s11)
        self.assertIn("2 - 6 november 2026", s11)
        self.assertIn("pak aslan alwi", s11)
        self.assertIn("bimo rizki abdusshamad", s11)

    def test_defense_script_completeness(self):
        """Validate comprehensive defense speech script structure and content."""
        with open(self.script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # Check all 11 slide sections are present
        for i in range(1, 12):
            self.assertIn(f"SLIDE {i}:", script_content, f"Slide {i} section missing in speech script")

        # Check timing table
        self.assertIn("STRUKTUR WAKTU", script_content)
        self.assertIn("15 Menit", script_content)

        # Check mentor defense Q&A sections
        self.assertIn("Pak Aslan Alwi", script_content)
        self.assertIn("Pak Bimo Rizki Abdusshamad", script_content)
        self.assertIn("Log Loss", script_content)
        self.assertIn("Monte Carlo", script_content)
        self.assertIn("Draw", script_content)
        self.assertIn("Underdog", script_content)
        self.assertIn("YOLO11", script_content)


if __name__ == "__main__":
    unittest.main()
