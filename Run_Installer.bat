@echo off
chcp 65001 >nul
title Fallout 2 Ultimate 2026 - Master Installer
cd /d "%~dp0"
python installer_gui.py
if errorlevel 1 (
    echo.
    echo [ERROR] Не удалось запустить инсталлятор через Python.
    pause
)
