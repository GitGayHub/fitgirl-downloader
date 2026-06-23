// Global Elements
const elStartPauseBtn = document.getElementById("btn-start-pause");
const elExtractBtn = document.getElementById("btn-extract");
const elInstallBtn = document.getElementById("btn-install");
const elResetSessionBtn = document.getElementById("btn-reset-session");
const elThreadsSelect = document.getElementById("threads-select");
const elSaveThreadsBtn = document.getElementById("btn-save-threads");
const elConsoleBox = document.getElementById("console-box");
const elClearLogsBtn = document.getElementById("btn-clear-logs");

// Sidebar & views
const elSidebarStatusSummary = document.getElementById("sidebar-status-summary");
const elSidebarSetupInfo = document.getElementById("sidebar-setup-info");
const elSidebarActionsContainer = document.getElementById("sidebar-actions-container");
const elSetupView = document.getElementById("setup-view");
const elDownloadView = document.getElementById("download-view");

// Setup Wizard Elements
const elUrlTextarea = document.getElementById("url-textarea");
const elAnalyzeBtn = document.getElementById("btn-analyze");
const elAnalyzeSpinner = document.getElementById("analyze-spinner");
const elAnalyzeBtnText = document.getElementById("analyze-btn-text");
const elAnalyzeError = document.getElementById("analyze-error");

const elConfigCard = document.getElementById("config-card");
const elMirrorSelectSection = document.getElementById("mirror-select-section");
const elMirrorsContainer = document.getElementById("mirrors-container");
const elGameNameInput = document.getElementById("game-name-input");
const elSaveDirInput = document.getElementById("save-dir-input");
const elFillDefaultDirBtn = document.getElementById("btn-fill-default-dir");

const elSelMainBtn = document.getElementById("btn-sel-main");
const elSelAllBtn = document.getElementById("btn-sel-all");
const elSelNoneBtn = document.getElementById("btn-sel-none");
const elFilesListMain = document.getElementById("files-list-main");
const elFilesListLang = document.getElementById("files-list-lang");
const elFilesListOther = document.getElementById("files-list-other");
const elFileGroupLangBox = document.getElementById("file-group-lang-box");
const elFileGroupOtherBox = document.getElementById("file-group-other-box");
const elConfirmQueueBtn = document.getElementById("btn-confirm-queue");

// Download View Elements
const elActiveGameTitle = document.getElementById("active-game-title");
const elActiveGameSubtitle = document.getElementById("active-game-subtitle");
const elDownloadDirDisplay = document.getElementById("download-dir-display");
const elQueueContainer = document.getElementById("queue-list-container");
const elQueueCompletedCount = document.getElementById("queue-completed-count");

const elTotalProgressText = document.getElementById("total-progress-text");
const elGlobalSpeed = document.getElementById("global-speed");
const elGlobalTimeLeft = document.getElementById("global-time-left");
const svgProgressCircleBar = document.querySelector(".progress-circle-bar");

// Application State
let appState = {
    game_title: "",
    files: [],
    download_dir: "",
    default_download_dir: "",
    is_configured: false,
    is_running: false,
    total_speed: 0,
    total_progress: 0,
    log_messages: [],
    is_extracting: false,
    extraction_progress: 0,
    is_extracted: false,
    max_workers: 4
};

let analyzedFiles = [];
let smoothedSpeed = 0;

// Utilities
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
    let cleaned = name.replace(/[-_]+fitgirl-repacks\.site[-_]+/gi, ' ');
    cleaned = cleaned.replace(/[-_]+fitgirl-repacks[-_]+/gi, ' ');
    cleaned = cleaned.replace(/_/g, ' ');
    
    // Check if multi-part RAR
    let partMatch = cleaned.match(/\.part([0-9]+)\.rar$/i);
    if (partMatch) {
        cleaned = cleaned.replace(/\.part[0-9]+\.rar$/i, '').trim() + ` - Part ${parseInt(partMatch[1])}`;
    }
    return cleaned.trim();
}

// Fetch state from Python backend
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

// Update UI based on loaded state
function updateUI(newState) {
    // 1. Manage setup vs download views
    if (newState.is_configured) {
        elSetupView.style.display = "none";
        elDownloadView.style.display = "block";
        
        elSidebarSetupInfo.style.display = "none";
        elSidebarStatusSummary.style.display = "flex";
        elSidebarActionsContainer.style.display = "flex";
        
        // Populate display info
        elActiveGameTitle.innerText = newState.game_title || "Custom Repack";
        elActiveGameSubtitle.innerText = `Save directory: ${newState.download_dir}`;
        elDownloadDirDisplay.value = newState.download_dir;
        
        // Sync worker select
        if (newState.max_workers && elThreadsSelect.value !== String(newState.max_workers) && document.activeElement !== elThreadsSelect) {
            elThreadsSelect.value = String(newState.max_workers);
        }
        
        // Sync Play/Pause Button
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
                elStartPauseBtn.style.backgroundColor = ""; // reset to primary
            }
        }
        
        // 2. Overall Download Progress & Speeds
        const isDownloading = newState.files.some(f => f.status === "downloading");
        if (isDownloading && newState.total_speed > 0) {
            if (smoothedSpeed === 0) {
                smoothedSpeed = newState.total_speed;
            } else {
                smoothedSpeed = 0.05 * newState.total_speed + 0.95 * smoothedSpeed;
            }
        } else {
            smoothedSpeed = 0;
        }

        elGlobalSpeed.innerText = formatSpeed(smoothedSpeed > 0 ? smoothedSpeed : newState.total_speed);
        elTotalProgressText.innerText = `${newState.total_progress}%`;
        
        // Circular progress SVG
        const offset = 283 - (283 * newState.total_progress) / 100;
        svgProgressCircleBar.style.strokeDashoffset = offset;
        
        // ETA Left
        if (isDownloading && smoothedSpeed > 0) {
            let totalBytesLeft = 0;
            newState.files.forEach(f => {
                if (f.status !== "finished") {
                    let expectedSize = f.size;
                    if (expectedSize <= 0) {
                        expectedSize = f.type === "installer" ? 7468619 : 524288000;
                    }
                    totalBytesLeft += Math.max(0, expectedSize - f.downloaded);
                }
            });
            const totalSecondsLeft = Math.floor(totalBytesLeft / smoothedSpeed);
            elGlobalTimeLeft.innerText = formatTime(totalSecondsLeft);
        } else {
            elGlobalTimeLeft.innerText = "--:--";
        }
        
        // 3. Extract & Install Buttons Coordination
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
        
        // 4. Completed items count
        const completedCount = newState.files.filter(f => f.status === "finished").length;
        elQueueCompletedCount.innerText = `${completedCount} / ${newState.files.length} Completed`;
        
        // 5. Render queue list
        if (JSON.stringify(newState.files) !== JSON.stringify(appState.files)) {
            elQueueContainer.innerHTML = "";
            
            if (newState.files.length === 0) {
                elQueueContainer.innerHTML = `
                    <div class="loading-placeholder">
                        <p>No active downloads in the queue.</p>
                    </div>
                `;
            } else {
                newState.files.forEach((file, index) => {
                    const item = document.createElement("div");
                    item.className = "queue-item";
                    if (file.status === "downloading" || file.status === "connecting") {
                        item.classList.add("active");
                    }
                    
                    let badgeText = "Part File";
                    if (file.type === "lang_part") badgeText = "Language";
                    if (file.type === "installer") badgeText = "Installer";
                    
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
    } else {
        // Setup View is Active
        elSetupView.style.display = "block";
        elDownloadView.style.display = "none";
        
        elSidebarSetupInfo.style.display = "block";
        elSidebarStatusSummary.style.display = "none";
        elSidebarActionsContainer.style.display = "none";
    }
    
    // Global: Sync Console logs
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
    
    appState = newState;
}

// URL Analysis trigger
elAnalyzeBtn.addEventListener("click", async () => {
    const url = elUrlTextarea.value.trim();
    if (!url) return;
    
    // Show spinner & disable button
    elAnalyzeSpinner.style.display = "inline-block";
    elAnalyzeBtnText.innerText = "Analyzing Link...";
    elAnalyzeBtn.setAttribute("disabled", "true");
    elAnalyzeError.style.display = "none";
    elConfigCard.style.display = "none";
    elMirrorSelectSection.style.display = "none";
    
    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        if (response.ok && data.success) {
            if (data.type === "fitgirl_page") {
                // Show game title
                elGameNameInput.value = data.title;
                
                // Prefill default directory
                const defaultDir = appState.default_download_dir || "C:\\Downloads";
                elSaveDirInput.value = defaultDir + "\\" + data.title.replace(/[:\/\\\*\?"<>\|]/g, '');
                
                // Show mirrors selection
                if (data.mirrors && data.mirrors.length > 0) {
                    elMirrorSelectSection.style.display = "block";
                    elMirrorsContainer.innerHTML = "";
                    
                    data.mirrors.forEach((m, idx) => {
                        const pill = document.createElement("button");
                        pill.className = "mirror-pill";
                        pill.innerText = m.name;
                        pill.addEventListener("click", () => {
                            // Highlight clicked pill
                            document.querySelectorAll(".mirror-pill").forEach(p => p.classList.remove("active"));
                            pill.classList.add("active");
                            
                            // Load this mirror's PrivateBin/Direct links
                            loadMirrorLinks(m.url);
                        });
                        elMirrorsContainer.appendChild(pill);
                    });
                    
                    // Auto click first mirror pill
                    elMirrorsContainer.querySelector(".mirror-pill").click();
                } else {
                    elAnalyzeError.style.display = "block";
                    elAnalyzeError.innerText = "No download mirror links found on this page. Try copying direct links instead.";
                }
                
                elConfigCard.style.display = "block";
            } else if (data.type === "files") {
                displayConfigCard(data.title, data.files);
            }
        } else {
            elAnalyzeError.style.display = "block";
            elAnalyzeError.innerText = data.error || "Failed to analyze link. Check logs.";
        }
    } catch (e) {
        console.error("Error analyzing:", e);
        elAnalyzeError.style.display = "block";
        elAnalyzeError.innerText = "Connection error. Make sure Python server is running.";
    } finally {
        elAnalyzeSpinner.style.display = "none";
        elAnalyzeBtnText.innerText = "Analyze Link";
        elAnalyzeBtn.removeAttribute("disabled");
    }
});

// Load links nested when user clicks mirror
async function loadMirrorLinks(mirrorUrl) {
    elConfirmQueueBtn.setAttribute("disabled", "true");
    elConfirmQueueBtn.innerText = "Resolving Mirror Paste...";
    
    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: mirrorUrl })
        });
        
        const data = await response.json();
        if (response.ok && data.success) {
            analyzedFiles = data.files;
            renderChecklist(data.files);
            elConfirmQueueBtn.removeAttribute("disabled");
            elConfirmQueueBtn.innerText = "Confirm and Start Download";
        } else {
            alert("Error loading mirror links: " + (data.error || "Unknown error"));
        }
    } catch (e) {
        console.error("Error loading mirror:", e);
        alert("Failed to load mirror. Check internet connection.");
    }
}

// Display config card for direct files/PrivateBin
function displayConfigCard(title, files) {
    elGameNameInput.value = title;
    
    const defaultDir = appState.default_download_dir || "C:\\Downloads";
    elSaveDirInput.value = defaultDir + "\\" + title.replace(/[:\/\\\*\?"<>\|]/g, '');
    
    analyzedFiles = files;
    renderChecklist(files);
    elConfigCard.style.display = "block";
}

// Render Checklists
function renderChecklist(files) {
    elFilesListMain.innerHTML = "";
    elFilesListLang.innerHTML = "";
    elFilesListOther.innerHTML = "";
    
    let langCount = 0;
    let otherCount = 0;
    
    files.forEach((f, idx) => {
        const item = document.createElement("label");
        item.className = "checkbox-item";
        
        const sizeText = f.size > 0 ? formatBytes(f.size) : "Pending...";
        const checkedStr = (f.type === "game_part" || f.type === "installer") ? "checked" : "";
        
        item.innerHTML = `
            <input type="checkbox" data-index="${idx}" ${checkedStr}>
            <span class="checkbox-label" title="${f.filename}">${cleanFilename(f.filename)}</span>
            <span class="checkbox-badge">${sizeText}</span>
        `;
        
        if (f.type === "game_part" || f.type === "installer") {
            elFilesListMain.appendChild(item);
        } else if (f.type === "lang_part") {
            elFilesListLang.appendChild(item);
            langCount++;
        } else {
            elFilesListOther.appendChild(item);
            otherCount++;
        }
    });
    
    // Hide empty group containers
    elFileGroupLangBox.style.display = langCount > 0 ? "block" : "none";
    elFileGroupOtherBox.style.display = otherCount > 0 ? "block" : "none";
}

// Checkbox selection controls
elSelMainBtn.addEventListener("click", () => {
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        const idx = cb.getAttribute("data-index");
        const file = analyzedFiles[idx];
        if (file.type === "game_part" || file.type === "installer") {
            cb.checked = true;
        } else {
            cb.checked = false;
        }
    });
});

elSelAllBtn.addEventListener("click", () => {
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        cb.checked = true;
    });
});

elSelNoneBtn.addEventListener("click", () => {
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        cb.checked = false;
    });
});

elFillDefaultDirBtn.addEventListener("click", () => {
    const title = elGameNameInput.value.trim() || "Custom Repack";
    const defaultDir = appState.default_download_dir || "C:\\Downloads";
    elSaveDirInput.value = defaultDir + "\\" + title.replace(/[:\/\\\*\?"<>\|]/g, '');
});

// Confirm download queue configuration
elConfirmQueueBtn.addEventListener("click", async () => {
    const gameTitle = elGameNameInput.value.trim();
    const downloadDir = elSaveDirInput.value.trim();
    
    if (!gameTitle || !downloadDir) {
        alert("Please enter a game name and select a save directory.");
        return;
    }
    
    // Gather checked files
    const selectedFiles = [];
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        if (cb.checked) {
            const idx = parseInt(cb.getAttribute("data-index"));
            selectedFiles.push(analyzedFiles[idx]);
        }
    });
    
    if (selectedFiles.length === 0) {
        alert("Please select at least one file to download.");
        return;
    }
    
    elConfirmQueueBtn.setAttribute("disabled", "true");
    elConfirmQueueBtn.innerText = "Configuring Queue...";
    
    try {
        const response = await fetch("/api/confirm_config", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                game_title: gameTitle,
                download_dir: downloadDir,
                files: selectedFiles
            })
        });
        
        const data = await response.json();
        if (response.ok && data.success) {
            // Trigger status polling and automatically start downloads
            fetchState();
            await fetch("/api/start", { method: "POST" });
            fetchState();
        } else {
            alert("Configuration failed: " + (data.error || "Unknown error"));
            elConfirmQueueBtn.removeAttribute("disabled");
            elConfirmQueueBtn.innerText = "Confirm and Start Download";
        }
    } catch (e) {
        console.error("Error setting config:", e);
        alert("Connection error setting configuration.");
        elConfirmQueueBtn.removeAttribute("disabled");
        elConfirmQueueBtn.innerText = "Confirm and Start Download";
    }
});

// Sidebar Controls (Pause/Start)
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

// Sidebar extraction
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

// Sidebar Launch Installer
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

// Save threads
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

// Clear console log view
elClearLogsBtn.addEventListener("click", () => {
    elConsoleBox.innerHTML = '<div class="console-line system">[SYSTEM] Logs cleared.</div>';
});

// Reset session (Download new game)
elResetSessionBtn.addEventListener("click", async () => {
    if (confirm("Are you sure you want to reset this downloader session? This will clear the active download queue config. Downloaded files on disk will NOT be deleted.")) {
        try {
            const response = await fetch("/api/reset", { method: "POST" });
            if (response.ok) {
                // Clear inputs
                elUrlTextarea.value = "";
                elConfigCard.style.display = "none";
                elMirrorSelectSection.style.display = "none";
                analyzedFiles = [];
                // Poll status to trigger Setup view
                fetchState();
            } else {
                alert("Failed to reset session.");
            }
        } catch (e) {
            console.error("Error resetting session:", e);
        }
    }
});

// Global function to retry a specific index (failsafe if UI gets stuck)
window.triggerRetry = async (index) => {
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
