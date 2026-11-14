@echo off
cd /d "%~dp0"
title CyberSnake: Neon Blitz

echo ==============================================
echo        CYBERSNAKE: NEON BLITZ
echo ==============================================
echo Launching game...

:: Try Python directly
python main.py
if %ERRORLEVEL% EQU 0 goto :eof

:: Try Windows Python launcher
py -3 main.py
if %ERRORLEVEL% EQU 0 goto :eof

:: Try detected user Python install path
if exist "%LOCALAPPDATA%\Python\pythoncore-3.15-64\python.exe" (
    "%LOCALAPPDATA%\Python\pythoncore-3.15-64\python.exe" main.py
    if %ERRORLEVEL% EQU 0 goto :eof
)

echo.
echo [ERROR] Could not start the game.
echo Please ensure Python 3 is installed and added to your PATH.
echo.
pause
