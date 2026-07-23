# Kill previous FitGirl Downloader servers and leftover launcher CMD windows.
# Safe: never kills this PowerShell process tree (the current launcher).
$ErrorActionPreference = 'SilentlyContinue'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRootNorm = (Resolve-Path -LiteralPath $projectRoot).Path.TrimEnd('\')
$projectRootLower = $projectRootNorm.ToLowerInvariant()

$protected = New-Object 'System.Collections.Generic.HashSet[int]'
$walk = $PID
while ($walk -and $walk -gt 0) {
    [void]$protected.Add($walk)
    $cim = Get-CimInstance Win32_Process -Filter "ProcessId=$walk" -ErrorAction SilentlyContinue
    if (-not $cim -or -not $cim.ParentProcessId -or [int]$cim.ParentProcessId -eq $walk) { break }
    $walk = [int]$cim.ParentProcessId
}

function Stop-IfNotProtected([int]$procId) {
    if (-not $procId -or $procId -le 0) { return }
    if ($protected.Contains($procId)) { return }
    try { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue } catch {}
}

# 1) Free LISTENING sockets on 8000
Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-IfNotProtected ([int]$_.OwningProcess)
}
try {
    netstat -ano | Select-String ':8000\s+.*LISTENING' | ForEach-Object {
        $parts = ($_.ToString() -split '\s+') | Where-Object { $_ }
        $pidStr = $parts[-1]
        if ($pidStr -match '^\d+$') { Stop-IfNotProtected ([int]$pidStr) }
    }
} catch {}

# 2) Kill python/pythonw running THIS project's main.py
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -match '^(python|pythonw)(\.exe)?$' -and
        $_.CommandLine -and
        $_.CommandLine -match 'main\.py' -and
        (
            $_.CommandLine.ToLowerInvariant().Contains($projectRootLower) -or
            $_.CommandLine -match 'fitgirl-downloader'
        )
    } |
    ForEach-Object { Stop-IfNotProtected ([int]$_.ProcessId) }

# 3) Kill leftover CMD windows from the old Run_Downloader.bat launcher only
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -match '^cmd(\.exe)?$' -and
        $_.CommandLine -and
        $_.CommandLine -match 'Run_Downloader\.bat' -and
        (
            $_.CommandLine.ToLowerInvariant().Contains($projectRootLower) -or
            $_.CommandLine -match 'fitgirl-downloader'
        )
    } |
    ForEach-Object { Stop-IfNotProtected ([int]$_.ProcessId) }

# 4) Wait until port 8000 is free (up to ~2s)
for ($i = 0; $i -lt 20; $i++) {
    $still = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if (-not $still) { break }
    foreach ($c in $still) { Stop-IfNotProtected ([int]$c.OwningProcess) }
    Start-Sleep -Milliseconds 100
}

Start-Sleep -Milliseconds 150
