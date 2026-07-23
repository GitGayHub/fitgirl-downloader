# Create Desktop + Start Menu shortcuts for FitGirl Downloader (this PC).
# Points at Launch_Downloader.vbs → silent app start (no CMD windows).
# Run: powershell -ExecutionPolicy Bypass -File .\install_shortcuts.ps1

$ErrorActionPreference = "Stop"
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$vbs = Join-Path $project "Launch_Downloader.vbs"
$ps1 = Join-Path $project "Launch.ps1"
$ico = Join-Path $project "assets\fitgirl-downloader.ico"

if (-not (Test-Path $vbs)) { throw "Missing: $vbs" }
if (-not (Test-Path $ps1)) { throw "Missing: $ps1" }
if (-not (Test-Path $ico)) { throw "Missing icon: $ico" }

$desktop = [Environment]::GetFolderPath("Desktop")
$programs = [Environment]::GetFolderPath("Programs")
$folder = Join-Path $programs "FitGirl Downloader"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

$shell = New-Object -ComObject WScript.Shell
$targets = @(
    (Join-Path $desktop "FitGirl Downloader.lnk"),
    (Join-Path $programs "FitGirl Downloader.lnk"),
    (Join-Path $folder "FitGirl Downloader.lnk"),
    (Join-Path $project "FitGirl Downloader.lnk")
)

foreach ($path in $targets) {
    $sc = $shell.CreateShortcut($path)
    # VBS wrapper = no console flash; wscript.exe is the host
    $sc.TargetPath = $vbs
    $sc.WorkingDirectory = $project
    $sc.WindowStyle = 7  # minimized host if anything flashes
    $sc.Description = "FitGirl Repack Downloader - silent start, open dashboard"
    $sc.IconLocation = "$ico,0"
    $sc.Save()
    Write-Host "Created: $path"
}

Write-Host ""
Write-Host "Done. Find 'FitGirl Downloader' on Desktop and in Start Menu."
Write-Host "Launch is silent: no CMD pile. Re-open just focuses the web UI if already running."
