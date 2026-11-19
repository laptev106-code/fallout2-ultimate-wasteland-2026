@echo off
chcp 65001 >nul
title Fallout 2 Next-Gen Launcher
cd /d "%~dp0\launcher_nextgen"

where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3 main.py
) else (
    python main.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Не удалось запустить лаунчер.
    pause
)
