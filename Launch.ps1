# FitGirl Downloader — silent app launcher (no CMD window).
# - Single instance: if server already healthy → just open browser
# - Mutex: double-click won't spawn two servers
# - Else kill leftovers, start pythonw hidden, open UI when ready
$ErrorActionPreference = 'SilentlyContinue'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

$Url = 'http://127.0.0.1:8000/'
$Pythonw = Join-Path $ProjectRoot '.venv\Scripts\pythonw.exe'
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$MainPy = Join-Path $ProjectRoot 'main.py'
$KillScript = Join-Path $ProjectRoot 'kill_old_servers.ps1'
$PidFile = Join-Path $ProjectRoot '.server.pid'

function Test-ServerReady {
    try {
        $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 1
        return ($r.StatusCode -eq 200)
    } catch {
        return $false
    }
}

function Open-AppUi {
    try { Start-Process $Url | Out-Null } catch {
        try { Start-Process 'cmd.exe' -ArgumentList '/c','start','',$Url -WindowStyle Hidden | Out-Null } catch {}
    }
}

function Show-Error([string]$msg) {
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
        [System.Windows.Forms.MessageBox]::Show($msg, 'FitGirl Downloader', 'OK', 'Error') | Out-Null
    } catch {}
}

# Already running cleanly? Just open the dashboard (no new process / no CMD).
if (Test-ServerReady) {
    Open-AppUi
    exit 0
}

# Prevent double-click race: only one launcher may start the server
$mutex = $null
$owned = $false
try {
    $mutex = [System.Threading.Mutex]::new($false, 'Local\FitGirlDownloader.Launch.v1')
    $owned = $mutex.WaitOne(10000)
} catch {
    $owned = $false
}

if (-not $owned) {
    # Another launcher is starting the server - wait for it
    for ($i = 0; $i -lt 60; $i++) {
        if (Test-ServerReady) { Open-AppUi; exit 0 }
        Start-Sleep -Milliseconds 200
    }
    Show-Error "Server is starting slowly or failed. Try again."
    exit 1
}

try {
    # Re-check after mutex (other launcher may have finished)
    if (Test-ServerReady) {
        Open-AppUi
        exit 0
    }

    # Wipe zombies / previous CMD piles / dead python on 8000
    # Dot-source so $PID tree (this launcher) is protected by kill_old_servers.ps1
    if (Test-Path -LiteralPath $KillScript) {
        . $KillScript
    } else {
        Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
            ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    }

    Start-Sleep -Milliseconds 250

    if (Test-ServerReady) {
        Open-AppUi
        exit 0
    }

    if (-not (Test-Path -LiteralPath $MainPy)) {
        Show-Error "main.py not found in:`n$ProjectRoot"
        exit 1
    }

    $py = $null
    if (Test-Path -LiteralPath $Pythonw) { $py = $Pythonw }
    elseif (Test-Path -LiteralPath $Python) { $py = $Python }
    else {
        Show-Error "Python venv not found:`n$Pythonw`n`nCreate .venv first."
        exit 1
    }

    # Fully hidden server (pythonw = no console)
    $proc = Start-Process -FilePath $py `
        -ArgumentList @('main.py') `
        -WorkingDirectory $ProjectRoot `
        -WindowStyle Hidden `
        -PassThru

    if ($proc -and $proc.Id) {
        try { Set-Content -LiteralPath $PidFile -Value $proc.Id -Encoding ascii -Force } catch {}
    }

    $opened = $false
    for ($i = 0; $i -lt 60; $i++) {
        if (Test-ServerReady) {
            Open-AppUi
            $opened = $true
            break
        }
        if ($proc -and $proc.HasExited) { break }
        Start-Sleep -Milliseconds 200
    }

    if (-not $opened) {
        Show-Error "Server did not start on port 8000.`nCheck that nothing else blocks the port."
        exit 1
    }

    exit 0
}
finally {
    if ($owned -and $mutex) {
        try { $mutex.ReleaseMutex() } catch {}
    }
    if ($mutex) {
        try { $mutex.Dispose() } catch {}
    }
}
