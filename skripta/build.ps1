# Build the study notes into a printable A4 PDF.
#
# Usage:  .\skripta\build.ps1 [-Open]
#
# Output: skripta\skripta.pdf
#
# Requires Tectonic. If it is not on PATH the script falls back to the portable
# copy in %LOCALAPPDATA%\Programs\tectonic (see skripta\README.md for install).

param([switch]$Open)

$skriptaDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$tectonic = (Get-Command tectonic -ErrorAction SilentlyContinue).Source
if (-not $tectonic) { $tectonic = "$env:LOCALAPPDATA\Programs\tectonic\tectonic.exe" }
if (-not (Test-Path $tectonic)) {
    Write-Host "Tectonic nije pronaden. Vidi skripta\README.md za instalaciju." -ForegroundColor Red
    exit 1
}

# Regenerate the figures first so the PDF never ships a stale plot.
Write-Host "--- Generiram grafove ---" -ForegroundColor Cyan
Get-ChildItem (Join-Path $skriptaDir "scripts") -Filter "fig_*.py" | ForEach-Object {
    Write-Host "  $($_.Name)" -ForegroundColor Gray
    python $_.FullName
    if ($LASTEXITCODE -ne 0) { Write-Host "  NEUSPJEH: $($_.Name)" -ForegroundColor Red; exit 1 }
}

Write-Host "--- Prevodim skriptu (A4) ---" -ForegroundColor Cyan
$buildDir = Join-Path $skriptaDir "build"
if (-not (Test-Path $buildDir)) { New-Item -ItemType Directory -Path $buildDir | Out-Null }

Push-Location $skriptaDir
& $tectonic -X compile "skripta.tex" --outdir "build" --keep-logs
$code = $LASTEXITCODE
Pop-Location

if ($code -ne 0) { Write-Host "PRIJEVOD NIJE USPIO" -ForegroundColor Red; exit 1 }

Copy-Item (Join-Path $buildDir "skripta.pdf") -Destination (Join-Path $skriptaDir "skripta.pdf") -Force

$log = Get-Content (Join-Path $buildDir "skripta.log") -Raw
if ($log -match 'Output written on[^(]+\((\d+) page') {
    Write-Host "Gotovo: skripta\skripta.pdf ($($Matches[1]) stranica, A4)" -ForegroundColor Green
} else {
    Write-Host "Gotovo: skripta\skripta.pdf" -ForegroundColor Green
}

if ($Open) { Invoke-Item (Join-Path $skriptaDir "skripta.pdf") }
