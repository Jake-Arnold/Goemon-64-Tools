@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-Windows.ps1"
if errorlevel 1 (
  echo.
  echo Build failed. See the error above.
  pause
  exit /b 1
)
echo.
echo Standalone executable built under dist\GoemonSpeedrunTools.exe
pause
