# Kill previous FitGirl Downloader servers without killing THIS launch chain.
$ErrorActionPreference = 'SilentlyContinue'

# Who called us? Never kill this process tree (parent cmd running Run_Downloader.bat)
$protected = New-Object 'System.Collections.Generic.HashSet[int]'
$walk = $PID
while ($walk -and $walk -gt 0) {
    [void]$protected.Add($walk)
    $p = Get-CimInstance Win32_Process -Filter "ProcessId=$walk" -ErrorAction SilentlyContinue
    if (-not $p -or -not $p.ParentProcessId -or $p.ParentProcessId -eq $walk) { break }
    $walk = [int]$p.ParentProcessId
}

function Stop-IfNotProtected([int]$procId) {
    if (-not $procId) { return }
    if ($protected.Contains($procId)) { return }
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
}

# 1) Free port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-IfNotProtected $_.OwningProcess
}

# 2) Old python main.py instances (previous servers)
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -match '^(python|pythonw)\.exe$' -and
    $_.CommandLine -and
    ($_.CommandLine -match 'main\.py')
} | ForEach-Object {
    Stop-IfNotProtected $_.ProcessId
}

# 3) Orphan CMD windows from PREVIOUS FitGirl launches only
#    (exclude our protected tree; match title-ish command lines of old bats)
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -eq 'cmd.exe' -and
    $_.CommandLine -and
    ($_.CommandLine -match 'Run_Downloader\.bat|FitGirl Repack Downloader')
} | ForEach-Object {
    Stop-IfNotProtected $_.ProcessId
}

Start-Sleep -Milliseconds 500
