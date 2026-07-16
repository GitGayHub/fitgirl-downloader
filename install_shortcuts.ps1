# Create Desktop + Start Menu shortcuts for FitGirl Downloader (this PC).
# Run: powershell -ExecutionPolicy Bypass -File .\install_shortcuts.ps1

$ErrorActionPreference = "Stop"
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$bat = Join-Path $project "Run_Downloader.bat"
$ico = Join-Path $project "assets\fitgirl-downloader.ico"

if (-not (Test-Path $bat)) { throw "Missing: $bat" }
if (-not (Test-Path $ico)) { throw "Missing icon: $ico (run assets icon generator first)" }

$desktop = [Environment]::GetFolderPath("Desktop")
$programs = [Environment]::GetFolderPath("Programs")
$folder = Join-Path $programs "FitGirl Downloader"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

$shell = New-Object -ComObject WScript.Shell
$targets = @(
    (Join-Path $desktop "FitGirl Downloader.lnk"),
    (Join-Path $programs "FitGirl Downloader.lnk"),
    (Join-Path $folder "FitGirl Downloader.lnk")
)

foreach ($path in $targets) {
    $sc = $shell.CreateShortcut($path)
    $sc.TargetPath = $bat
    $sc.WorkingDirectory = $project
    $sc.WindowStyle = 1
    $sc.Description = "FitGirl Repack Downloader — start server and open dashboard"
    $sc.IconLocation = "$ico,0"
    $sc.Save()
    Write-Host "Created: $path"
}

Write-Host ""
Write-Host "Done. Find 'FitGirl Downloader' on Desktop and in Start Menu search."
Write-Host "Tip: right-click Start Menu entry → Pin to Start / Pin to taskbar."
