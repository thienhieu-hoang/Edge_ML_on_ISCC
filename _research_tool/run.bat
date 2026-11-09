@echo off
chcp 65001 >nul
title Standalone Literature Review Tool
echo ======================================================================
echo   _research_tool: Standalone Literature Review & Verification
echo ======================================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check .env file
if not exist ".env" (
    if exist "..\.env" (
        echo [*] Using .env from project root.
    ) else (
        echo [!] No .env found. Creating one from .env.example...
        copy .env.example .env >nul
        notepad .env
        echo After entering your GEMINI_API_KEY, press any key to continue...
        pause >nul
    )
)

echo.
set "USER_QUERY="
set /p USER_QUERY=">> Enter your research question / hypothesis (press ENTER for interactive mode): "

echo.
if "%USER_QUERY%"=="" (
    python research_agent.py
) else (
    python research_agent.py --query "%USER_QUERY%"
)

echo.
echo ======================================================================
echo Done! Results saved to: %SCRIPT_DIR%literature\
echo ======================================================================
pause
