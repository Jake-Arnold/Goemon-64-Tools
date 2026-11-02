@echo off
setlocal
cd /d "%~dp0"
title Goemon Practice Toolkit v0.11.6
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
echo Goemon Practice Toolkit v0.11.6 - EXPERIMENTAL PRACTICE ONLY.
echo Unsafe tools enabled by default. Use --read-only to disable game writes and input.
echo Use a disposable game save.
py -m practice.toolkit --route route.json %*
if errorlevel 1 (
  echo Toolkit exited with an error.
  pause
)
endlocal
