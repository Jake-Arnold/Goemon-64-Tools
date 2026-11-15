# Run the Japanese Toolkit and USA regression suites on native Windows PowerShell.
# Equivalent to scripts/test_japan_party.sh; no Bash, WSL or Xvfb required.
# Synthetic RAM tests do not attach to or write a running emulator.
# Usage: .\scripts\test_japan_party.ps1
#        .\scripts\test_japan_party.ps1 -PythonCommand python
[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string]$PythonCommand
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

# Prefer the Windows Python launcher, but support a conventional python on PATH.
if (-not $PythonCommand) {
    if (Get-Command 'py' -ErrorAction SilentlyContinue) {
        $PythonCommand = 'py'
    } elseif (Get-Command 'python' -ErrorAction SilentlyContinue) {
        $PythonCommand = 'python'
    } else {
        throw 'Python not found. Install Python 3 with Tkinter and add py.exe or python.exe to PATH.'
    }
}

$pythonArgs = @()
if ([IO.Path]::GetFileName($PythonCommand) -in @('py', 'py.exe')) {
    $pythonArgs = @('-3')
}

function Invoke-PythonTest {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    & $PythonCommand @pythonArgs @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python test step failed with exit code $LASTEXITCODE : $($Arguments -join ' ')"
    }
}

$backendTests = @(
    'tests.test_japanese_fields',
    'tests.test_japanese_scene_probes',
    'tests.test_japanese_party_unlock',
    'tests.test_japanese_position',
    'tests.test_japanese_debug_warp',
    'tests.test_japan_debug_menu_controller',
    'tests.test_japan_position_controller',
    'tests.test_japan_party_cli',
    'tests.test_japan_party_controller',
    'tests.test_japanese_mupen_attach',
    'tests.test_japan_project64',
    'tests.test_remembered_rom',
    'tests.test_region_views',
    'tests.test_region_unlocks',
    'tests.test_rom_layout_audit',
    'tests.test_rom_context_audit',
    'tests.test_japan_live_memory_edit',
    'tests.test_japan_event_sessions',
    'tests.test_japan_damage_capture',
    'tests.test_japan_native_scene_warp',
    'tests.test_japan_direct_scene_reload',
    'tests.test_japan_native_scene_controller',
    'tests.test_japan_state_comparison',
    'tests.test_japan_player_position_research',
    'tests.test_value_search',
    'tests.test_state_discovery'
)
$guiTests = @(
    'tests.test_japanese_fields_ui',
    'tests.test_japanese_scene_probe_ui',
    'tests.test_japanese_party_controls_ui',
    'tests.test_japanese_position_ui',
    'tests.test_japanese_debug_ui',
    'tests.test_japan_event_sessions_ui',
    'tests.test_japan_readonly_parity',
    'tests.test_japan_state_comparison_ui',
    'tests.test_value_search_ui',
    'tests.test_state_discovery_ui',
    'tests.test_region_unlocks_ui',
    'tests.test_dashboard'
)

Push-Location -LiteralPath $repoRoot
try {
    Write-Host 'Checking Python syntax...'
    Invoke-PythonTest -Arguments @('-m', 'compileall', '-q', 'practice')

    Write-Host 'Running read-only and synthetic memory tests...'
    Invoke-PythonTest -Arguments (@('-m', 'unittest') + $backendTests + @('-v'))

    if ($env:GOEMON_USA_DECOMPRESSED -and $env:GOEMON_JAPAN_DECOMPRESSED) {
        Write-Host 'Running optional exact-ROM MIPS cross-region reference audit...'
        Invoke-PythonTest -Arguments @('-m', 'practice.rom_layout_audit', '--usa',
            $env:GOEMON_USA_DECOMPRESSED, '--japan',
            $env:GOEMON_JAPAN_DECOMPRESSED, '--summary')
        if ($env:GOEMON_ROM_CONTEXT_AUDIT -eq '1') {
            Invoke-PythonTest -Arguments @('-m', 'practice.rom_context_audit', '--usa',
                $env:GOEMON_USA_DECOMPRESSED, '--japan',
                $env:GOEMON_JAPAN_DECOMPRESSED, '--summary')
        }
    }

    Write-Host 'Running native Windows Tk GUI tests (desktop session required)...'
    Invoke-PythonTest -Arguments (@('-m', 'unittest') + $guiTests + @('-v'))

    Write-Host 'Japanese/USA parity regression suite passed.'
} finally {
    Pop-Location
}
