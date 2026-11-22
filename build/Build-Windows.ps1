# Build a branded, standalone 64-bit Windows executable with Python 3.11+.
# Run from PowerShell or use Build-Windows.cmd; requires internet once for pip.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Venv = Join-Path $Root '.build-venv'
$Python = Join-Path $Venv 'Scripts\python.exe'
$Icon = Join-Path $Root 'assets\goemon_tools_logo.ico'
$Png = Join-Path $Root 'assets\goemon_tools_logo.png'
$SmallPng = Join-Path $Root 'assets\goemon_tools_logo_small.png'
$Entry = Join-Path $Root 'goemon_app.py'
$Dist = Join-Path $Root 'dist'
$Work = Join-Path $Root 'build-output'

foreach ($File in @($Icon, $Png, $SmallPng, $Entry)) {
    if (-not (Test-Path -LiteralPath $File)) { throw "Missing required file: $File" }
}
if (-not (Test-Path -LiteralPath $Python)) {
    & py -3 -m venv $Venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create Python environment. Install 64-bit Python 3.11+ and its py launcher.' }
}
& $Python -m pip install --disable-pip-version-check -r (Join-Path $Root 'requirements.txt') 'pyinstaller>=6.12,<7'
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }

Push-Location $Root
try {
    & $Python -m PyInstaller `
        --noconfirm --clean --onefile --windowed `
        --name 'GoemonSpeedrunTools' `
        --icon $Icon `
        --add-data "${Icon};assets" `
        --add-data "${Png};assets" `
        --add-data "${SmallPng};assets" `
        --collect-data practice `
        --collect-all tkinterdnd2 `
        --distpath $Dist --workpath $Work `
        --specpath $Work `
        $Entry
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed.' }
} finally {
    Pop-Location
}
$Exe = Join-Path $Dist 'GoemonSpeedrunTools.exe'
if (-not (Test-Path -LiteralPath $Exe)) { throw "Build succeeded without expected executable: $Exe" }
Write-Host "Build complete: $Exe" -ForegroundColor Green
Write-Host 'Data files go to %LOCALAPPDATA%\GoemonSpeedrunTools.'
Write-Host 'Experimental practice mode. Use a disposable game save.'
