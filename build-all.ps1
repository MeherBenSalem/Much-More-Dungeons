# build-all.ps1
# Builds Much More Dungeons for all versions and collects JARs into dist/

$root  = $PSScriptRoot
$dist  = Join-Path $root "dist"

# Per-version loader configuration
$versionLoaders = [ordered]@{
    "1.20.1"  = @("fabric", "forge")
    "1.21.1"  = @("fabric", "neoforge")
    "1.21.5"  = @("fabric", "neoforge")
    "1.21.8"  = @("fabric", "neoforge")
    "1.21.11" = @("fabric", "neoforge")
    "26.1.1"  = @("fabric", "neoforge")
}

# Recreate dist folder
if (Test-Path $dist) { Remove-Item $dist -Recurse -Force }
New-Item -ItemType Directory -Path $dist | Out-Null
Write-Host "Output folder: $dist`n"

$success = @()
$failed  = @()

foreach ($ver in $versionLoaders.Keys) {
    $loaders = $versionLoaders[$ver]
    $dir = Join-Path $root $ver
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " Building $ver ($($loaders -join ', '))" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan

    # Build tasks for each loader
    $tasks = $loaders | ForEach-Object { ":${_}:build" }

    Push-Location $dir
    & .\gradlew.bat @tasks --console=plain 2>&1
    $exitCode = $LASTEXITCODE
    Pop-Location

    if ($exitCode -ne 0) {
        Write-Host "BUILD FAILED for $ver (exit $exitCode)" -ForegroundColor Red
        $failed += $ver
        continue
    }

    # Collect the remapped JARs (exclude -dev, -sources, -javadoc, -slim)
    $collected = 0
    foreach ($loader in $loaders) {
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
