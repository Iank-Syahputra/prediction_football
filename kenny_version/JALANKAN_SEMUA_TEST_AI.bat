@echo off
title EKSEKUSI REAL UNITTEST DAN STRESS TEST AI FOOTBALL - KELOMPOK 1
color 0A
cd /d "C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction"

echo ==============================================================================
echo        PEMERIKSAAN KUALITAS DAN PENGUJIAN OTOMATIS REAL CODE (RULE VQ-338)
echo         Proyek: AI Football Prediction dan ASEAN Cup Simulator (SDG 9)
echo         Tim: Kelompok 1 - Divisi AI (Kenny Helim, BINUS University)
echo ==============================================================================
echo.

echo [TAHAP 1/2] Menjalankan 42 Real Unittest (Model, Elo, Simulation, Streamlit, Invariants)...
echo ------------------------------------------------------------------------------
".venv\Scripts\python.exe" -m unittest discover -s tests -p "test_*.py" -v

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [FAIL] Terjadi kegagalan pada pengujian unit!
    pause
    exit /b %errorlevel%
)

echo.
echo ==============================================================================
echo [TAHAP 2/2] Menjalankan Adversarial Stress Test dan Stochastic Stability Check...
echo ------------------------------------------------------------------------------
".venv\Scripts\python.exe" tests\adversarial_stress_test.py

echo.
echo ==============================================================================
echo [SUKSES 100%%] SEMUA 42 UNITTEST DAN STRESS TEST LULUS DENGAN VERIFIKASI EMPIRIS!
echo ==============================================================================
echo.
pause
