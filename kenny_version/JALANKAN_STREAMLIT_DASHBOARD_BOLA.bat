@echo off
title Streamlit Dashboard Interaktif - AI Football Prediction & ASEAN Cup
color 0B
cd /d "C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction"

echo ==============================================================================
echo        MELUNCURKAN STREAMLIT INTERACTIVE WEB DASHBOARD (5 TABS)
echo         Proyek: AI Football Prediction & ASEAN Cup Simulator (SDG 9)
echo         Peserta: Kenny Helim (BINUS University) | Kelompok 1 (AI)
echo         Periode Magang: 4 Bulan (MUTLAK)
echo ==============================================================================
echo.
echo [1/2] Membuka browser pada http://localhost:8501 ...
start "" "http://localhost:8501"

echo [2/2] Memulai server Streamlit pada port 8501...
".venv\Scripts\streamlit.exe" run app\streamlit_app.py --server.port 8501 --browser.gatherUsageStats false

pause

