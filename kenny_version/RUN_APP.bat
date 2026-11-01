@echo off
title AI Football Prediction & ASEAN Cup Studio - Kelompok 1 (SDG 9)
cd /d "%~dp0"

echo ==============================================================================
echo [STARTING] AI Football Prediction & ASEAN Cup Simulator
echo Kelompok 1 - Divisi AI (SDG 9)
echo Kenny Helim, Arya Wicaksana, M. Ihram, Gisela Venska, Christian
echo ==============================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment .venv not found!
    pause
    exit /b 1
)

echo [1/2] Opening browser at http://localhost:38800 ...
start "" "http://localhost:38800"

echo [2/2] Launching Flask Web Server...
".venv\Scripts\python.exe" app\server.py

pause
