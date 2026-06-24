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

// New Subviews
const elCatalogContainer = document.getElementById("catalog-container");
const elGameDetailsContainer = document.getElementById("game-details-container");

// Browse Catalog & Search Elements
const elSearchInput = document.getElementById("search-input");
const elPillPopularMonth = document.getElementById("pill-popular-month");
const elPillPopularYear = document.getElementById("pill-popular-year");
const elGamesLoader = document.getElementById("games-loader");
const elGamesGridContainer = document.getElementById("games-grid-container");
const elSearchResultsTitle = document.getElementById("search-results-title");

// Settings Modal & Gear
const elSettingsGearBtn = document.getElementById("btn-settings-gear");
const elSettingsModal = document.getElementById("settings-modal");
const elCloseSettingsModalBtn = document.getElementById("btn-close-settings-modal");
const elSaveSettingsBtn = document.getElementById("btn-save-settings");
const elProviderSelect = document.getElementById("provider-select");
const elChkShowLogs = document.getElementById("chk-show-logs");
const elChkRainbowBg = document.getElementById("chk-rainbow-bg");
const elGameInfoCard = document.getElementById("game-info-card");
const elGameDescription = document.getElementById("game-description");
const elGameScreenshotsSection = document.getElementById("game-screenshots-section");
const elGameScreenshotsContainer = document.getElementById("game-screenshots-container");
const elScreenshotModal = document.getElementById("screenshot-modal");
const elScreenshotModalImg = document.getElementById("screenshot-modal-img");
const elCloseScreenshotModalBtn = document.getElementById("btn-close-screenshot-modal");

// Pagination Controls
const elBtnPrevPage = document.getElementById("btn-prev-page");
const elBtnNextPage = document.getElementById("btn-next-page");
const elPageIndicator = document.getElementById("page-indicator");

// Setup Wizard Elements (Pasted URL / Config)
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
const elBrowseDirBtn = document.getElementById("btn-browse-dir");
const elChangeProviderBtn = document.getElementById("btn-change-provider");
const elProviderModal = document.getElementById("provider-modal");
const elCloseProviderModalBtn = document.getElementById("btn-close-provider-modal");
const elCancelProviderSwitchBtn = document.getElementById("btn-cancel-provider-switch");
const elConfirmProviderSwitchBtn = document.getElementById("btn-confirm-provider-switch");
const elModalMirrorsContainer = document.getElementById("modal-mirrors-container");
const elChkDeleteOldFiles = document.getElementById("chk-delete-old-files");

const elSelMainBtn = document.getElementById("btn-sel-main");
const elSelAllBtn = document.getElementById("btn-sel-all");
const elSelNoneBtn = document.getElementById("btn-sel-none");
const elSelRusBtn = document.getElementById("btn-sel-rus");
const elSiteToggleTrigger = document.getElementById("site-toggle-trigger");
const elLabelSiteFitGirl = document.getElementById("label-site-fitgirl");
const elLabelSiteOnlineFix = document.getElementById("label-site-onlinefix");
const elToggleManualInputBtn = document.getElementById("btn-toggle-manual-input");
const elUrlInputCard = document.getElementById("url-input-card");
const elFilesListMain = document.getElementById("files-list-main");
const elFilesListLang = document.getElementById("files-list-lang");
const elFilesListOther = document.getElementById("files-list-other");
const elFileGroupLangBox = document.getElementById("file-group-lang-box");
const elFileGroupOtherBox = document.getElementById("file-group-other-box");
const elConfirmQueueBtn = document.getElementById("btn-confirm-queue");

const elActiveMirrorBadge = document.getElementById("active-mirror-badge-container");
const elActiveMirrorName = document.getElementById("active-mirror-name");
const elDownloadMirrorBadge = document.getElementById("download-mirror-badge");
const elChecklistLoadingSpinner = document.getElementById("checklist-loading-spinner");

// New Setup Dashboard Elements
const elSetupDashboard = document.getElementById("setup-dashboard");
const elSetupCover = document.getElementById("setup-cover");
const elSetupCoverPlaceholder = document.getElementById("setup-cover-placeholder");
const elMetadataOriginalSize = document.getElementById("metadata-original-size");
const elMetadataRepackSize = document.getElementById("metadata-repack-size");
const elMetadataTotalParts = document.getElementById("metadata-total-parts");
const elMetadataSelectedSize = document.getElementById("metadata-selected-size");
const elMetadataEta = document.getElementById("metadata-eta");
const elMetadataAvgSpeed = document.getElementById("metadata-avg-speed");
const elSortingSelect = document.getElementById("sorting-select");

// Details view specific elements
const elBtnBackToCatalog = document.getElementById("btn-back-to-catalog");
const elDetailsGameTitle = document.getElementById("details-game-title");
const elDetailsVersionBadge = document.getElementById("details-version-badge");
const elBtnOpenBrowser = document.getElementById("btn-open-browser");
const elCatalogTitle = document.getElementById("catalog-title");

// Haze Background Elements
const elHazeBgImg1 = document.getElementById("haze-bg-img-1");
const elHazeBgImg2 = document.getElementById("haze-bg-img-2");
let activeHazeBuffer = 1;

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
    max_workers: 4,
    average_download_speed: 5000000.0
};
// Local memory cache for cover blobs to prevent pagination re-loading lag
const blobUrlCache = new Map();

async function getCachedImageUrl(url) {
    if (!url) return "";
    if (blobUrlCache.has(url)) {
        return blobUrlCache.get(url);
    }
    try {
        const res = await fetch(url);
        if (res.ok) {
            const blob = await res.blob();
            const blobUrl = URL.createObjectURL(blob);
            blobUrlCache.set(url, blobUrl);
            return blobUrl;
        }
    } catch (e) {
        console.warn("Failed caching image in memory:", e);
    }
    return url;
}

let analyzedFiles = [];
let smoothedSpeed = 0;
let checkedFiles = new Set();
let activeMirrorName = "";
let scrapedMirrors = [];
let scrapedMetadata = {
    original_size: "Unknown",
    repack_size: "Unknown",
    cover_image: ""
};

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
    if (seconds <= 0 || seconds === -1 || !isFinite(seconds)) return "Ожидание загрузки";
    const mins = Math.ceil(seconds / 60);
    if (mins < 60) return `~${mins} мин`;
    const hrs = Math.floor(mins / 60);
    const remMins = mins % 60;
    if (hrs < 24) {
        return remMins > 0 ? `~${hrs} ч ${remMins} мин` : `~${hrs} ч`;
    }
    const days = Math.floor(hrs / 24);
    const remHrs = hrs % 24;
    return remHrs > 0 ? `~${days} дн ${remHrs} ч` : `~${days} дн`;
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

let rawFilesList = [];

function getPartNumber(filename) {
    const match = filename.match(/part\s*(\d+)/i);
    if (match) return parseInt(match[1], 10);
    
    const matchBin = filename.match(/setup[-_](\d+)\.bin/i);
    if (matchBin) return parseInt(matchBin[1], 10);
    
    return null;
}

function sortFiles(files, orderType) {
    if (orderType === "original") {
        return [...files];
    }
    const rusRegex = /(?:^|[\s\.\-_])(rus|russian)(?:$|[\s\.\-_])/i;
    const isOptionalRussianFile = (f) => {
        if (f.type === "game_part" || f.type === "installer") return false;
        return f.filename && rusRegex.test(f.filename);
    };
    
    if (orderType === "russian_first") {
        return [...files].sort((a, b) => {
            const isRusA = isOptionalRussianFile(a);
            const isRusB = isOptionalRussianFile(b);
            if (isRusA && !isRusB) return -1;
            if (isRusB && !isRusA) return 1;
            
            if (a.type === "installer" && b.type !== "installer") return -1;
            if (b.type === "installer" && a.type !== "installer") return 1;
            
            const partA = getPartNumber(a.filename);
            const partB = getPartNumber(b.filename);
            if (partA !== null && partB !== null) return partA - partB;
            if (partA !== null) return 1;
            if (partB !== null) return -1;
            
            return a.filename.localeCompare(b.filename, undefined, {numeric: true, sensitivity: 'base'});
        });
    }
    
    return [...files].sort((a, b) => {
        if (a.type === "installer" && b.type !== "installer") return -1;
        if (b.type === "installer" && a.type !== "installer") return 1;
        
        const partA = getPartNumber(a.filename);
        const partB = getPartNumber(b.filename);
        
        if (partA !== null && partB !== null) {
            return partA - partB;
        }
        if (partA !== null) return 1;
        if (partB !== null) return -1;
        
        return a.filename.localeCompare(b.filename, undefined, {numeric: true, sensitivity: 'base'});
    });
}

function updateMetadataETA() {
    let totalSize = 0;
    let selectedCount = 0;
    
    rawFilesList.forEach(f => {
        if (checkedFiles.has(f.filename)) {
            selectedCount++;
            let sz = f.size;
            if (sz <= 0) {
                if (f.type === "installer") sz = 7468619;
                else if (f.filename.includes("part")) sz = 1.5 * 1024 * 1024 * 1024;
                else sz = 500 * 1024 * 1024;
            }
            totalSize += sz;
        }
    });
    
    elMetadataSelectedSize.innerText = formatBytes(totalSize);
    
    const gameParts = rawFilesList.filter(f => f.type === "game_part");
    const totalParts = gameParts.length > 0 ? gameParts.length : rawFilesList.length;
    const selectedParts = gameParts.length > 0 
        ? gameParts.filter(f => checkedFiles.has(f.filename)).length 
        : selectedCount;
    elMetadataTotalParts.innerText = `${selectedParts} / ${totalParts}`;
    
    const avgSpeed = appState.average_download_speed || 5000000.0;
    const seconds = totalSize / avgSpeed;
    elMetadataEta.innerText = formatTime(seconds);
    elMetadataAvgSpeed.innerText = formatSpeed(avgSpeed);
}

function updateChecklistSorted() {
    const sortVal = elSortingSelect.value;
    analyzedFiles = sortFiles(rawFilesList, sortVal);
    renderChecklist(analyzedFiles);
    updateMetadataETA();
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
        document.querySelector(".app-container").classList.add("has-sidebar");
        document.querySelector(".sidebar").style.display = "flex";
        
        elSetupView.style.display = "none";
        elDownloadView.style.display = "flex";
        
        elSidebarSetupInfo.style.display = "none";
        elSidebarStatusSummary.style.display = "flex";
        elSidebarActionsContainer.style.display = "flex";
        
        // Populate display info
        elActiveGameTitle.innerText = newState.game_title || "Custom Repack";
        elActiveGameSubtitle.innerText = `Save directory: ${newState.download_dir}`;
        elDownloadDirDisplay.value = newState.download_dir;
        
        // Sync mirror badge
        if (newState.active_mirror) {
            elDownloadMirrorBadge.innerText = `Mirror: ${newState.active_mirror}`;
            elDownloadMirrorBadge.style.display = "inline-block";
        } else {
            elDownloadMirrorBadge.style.display = "none";
        }
        
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
            elGlobalTimeLeft.innerText = "Ожидание загрузки";
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
        syncViewState();
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

function resetSetupDashboard() {
    activeMirrorName = "";
    elSetupDashboard.style.display = "none";
    elConfigCard.style.display = "none";
    elMirrorSelectSection.style.display = "none";
    analyzedFiles = [];
    rawFilesList = [];
    checkedFiles.clear();
    
    // Clear sidebar metadata
    elDetailsGameTitle.innerText = "Game Title";
    elDetailsVersionBadge.style.display = "none";
    elMetadataOriginalSize.innerText = "--";
    elMetadataRepackSize.innerText = "--";
    elMetadataTotalParts.innerText = "--";
    elMetadataSelectedSize.innerText = "--";
    elMetadataEta.innerText = "--";
    elSetupCover.src = "";
    elSetupCover.style.display = "none";
    elSetupCoverPlaceholder.style.display = "flex";
    
    // Clear game info card contents
    if (elGameDescription) elGameDescription.innerText = "";
    if (elGameScreenshotsContainer) elGameScreenshotsContainer.innerHTML = "";
    if (elGameScreenshotsSection) elGameScreenshotsSection.style.display = "none";
    if (elGameInfoCard) elGameInfoCard.style.display = "none";
    if (elSetupDashboard) elSetupDashboard.classList.add("no-info-card");
}

function initCheckedFiles(files) {
    checkedFiles.clear();
    const rusRegex = /(?:^|[\s\.\-_])(rus|russian)(?:$|[\s\.\-_])/i;
    files.forEach(f => {
        if (f.type === "game_part" || f.type === "installer") {
            checkedFiles.add(f.filename);
        } else if (f.filename && rusRegex.test(f.filename)) {
            checkedFiles.add(f.filename);
        }
    });
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
    resetSetupDashboard();
    
    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        if (response.ok && data.success) {
            if (data.type === "fitgirl_page") {
                // Populate metadata sidebar
                scrapedMetadata.original_size = data.original_size || "Unknown";
                scrapedMetadata.repack_size = data.repack_size || "Unknown";
                scrapedMetadata.cover_image = data.cover_image || "";
                
                elDetailsGameTitle.innerText = data.title || "Custom Repack";
                if (data.version) {
                    elDetailsVersionBadge.innerText = data.version;
                    elDetailsVersionBadge.style.display = "inline-block";
                } else {
                    elDetailsVersionBadge.style.display = "none";
                }
                
                // Open in Browser URL mapping
                if (elBtnOpenBrowser) {
                    elBtnOpenBrowser.href = url;
                    elBtnOpenBrowser.style.display = "inline-block";
                }
                
                elMetadataOriginalSize.innerText = scrapedMetadata.original_size;
                elMetadataRepackSize.innerText = scrapedMetadata.repack_size;
                
                // Render video trailer
                const elVideoContainer = document.getElementById("details-video-container");
                const elVideoIframe = document.getElementById("video-iframe");
                if (elVideoContainer && elVideoIframe) {
                    if (data.videos && data.videos.length > 0) {
                        let videoUrl = data.videos[0];
                        if (videoUrl.includes("youtube.com/watch?v=")) {
                            const videoId = videoUrl.split("watch?v=")[1].split("&")[0];
                            videoUrl = `https://www.youtube.com/embed/${videoId}`;
                        } else if (videoUrl.includes("youtu.be/")) {
                            const videoId = videoUrl.split("youtu.be/")[1].split("?")[0];
                            videoUrl = `https://www.youtube.com/embed/${videoId}`;
                        }
                        if (videoUrl.startsWith("//")) {
                            videoUrl = "https:" + videoUrl;
                        }
                        elVideoIframe.src = videoUrl;
                        elVideoContainer.style.display = "block";
                    } else {
                        elVideoIframe.src = "";
                        elVideoContainer.style.display = "none";
                    }
                }

                if (scrapedMetadata.cover_image) {
                    const proxiedUrl = `/api/proxy_image?url=${encodeURIComponent(scrapedMetadata.cover_image)}`;
                    getCachedImageUrl(proxiedUrl).then(cachedUrl => {
                        elSetupCover.src = cachedUrl;
                        elSetupCover.style.display = "block";
                        elSetupCoverPlaceholder.style.display = "none";
                        elSetupCover.onerror = () => {
                            elSetupCover.src = "";
                            elSetupCover.style.display = "none";
                            elSetupCoverPlaceholder.style.display = "flex";
                            clearDynamicBackground();
                        };
                        setHazeBackground(cachedUrl);
                        updateAccentFromImage(elSetupCover);
                    });
                } else {
                    elSetupCover.src = "";
                    elSetupCover.style.display = "none";
                    elSetupCoverPlaceholder.style.display = "flex";
                    clearDynamicBackground();
                }

                // Show game title
                elGameNameInput.value = data.title;
                
                // Prefill default directory
                const defaultDir = appState.default_download_dir || "D:\\Downloads";
                elSaveDirInput.value = defaultDir;
                
                // Store mirrors list for provider switching
                scrapedMirrors = data.mirrors || [];
                
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
                            loadMirrorLinks(m.url, m.name);
                        });
                        elMirrorsContainer.appendChild(pill);
                    });
                    
                    // Auto click first mirror pill
                    elMirrorsContainer.querySelector(".mirror-pill").click();
                } else {
                    elAnalyzeError.style.display = "block";
                    elAnalyzeError.innerText = "No download mirror links found on this page. Try copying direct links instead.";
                }

                // Render description & screenshots
                if (elGameDescription && data.description) {
                    elGameDescription.innerText = data.description;
                    elGameDescription.style.display = "block";
                } else if (elGameDescription) {
                    elGameDescription.innerText = "";
                    elGameDescription.style.display = "none";
                }

                if (elGameScreenshotsSection && elGameScreenshotsContainer && data.screenshots && data.screenshots.length > 0) {
                    elGameScreenshotsSection.style.display = "block";
                    elGameScreenshotsContainer.innerHTML = "";
                    data.screenshots.forEach(src => {
                        const img = document.createElement("img");
                        img.className = "screenshot-img";
                        img.src = `/api/proxy_image?url=${encodeURIComponent(src)}`;
                        img.alt = "Screenshot";
                        img.addEventListener("click", () => {
                            openScreenshotModal(img.src);
                        });
                        elGameScreenshotsContainer.appendChild(img);
                    });
                } else if (elGameScreenshotsSection) {
                    elGameScreenshotsSection.style.display = "none";
                    if (elGameScreenshotsContainer) elGameScreenshotsContainer.innerHTML = "";
                }

                if (elGameInfoCard) {
                    if (data.description || (data.screenshots && data.screenshots.length > 0)) {
                        elGameInfoCard.style.display = "block";
                        if (elSetupDashboard) elSetupDashboard.classList.remove("no-info-card");
                    } else {
                        elGameInfoCard.style.display = "none";
                        if (elSetupDashboard) elSetupDashboard.classList.add("no-info-card");
                    }
                }
                
                elSetupDashboard.style.display = "grid";
                elConfigCard.style.display = "block";
                setViewState("details");
            } else if (data.type === "files") {
                displayConfigCard(data.title, data.files, url);
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

function configureRussianSorting(files) {
    const rusRegex = /(?:^|[\s\.\-_])(rus|russian)(?:$|[\s\.\-_])/i;
    const hasOptRus = files.some(f => (f.type !== "game_part" && f.type !== "installer") && f.filename && rusRegex.test(f.filename));
    const optRusExists = Array.from(elSortingSelect.options).some(o => o.value === "russian_first");
    
    if (hasOptRus) {
        elSelRusBtn.style.display = "inline-block";
        if (!optRusExists) {
            const opt = document.createElement("option");
            opt.value = "russian_first";
            opt.innerText = "Сначала русские + По порядку";
            elSortingSelect.insertBefore(opt, elSortingSelect.firstChild);
        }
        elSortingSelect.value = "russian_first";
    } else {
        elSelRusBtn.style.display = "none";
        if (optRusExists) {
            const optIndex = Array.from(elSortingSelect.options).findIndex(o => o.value === "russian_first");
            if (optIndex !== -1) elSortingSelect.remove(optIndex);
        }
        elSortingSelect.value = "sequential";
    }
}

// Load links nested when user clicks mirror
async function loadMirrorLinks(mirrorUrl, mirrorName) {
    activeMirrorName = mirrorName;
    elConfirmQueueBtn.setAttribute("disabled", "true");
    elConfirmQueueBtn.innerText = "Resolving Mirror Paste...";
    
    // Show checklist loading overlay
    elChecklistLoadingSpinner.style.display = "flex";
    elActiveMirrorBadge.style.display = "none";
    
    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: mirrorUrl })
        });
        
        const data = await response.json();
        if (response.ok && data.success) {
            rawFilesList = data.files;
            initCheckedFiles(data.files);
            
            configureRussianSorting(data.files);
            
            // Show mirror badge and update label
            elActiveMirrorName.innerText = mirrorName;
            elActiveMirrorBadge.style.display = "inline-block";
            
            elConfirmQueueBtn.removeAttribute("disabled");
            elConfirmQueueBtn.innerText = "Confirm and Start Download";
            
            updateChecklistSorted();
        } else {
            alert("Error loading mirror links: " + (data.error || "Unknown error"));
        }
    } catch (e) {
        console.error("Error loading mirror:", e);
        alert("Failed to load mirror. Check internet connection.");
    } finally {
        elChecklistLoadingSpinner.style.display = "none";
    }
}

// Display config card for direct files/PrivateBin
function displayConfigCard(title, files, url = "") {
    activeMirrorName = "";
    elGameNameInput.value = title;
    
    const defaultDir = appState.default_download_dir || "D:\\Downloads";
    elSaveDirInput.value = defaultDir;
    
    // Hide mirror selection since it's a direct paste
    elMirrorSelectSection.style.display = "none";
    elActiveMirrorBadge.style.display = "none";
    
    // Set placeholder metadata
    scrapedMetadata.original_size = "N/A";
    scrapedMetadata.repack_size = "N/A";
    scrapedMetadata.cover_image = "";
    
    elDetailsGameTitle.innerText = title;
    elDetailsVersionBadge.style.display = "none";
    
    if (elBtnOpenBrowser && url) {
        elBtnOpenBrowser.href = url;
        elBtnOpenBrowser.style.display = "inline-block";
    } else if (elBtnOpenBrowser) {
        elBtnOpenBrowser.style.display = "none";
    }
    
    elMetadataOriginalSize.innerText = "N/A";
    elMetadataRepackSize.innerText = "N/A";
    elSetupCover.src = "";
    elSetupCover.style.display = "none";
    elSetupCoverPlaceholder.style.display = "flex";
    clearDynamicBackground();
    
    if (elGameInfoCard) elGameInfoCard.style.display = "none";
    if (elSetupDashboard) elSetupDashboard.classList.add("no-info-card");
    
    rawFilesList = files;
    initCheckedFiles(files);
    
    configureRussianSorting(files);
    
    elSetupDashboard.style.display = "grid";
    elConfigCard.style.display = "block";
    
    updateChecklistSorted();
    setViewState("details");
}

// Part Files Grouping helpers
function getPartGroupInfo(filename) {
    // Match "part 1", ".part1", "_part01", etc.
    const match = filename.match(/(.*?)([\s\.\-_]+part\s*(\d+))([^/\\]*)$/i);
    if (match) {
        return {
            base: match[1].trim(),
            partNum: parseInt(match[3], 10),
            suffix: match[4]
        };
    }
    return null;
}

function setupGroupCheckboxBehavior(headerCheckbox, childCheckboxes, filesInGroup) {
    const updateHeaderState = () => {
        let checkedCount = 0;
        childCheckboxes.forEach(cb => {
            if (cb.checked) checkedCount++;
        });
        if (checkedCount === 0) {
            headerCheckbox.checked = false;
            headerCheckbox.indeterminate = false;
        } else if (checkedCount === childCheckboxes.length) {
            headerCheckbox.checked = true;
            headerCheckbox.indeterminate = false;
        } else {
            headerCheckbox.checked = false;
            headerCheckbox.indeterminate = true;
        }
    };
    
    headerCheckbox.addEventListener("change", () => {
        const checked = headerCheckbox.checked;
        childCheckboxes.forEach((cb, idx) => {
            cb.checked = checked;
            const f = filesInGroup[idx];
            if (checked) {
                checkedFiles.add(f.filename);
            } else {
                checkedFiles.delete(f.filename);
            }
        });
        updateMetadataETA();
    });
    
    childCheckboxes.forEach((cb, idx) => {
        cb.addEventListener("change", () => {
            const f = filesInGroup[idx];
            if (cb.checked) {
                checkedFiles.add(f.filename);
            } else {
                checkedFiles.delete(f.filename);
            }
            updateHeaderState();
            updateMetadataETA();
        });
    });
    
    updateHeaderState();
}

function renderFileListToContainer(files, containerElement) {
    containerElement.innerHTML = "";
    if (files.length === 0) return;
    
    // Group files by Part
    const groups = {};
    const singleFiles = [];
    
    files.forEach(f => {
        const info = getPartGroupInfo(f.filename);
        if (info) {
            const key = `${info.base}`;
            if (!groups[key]) groups[key] = [];
            groups[key].push(f);
        } else {
            singleFiles.push(f);
        }
    });
    
    // Move groups with only 1 file to singleFiles
    for (const key in groups) {
        if (groups[key].length === 1) {
            singleFiles.push(groups[key][0]);
            delete groups[key];
        }
    }
    
    // Render groups
    for (const groupName in groups) {
        const groupFiles = groups[groupName];
        
        // Sort files within the group by part number
        groupFiles.sort((a, b) => {
            const infoA = getPartGroupInfo(a.filename);
            const infoB = getPartGroupInfo(b.filename);
            return (infoA ? infoA.partNum : 0) - (infoB ? infoB.partNum : 0);
        });
        
        const details = document.createElement("details");
        details.className = "file-group-collapsible";
        details.open = false;
        
        const totalSize = groupFiles.reduce((acc, f) => acc + (f.size || 0), 0);
        const totalSizeText = totalSize > 0 ? formatBytes(totalSize) : "Pending...";
        
        details.innerHTML = `
            <summary class="file-group-summary">
                <span class="summary-toggle-icon">⏵</span>
                <input type="checkbox" class="group-header-checkbox">
                <span class="group-title-label">${groupName} (${groupFiles.length} Parts)</span>
                <span class="checkbox-badge">${totalSizeText}</span>
            </summary>
            <div class="file-group-list"></div>
        `;
        
        const listDiv = details.querySelector(".file-group-list");
        const headerCheckbox = details.querySelector(".group-header-checkbox");
        const childCheckboxes = [];
        
        groupFiles.forEach(f => {
            const item = document.createElement("label");
            item.className = "checkbox-item group-child-item";
            
            const sizeText = f.size > 0 ? formatBytes(f.size) : "Pending...";
            const checkedStr = checkedFiles.has(f.filename) ? "checked" : "";
            
            item.innerHTML = `
                <input type="checkbox" data-filename="${f.filename}" ${checkedStr}>
                <span class="checkbox-label" title="${f.filename}">${cleanFilename(f.filename)}</span>
                <span class="checkbox-badge">${sizeText}</span>
            `;
            listDiv.appendChild(item);
            childCheckboxes.push(item.querySelector("input"));
        });
        
        setupGroupCheckboxBehavior(headerCheckbox, childCheckboxes, groupFiles);
        containerElement.appendChild(details);
        
        // Prevent clicking summary checkbox from toggling details expansion
        headerCheckbox.addEventListener("click", (e) => {
            e.stopPropagation();
        });
    }
    
    // Render single files
    singleFiles.forEach(f => {
        const item = document.createElement("label");
        item.className = "checkbox-item";
        
        const sizeText = f.size > 0 ? formatBytes(f.size) : "Pending...";
        const checkedStr = checkedFiles.has(f.filename) ? "checked" : "";
        
        item.innerHTML = `
            <input type="checkbox" data-filename="${f.filename}" ${checkedStr}>
            <span class="checkbox-label" title="${f.filename}">${cleanFilename(f.filename)}</span>
            <span class="checkbox-badge">${sizeText}</span>
        `;
        
        const cb = item.querySelector("input");
        cb.addEventListener("change", () => {
            if (cb.checked) {
                checkedFiles.add(f.filename);
            } else {
                checkedFiles.delete(f.filename);
            }
            updateMetadataETA();
        });
        
        containerElement.appendChild(item);
    });
}

// Render Checklists
// Render Checklists
function renderChecklist(files) {
    elFilesListMain.innerHTML = "";
    elFilesListLang.innerHTML = "";
    elFilesListOther.innerHTML = "";
    
    let langCount = 0;
    let otherCount = 0;
    
    const mainFiles = [];
    const langFiles = [];
    const otherFiles = [];
    
    const sortVal = elSortingSelect ? elSortingSelect.value : "sequential";
    const rusRegex = /(?:^|[\s\.\-_])(rus|russian)(?:$|[\s\.\-_])/i;
    
    files.forEach(f => {
        if (f.type === "game_part" || f.type === "installer") {
            mainFiles.push(f);
        } else if (f.type === "lang_part") {
            langFiles.push(f);
            langCount++;
        } else {
            otherFiles.push(f);
            otherCount++;
        }
    });
    
    if (sortVal === "russian_first") {
        const sortRusFirst = (a, b) => {
            const isRusA = a.filename && rusRegex.test(a.filename);
            const isRusB = b.filename && rusRegex.test(b.filename);
            if (isRusA && !isRusB) return -1;
            if (isRusB && !isRusA) return 1;
            return 0;
        };
        langFiles.sort(sortRusFirst);
        otherFiles.sort(sortRusFirst);
    }
    
    renderFileListToContainer(mainFiles, elFilesListMain);
    renderFileListToContainer(langFiles, elFilesListLang);
    renderFileListToContainer(otherFiles, elFilesListOther);
    
    // Hide empty group containers
    elFileGroupLangBox.style.display = langCount > 0 ? "block" : "none";
    elFileGroupOtherBox.style.display = otherCount > 0 ? "block" : "none";
    
    // Collapse all detail sections by default when rendering
    document.querySelectorAll("#game-details-container details.file-group-collapsible").forEach(d => {
        d.open = false;
    });
    
    updateSelectionPill();
}

function updateSelectionPill() {
    const elPillsContainer = document.getElementById("selection-status-pills");
    if (!elPillsContainer) return;
    
    if (!rawFilesList || rawFilesList.length === 0) {
        elPillsContainer.innerHTML = "";
        return;
    }
    
    const rusRegex = /(?:^|[\s\.\-_])(rus|russian)(?:$|[\s\.\-_])/i;
    
    // Categorize raw files list
    const mainFiles = rawFilesList.filter(f => f.type === "game_part" || f.type === "installer");
    const optionalFiles = rawFilesList.filter(f => f.type !== "game_part" && f.type !== "installer");
    const russianFiles = optionalFiles.filter(f => f.filename && rusRegex.test(f.filename));
    const nonRussianOptional = optionalFiles.filter(f => !f.filename || !rusRegex.test(f.filename));
    
    // Check currently selected
    const mainChecked = mainFiles.every(f => checkedFiles.has(f.filename));
    const optionalChecked = optionalFiles.every(f => checkedFiles.has(f.filename));
    const optionalNoneChecked = optionalFiles.every(f => !checkedFiles.has(f.filename));
    
    const russianChecked = russianFiles.length > 0 && russianFiles.every(f => checkedFiles.has(f.filename));
    const russianNoneChecked = russianFiles.every(f => !checkedFiles.has(f.filename));
    const nonRussianOptionalNoneChecked = nonRussianOptional.every(f => !checkedFiles.has(f.filename));
    
    let state = "custom";
    let text = "Custom Selection";
    let icon = `<svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>`;
    
    if (checkedFiles.size === 0) {
        state = "none";
        text = "Deselected All";
        icon = `<svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>`;
    } else if (mainChecked && optionalNoneChecked) {
        state = "main";
        text = "Main Game Only";
        icon = `<svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>`;
    } else if (mainChecked && optionalChecked) {
        state = "full";
        text = "Full Repack";
        icon = `<svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M18 7l-1.41-1.41-6.34 6.34 1.41 1.41L18 7zm4.24-1.41L11.66 16.17 7.48 12l-1.41 1.41L11.66 19l12-12-1.42-1.41zM2 12.5l1.5-1.5L7 14.5l-1.5 1.5L2 12.5z"/></svg>`;
    } else if (russianFiles.length > 0 && mainChecked && russianChecked && nonRussianOptionalNoneChecked) {
        state = "russian";
        text = "Russian Selected";
        icon = `<svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>`;
    }
    
    elPillsContainer.innerHTML = `
        <span class="selection-pill state-${state}">
            ${icon}
            <span>${text}</span>
        </span>
    `;
}

// Checkbox selection controls
function syncGroupHeaders() {
    document.querySelectorAll(".file-group-collapsible").forEach(details => {
        const headerCheckbox = details.querySelector(".group-header-checkbox");
        if (!headerCheckbox) return;
        const childCheckboxes = details.querySelectorAll(".file-group-list input");
        let checkedCount = 0;
        childCheckboxes.forEach(cb => {
            if (cb.checked) checkedCount++;
        });
        if (checkedCount === 0) {
            headerCheckbox.checked = false;
            headerCheckbox.indeterminate = false;
        } else if (checkedCount === childCheckboxes.length) {
            headerCheckbox.checked = true;
            headerCheckbox.indeterminate = false;
        } else {
            headerCheckbox.checked = false;
            headerCheckbox.indeterminate = true;
        }
    });
    updateSelectionPill();
}

elSelMainBtn.addEventListener("click", () => {
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        const filename = cb.getAttribute("data-filename");
        const file = rawFilesList.find(f => f.filename === filename);
        if (file && (file.type === "game_part" || file.type === "installer")) {
            cb.checked = true;
            checkedFiles.add(filename);
        } else {
            cb.checked = false;
            checkedFiles.delete(filename);
        }
    });
    syncGroupHeaders();
    updateMetadataETA();
});

elSelAllBtn.addEventListener("click", () => {
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        const filename = cb.getAttribute("data-filename");
        cb.checked = true;
        checkedFiles.add(filename);
    });
    syncGroupHeaders();
    updateMetadataETA();
});

elSelNoneBtn.addEventListener("click", () => {
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        const filename = cb.getAttribute("data-filename");
        cb.checked = false;
        checkedFiles.delete(filename);
    });
    syncGroupHeaders();
    updateMetadataETA();
});

elSelRusBtn.addEventListener("click", () => {
    const rusRegex = /(?:^|[\s\.\-_])(rus|russian)(?:$|[\s\.\-_])/i;
    document.querySelectorAll(".checkbox-item input").forEach(cb => {
        const filename = cb.getAttribute("data-filename");
        if (filename && rusRegex.test(filename)) {
            cb.checked = true;
            checkedFiles.add(filename);
        }
    });
    
    syncGroupHeaders();
    updateMetadataETA();
});

elBrowseDirBtn.addEventListener("click", async () => {
    elBrowseDirBtn.setAttribute("disabled", "true");
    try {
        const response = await fetch("/api/browse_folder");
        const data = await response.json();
        if (response.ok && data.success && data.path) {
            elSaveDirInput.value = data.path;
        } else if (data.error) {
            console.log("Folder browser result:", data.error);
        }
    } catch (e) {
        console.error("Error browsing folder:", e);
        alert("Failed to open folder picker.");
    } finally {
        elBrowseDirBtn.removeAttribute("disabled");
    }
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
    const selectedFiles = rawFilesList.filter(f => checkedFiles.has(f.filename));
    
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
                base_download_dir: downloadDir,
                download_dir: downloadDir,
                files: selectedFiles,
                active_mirror: activeMirrorName
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

// Sorting select listener
elSortingSelect.addEventListener("change", () => {
    updateChecklistSorted();
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
                resetSetupDashboard();
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

// Sidebar provider switch immediately toggles the site provider
if (elChangeProviderBtn) {
    elChangeProviderBtn.addEventListener("click", () => {
        const next = activeProvider === "fitgirl" ? "onlinefix" : "fitgirl";
        switchProvider(next);
    });
}

// ViewState Router
let viewState = "catalog"; // "catalog", "details", "downloading"

function setViewState(state) {
    viewState = state;
    syncViewState();
}

function syncViewState() {
    if (appState.is_configured) {
        viewState = "downloading";
    } else if (viewState === "downloading") {
        viewState = "catalog";
    }

    if (viewState === "downloading") {
        document.querySelector(".app-container").classList.add("has-sidebar");
        document.querySelector(".sidebar").style.display = "flex";
        
        elSetupView.style.display = "none";
        elDownloadView.style.display = "flex";
        
        elSidebarSetupInfo.style.display = "none";
        elSidebarStatusSummary.style.display = "flex";
        elSidebarActionsContainer.style.display = "flex";
    } else {
        document.querySelector(".app-container").classList.remove("has-sidebar");
        document.querySelector(".sidebar").style.display = "none";
        
        elSetupView.style.display = "flex";
        elDownloadView.style.display = "none";
        
        elSidebarSetupInfo.style.display = "block";
        elSidebarStatusSummary.style.display = "none";
        elSidebarActionsContainer.style.display = "none";

        if (viewState === "catalog") {
            elCatalogContainer.classList.remove("hidden-view");
            elGameDetailsContainer.classList.add("hidden-view");
            clearDynamicBackground();
        } else if (viewState === "details") {
            elCatalogContainer.classList.add("hidden-view");
            elGameDetailsContainer.classList.remove("hidden-view");
        }
    }
}

let dynamicResetTimeout = null;

// Haze Background Swap (Harmonoid style - double-buffered cross-fade)
function setHazeBackground(coverUrl) {
    if (dynamicResetTimeout) {
        clearTimeout(dynamicResetTimeout);
        dynamicResetTimeout = null;
    }
    if (!coverUrl) {
        clearDynamicBackground();
        return;
    }
    
    const currentImg = activeHazeBuffer === 1 ? elHazeBgImg1 : elHazeBgImg2;
    const nextImg = activeHazeBuffer === 1 ? elHazeBgImg2 : elHazeBgImg1;
    
    if (currentImg.src === coverUrl && currentImg.style.opacity === "1") return;

    nextImg.onload = () => {
        nextImg.style.opacity = "1";
        currentImg.style.opacity = "0";
        activeHazeBuffer = activeHazeBuffer === 1 ? 2 : 1;
    };
    nextImg.src = coverUrl;
}

// Smoothly animate theme colors transition
function animateCSSColorVariables(targetPrimary, targetSecondary, duration = 400) {
    const startPrimary = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#a83279';
    const startSecondary = getComputedStyle(document.documentElement).getPropertyValue('--color-secondary').trim() || '#9b59b6';
    
    function parseRgb(colorStr) {
        if (colorStr.startsWith("rgb")) {
            const m = colorStr.match(/\d+/g);
            if (m) return { r: parseInt(m[0]), g: parseInt(m[1]), b: parseInt(m[2]) };
        } else if (colorStr.startsWith("#")) {
            let hex = colorStr.slice(1);
            if (hex.length === 3) hex = hex.split('').map(x => x + x).join('');
            return {
                r: parseInt(hex.slice(0, 2), 16),
                g: parseInt(hex.slice(2, 4), 16),
                b: parseInt(hex.slice(4, 6), 16)
            };
        }
        return { r: 168, g: 50, b: 121 };
    }
    
    const fromP = parseRgb(startPrimary);
    const fromS = parseRgb(startSecondary);
    const toP = parseRgb(targetPrimary);
    const toS = parseRgb(targetSecondary);
    
    const startTime = performance.now();
    
    function update(time) {
        const elapsed = time - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const ease = progress < 0.5 ? 2 * progress * progress : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        
        const rP = Math.round(fromP.r + (toP.r - fromP.r) * ease);
        const gP = Math.round(fromP.g + (toP.g - fromP.g) * ease);
        const bP = Math.round(fromP.b + (toP.b - fromP.b) * ease);
        
        const rS = Math.round(fromS.r + (toS.r - fromS.r) * ease);
        const gS = Math.round(fromS.g + (toS.g - fromS.g) * ease);
        const bS = Math.round(fromS.b + (toS.b - fromS.b) * ease);
        
        const primary = `rgb(${rP}, ${gP}, ${bP})`;
        const secondary = `rgb(${rS}, ${gS}, ${bS})`;
        const glow = `rgba(${rP}, ${gP}, ${bP}, 0.35)`;
        const border = `rgba(${rP}, ${gP}, ${bP}, 0.15)`;
        
        document.documentElement.style.setProperty('--color-primary', primary);
        document.documentElement.style.setProperty('--color-secondary', secondary);
        document.documentElement.style.setProperty('--color-primary-glow', glow);
        document.documentElement.style.setProperty('--border-glow', border);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function clearDynamicBackground() {
    if (dynamicResetTimeout) {
        clearTimeout(dynamicResetTimeout);
    }
    dynamicResetTimeout = setTimeout(() => {
        if (elHazeBgImg1) elHazeBgImg1.style.opacity = "0";
        if (elHazeBgImg2) elHazeBgImg2.style.opacity = "0";
        // Smoothly animate back to neutral purple
        animateCSSColorVariables('#a83279', '#9b59b6', 1200);
        dynamicResetTimeout = null;
    }, 500);
}

// Canvas Dynamic Accent Extraction
function updateAccentFromImage(imgElement) {
    if (dynamicResetTimeout) {
        clearTimeout(dynamicResetTimeout);
        dynamicResetTimeout = null;
    }
    if (!imgElement || !imgElement.src || imgElement.style.display === "none") {
        return;
    }

    const extract = () => {
        try {
            const canvas = document.createElement("canvas");
            canvas.width = 16;
            canvas.height = 16;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(imgElement, 0, 0, 16, 16);
            
            const imageData = ctx.getImageData(0, 0, 16, 16);
            const data = imageData.data;
            
            let rSum = 0, gSum = 0, bSum = 0, count = 0;
            let bestColor = null;
            let maxSaturation = -1;
            
            for (let i = 0; i < data.length; i += 4) {
                const r = data[i];
                const g = data[i+1];
                const b = data[i+2];
                const a = data[i+3];
                
                if (a < 200) continue;
                
                // RGB to HSL
                const rNorm = r / 255;
                const gNorm = g / 255;
                const bNorm = b / 255;
                const max = Math.max(rNorm, gNorm, bNorm);
                const min = Math.min(rNorm, gNorm, bNorm);
                let h = 0, s = 0, l = (max + min) / 2;
                
                if (max !== min) {
                    const d = max - min;
                    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
                    switch (max) {
                        case rNorm: h = (gNorm - bNorm) / d + (gNorm < bNorm ? 6 : 0); break;
                        case gNorm: h = (bNorm - rNorm) / d + 2; break;
                        case bNorm: h = (rNorm - gNorm) / d + 4; break;
                    }
                    h /= 6;
                }
                
                // Keep S > 25% and L in [30%, 75%] for a nice vibrant accent
                if (l >= 0.3 && l <= 0.75 && s >= 0.25) {
                    const energy = s * l;
                    if (energy > maxSaturation) {
                        maxSaturation = energy;
                        bestColor = { r, g, b };
                    }
                }
                
                rSum += r;
                gSum += g;
                bSum += b;
                count++;
            }
            
            let rgb = bestColor;
            if (!rgb && count > 0) {
                rgb = {
                    r: Math.floor(rSum / count),
                    g: Math.floor(gSum / count),
                    b: Math.floor(bSum / count)
                };
            }
            
            if (rgb) {
                const accent = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
                const glow = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.35)`;
                const border = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.15)`;
                
                // Calculate secondary color
                const factor = 1.2;
                const r2 = Math.min(255, Math.floor(rgb.r * factor));
                const g2 = Math.min(255, Math.floor(rgb.g * factor));
                const b2 = Math.min(255, Math.floor(rgb.b * factor));
                const secondaryAccent = `rgb(${r2}, ${g2}, ${b2})`;

                // Smoothly animate colors to dynamic values
                animateCSSColorVariables(accent, secondaryAccent, 1200);
            }
        } catch (e) {
            console.error("Color extraction exception:", e);
        }
    };

    if (imgElement.complete) {
        extract();
    } else {
        imgElement.onload = extract;
    }
}

// Catalog Pagination and State Controls
let currentPage = 1;
let activeTab = "popular-month";
let searchQuery = "";
let activeProvider = "fitgirl";

// Frontend page cache
const catalogPagesCache = new Map();
function getCatalogCacheKey(provider, page, query, tab) {
    return `${provider}_${page}_${query || ''}_${tab || ''}`;
}

const GAMEPAD_SVG = `
<svg class="gamepad-placeholder-icon" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.45; color: var(--text-muted);">
  <rect x="2" y="6" width="20" height="12" rx="3"></rect>
  <path d="M6 12h4M8 10v4"></path>
  <circle cx="15" cy="11" r="1" fill="currentColor"></circle>
  <circle cx="18" cy="13" r="1" fill="currentColor"></circle>
</svg>
`;

function renderGamesList(results) {
    elGamesGridContainer.innerHTML = "";
    if (!results || results.length === 0) {
        elGamesGridContainer.innerHTML = `<div class="no-results-message">No repacks found.</div>`;
        return;
    }
    
    results.forEach(game => {
        const card = document.createElement("div");
        card.className = "game-card";
        
        const coverUrl = game.cover_image 
            ? `/api/proxy_image?url=${encodeURIComponent(game.cover_image)}`
            : "";
            
        card.innerHTML = `
            <div class="card-cover-area">
                <div class="card-cover-placeholder">${GAMEPAD_SVG}</div>
            </div>
            <div class="card-info">
                <h4 class="card-title" title="${game.title}">${game.title}</h4>
                <div class="card-sizes" style="display: flex; align-items: center; width: 100%;">
                    ${game.repack_size !== "Unknown" ? `<span class="size-badge repack">Repack: ${game.repack_size}</span>` : ""}
                    ${game.original_size !== "Unknown" ? `<span class="size-badge original">Orig: ${game.original_size}</span>` : ""}
                </div>
            </div>
        `;
        
        if (coverUrl) {
            getCachedImageUrl(coverUrl).then(cachedUrl => {
                const coverArea = card.querySelector(".card-cover-area");
                if (coverArea) {
                    const img = document.createElement("img");
                    img.className = "card-cover";
                    img.src = cachedUrl;
                    img.alt = "Cover";
                    img.onerror = () => {
                        coverArea.innerHTML = `<div class="card-cover-placeholder">${GAMEPAD_SVG}</div>`;
                    };
                    coverArea.innerHTML = "";
                    coverArea.appendChild(img);
                }
            });
        }
        
        card.addEventListener("click", () => {
            elUrlTextarea.value = game.url;
            elAnalyzeBtn.click();
        });
        
        elGamesGridContainer.appendChild(card);
    });
}

async function loadCatalogGames() {
    elGamesLoader.style.display = "flex";
    elGamesGridContainer.innerHTML = "";
    elSearchResultsTitle.style.display = "none";
    
    const cacheKey = getCatalogCacheKey(activeProvider, currentPage, searchQuery, activeTab);
    if (catalogPagesCache.has(cacheKey)) {
        const cached = catalogPagesCache.get(cacheKey);
        renderGamesList(cached.results);
        if (cached.has_next) {
            elBtnNextPage.removeAttribute("disabled");
        } else {
            elBtnNextPage.setAttribute("disabled", "true");
        }
        elGamesLoader.style.display = "none";
        elBtnPrevPage.disabled = (currentPage === 1);
        elPageIndicator.innerText = `Page ${currentPage}`;
        if (searchQuery) {
            elSearchResultsTitle.style.display = "block";
            elSearchResultsTitle.innerText = `Search results for: "${searchQuery}"`;
        }
        return;
    }
    
    try {
        let response;
        if (searchQuery) {
            elSearchResultsTitle.style.display = "block";
            elSearchResultsTitle.innerText = `Search results for: "${searchQuery}"`;
            
            response = await fetch("/api/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: searchQuery,
                    provider: activeProvider,
                    page: currentPage
                })
            });
        } else {
            const type = (activeTab === "popular-year" ? "yearly" : "monthly");
            response = await fetch(`/api/popular?provider=${activeProvider}&type=${type}&page=${currentPage}`);
        }
        
        const data = await response.json();
        if (data.success) {
            catalogPagesCache.set(cacheKey, {
                results: data.results,
                has_next: data.has_next
            });
            renderGamesList(data.results);
            
            // Toggle pagination next button based on has_next returned from server
            if (data.has_next) {
                elBtnNextPage.removeAttribute("disabled");
            } else {
                elBtnNextPage.setAttribute("disabled", "true");
            }
        } else {
            elGamesGridContainer.innerHTML = `<div class="error-text">Failed to load catalog repacks: ${data.error}</div>`;
        }
    } catch (e) {
        console.error("Load catalog games exception:", e);
        elGamesGridContainer.innerHTML = `<div class="error-text">Connection error loading catalog repacks.</div>`;
    } finally {
        elGamesLoader.style.display = "none";
        
        // Update pagination buttons state
        elBtnPrevPage.disabled = (currentPage === 1);
        elPageIndicator.innerText = `Page ${currentPage}`;
    }
}

// Navigation event listeners
elPillPopularMonth.addEventListener("click", () => {
    elPillPopularMonth.classList.add("active");
    elPillPopularYear.classList.remove("active");
    elSearchInput.value = "";
    searchQuery = "";
    activeTab = "popular-month";
    currentPage = 1;
    loadCatalogGames();
});

elPillPopularYear.addEventListener("click", () => {
    elPillPopularMonth.classList.remove("active");
    elPillPopularYear.classList.add("active");
    elSearchInput.value = "";
    searchQuery = "";
    activeTab = "popular-year";
    currentPage = 1;
    loadCatalogGames();
});

elSearchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        const q = elSearchInput.value.trim();
        if (q) {
            searchQuery = q;
            currentPage = 1;
            elPillPopularMonth.classList.remove("active");
            elPillPopularYear.classList.remove("active");
            loadCatalogGames();
        }
    }
});

elBtnPrevPage.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        loadCatalogGames();
    }
});

elBtnNextPage.addEventListener("click", () => {
    currentPage++;
    loadCatalogGames();
});

elBtnBackToCatalog.addEventListener("click", () => {
    const elVideoIframe = document.getElementById("video-iframe");
    if (elVideoIframe) elVideoIframe.src = "";
    setViewState("catalog");
});

// Settings Modal controls
elSettingsGearBtn.addEventListener("click", () => {
    elSettingsModal.style.display = "flex";
});

const closeSettings = () => {
    elSettingsModal.style.display = "none";
};

elCloseSettingsModalBtn.addEventListener("click", closeSettings);
elSaveSettingsBtn.addEventListener("click", () => {
    const showLogs = elChkShowLogs.checked;
    elConsoleBox.parentElement.classList.toggle("hidden", !showLogs);
    localStorage.setItem("showLogs", showLogs ? "true" : "false");
    
    if (elChkRainbowBg) {
        const rainbowBg = elChkRainbowBg.checked;
        document.body.classList.toggle("rainbow-active", rainbowBg);
        localStorage.setItem("rainbowBg", rainbowBg ? "true" : "false");
    }
    
    closeSettings();
});

// Quick site switcher behavior
function switchProvider(newProvider) {
    if (activeProvider === newProvider) return;
    
    activeProvider = newProvider;
    localStorage.setItem("activeProvider", activeProvider);
    
    if (elProviderSelect) {
        elProviderSelect.value = activeProvider;
    }
    
    // Sync header quick switch toggle
    if (activeProvider === "onlinefix") {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.add("onlinefix-active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.add("active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.remove("active");
        
        elPillPopularMonth.innerText = "Latest Fixes";
        elPillPopularYear.style.display = "none";
    } else {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.remove("onlinefix-active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.add("active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.remove("active");
        
        elPillPopularMonth.innerText = "Top 50 Month";
        elPillPopularYear.style.display = "inline-block";
    }
    
    if (elChangeProviderBtn) {
        const span = elChangeProviderBtn.querySelector("span");
        if (span) {
            span.innerText = activeProvider === "onlinefix" ? "Active: Online-Fix" : "Active: FitGirl";
        }
    }
    
    if (elSearchInput) {
        elSearchInput.placeholder = activeProvider === "onlinefix" ? "Search Online-Fix..." : "Search FitGirl repacks...";
    }
    
    // Reset state
    currentPage = 1;
    searchQuery = "";
    elSearchInput.value = "";
    
    // Reset navigation pills
    elPillPopularMonth.classList.add("active");
    elPillPopularYear.classList.remove("active");
    
    loadCatalogGames();
}

// Bind sliding toggle click & drag behaviors (vertical slider)
// Bind sliding toggle click behaviors (click-to-expand vertical switcher)
if (elSiteToggleTrigger) {
    elSiteToggleTrigger.addEventListener("click", (e) => {
        e.stopPropagation();
        
        // If not expanded, expand it
        if (!elSiteToggleTrigger.classList.contains("expanded")) {
            elSiteToggleTrigger.classList.add("expanded");
            
            // Add a one-time click handler to document to close it if clicked outside
            const closeMenu = (event) => {
                if (!elSiteToggleTrigger.contains(event.target)) {
                    elSiteToggleTrigger.classList.remove("expanded");
                    document.removeEventListener("click", closeMenu);
                }
            };
            setTimeout(() => {
                document.addEventListener("click", closeMenu);
            }, 0);
        }
    });

    const labelFitgirl = document.getElementById("label-site-fitgirl");
    const labelOnlineFix = document.getElementById("label-site-onlinefix");

    if (labelFitgirl) {
        labelFitgirl.addEventListener("click", (e) => {
            if (elSiteToggleTrigger.classList.contains("expanded")) {
                e.stopPropagation();
                elSiteToggleTrigger.classList.remove("expanded");
                if (activeProvider !== "fitgirl") {
                    switchProvider("fitgirl");
                }
            }
        });
    }

    if (labelOnlineFix) {
        labelOnlineFix.addEventListener("click", (e) => {
            if (elSiteToggleTrigger.classList.contains("expanded")) {
                e.stopPropagation();
                elSiteToggleTrigger.classList.remove("expanded");
                if (activeProvider !== "onlinefix") {
                    switchProvider("onlinefix");
                }
            }
        });
    }
}

// Catalog Title Click Navigation
if (elCatalogTitle) {
    elCatalogTitle.addEventListener("click", () => {
        currentPage = 1;
        searchQuery = "";
        activeTab = "popular-month";
        if (elSearchInput) elSearchInput.value = "";
        if (elPillPopularMonth) elPillPopularMonth.classList.add("active");
        if (elPillPopularYear) elPillPopularYear.classList.remove("active");
        viewState = "catalog";
        syncViewState();
        loadCatalogGames();
    });
}

// Centered manual input toggler
if (elToggleManualInputBtn && elUrlInputCard) {
    elToggleManualInputBtn.addEventListener("click", () => {
        if (elUrlInputCard.style.display === "none" || elUrlInputCard.style.display === "") {
            elUrlInputCard.style.display = "block";
            elToggleManualInputBtn.classList.add("active");
            elToggleManualInputBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
                </svg>
            `;
        } else {
            elUrlInputCard.style.display = "none";
            elToggleManualInputBtn.classList.remove("active");
            elToggleManualInputBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                </svg>
            `;
        }
    });
}

// Initialize Settings state on startup
function initSettings() {
    activeProvider = localStorage.getItem("activeProvider") || "fitgirl";
    const showLogs = localStorage.getItem("showLogs") === "true"; // False by default
    const rainbowBg = localStorage.getItem("rainbowBg") === "true";
    
    if (elProviderSelect) {
        elProviderSelect.value = activeProvider;
    }
    elChkShowLogs.checked = showLogs;
    if (elChkRainbowBg) {
        elChkRainbowBg.checked = rainbowBg;
    }
    document.body.classList.toggle("rainbow-active", rainbowBg);
    
    elConsoleBox.parentElement.classList.toggle("hidden", !showLogs);
    
    if (activeProvider === "onlinefix") {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.add("onlinefix-active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.add("active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.remove("active");
        
        elPillPopularMonth.innerText = "Latest Fixes";
        elPillPopularYear.style.display = "none";
    } else {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.remove("onlinefix-active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.add("active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.remove("active");
        
        elPillPopularMonth.innerText = "Top 50 Month";
        elPillPopularYear.style.display = "inline-block";
    }
    
    if (elChangeProviderBtn) {
        const span = elChangeProviderBtn.querySelector("span");
        if (span) {
            span.innerText = activeProvider === "onlinefix" ? "Active: Online-Fix" : "Active: FitGirl";
        }
    }
    
    if (elSearchInput) {
        elSearchInput.placeholder = activeProvider === "onlinefix" ? "Search Online-Fix..." : "Search FitGirl repacks...";
    }
}

// Fallback wheel scroll event listener to fix Electron/Chromium nested scrollbar bugs
const elChecklistContainer = document.querySelector(".files-checklist-container");
if (elChecklistContainer) {
    elChecklistContainer.addEventListener("wheel", (e) => {
        elChecklistContainer.scrollTop += e.deltaY;
    }, { passive: true });
}

// Start Application logic
initSettings();
syncViewState();
loadCatalogGames();

// Screenshot modal controls
function openScreenshotModal(imgSrc) {
    if (elScreenshotModal && elScreenshotModalImg) {
        elScreenshotModalImg.src = imgSrc;
        elScreenshotModal.style.display = "flex";
    }
}

if (elCloseScreenshotModalBtn) {
    elCloseScreenshotModalBtn.addEventListener("click", () => {
        if (elScreenshotModal) elScreenshotModal.style.display = "none";
    });
}

if (elScreenshotModal) {
    elScreenshotModal.addEventListener("click", (e) => {
        if (e.target === elScreenshotModal) {
            elScreenshotModal.style.display = "none";
        }
    });
}

// Start Polling Loop
fetchState();
setInterval(fetchState, 1000);
