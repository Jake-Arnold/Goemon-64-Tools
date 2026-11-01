@echo off
setlocal
cd /d "%~dp0"
title Goemon Practice Toolkit v0.9.9
where py >nul 2>&1
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11 or newer from python.org.
  pause
  exit /b 1
)
py -c "import psutil" >nul 2>&1
if errorlevel 1 (
  echo Installing required Python dependency...
  py -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
  )
)
echo Goemon Practice Toolkit v0.9.9 - EXPERIMENTAL PRACTICE ONLY.
echo All experimental tools enabled. Do NOT use for submitted runs.
echo Use a disposable game save.
py -m practice.toolkit --route route.json --enable-teleport --enable-state-restore --enable-debug-menu --enable-hex-edit
if errorlevel 1 (
  echo Toolkit exited with an error.
  pause
)
endlocal
