# Prefer discrete NVIDIA GPU (High performance) for GPU-heavy apps on hybrid laptops.
# GpuPreference=2 => High performance (dGPU); 1 => Power saving (iGPU); 0 => Auto.
# Safe to re-run. Affects Windows Graphics settings (same as Settings > Display > Graphics).

$ErrorActionPreference = "SilentlyContinue"

$hasNvidia = $false
try {
    $gpus = @(Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name)
    $hasNvidia = ($gpus | Where-Object { $_ -match "NVIDIA|GeForce|RTX" }).Count -gt 0
    Write-Host ("GPU adapters: " + ($gpus -join " | "))
} catch {}

if (-not $hasNvidia) {
    Write-Host "GPU: No NVIDIA adapter found - skipping dGPU preference."
    exit 0
}

$regPath = "HKCU:\Software\Microsoft\DirectX\UserGpuPreferences"
if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}

function Register-GpuHighPerf([string]$exe) {
    if (-not $exe) { return $false }
    if (-not (Test-Path -LiteralPath $exe)) { return $false }
    $full = (Resolve-Path -LiteralPath $exe).Path
    New-ItemProperty -Path $regPath -Name $full -Value "GpuPreference=2;" -PropertyType String -Force | Out-Null
    Write-Host "GPU: High performance (dGPU) -> $full"
    return $true
}

$candidates = [System.Collections.Generic.List[string]]::new()

# --- Browsers ---
@(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles}\BraveSoftware\Brave-Browser\Application\brave.exe",
    "$env:LOCALAPPDATA\Programs\Zen Browser\zen.exe",
    "$env:LOCALAPPDATA\Zen\zen.exe",
    "${env:ProgramFiles}\Mozilla Firefox\firefox.exe"
) | ForEach-Object { $candidates.Add($_) }

# --- Node / Electron (Bebranoid dev + other Electron apps) ---
@(
    "${env:ProgramFiles}\nodejs\node.exe",
    "${env:ProgramFiles(x86)}\nodejs\node.exe",
    "$env:LOCALAPPDATA\Programs\node\node.exe",
    "C:\VibeCoding\Bebranoid\node_modules\electron\dist\electron.exe",
    "C:\VibeCoding\Bebranoid\dist-package\Bebranoid-win32-x64\Bebranoid.exe"
) | ForEach-Object { $candidates.Add($_) }

# --- Python (FitGirl server / tools; rarely GPU, but safe) ---
@(
    "C:\VibeCoding\fitgirl-downloader\.venv\Scripts\python.exe",
    "${env:LOCALAPPDATA}\Programs\Python\Python312\python.exe",
    "${env:ProgramFiles}\Python312\python.exe"
) | ForEach-Object { $candidates.Add($_) }

# --- Auto-discover packaged Electron apps under VibeCoding ---
$roots = @("C:\VibeCoding")
foreach ($root in $roots) {
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $proj = $_.FullName
        # electron\dist\electron.exe
        $el = Join-Path $proj "node_modules\electron\dist\electron.exe"
        if (Test-Path $el) { $candidates.Add($el) }
        # dist-package\*\*.exe (skip uninstallers)
        $pkg = Join-Path $proj "dist-package"
        if (Test-Path $pkg) {
            Get-ChildItem -Path $pkg -Recurse -Filter "*.exe" -ErrorAction SilentlyContinue |
                Where-Object {
                    $_.Name -notmatch "(?i)uninstall|setup|update|crashpad|elevate" -and
                    $_.FullName -notmatch "(?i)\\locales\\|\\swiftshader\\"
                } |
                ForEach-Object { $candidates.Add($_.FullName) }
        }
    }
}

# Deduplicate
$unique = $candidates | Where-Object { $_ } | ForEach-Object { $_.Trim() } | Select-Object -Unique

$set = 0
foreach ($exe in $unique) {
    if (Register-GpuHighPerf $exe) { $set++ }
}

# Packaged Bebranoid often also ships chrome_100_percent etc. under same folder — main exe is enough.
# Also register electron helper if present next to Bebranoid.exe
$bebraRoot = "C:\VibeCoding\Bebranoid\dist-package\Bebranoid-win32-x64"
if (Test-Path $bebraRoot) {
    Get-ChildItem $bebraRoot -Filter "*.exe" -ErrorAction SilentlyContinue | ForEach-Object {
        if (Register-GpuHighPerf $_.FullName) { $set++ }
    }
}

Write-Host ""
if ($set -eq 0) {
    Write-Host "GPU: No EXE paths registered."
} else {
    Write-Host "GPU: Registered $set path(s) for High performance NVIDIA GPU."
    Write-Host "GPU: Fully quit apps (Bebranoid / Chrome / Electron) and reopen for effect."
    Write-Host "GPU: Tip - NVIDIA Control Panel > Manage 3D Settings > Global > Preferred graphics = High-performance NVIDIA."
}

# Optional env hint for current session / launchers
[Environment]::SetEnvironmentVariable("ELECTRON_FORCE_HIGH_PERFORMANCE_GPU", "1", "User")
Write-Host "GPU: Set user env ELECTRON_FORCE_HIGH_PERFORMANCE_GPU=1"
