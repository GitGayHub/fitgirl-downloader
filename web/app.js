// Global Elements
const elStartPauseBtn = document.getElementById("btn-start-pause");
const elExtractBtn = document.getElementById("btn-extract");
const elInstallBtn = document.getElementById("btn-install");
const elDownloadDirInput = document.getElementById("download-dir-input");
const elSaveDirBtn = document.getElementById("btn-save-dir");
const elQueueContainer = document.getElementById("queue-list-container");
const elThreadsSelect = document.getElementById("threads-select");
const elSaveThreadsBtn = document.getElementById("btn-save-threads");
const elConsoleBox = document.getElementById("console-box");
const elClearLogsBtn = document.getElementById("btn-clear-logs");

const elTotalProgressText = document.getElementById("total-progress-text");
const elGlobalSpeed = document.getElementById("global-speed");
const elGlobalTimeLeft = document.getElementById("global-time-left");
const elQueueCompletedCount = document.getElementById("queue-completed-count");
const svgProgressCircleBar = document.querySelector(".progress-circle-bar");

let appState = {
    is_running: false,
    files: [],
    download_dir: "",
    total_speed: 0,
    total_progress: 0,
    log_messages: [],
    is_extracting: false,
    extraction_progress: 0,
    is_extracted: false
};

let smoothedSpeed = 0;

// Utilities for formatting
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function formatSpeed(bytesPerSec) {
    if (bytesPerSec === 0) return "0.0 MB/s";
    const mb = bytesPerSec / (1024 * 1024);
    return `${mb.toFixed(1)} MB/s`;
}

function formatTime(seconds) {
    if (seconds === -1) return "--:--";
    if (seconds < 60) return `${seconds}s`;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    if (mins < 60) return `${mins}m ${secs}s`;
    const hrs = Math.floor(mins / 60);
    const remMins = mins % 60;
    return `${hrs}h ${remMins}m`;
}

function cleanFilename(name) {
    // Call_of_Duty_MW_2019_--_fitgirl-repacks.site_--_.part001.rar -> CoD MW 2019 - Part 001
    if (name.startsWith("Call_of_Duty_MW_2019")) {
        const partMatch = name.match(/\.part([0-9]+)\.rar$/);
        if (partMatch) {
            return `CoD MW 2019 - Part ${partMatch[1]}`;
        }
    }
    return name;
}

// Fetch backend state
async function fetchState() {
    try {
        const response = await fetch("/api/status");
        if (response.ok) {
            const newState = await response.json();
            updateUI(newState);
        }
    } catch (e) {
        console.error("Failed to connect to backend API:", e);
    }
}

// Update UI elements based on state
function updateUI(newState) {
    // 1. Directory Input
    if (newState.download_dir && elDownloadDirInput.value !== newState.download_dir && document.activeElement !== elDownloadDirInput) {
        elDownloadDirInput.value = newState.download_dir;
    }
    
    // Threads select sync (only if not active/focused)
    if (newState.max_workers && elThreadsSelect.value !== String(newState.max_workers) && document.activeElement !== elThreadsSelect) {
        elThreadsSelect.value = String(newState.max_workers);
    }
    
    // 2. Play/Pause Button
    if (newState.is_running !== appState.is_running) {
        if (newState.is_running) {
            elStartPauseBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                </svg>
                <span>Pause Download</span>
            `;
            elStartPauseBtn.classList.remove("btn-pulse");
            elStartPauseBtn.style.backgroundColor = "#e67e22";
        } else {
            elStartPauseBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                </svg>
                <span>Start Download</span>
            `;
            elStartPauseBtn.classList.add("btn-pulse");
            elStartPauseBtn.style.backgroundColor = ""; // reset to css primary
        }
    }
    
    // 3. Overall Stats
    // Smooth the speed using EMA if downloading
    const isDownloading = newState.files.some(f => f.status === "downloading");
    if (isDownloading && newState.total_speed > 0) {
        if (smoothedSpeed === 0) {
            smoothedSpeed = newState.total_speed;
        } else {
            // EMA filter: 5% new speed weight, 95% old speed weight. Very stable.
            smoothedSpeed = 0.05 * newState.total_speed + 0.95 * smoothedSpeed;
        }
    } else {
        smoothedSpeed = 0;
    }

    elGlobalSpeed.innerText = formatSpeed(smoothedSpeed > 0 ? smoothedSpeed : newState.total_speed);
    elTotalProgressText.innerText = `${newState.total_progress}%`;
    
    // Circular SVG Progress logic (circumference of r=45 is 282.7)
    const offset = 283 - (283 * newState.total_progress) / 100;
    svgProgressCircleBar.style.strokeDashoffset = offset;
    
    // Calculate total time left for the entire download
    if (isDownloading && smoothedSpeed > 0) {
        let totalBytesLeft = 0;
        newState.files.forEach(f => {
            if (f.status !== "finished") {
                let expectedSize = f.size;
                if (expectedSize <= 0) {
                    expectedSize = f.type === "installer" ? 7468619 : (f.filename === "Call_of_Duty_MW_2019_--_fitgirl-repacks.site_--_.part145.rar" ? 209228843 : (f.filename === "fg-optional-russian.part5.rar" ? 3592179 : 524288000));
                }
                const downloaded = f.downloaded;
                totalBytesLeft += Math.max(0, expectedSize - downloaded);
            }
        });
        const totalSecondsLeft = Math.floor(totalBytesLeft / smoothedSpeed);
        elGlobalTimeLeft.innerText = formatTime(totalSecondsLeft);
    } else {
        elGlobalTimeLeft.innerText = "--:--";
    }
    
    // 4. Extract & Install Buttons Coordination
    const downloadsFinished = (newState.total_progress === 100 && newState.files.length > 0);
    
    if (!downloadsFinished) {
        elExtractBtn.setAttribute("disabled", "true");
        elExtractBtn.classList.remove("btn-pulse-green");
        elExtractBtn.style.backgroundColor = "";
        elExtractBtn.querySelector("span").innerText = "Extract Archives";
        
        elInstallBtn.setAttribute("disabled", "true");
        elInstallBtn.classList.remove("btn-pulse-green");
        elInstallBtn.style.backgroundColor = "";
    } else {
        if (newState.is_extracted) {
            elExtractBtn.setAttribute("disabled", "true");
            elExtractBtn.classList.remove("btn-pulse-green");
            elExtractBtn.style.backgroundColor = "#2c3e50";
            elExtractBtn.querySelector("span").innerText = "Archives Extracted";
            
            elInstallBtn.removeAttribute("disabled");
            elInstallBtn.classList.add("btn-pulse-green");
            elInstallBtn.style.backgroundColor = "#2ecc71";
        } else {
            elInstallBtn.setAttribute("disabled", "true");
            elInstallBtn.classList.remove("btn-pulse-green");
            elInstallBtn.style.backgroundColor = "";
            
            if (newState.is_extracting) {
                elExtractBtn.setAttribute("disabled", "true");
                elExtractBtn.classList.remove("btn-pulse-green");
                elExtractBtn.style.backgroundColor = "#d35400";
                elExtractBtn.querySelector("span").innerText = `Extracting (${newState.extraction_progress}%)`;
            } else {
                elExtractBtn.removeAttribute("disabled");
                elExtractBtn.classList.add("btn-pulse-green");
                elExtractBtn.style.backgroundColor = "#2ecc71";
                elExtractBtn.querySelector("span").innerText = "Extract Archives";
            }
        }
    }
    
    // 5. Completed Items count
    const completedCount = newState.files.filter(f => f.status === "finished").length;
    elQueueCompletedCount.innerText = `${completedCount} / ${newState.files.length} Completed`;
    
    // 6. Logs updating
    if (JSON.stringify(newState.log_messages) !== JSON.stringify(appState.log_messages)) {
        elConsoleBox.innerHTML = "";
        newState.log_messages.forEach(log => {
            const div = document.createElement("div");
            div.className = "console-line";
            if (log.includes("[SYSTEM]") || log.includes("ALL DOWNLOADS COMPLETED")) div.classList.add("system");
            if (log.includes("Error") || log.includes("failed") || log.includes("Exception")) div.classList.add("error");
            div.innerText = log;
            elConsoleBox.appendChild(div);
        });
        elConsoleBox.scrollTop = elConsoleBox.scrollHeight;
    }
    
    // 7. Queue List Rendering
    if (JSON.stringify(newState.files) !== JSON.stringify(appState.files)) {
        elQueueContainer.innerHTML = "";
        
        if (newState.files.length === 0) {
            elQueueContainer.innerHTML = `
                <div class="loading-placeholder">
                    <p>No target files populated. Check PrivateBin connection.</p>
                </div>
            `;
        } else {
            newState.files.forEach((file, index) => {
                const item = document.createElement("div");
                item.className = "queue-item";
                if (file.status === "downloading" || file.status === "connecting") {
                    item.classList.add("active");
                }
                
                // Format type badge text
                let badgeText = "Game Part";
                if (file.type === "lang_part") badgeText = "RU Language";
                if (file.type === "installer") badgeText = "Installer";
                
                // Format file sizes / progress
                const sizeText = file.size > 0 ? formatBytes(file.size) : "Pending...";
                const speedText = file.status === "downloading" ? formatSpeed(file.speed) : "";
                
                item.innerHTML = `
                    <div class="file-name" title="${file.filename}">${cleanFilename(file.filename)}</div>
                    <div class="file-badge ${file.type}">${badgeText}</div>
                    <div class="file-progress-container">
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${file.progress}%"></div>
                        </div>
                        <div class="file-progress-text">
                            <span>${file.progress}% (${formatBytes(file.downloaded)} of ${sizeText})</span>
                            <span class="file-speed">${speedText}</span>
                        </div>
                    </div>
                    <div class="file-status ${file.status}">${file.status}</div>
                    <div class="file-actions">
                        ${file.status === "failed" ? `<button class="btn btn-accent btn-retry" onclick="triggerRetry(${index})">Retry</button>` : ""}
                    </div>
                `;
                elQueueContainer.appendChild(item);
            });
        }
    }
    
    appState = newState;
}

// User Actions
elStartPauseBtn.addEventListener("click", async () => {
    const api = appState.is_running ? "/api/pause" : "/api/start";
    try {
        const response = await fetch(api, { method: "POST" });
        if (response.ok) {
            fetchState();
        }
    } catch (e) {
        console.error("Error toggling download status:", e);
    }
});

elSaveDirBtn.addEventListener("click", async () => {
    const newDir = elDownloadDirInput.value.trim();
    if (!newDir) return;
    try {
        const response = await fetch("/api/set_dir", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ download_dir: newDir })
        });
        if (response.ok) {
            fetchState();
            alert("Download directory successfully updated!");
        } else {
            alert("Failed to update download directory.");
        }
    } catch (e) {
        console.error("Error setting save directory:", e);
    }
});

elSaveThreadsBtn.addEventListener("click", async () => {
    const workers = parseInt(elThreadsSelect.value);
    if (isNaN(workers) || workers < 1 || workers > 10) return;
    try {
        const response = await fetch("/api/set_workers", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ max_workers: workers })
        });
        if (response.ok) {
            fetchState();
            alert(`Parallel download threads updated to: ${workers}`);
        } else {
            alert("Failed to update threads count.");
        }
    } catch (e) {
        console.error("Error setting max workers:", e);
    }
});

elExtractBtn.addEventListener("click", async () => {
    try {
        const response = await fetch("/api/extract", { method: "POST" });
        if (response.ok) {
            fetchState();
        } else {
            alert("Failed to start extraction. Check logs.");
        }
    } catch (e) {
        console.error("Error running extraction:", e);
    }
});

elInstallBtn.addEventListener("click", async () => {
    if (confirm("Do you want to run the installer setup now? Make sure the download of all parts is completed.")) {
        try {
            const response = await fetch("/api/install", { method: "POST" });
            if (response.ok) {
                alert("Installer launched successfully! Follow the setup instructions on your desktop.");
            } else {
                alert("Failed to launch installer. Check console logs.");
            }
        } catch (e) {
            console.error("Error running installer:", e);
        }
    }
});

elClearLogsBtn.addEventListener("click", () => {
    elConsoleBox.innerHTML = '<div class="console-line system">[SYSTEM] Logs cleared.</div>';
});

// Global function to retry a specific index (failsafe if UI gets stuck)
window.triggerRetry = async (index) => {
    // Directly start queue, which automatically picks up failed links
    try {
        await fetch("/api/start", { method: "POST" });
        fetchState();
    } catch (e) {
        console.error("Failed to retry download:", e);
    }
};

// Start Polling Loop
fetchState();
setInterval(fetchState, 1000);
