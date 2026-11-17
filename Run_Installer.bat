@echo off
chcp 65001 >nul
title Fallout 2 Ultimate 2026 - Master Installer
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3 installer_gui.py
) else (
    python installer_gui.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Не удалось запустить инсталлятор.
    echo Убедитесь, что Python установлен и добавлен в PATH.
    pause
)
