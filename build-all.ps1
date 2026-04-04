# build-all.ps1
# Builds Much More Dungeons for all versions and collects JARs into dist/

$root  = $PSScriptRoot
$dist  = Join-Path $root "dist"
$versions = @("1.21.8", "1.21.11", "26.1.1")

# Recreate dist folder
if (Test-Path $dist) { Remove-Item $dist -Recurse -Force }
New-Item -ItemType Directory -Path $dist | Out-Null
Write-Host "Output folder: $dist`n"

$success = @()
$failed  = @()

foreach ($ver in $versions) {
    $dir = Join-Path $root $ver
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " Building $ver" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan

    Push-Location $dir
    & .\gradlew.bat :fabric:build :neoforge:build --console=plain 2>&1
    $exitCode = $LASTEXITCODE
    Pop-Location

    if ($exitCode -ne 0) {
        Write-Host "BUILD FAILED for $ver (exit $exitCode)" -ForegroundColor Red
        $failed += $ver
        continue
    }

    # Collect the remapped JARs (exclude -dev, -sources, -javadoc)
    $collected = 0
    foreach ($loader in @("fabric", "neoforge")) {
        $libDir = Join-Path $dir "$loader\build\libs"
        if (-not (Test-Path $libDir)) { continue }
        Get-ChildItem $libDir -Filter "*.jar" |
            Where-Object { $_.Name -notmatch "-dev|-sources|-javadoc|-slim" } |
            ForEach-Object {
                Copy-Item $_.FullName (Join-Path $dist $_.Name) -Force
                Write-Host "  Collected: $($_.Name)" -ForegroundColor Green
                $collected++
            }
    }
    Write-Host "  ${ver}: $collected JAR(s) collected`n"
    $success += $ver
}

Write-Host "========================================"
Write-Host "Build summary"
Write-Host "========================================"
foreach ($v in $success) { Write-Host "  [OK]   $v" -ForegroundColor Green }
foreach ($v in $failed)  { Write-Host "  [FAIL] $v" -ForegroundColor Red }
Write-Host ""
Write-Host "All JARs in: $dist"
Get-ChildItem $dist | Select-Object -ExpandProperty Name | ForEach-Object { Write-Host "  $_" }
