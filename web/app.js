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
const elChkGofileProxy = document.getElementById("chk-gofile-proxy");
const elChkHideGDrive = document.getElementById("chk-hide-gdrive");

// Google Drive Elements
const elGDriveCleanupBtn = document.getElementById("btn-gdrive-cleanup");
const elAddGDriveAccountBtn = document.getElementById("btn-add-gdrive-account");

const elGDriveAccountsList = document.getElementById("gdrive-accounts-list");

let isShowingPixeldrainLimitAlert = false;

// WARP Modal Elements
const elWarpModal = document.getElementById("warp-modal");
const elWarpSpinner = document.getElementById("warp-spinner");
const elWarpWarningIcon = document.getElementById("warp-warning-icon");
const elWarpModalTitle = document.getElementById("warp-modal-title");
const elWarpModalMessage = document.getElementById("warp-modal-message");
const elWarpSkipBtn = document.getElementById("btn-skip-warp");
const elWarpRetryBtn = document.getElementById("btn-retry-warp");

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

function handleWarpState(newState) {
    if (!elWarpModal) return;
    
    const status = newState.warp_status;
    if (status === "checking") {
        elWarpModal.style.display = "flex";
        elWarpSpinner.style.display = "block";
        elWarpWarningIcon.style.display = "none";
        elWarpModalTitle.innerText = "Checking Cloudflare WARP";
        elWarpModalMessage.innerText = "Checking if Cloudflare WARP is installed on your PC...";
        elWarpSkipBtn.style.display = "none";
        elWarpRetryBtn.style.display = "none";
    } else if (status === "installing") {
        elWarpModal.style.display = "flex";
        elWarpSpinner.style.display = "block";
        elWarpWarningIcon.style.display = "none";
        elWarpModalTitle.innerText = "Installing Cloudflare WARP";
        elWarpModalMessage.innerText = "Downloading and silently installing Cloudflare WARP...";
        elWarpSkipBtn.style.display = "none";
        elWarpRetryBtn.style.display = "none";
    } else if (status === "error") {
        elWarpModal.style.display = "flex";
        elWarpSpinner.style.display = "none";
        elWarpWarningIcon.style.display = "block";
        elWarpModalTitle.innerText = "Cloudflare WARP Required";
        elWarpModalMessage.innerText = newState.warp_error_message || "Cloudflare WARP is not installed and silent installation failed.";
        elWarpSkipBtn.style.display = "block";
        elWarpRetryBtn.style.display = "block";
    } else {
        // installed or skipped
        elWarpModal.style.display = "none";
    }
}

// Update UI based on loaded state
function updateUI(newState) {
    handleWarpState(newState);
    
    // Pixeldrain limit warning modal trigger
    if (newState.pixeldrain_limit_reached && !isShowingPixeldrainLimitAlert) {
        isShowingPixeldrainLimitAlert = true;
        Swal.fire({
            title: 'Pixeldrain Limit Reached',
            text: "You have reached Pixeldrain's daily free bandwidth limit (6 GB). Speed is throttled to 1 MB/s total. Please enable a VPN or Cloudflare WARP, then Pause and Resume the download in this app to reconnect at high speed.",
            icon: 'warning',
            confirmButtonText: 'OK',
            confirmButtonColor: '#9b59b6',
            background: '#040409',
            color: '#e2e2ec'
        }).then(() => {
            fetch("/api/clear_pixeldrain_limit");
            isShowingPixeldrainLimitAlert = false;
        });
    }

    // 1. Manage setup vs download views
    syncViewState();
    
    if (newState.is_configured) {
        // Populate display info
        elActiveGameTitle.innerText = newState.game_title || "Custom Repack";
        elActiveGameSubtitle.innerText = `Save directory: ${newState.download_dir}`;
        elDownloadDirDisplay.value = newState.download_dir;
        
        const elActiveGameOriginalSize = document.getElementById("active-game-original-size");
        if (elActiveGameOriginalSize) {
            if (newState.original_size && newState.original_size !== "Unknown") {
                elActiveGameOriginalSize.innerText = `Size after unpacking: ${newState.original_size}`;
                elActiveGameOriginalSize.style.display = "block";
            } else {
                elActiveGameOriginalSize.style.display = "none";
            }
        }
        
        // Sync mirror badge
        if (newState.active_mirror) {
            elDownloadMirrorBadge.innerText = `Mirror: ${newState.active_mirror}`;
            elDownloadMirrorBadge.style.display = "inline-block";
        } else {
            elDownloadMirrorBadge.style.display = "none";
        }
        
        // Google Drive manual cleanup button toggle
        const isOnlineFixMirror = newState.active_mirror && 
            (newState.active_mirror.toLowerCase().includes("online-fix") || 
             newState.active_mirror.toLowerCase().includes("onlinefix") ||
             newState.active_mirror.toLowerCase().includes("google") ||
             newState.active_mirror.toLowerCase().includes("own google") ||
             newState.active_mirror.toLowerCase().includes("disk"));
        const hasGDriveFiles = newState.files && newState.files.some(f => f.url && f.url.includes("drive.online-fix.me"));
        
        if (elGDriveCleanupBtn) {
            if (isOnlineFixMirror || hasGDriveFiles) {
                elGDriveCleanupBtn.style.display = "inline-flex";
            } else {
                elGDriveCleanupBtn.style.display = "none";
            }
        }
        
        // Sync worker select
        if (newState.max_workers && elThreadsSelect.value !== String(newState.max_workers) && document.activeElement !== elThreadsSelect) {
            elThreadsSelect.value = String(newState.max_workers);
        }
        
        // Sync Play/Pause Button & Status Badge
        const elDownloadStatusBadge = document.getElementById("download-status-badge");
        if (newState.is_running) {
            elStartPauseBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                </svg>
                <span>Pause</span>
            `;
            elStartPauseBtn.classList.remove("btn-pulse");
            elStartPauseBtn.style.backgroundColor = "#e67e22";
            elStartPauseBtn.style.borderColor = "#d35400";
            
            if (elDownloadStatusBadge) {
                elDownloadStatusBadge.innerText = "DOWNLOADING";
                elDownloadStatusBadge.style.background = "rgba(155, 89, 182, 0.15)";
                elDownloadStatusBadge.style.borderColor = "rgba(155, 89, 182, 0.35)";
                elDownloadStatusBadge.style.color = "#be90d4";
            }
        } else {
            elStartPauseBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                </svg>
                <span>Resume</span>
            `;
            elStartPauseBtn.classList.add("btn-pulse");
            elStartPauseBtn.style.backgroundColor = ""; // reset to primary
            elStartPauseBtn.style.borderColor = "";
            
            if (elDownloadStatusBadge) {
                elDownloadStatusBadge.innerText = "PAUSED";
                elDownloadStatusBadge.style.background = "rgba(230, 126, 34, 0.15)";
                elDownloadStatusBadge.style.borderColor = "rgba(230, 126, 34, 0.35)";
                elDownloadStatusBadge.style.color = "#f39c12";
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
            elExtractBtn.style.display = "none";
            elInstallBtn.style.display = "none";
            
            elExtractBtn.setAttribute("disabled", "true");
            elExtractBtn.classList.remove("btn-pulse-green");
            elExtractBtn.style.backgroundColor = "";
            elExtractBtn.querySelector("span").innerText = "Extract Archives";
            
            elInstallBtn.setAttribute("disabled", "true");
            elInstallBtn.classList.remove("btn-pulse-green");
            elInstallBtn.style.backgroundColor = "";
        } else {
            if (newState.is_extracted) {
                elExtractBtn.style.display = "none";
                elInstallBtn.style.display = "flex";
                
                elExtractBtn.setAttribute("disabled", "true");
                elExtractBtn.classList.remove("btn-pulse-green");
                elExtractBtn.style.backgroundColor = "#2c3e50";
                elExtractBtn.querySelector("span").innerText = "Archives Extracted";
                
                elInstallBtn.removeAttribute("disabled");
                elInstallBtn.classList.add("btn-pulse-green");
                elInstallBtn.style.backgroundColor = "#2ecc71";
            } else {
                elExtractBtn.style.display = "flex";
                elInstallBtn.style.display = "none";
                
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
            // Group files by Part base name to collapse them
            const groupCounts = {};
            newState.files.forEach(f => {
                const info = getPartGroupInfo(f.filename);
                if (info) {
                    groupCounts[info.base] = (groupCounts[info.base] || 0) + 1;
                }
            });

            const renderedGroups = new Set();
            const getGroupFiles = (baseName) => {
                return newState.files
                    .map((file, idx) => ({ file, idx }))
                    .filter(item => {
                        const info = getPartGroupInfo(item.file.filename);
                        return info && info.base === baseName;
                    });
            };

            newState.files.forEach((file, index) => {
                const info = getPartGroupInfo(file.filename);
                if (info && groupCounts[info.base] > 1) {
                    const baseName = info.base;
                    if (renderedGroups.has(baseName)) return; // Already rendered this group
                    renderedGroups.add(baseName);
                    
                    const groupItems = getGroupFiles(baseName);
                    
                    // Render collapsible group details
                    const details = document.createElement("details");
                    details.className = "queue-group-collapsible";
                    details.open = false; // Collapsed by default (прикрыто по умолчанию)
                    
                    // Calculate group aggregates
                    const totalSize = groupItems.reduce((sum, item) => sum + (item.file.size || 0), 0);
                    const totalDownloaded = groupItems.reduce((sum, item) => sum + (item.file.downloaded || 0), 0);
                    const groupProgress = totalSize > 0 ? Math.min(100, Math.floor((totalDownloaded / totalSize) * 100)) : 0;
                    const groupSpeed = groupItems.reduce((sum, item) => sum + (item.file.speed || 0), 0);
                    
                    // Determine overall status
                    let overallStatus = "waiting";
                    const statuses = groupItems.map(item => item.file.status);
                    if (statuses.includes("downloading")) overallStatus = "downloading";
                    else if (statuses.includes("copying")) overallStatus = "copying";
                    else if (statuses.includes("connecting")) overallStatus = "connecting";
                    else if (statuses.every(s => s === "finished")) overallStatus = "finished";
                    else if (statuses.every(s => s === "failed" || s === "finished")) {
                        if (statuses.includes("failed")) overallStatus = "failed";
                        else overallStatus = "finished";
                    }
                    
                    let activeClass = (overallStatus === "downloading" || overallStatus === "connecting" || overallStatus === "copying") ? "active" : "";
                    const sizeText = totalSize > 0 ? formatBytes(totalSize) : "Pending...";
                    const speedText = overallStatus === "downloading" ? formatSpeed(groupSpeed) : "";
                    
                    details.innerHTML = `
                        <summary class="queue-group-summary ${activeClass}">
                            <div class="summary-header">
                                <span class="summary-toggle-icon">⏵</span>
                                <div class="file-name" title="${baseName}">${baseName} (${groupItems.length} Parts)</div>
                                <div class="file-badge game_part">Part Files</div>
                                <div class="file-progress-container">
                                    <div class="progress-bar-bg">
                                        <div class="progress-bar-fill" style="width: ${groupProgress}%"></div>
                                    </div>
                                    <div class="file-progress-text">
                                        <span>${groupProgress}% (${formatBytes(totalDownloaded)} of ${sizeText})</span>
                                        <span class="file-speed">${speedText}</span>
                                    </div>
                                </div>
                                <div class="file-status ${overallStatus}">${overallStatus}</div>
                                <div class="file-actions">
                                    ${statuses.includes("failed") ? `<button class="btn btn-accent btn-retry-group">Retry Failed</button>` : ""}
                                </div>
                            </div>
                        </summary>
                        <div class="queue-group-list"></div>
                    `;
                    
                    // Render children
                    const listDiv = details.querySelector(".queue-group-list");
                    groupItems.sort((a, b) => {
                        const infoA = getPartGroupInfo(a.file.filename);
                        const infoB = getPartGroupInfo(b.file.filename);
                        return (infoA ? infoA.partNum : 0) - (infoB ? infoB.partNum : 0);
                    });
                    
                    groupItems.forEach(item => {
                        const childFile = item.file;
                        const childIndex = item.idx;
                        const childItem = document.createElement("div");
                        childItem.className = "queue-item child-item";
                        if (childFile.status === "downloading" || childFile.status === "connecting") {
                            childItem.classList.add("active");
                        }
                        
                        const childSizeText = childFile.size > 0 ? formatBytes(childFile.size) : "Pending...";
                        const childSpeedText = childFile.status === "downloading" ? formatSpeed(childFile.speed) : "";
                        
                        childItem.innerHTML = `
                            <div class="file-name" title="${childFile.filename}">${cleanFilename(childFile.filename)}</div>
                            <div class="file-progress-container">
                                <div class="progress-bar-bg">
                                    <div class="progress-bar-fill" style="width: ${childFile.progress}%"></div>
                                </div>
                                <div class="file-progress-text">
                                    <span>${childFile.progress}% (${formatBytes(childFile.downloaded)} of ${childSizeText})</span>
                                    <span class="file-speed">${childSpeedText}</span>
                                </div>
                            </div>
                            <div class="file-status ${childFile.status}">${childFile.status}</div>
                            <div class="file-actions">
                                ${childFile.status === "failed" ? `<button class="btn btn-accent btn-retry" onclick="triggerRetry(${childIndex})">Retry</button>` : ""}
                            </div>
                        `;
                        listDiv.appendChild(childItem);
                    });
                    
                    // Bind retry group button
                    const retryGroupBtn = details.querySelector(".btn-retry-group");
                    if (retryGroupBtn) {
                        retryGroupBtn.addEventListener("click", (e) => {
                            e.stopPropagation();
                            e.preventDefault();
                            groupItems.forEach(item => {
                                if (item.file.status === "failed") {
                                    triggerRetry(item.idx);
                                }
                            });
                        });
                    }
                    
                    elQueueContainer.appendChild(details);
                } else {
                    // Render single file
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
                }
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
    
    updateMiniBadge(newState);
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
    if (typeof resetTranslationCache === "function") resetTranslationCache();
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
                
                // Render Hero Banner backdrop
                const heroBanner = document.getElementById("details-hero-banner");
                const detailsSubtitle = document.getElementById("details-game-subtitle");
                if (heroBanner) {
                    const bannerUrl = data.header_image || (data.screenshots && data.screenshots.length > 0 ? data.screenshots[0] : scrapedMetadata.cover_image);
                    if (bannerUrl) {
                        heroBanner.style.backgroundImage = `url(${bannerUrl})`;
                    } else {
                        heroBanner.style.backgroundImage = "none";
                    }
                }
                if (detailsSubtitle) {
                    detailsSubtitle.innerText = data.developer || "FitGirl Repack";
                }
                
                // Render description / About the Game
                const descSection = document.getElementById("details-desc-section");
                if (descSection && elGameDescription) {
                    if (data.description) {
                        elGameDescription.innerHTML = data.description.replace(/\n/g, "<br>");
                        descSection.style.display = "block";
                    } else {
                        descSection.style.display = "none";
                    }
                }
                
                // Render Repack Features list
                const featuresSection = document.getElementById("details-features-section");
                const featuresList = document.getElementById("repack-features-list");
                if (featuresSection && featuresList) {
                    if (data.repack_features && data.repack_features.length > 0) {
                        featuresList.innerHTML = "";
                        data.repack_features.forEach(feat => {
                            const li = document.createElement("li");
                            li.innerText = feat;
                            featuresList.appendChild(li);
                        });
                        featuresSection.style.display = "block";
                    } else {
                        featuresSection.style.display = "none";
                    }
                }

                // Bind collapsible header toggle behaviors
                const descHeader = document.getElementById("details-desc-header");
                if (descHeader) {
                    descHeader.onclick = () => {
                        const parent = descHeader.parentElement;
                        parent.classList.toggle("active");
                        const titleEl = descHeader.querySelector(".section-title");
                        titleEl.innerText = parent.classList.contains("active") ? "− Game Description" : "+ Game Description";
                    };
                    descHeader.parentElement.classList.remove("active");
                    const titleEl = descHeader.querySelector(".section-title");
                    if (titleEl) titleEl.innerText = "+ Game Description";
                }
                
                const featuresHeader = document.getElementById("details-features-header");
                if (featuresHeader) {
                    featuresHeader.onclick = () => {
                        const parent = featuresHeader.parentElement;
                        parent.classList.toggle("active");
                        const titleEl = featuresHeader.querySelector(".section-title");
                        titleEl.innerText = parent.classList.contains("active") ? "− Repack Features" : "+ Repack Features";
                    };
                    featuresHeader.parentElement.classList.remove("active");
                    const titleEl = featuresHeader.querySelector(".section-title");
                    if (titleEl) titleEl.innerText = "+ Repack Features";
                }

                // Bind Sticky Top Header Buttons
                const btnBackTop = document.getElementById("btn-back-to-catalog-top");
                if (btnBackTop) {
                    btnBackTop.onclick = () => {
                        setViewState("catalog");
                    };
                }
                const btnOpenBrowserTop = document.getElementById("btn-open-browser-top");
                if (btnOpenBrowserTop && url) {
                    btnOpenBrowserTop.href = url;
                    btnOpenBrowserTop.style.display = "flex";
                } else if (btnOpenBrowserTop) {
                    btnOpenBrowserTop.style.display = "none";
                }

                // Render Screenshots & Videos Gallery
                renderScreenshots(data.screenshots, data.videos);
                updateMiniBadge(appState);
                
                // Populate FitGirl website metadata fields
                const rowFgGenres = document.getElementById("row-fg-genres");
                const elFgGenres = document.getElementById("details-fg-genres");
                if (rowFgGenres && elFgGenres) {
                    if (data.genres_tags) {
                        elFgGenres.innerText = data.genres_tags;
                        rowFgGenres.style.display = "flex";
                    } else {
                        rowFgGenres.style.display = "none";
                    }
                }

                const rowFgCompany = document.getElementById("row-fg-company");
                const elFgCompany = document.getElementById("details-fg-company");
                if (rowFgCompany && elFgCompany) {
                    if (data.company) {
                        elFgCompany.innerText = data.company;
                        rowFgCompany.style.display = "flex";
                    } else {
                        rowFgCompany.style.display = "none";
                    }
                }

                const rowFgLanguages = document.getElementById("row-fg-languages");
                const elFgLanguages = document.getElementById("details-fg-languages");
                if (rowFgLanguages && elFgLanguages) {
                    if (data.languages) {
                        elFgLanguages.innerText = data.languages;
                        rowFgLanguages.style.display = "flex";
                    } else {
                        rowFgLanguages.style.display = "none";
                    }
                }

                const rowFgOrigSize = document.getElementById("row-fg-orig-size");
                const elFgOrigSize = document.getElementById("details-fg-orig-size");
                if (rowFgOrigSize && elFgOrigSize) {
                    if (data.original_size && data.original_size !== "Unknown") {
                        elFgOrigSize.innerText = data.original_size;
                        rowFgOrigSize.style.display = "flex";
                    } else {
                        rowFgOrigSize.style.display = "none";
                    }
                }

                const rowFgRepackSize = document.getElementById("row-fg-repack-size");
                const elFgRepackSize = document.getElementById("details-fg-repack-size");
                if (rowFgRepackSize && elFgRepackSize) {
                    if (data.repack_size && data.repack_size !== "Unknown") {
                        elFgRepackSize.innerText = data.repack_size;
                        rowFgRepackSize.style.display = "flex";
                    } else {
                        rowFgRepackSize.style.display = "none";
                    }
                }
                
                // Update sticky bottom download bar repack size
                const detailsBottomBar = document.getElementById("details-bottom-bar");
                const detailsBottomSize = document.getElementById("details-bottom-size");
                if (detailsBottomBar && detailsBottomSize) {
                    detailsBottomSize.innerText = scrapedMetadata.repack_size !== "Unknown" ? scrapedMetadata.repack_size : "Size Unknown";
                    detailsBottomBar.style.display = "flex";
                }
                
                const detailsCoverCard = document.getElementById("details-cover-card");
                const detailsCoverImage = document.getElementById("details-cover-image");
                const detailsCoverPlaceholder = document.getElementById("details-cover-placeholder");

                if (scrapedMetadata.cover_image) {
                    const proxiedUrl = `/api/proxy_image?url=${encodeURIComponent(scrapedMetadata.cover_image)}`;
                    getCachedImageUrl(proxiedUrl).then(cachedUrl => {
                        elSetupCover.src = cachedUrl;
                        elSetupCover.style.display = "block";
                        elSetupCoverPlaceholder.style.display = "none";
                        
                        if (detailsCoverImage) {
                            detailsCoverImage.src = cachedUrl;
                            detailsCoverImage.style.display = "block";
                        }
                        if (detailsCoverPlaceholder) detailsCoverPlaceholder.style.display = "none";
                        if (detailsCoverCard) detailsCoverCard.style.display = "block";

                        elSetupCover.onerror = () => {
                            elSetupCover.src = "";
                            elSetupCover.style.display = "none";
                            elSetupCoverPlaceholder.style.display = "flex";
                            
                            if (detailsCoverImage) {
                                detailsCoverImage.src = "";
                                detailsCoverImage.style.display = "none";
                            }
                            if (detailsCoverPlaceholder) detailsCoverPlaceholder.style.display = "flex";
                            clearDynamicBackground();
                        };
                        setHazeBackground(cachedUrl);
                        updateAccentFromImage(elSetupCover);
                    });
                } else {
                    elSetupCover.src = "";
                    elSetupCover.style.display = "none";
                    elSetupCoverPlaceholder.style.display = "flex";
                    
                    if (detailsCoverImage) {
                        detailsCoverImage.src = "";
                        detailsCoverImage.style.display = "none";
                    }
                    if (detailsCoverPlaceholder) detailsCoverPlaceholder.style.display = "flex";
                    if (detailsCoverCard) detailsCoverCard.style.display = "none";
                    clearDynamicBackground();
                }

                // Show game title
                elGameNameInput.value = data.title;
                
                // Prefill default directory
                const defaultDir = appState.default_download_dir || "D:\\Downloads";
                elSaveDirInput.value = defaultDir;
                
                // Store mirrors list for provider switching
                scrapedMirrors = data.mirrors || [];
                
                const hideGDrive = localStorage.getItem("hideGDrive") !== "false";
                const filteredMirrors = (data.mirrors || []).filter(m => {
                    if (hideGDrive) {
                        const name = m.name.toLowerCase();
                        return !(name.includes("google") || name.includes("gdrive") || name.includes("drive") || name.includes("disk") || name.includes("диск") || name.includes("гугл"));
                    }
                    return true;
                });

                if (filteredMirrors.length > 0) {
                    elMirrorSelectSection.style.display = "block";
                    elMirrorsContainer.innerHTML = "";
                    
                    filteredMirrors.forEach((m, idx) => {
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
                    
                    // Populate new premium modal mirrors list
                    populateModalMirrors(filteredMirrors);
                    
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

                renderScreenshots(data.screenshots, data.videos);

                // Toggle media column visibility and columns
                const elMediaColumnCard = document.getElementById("media-column-card");
                const hasMedia = (data.videos && data.videos.length > 0) || (data.screenshots && data.screenshots.length > 0);
                if (elMediaColumnCard) {
                    elMediaColumnCard.style.display = hasMedia ? "flex" : "none";
                }
                
                if (elGameInfoCard) {
                    if (data.description) {
                        elGameInfoCard.style.display = "block";
                    } else {
                        elGameInfoCard.style.display = "none";
                    }
                }
                
                if (elSetupDashboard) {
                    if (hasMedia) {
                        elSetupDashboard.style.setProperty("--details-grid-columns", "260px 1.15fr 0.85fr");
                    } else {
                        elSetupDashboard.style.setProperty("--details-grid-columns", "260px 1fr");
                    }
                    elSetupDashboard.classList.toggle("no-info-card", !data.description);
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
            if (viewState === "details") {
                alert("Failed to load game details: " + (data.error || "Check logs."));
                setViewState("catalog");
            }
        }
    } catch (e) {
        console.error("Error analyzing:", e);
        elAnalyzeError.style.display = "block";
        elAnalyzeError.innerText = "Connection error. Make sure Python server is running.";
        if (viewState === "details") {
            alert("Connection error while loading game details.");
            setViewState("catalog");
        }
    } finally {
        const elDetailsLoader = document.getElementById("details-page-loader");
        if (elDetailsLoader) elDetailsLoader.style.display = "none";
        elSetupDashboard.style.display = "grid";
        
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
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
        controller.abort();
    }, 20000); // 20s timeout
    
    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: mirrorUrl }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
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
        clearTimeout(timeoutId);
        console.error("Error loading mirror:", e);
        if (e.name === 'AbortError') {
            alert("Timeout loading mirror links. Please try another mirror or check server status.");
        } else {
            alert("Failed to load mirror. Check internet connection.");
        }
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
    
    // Reset Hero Banner and Subtitle
    const heroBanner = document.getElementById("details-hero-banner");
    const detailsSubtitle = document.getElementById("details-game-subtitle");
    if (heroBanner) {
        heroBanner.style.backgroundImage = "none";
    }
    if (detailsSubtitle) {
        detailsSubtitle.innerText = "Direct Link Queue";
    }
    
    // Hide details page dynamic parts
    const descSection = document.getElementById("details-desc-section");
    if (descSection) descSection.style.display = "none";
    
    const elScreenshotsSection = document.getElementById("game-screenshots-section");
    const elScreenshotsContainer = document.getElementById("game-screenshots-container");
    if (elScreenshotsSection) elScreenshotsSection.style.display = "none";
    if (elScreenshotsContainer) elScreenshotsContainer.innerHTML = "";
    
    const detailsCoverCard = document.getElementById("details-cover-card");
    if (detailsCoverCard) detailsCoverCard.style.display = "none";
    
    // Reset metadata sidebar table
    const sidebarRows = ["row-developer", "row-publisher", "row-release-date", "row-steam-rating", "row-genres", "row-unpack-size"];
    sidebarRows.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    });
    
    const metacriticCard = document.getElementById("details-metacritic-card");
    if (metacriticCard) metacriticCard.style.display = "none";
    
    const detailsBottomBar = document.getElementById("details-bottom-bar");
    const detailsBottomSize = document.getElementById("details-bottom-size");
    if (detailsBottomBar && detailsBottomSize) {
        detailsBottomSize.innerText = "Direct Link";
        detailsBottomBar.style.display = "flex";
    }
    
    clearDynamicBackground();
    
    rawFilesList = files;
    initCheckedFiles(files);
    
    configureRussianSorting(files);
    
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
async function confirmDownloadQueue(gameTitle, downloadDir) {
    if (!gameTitle || !downloadDir) {
        alert("Please enter a game folder name and select a save directory.");
        return false;
    }
    
    // Gather checked files
    const selectedFiles = rawFilesList.filter(f => checkedFiles.has(f.filename));
    
    if (selectedFiles.length === 0) {
        alert("Please select at least one file to download.");
        return false;
    }
    
    if (elConfirmQueueBtn) {
        elConfirmQueueBtn.setAttribute("disabled", "true");
        elConfirmQueueBtn.innerText = "Configuring Queue...";
    }
    if (elModalStartDownloadBtn) {
        elModalStartDownloadBtn.setAttribute("disabled", "true");
        const span = elModalStartDownloadBtn.querySelector("span");
        if (span) span.innerText = "Starting...";
    }
    
    try {
        const response = await fetch("/api/confirm_config", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                game_title: gameTitle,
                base_download_dir: downloadDir,
                download_dir: downloadDir,
                files: selectedFiles,
                active_mirror: activeMirrorName,
                original_size: scrapedMetadata.original_size,
                gofile_proxy: elChkGofileProxy ? elChkGofileProxy.checked : false
            })
        });
        
        const data = await response.json();
        if (response.ok && data.success) {
            fetchState();
            await fetch("/api/start", { method: "POST" });
            fetchState();
            
            if (downloadConfigModal) {
                downloadConfigModal.classList.remove("active");
                setTimeout(() => {
                    downloadConfigModal.style.display = "none";
                }, 250);
            }
            return true;
        } else {
            alert("Configuration failed: " + (data.error || "Unknown error"));
        }
    } catch (e) {
        console.error("Error setting config:", e);
        alert("Connection error setting configuration.");
    } finally {
        if (elConfirmQueueBtn) {
            elConfirmQueueBtn.removeAttribute("disabled");
            elConfirmQueueBtn.innerText = "Confirm and Start Download";
        }
        if (elModalStartDownloadBtn) {
            elModalStartDownloadBtn.removeAttribute("disabled");
            const span = elModalStartDownloadBtn.querySelector("span");
            if (span) span.innerText = "Next";
        }
    }
    return false;
}

elConfirmQueueBtn.addEventListener("click", () => {
    const gameTitle = elGameNameInput.value.trim();
    const downloadDir = elSaveDirInput.value.trim();
    confirmDownloadQueue(gameTitle, downloadDir);
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
        await fetch("/api/retry", { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ index })
        });
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

function updateMiniBadge(newState) {
    const elMiniBadge = document.getElementById("floating-download-badge");
    if (!elMiniBadge) return;
    
    if (newState.is_configured && viewState !== "downloading") {
        elMiniBadge.style.display = "flex";
        
        const elMiniTitle = document.getElementById("mini-game-title");
        const elMiniEta = document.getElementById("mini-game-eta");
        const elMiniStatus = document.getElementById("mini-game-status");
        const elMiniProgressBarFill = document.getElementById("mini-progress-bar-fill");
        
        if (elMiniTitle) elMiniTitle.innerText = newState.game_title || "Downloading";
        
        // Check if there is an active downloading task or install/extract
        const isDownloading = newState.files && newState.files.some(f => f.status === "downloading");
        
        // speed and progress
        const speedText = isDownloading ? formatSpeed(smoothedSpeed > 0 ? smoothedSpeed : newState.total_speed) : "0.0 MB/s";
        
        // Format downloaded / total size
        const totalBytes = newState.files ? newState.files.reduce((acc, f) => acc + (f.size || 0), 0) : 0;
        const downloadedBytes = newState.files ? newState.files.reduce((acc, f) => acc + (f.downloaded || 0), 0) : 0;
        const totalSizeText = formatBytes(totalBytes);
        const downloadedSizeText = formatBytes(downloadedBytes);
        
        if (elMiniStatus) {
            elMiniStatus.innerText = `${speedText} | ${downloadedSizeText} / ${totalSizeText}`;
        }
        
        // ETA calculation
        if (elMiniEta) {
            if (newState.is_running && isDownloading && smoothedSpeed > 0) {
                const remainingBytes = totalBytes - downloadedBytes;
                const etaSeconds = Math.max(0, remainingBytes / smoothedSpeed);
                elMiniEta.innerText = "Remaining: " + formatTime(etaSeconds);
            } else if (!newState.is_running) {
                elMiniEta.innerText = "Paused";
            } else {
                elMiniEta.innerText = "Checking files...";
            }
        }
        
        if (elMiniProgressBarFill) {
            elMiniProgressBarFill.style.width = `${newState.total_progress}%`;
        }

        // Update the play/pause button state in mini-badge
        const playPauseBtn = document.getElementById("mini-btn-play-pause");
        if (playPauseBtn) {
            playPauseBtn.innerHTML = newState.is_running ? `
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                </svg>
            ` : `
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                </svg>
            `;
        }
        // Dynamic positioning of the floating badge based on active game view
        const elDetailsGameTitle = document.getElementById("details-game-title");
        const isViewingActiveGame = viewState === "details" && 
                                    elDetailsGameTitle && 
                                    elDetailsGameTitle.innerText === newState.game_title;
        
        const detailsBottomBar = document.getElementById("details-bottom-bar");
        
        if (isViewingActiveGame) {
            // Move to bottom, covering the download trigger button
            elMiniBadge.style.top = "auto";
            elMiniBadge.style.bottom = "24px";
            elMiniBadge.style.transform = "translateX(-50%)";
            
            if (detailsBottomBar) {
                detailsBottomBar.style.display = "none";
            }
        } else {
            // Move to top (dynamic island)
            elMiniBadge.style.top = "24px";
            elMiniBadge.style.bottom = "auto";
            elMiniBadge.style.transform = "translateX(-50%)";
            
            if (viewState === "details" && detailsBottomBar) {
                detailsBottomBar.style.display = "flex";
            }
        }
    } else {
        elMiniBadge.style.display = "none";
        
        // Show details bottom bar if we are not downloading this game anymore
        const detailsBottomBar = document.getElementById("details-bottom-bar");
        if (viewState === "details" && detailsBottomBar) {
            detailsBottomBar.style.display = "flex";
        }
    }
}

// ViewState Router
let viewState = "catalog"; // "catalog", "details", "downloading"

function setViewState(state) {
    viewState = state;
    syncViewState();
    updateMiniBadge(appState);
}

function syncViewState() {
    if (appState.is_configured) {
        if (viewState !== "catalog" && viewState !== "details") {
            viewState = "downloading";
        }
    } else {
        if (viewState === "downloading") {
            viewState = "catalog";
        }
    }

    const elMiniBadge = document.getElementById("floating-download-badge");

    if (viewState === "downloading") {
        document.querySelector(".app-container").classList.remove("has-sidebar");
        document.querySelector(".sidebar").style.display = "none";
        
        elSetupView.classList.add("hidden-view");
        elDownloadView.classList.remove("hidden-view");
        elDownloadView.style.display = "flex";
        
        if (elMiniBadge) elMiniBadge.style.display = "none";
    } else {
        document.querySelector(".app-container").classList.remove("has-sidebar");
        document.querySelector(".sidebar").style.display = "none";
        
        elSetupView.classList.remove("hidden-view");
        elDownloadView.classList.add("hidden-view");
        
        if (elMiniBadge && appState.is_configured) {
            elMiniBadge.style.display = "flex";
            updateMiniBadge(appState);
        } else if (elMiniBadge) {
            elMiniBadge.style.display = "none";
        }

        if (viewState === "catalog") {
            elCatalogContainer.classList.remove("hidden-view");
            elGameDetailsContainer.classList.add("hidden-view");
            clearDynamicBackground();
            const detailsBottomBar = document.getElementById("details-bottom-bar");
            if (detailsBottomBar) detailsBottomBar.style.display = "none";
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
        const secondaryGlow = `rgba(${rS}, ${gS}, ${bS}, 0.28)`;
        const border = `rgba(${rS}, ${gS}, ${bS}, 0.15)`;
        
        document.documentElement.style.setProperty('--color-primary', primary);
        document.documentElement.style.setProperty('--color-secondary', secondary);
        document.documentElement.style.setProperty('--color-primary-glow', glow);
        document.documentElement.style.setProperty('--color-secondary-glow', secondaryGlow);
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

// Canvas Dynamic Accent Extraction for individual game cards
function applyCardDynamicAccent(imgElement, cardElement) {
    try {
        const canvas = document.createElement("canvas");
        canvas.width = 16;
        canvas.height = 16;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(imgElement, 0, 0, 16, 16);
        
        const imageData = ctx.getImageData(0, 0, 16, 16);
        const data = imageData.data;
        
        let rSum = 0, gSum = 0, bSum = 0, count = 0;
        const topBuckets = {};
        const botBuckets = {};
        
        for (let y = 0; y < 16; y++) {
            for (let x = 0; x < 16; x++) {
                const idx = (y * 16 + x) * 4;
                const r = data[idx];
                const g = data[idx+1];
                const b = data[idx+2];
                const a = data[idx+3];
                if (a < 200) continue;
                
                rSum += r;
                gSum += g;
                bSum += b;
                count++;
                
                // RGB to HSL
                const rNorm = r / 255;
                const gNorm = g / 255;
                const bNorm = b / 255;
                const max = Math.max(rNorm, gNorm, bNorm);
                const min = Math.min(rNorm, gNorm, bNorm);
                const d = max - min;
                const l = (max + min) / 2;
                const s = max === min ? 0 : (l > 0.5 ? d / (2 - max - min) : d / (max + min));
                
                // Ignore extremely dark or extremely white pixels
                if (l < 0.12 || l > 0.88) continue;
                if (s < 0.15) continue;
                
                // Quantize
                const qr = Math.floor(r / 24) * 24;
                const qg = Math.floor(g / 24) * 24;
                const qb = Math.floor(b / 24) * 24;
                const key = `${qr},${qg},${qb}`;
                
                const weight = 1 + s * 3.5;
                if (y < 8) {
                    topBuckets[key] = (topBuckets[key] || 0) + weight;
                } else {
                    botBuckets[key] = (botBuckets[key] || 0) + weight;
                }
            }
        }
        
        const extractDominant = (buckets) => {
            let dominant = null;
            let maxWeight = -1;
            for (const key in buckets) {
                if (buckets[key] > maxWeight) {
                    maxWeight = buckets[key];
                    const parts = key.split(",").map(Number);
                    dominant = { r: parts[0], g: parts[1], b: parts[2] };
                }
            }
            return dominant;
        };
        
        let topColor = extractDominant(topBuckets);
        let botColor = extractDominant(botBuckets);
        
        const globalAvg = count > 0 ? {
            r: Math.floor(rSum / count),
            g: Math.floor(gSum / count),
            b: Math.floor(bSum / count)
        } : { r: 155, g: 89, b: 182 };
        
        if (!topColor) topColor = globalAvg;
        if (!botColor) botColor = globalAvg;
        
        // Boost colors if they are too dark so they are always visible on dark backgrounds
        const boostColor = (color) => {
            let { r, g, b } = color;
            const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
            if (luminance < 110) {
                const boost = Math.floor((110 - luminance) * 0.8 + 35);
                r = Math.min(255, r + boost);
                g = Math.min(255, g + boost);
                b = Math.min(255, b + boost);
            }
            return { r, g, b };
        };
        
        topColor = boostColor(topColor);
        botColor = boostColor(botColor);
        
        // If colors are too close, shift the bottom hue slightly to create a nice, smooth transition
        const dist = Math.abs(topColor.r - botColor.r) + Math.abs(topColor.g - botColor.g) + Math.abs(topColor.b - botColor.b);
        if (dist < 40) {
            botColor.r = Math.min(255, Math.max(0, botColor.r + 25));
            botColor.g = Math.min(255, Math.max(0, botColor.g - 15));
            botColor.b = Math.min(255, Math.max(0, botColor.b + 35));
        }
        
        // Rich colors but softer opacity so they don't look grey but aren't blinding (aesthetic, slightly visible)
        const accentTop = `rgba(${topColor.r}, ${topColor.g}, ${topColor.b}, 0.52)`;
        const accentTopHover = `rgba(${topColor.r}, ${topColor.g}, ${topColor.b}, 0.88)`;
        
        const accentBot = `rgba(${botColor.r}, ${botColor.g}, ${botColor.b}, 0.52)`;
        const accentBotHover = `rgba(${botColor.r}, ${botColor.g}, ${botColor.b}, 0.88)`;
        
        const glow = `rgba(${botColor.r}, ${botColor.g}, ${botColor.b}, 0.18)`;
        const glowHover = `rgba(${botColor.r}, ${botColor.g}, ${botColor.b}, 0.45)`;
        
        cardElement.style.setProperty("--card-accent-top", accentTop);
        cardElement.style.setProperty("--card-accent-top-hover", accentTopHover);
        cardElement.style.setProperty("--card-accent-bot", accentBot);
        cardElement.style.setProperty("--card-accent-bot-hover", accentBotHover);
        cardElement.style.setProperty("--card-glow-color", glow);
        cardElement.style.setProperty("--card-glow-color-hover", glowHover);
    } catch (e) {
        // Silent catch for cross-origin or canvas read errors
    }
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

function createGameCard(game) {
    const card = document.createElement("div");
    card.className = activeProvider === "onlinefix" ? "game-card onlinefix-card" : "game-card";
    
    const coverUrl = game.cover_image 
        ? `/api/proxy_image?url=${encodeURIComponent(game.cover_image)}`
        : "";
        
    card.innerHTML = `
        <div class="card-cover-area">
            <div class="card-cover-placeholder">${GAMEPAD_SVG}</div>
        </div>
        <div class="card-info">
            <h4 class="card-title" title="${game.title}">${game.title}</h4>
            ${game.developer ? `<div class="card-developer">${game.developer}</div>` : ""}
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
                img.onload = () => {
                    applyCardDynamicAccent(img, card);
                };
                if (img.complete) {
                    applyCardDynamicAccent(img, card);
                }
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
        setViewState("details");
        showDetailsLoadingState(game.title);
        elAnalyzeBtn.click();
    });
    
    return card;
}

function renderGamesList(results, popularList) {
    elGamesGridContainer.innerHTML = "";
    if (!results || results.length === 0) {
        elGamesGridContainer.innerHTML = `<div class="no-results-message">No repacks found.</div>`;
        return;
    }
    
    // If Online-Fix and we have a popularList, and we're not performing a search query
    if (activeProvider === "onlinefix" && popularList && popularList.length > 0 && !searchQuery) {
        const popSection = document.createElement("div");
        popSection.className = "popular-section";
        popSection.innerHTML = `
            <h3 class="section-title">Popular</h3>
            <div class="popular-slider-wrapper">
                <div class="popular-slider-scroll"></div>
            </div>
        `;
        
        const scrollTrack = popSection.querySelector(".popular-slider-scroll");
        const doubleList = [...popularList, ...popularList];
        doubleList.forEach(game => {
            scrollTrack.appendChild(createGameCard(game));
        });
        
        elGamesGridContainer.appendChild(popSection);
        
        const staticTitle = document.createElement("h3");
        staticTitle.className = "section-title";
        staticTitle.style.marginTop = "20px";
        staticTitle.style.marginBottom = "15px";
        staticTitle.innerText = "Latest Releases";
        elGamesGridContainer.appendChild(staticTitle);
        
        const staticGrid = document.createElement("div");
        staticGrid.className = "games-grid static-grid";
        results.forEach(game => {
            staticGrid.appendChild(createGameCard(game));
        });
        elGamesGridContainer.appendChild(staticGrid);
    } else {
        results.forEach(game => {
            elGamesGridContainer.appendChild(createGameCard(game));
        });
    }
}

function showDetailsLoadingState(gameTitle) {
    elDetailsGameTitle.innerText = gameTitle || "Loading Game...";
    elDetailsVersionBadge.style.display = "none";
    if (elBtnOpenBrowser) elBtnOpenBrowser.style.display = "none";
    elMetadataOriginalSize.innerText = "--";
    elMetadataRepackSize.innerText = "--";
    
    const detailsBottomBar = document.getElementById("details-bottom-bar");
    const detailsBottomSize = document.getElementById("details-bottom-size");
    if (detailsBottomSize) detailsBottomSize.innerText = "--";
    if (detailsBottomBar) detailsBottomBar.style.display = "none";
    
    const elVideoContainer = document.getElementById("details-video-container");
    const elVideoIframe = document.getElementById("video-iframe");
    if (elVideoIframe) elVideoIframe.src = "";
    if (elVideoContainer) elVideoContainer.style.display = "none";
    
    elSetupCover.src = "";
    elSetupCover.style.display = "none";
    elSetupCoverPlaceholder.style.display = "flex";
    clearDynamicBackground();
    
    if (elGameDescription) elGameDescription.style.display = "none";
    if (elGameScreenshotsSection) elGameScreenshotsSection.style.display = "none";
    
    elConfigCard.style.display = "none";
    elMirrorSelectSection.style.display = "none";
    
    let elDetailsLoader = document.getElementById("details-page-loader");
    if (!elDetailsLoader) {
        elDetailsLoader = document.createElement("div");
        elDetailsLoader.id = "details-page-loader";
        elDetailsLoader.className = "section-loader";
        elDetailsLoader.innerHTML = `
            <div class="spinner"></div>
            <p style="margin-top: 10px; font-weight: 500; color: var(--text-muted);">Fetching game mirrors & files...</p>
        `;
        elSetupDashboard.parentElement.appendChild(elDetailsLoader);
    }
    elDetailsLoader.style.display = "flex";
    elSetupDashboard.style.display = "none";
}

async function loadCatalogGames() {
    elGamesLoader.style.display = "flex";
    elGamesGridContainer.innerHTML = "";
    elSearchResultsTitle.style.display = "none";
    
    const cacheKey = getCatalogCacheKey(activeProvider, currentPage, searchQuery, activeTab);
    if (catalogPagesCache.has(cacheKey)) {
        const cached = catalogPagesCache.get(cacheKey);
        renderGamesList(cached.results, cached.popular);
        if (cached.has_next) {
            elBtnNextPage.removeAttribute("disabled");
        } else {
            elBtnNextPage.setAttribute("disabled", "true");
        }
        elGamesLoader.style.display = "none";
        elBtnPrevPage.disabled = (currentPage === 1);
        elPageIndicator.innerText = currentPage;
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
                popular: data.popular,
                has_next: data.has_next
            });
            renderGamesList(data.results, data.popular);
            
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
        elPageIndicator.innerText = currentPage;
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
    setTimeout(() => {
        elSettingsModal.classList.add("active");
    }, 15);
    loadGDriveAccounts();
});

const closeSettings = () => {
    elSettingsModal.classList.remove("active");
    setTimeout(() => {
        elSettingsModal.style.display = "none";
    }, 250);
};

elCloseSettingsModalBtn.addEventListener("click", closeSettings);
elSaveSettingsBtn.addEventListener("click", async () => {
    const showLogs = elChkShowLogs.checked;
    elConsoleBox.parentElement.classList.toggle("hidden", !showLogs);
    localStorage.setItem("showLogs", showLogs ? "true" : "false");
    
    if (elChkRainbowBg) {
        const rainbowBg = elChkRainbowBg.checked;
        document.body.classList.toggle("rainbow-active", rainbowBg);
        localStorage.setItem("rainbowBg", rainbowBg ? "true" : "false");
    }
    
    if (elChkGofileProxy) {
        localStorage.setItem("gofileProxy", elChkGofileProxy.checked ? "true" : "false");
    }
    
    if (elChkHideGDrive) {
        localStorage.setItem("hideGDrive", elChkHideGDrive.checked ? "true" : "false");
    }
    
    const elClientId = document.getElementById("txt-gdrive-client-id");
    const elClientSecret = document.getElementById("txt-gdrive-client-secret");
    if (elClientId && elClientSecret) {
        const client_id = elClientId.value.trim();
        const client_secret = elClientSecret.value.trim();
        try {
            await fetch("/api/gdrive/set_credentials", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ client_id, client_secret })
            });
        } catch (e) {
            console.error("Failed to save custom credentials:", e);
        }
    }
    
    closeSettings();
});

// Google Drive Account & Cleanup event bindings
if (elAddGDriveAccountBtn) {
    elAddGDriveAccountBtn.addEventListener("click", async () => {
        elAddGDriveAccountBtn.disabled = true;
        const originalText = `<span>+ Add Google Account</span>`;
        
        try {
            // === PHASE 1: Private API Authorization ===
            elAddGDriveAccountBtn.innerHTML = `
                <div class="spinner" style="width: 12px; height: 12px; border-width: 1.5px; border-color: currentColor; border-top-color: transparent;"></div>
                <span>Starting authorization...</span>
            `;
            
            const startResp = await fetch("/api/gdrive/start_auth", { method: "POST" });
            const startData = await startResp.json();
            
            if (!startData.success) {
                throw new Error(startData.error || "Failed to start authorization.");
            }
            
            window.open(startData.auth_url, "_blank");
            
            elAddGDriveAccountBtn.innerHTML = `
                <div class="spinner" style="width: 12px; height: 12px; border-width: 1.5px; border-color: currentColor; border-top-color: transparent;"></div>
                <span>Step 1: Waiting for Private API...</span>
            `;
            
            let result = null;
            for (let i = 0; i < 90; i++) {
                await new Promise(r => setTimeout(r, 2000));
                try {
                    const pollResp = await fetch("/api/gdrive/poll_auth", { method: "POST" });
                    const pollData = await pollResp.json();
                    
                    if (pollData.status === "done") {
                        result = pollData;
                        break;
                    } else if (pollData.status === "error") {
                        throw new Error(pollData.error || "Authorization failed.");
                    }
                } catch (pollErr) {
                    if (pollErr.message && pollErr.message !== "Failed to fetch") throw pollErr;
                }
            }
            
            if (!result || !result.success) {
                throw new Error("Authorization timed out. Please try again.");
            }
            
            const linkedEmail = result.email;
            loadGDriveAccounts();
            
            // === PHASE 2: Copy Flow Authorization via SweetAlert2 user gesture ===
            // Show Swal with confirm button. Clicking it is a USER GESTURE so Chrome won't block window.open
            const swalRes = await Swal.fire({
                icon: 'success',
                title: 'Step 1 Complete!',
                html: `Private API linked for <b>${linkedEmail}</b>.<br><br>Click below to complete setup (Step 2: Copy Flow).`,
                confirmButtonText: '🔑 Authorize Copy Flow (Step 2)',
                showCancelButton: true,
                cancelButtonText: 'Skip (configure later)',
                background: '#121220',
                color: '#e2e2ec',
                confirmButtonColor: '#9b59b6',
                cancelButtonColor: '#555',
                allowOutsideClick: false
            });
            
            if (!swalRes.isConfirmed) {
                Swal.fire({
                    icon: 'info',
                    title: 'Partial Setup',
                    text: 'Account linked. Copy Flow will be configured when you start downloading.',
                    background: '#121220',
                    color: '#e2e2ec',
                    confirmButtonColor: '#9b59b6'
                });
                return;
            }
            
            // User clicked confirm — this is a direct user gesture, so window.open works!
            elAddGDriveAccountBtn.innerHTML = `
                <div class="spinner" style="width: 12px; height: 12px; border-width: 1.5px; border-color: currentColor; border-top-color: transparent;"></div>
                <span>Step 2: Configuring copy flow...</span>
            `;
            
            const copyResp = await fetch("/api/gdrive/start_copy_auth", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: linkedEmail })
            });
            const copyData = await copyResp.json();
            
            if (!copyData.success) {
                throw new Error(copyData.error || "Failed to start copy flow.");
            }
            
            // Open Phase 2 tab — allowed because we're inside a Swal confirm click handler
            window.open(copyData.auth_url, "_blank");
            
            elAddGDriveAccountBtn.innerHTML = `
                <div class="spinner" style="width: 12px; height: 12px; border-width: 1.5px; border-color: currentColor; border-top-color: transparent;"></div>
                <span>Step 2: Waiting for Copy Flow permission...</span>
            `;
            
            let copyResult = null;
            for (let i = 0; i < 90; i++) {
                await new Promise(r => setTimeout(r, 2000));
                try {
                    const pollCopyResp = await fetch("/api/gdrive/poll_copy_auth", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ email: linkedEmail })
                    });
                    const pollCopyData = await pollCopyResp.json();
                    
                    if (pollCopyData.status === "done") {
                        copyResult = pollCopyData;
                        break;
                    } else if (pollCopyData.status === "error") {
                        throw new Error(pollCopyData.error || "Copy flow authorization failed.");
                    }
                } catch (pollErr) {
                    if (pollErr.message && pollErr.message !== "Failed to fetch") throw pollErr;
                }
            }
            
            if (copyResult && copyResult.success) {
                Swal.fire({
                    icon: 'success',
                    title: '✅ Setup Complete!',
                    html: `Account <b>${linkedEmail}</b> is fully configured.<br>Downloads will now run silently in the background.`,
                    background: '#121220',
                    color: '#e2e2ec',
                    confirmButtonColor: '#9b59b6'
                });
                loadGDriveAccounts();
            } else {
                throw new Error("Copy flow configuration timed out.");
            }
        } catch (e) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: e.message,
                background: '#121220',
                color: '#e2e2ec',
                confirmButtonColor: '#e74c3c'
            });
        } finally {
            elAddGDriveAccountBtn.disabled = false;
            elAddGDriveAccountBtn.innerHTML = originalText;
        }
    });
}


if (elGDriveCleanupBtn) {
    elGDriveCleanupBtn.addEventListener("click", async () => {
        if (confirm("Are you sure you want to delete all files in the current download queue from your Google Drive? This will free up your Drive space.")) {
            elGDriveCleanupBtn.disabled = true;
            try {
                const response = await fetch("/api/gdrive/cleanup", { method: "POST" });
                const data = await response.json();
                if (data.success) {
                    alert("Google Drive cleanup started in the background. Check logs below for progress.");
                } else {
                    alert(data.error || "Failed to trigger cleanup.");
                }
            } catch (e) {
                alert("Error: " + e.message);
            } finally {
                elGDriveCleanupBtn.disabled = false;
            }
        }
    });
}

// Google Drive accounts API helpers
async function loadGDriveAccounts() {
    try {
        const response = await fetch("/api/gdrive/list_accounts");
        const data = await response.json();
        if (data.success) {
            renderGDriveAccounts(data.accounts, data.active_account, data.custom_client_id);
            
            const elClientId = document.getElementById("txt-gdrive-client-id");
            const elClientSecret = document.getElementById("txt-gdrive-client-secret");
            if (elClientId) elClientId.value = data.custom_client_id || "";
            if (elClientSecret) elClientSecret.value = data.custom_client_secret || "";
        }
    } catch (e) {
        console.error("Failed to load Google Drive accounts:", e);
    }
}

function getSubscriptionTier(limitBytes) {
    if (!limitBytes || limitBytes <= 0) return "15 GB Free";
    const GB = 1024 * 1024 * 1024;
    const limitGB = limitBytes / GB;
    
    if (limitGB <= 17) return "15 GB Free";
    if (limitGB <= 110) return "100 GB Plan";
    if (limitGB <= 220) return "200 GB Plan";
    if (limitGB <= 2200) return "2 TB Plan";
    if (limitGB <= 5500) return "5 TB Plan";
    if (limitGB <= 11000) return "10 TB Plan";
    if (limitGB <= 22000) return "20 TB Plan";
    if (limitGB <= 33000) return "30 TB Plan";
    
    if (limitBytes >= 1024 * GB) {
        return `${(limitBytes / (1024 * GB)).toFixed(0)} TB Plan`;
    }
    return `${limitGB.toFixed(0)} GB Plan`;
}

function getGooglePlanInfo(limitBytes) {
    const GB = 1024 * 1024 * 1024;
    const limitGB = limitBytes / GB;
    
    let planName = "Free Account";
    let badgeHtml = "";
    let sizeText = "15 GB";
    
    if (!limitBytes || limitBytes <= 0) {
        return { planName: "Google One", badgeHtml: "", sizeText: "15 GB" };
    }
    
    const sparkleSvg = `<svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor" style="display: inline-block; margin-right: 3px; vertical-align: middle;"><path d="M12 2l2.4 7.6 7.6 2.4-7.6 2.4-2.4 7.6-2.4-7.6-7.6-2.4 7.6-2.4z"/></svg>`;
    
    if (limitGB <= 17) {
        planName = "Free Account";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 600; color: #e0e0e0; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center;">Free</span>`;
        sizeText = "15 GB";
    } else if (limitGB <= 110) {
        planName = "Basic";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 600; color: #4285f4; background: rgba(66, 133, 244, 0.1); border: 1px solid rgba(66, 133, 244, 0.25); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center;">Basic</span>`;
        sizeText = "100 GB";
    } else if (limitGB <= 220) {
        planName = "Standard";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 600; color: #34a853; background: rgba(52, 168, 83, 0.1); border: 1px solid rgba(52, 168, 83, 0.25); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center;">Standard</span>`;
        sizeText = "200 GB";
    } else if (limitGB <= 440) {
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 600; color: #ba68c8; background: rgba(171, 71, 188, 0.15); border: 1px solid rgba(171, 71, 188, 0.3); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center; box-shadow: 0 0 8px rgba(171, 71, 188, 0.25);">Plus</span>`;
        sizeText = "400 GB";
    } else if (limitGB <= 2200) {
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 600; color: #ba68c8; background: rgba(171, 71, 188, 0.15); border: 1px solid rgba(171, 71, 188, 0.3); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center; box-shadow: 0 0 8px rgba(171, 71, 188, 0.25);">Plus</span>`;
        sizeText = "2 TB";
    } else if (limitGB <= 5500) {
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 700; color: #ffffff; background: linear-gradient(135deg, #1a73e8, #4285f4, #0052d4, #1a73e8); background-size: 300% 300%; animation: blue-haze 4s ease infinite; padding: 2px 10px; border-radius: 14px; display: inline-flex; align-items: center; gap: 2px; box-shadow: 0 0 10px rgba(66,133,244,0.55); border: 1px solid rgba(255,255,255,0.15);">${sparkleSvg}Pro</span>`;
        sizeText = "5 TB";
    } else if (limitGB <= 11000) {
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 700; color: #ffffff; background: linear-gradient(135deg, #1a73e8, #4285f4, #0052d4, #1a73e8); background-size: 300% 300%; animation: blue-haze 4s ease infinite; padding: 2px 10px; border-radius: 14px; display: inline-flex; align-items: center; gap: 2px; box-shadow: 0 0 10px rgba(66,133,244,0.55); border: 1px solid rgba(255,255,255,0.15);">${sparkleSvg}Pro</span>`;
        sizeText = "10 TB";
    } else if (limitGB <= 22000) {
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 700; color: #ffffff; background: linear-gradient(135deg, #ea4335, #f12711, #f5af19, #ea4335); background-size: 300% 300%; animation: blue-haze 4s ease infinite; padding: 2px 10px; border-radius: 14px; display: inline-flex; align-items: center; gap: 2px; box-shadow: 0 0 10px rgba(234,67,53,0.55); border: 1px solid rgba(255,255,255,0.15);">${sparkleSvg}Ultra</span>`;
        sizeText = "20 TB";
    } else if (limitGB <= 33000) {
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 700; color: #ffffff; background: linear-gradient(135deg, #ea4335, #f12711, #f5af19, #ea4335); background-size: 300% 300%; animation: blue-haze 4s ease infinite; padding: 2px 10px; border-radius: 14px; display: inline-flex; align-items: center; gap: 2px; box-shadow: 0 0 10px rgba(234,67,53,0.55); border: 1px solid rgba(255,255,255,0.15);">${sparkleSvg}Ultra</span>`;
        sizeText = "30 TB";
    } else {
        const tbLimit = (limitGB / 1024).toFixed(0);
        planName = "Google AI";
        badgeHtml = `<span style="font-size: 0.65rem; font-weight: 700; color: #ffffff; background: linear-gradient(135deg, #ea4335, #f12711, #f5af19, #ea4335); background-size: 300% 300%; animation: blue-haze 4s ease infinite; padding: 2px 10px; border-radius: 14px; display: inline-flex; align-items: center; gap: 2px; box-shadow: 0 0 10px rgba(234,67,53,0.55); border: 1px solid rgba(255,255,255,0.15);">${sparkleSvg}Ultra</span>`;
        sizeText = `${tbLimit} TB`;
    }
    
    return { planName, badgeHtml, sizeText };
}

function getAvatarColor(email) {
    if (!email || email === "Unknown Account") return "#9b59b6"; // default purple
    const colors = [
        "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e",
        "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50",
        "#e67e22", "#e74c3c", "#d35400", "#c0392b"
    ];
    let hash = 0;
    for (let i = 0; i < email.length; i++) {
        hash = email.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % colors.length;
    return colors[index];
}

function renderGDriveAccounts(accounts, activeAccount, customClientId) {
    if (!elGDriveAccountsList) return;
    
    if (accounts.length === 0) {
        elGDriveAccountsList.innerHTML = `
            <div style="font-size: 0.8rem; color: var(--text-muted); text-align: center; padding: 10px; background: rgba(255,255,255,0.02); border-radius: 6px; border: 1px dashed rgba(255,255,255,0.1);">
                No Google Accounts linked.
            </div>
        `;
        return;
    }
    
    const hasCustom = customClientId && customClientId.trim() !== "";
    const apiBadgeHtml = hasCustom
        ? `<span style="font-size: 0.72rem; padding: 2px 6px; border-radius: 6px; background: rgba(46, 204, 113, 0.12); border: 1px solid rgba(46, 204, 113, 0.25); color: #2ecc71; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; width: max-content;">Private API</span>`
        : `<span style="font-size: 0.72rem; padding: 2px 6px; border-radius: 6px; background: rgba(231, 76, 60, 0.12); border: 1px solid rgba(231, 76, 60, 0.25); color: #e74c3c; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; width: max-content;">Shared API</span>`;
    
    elGDriveAccountsList.innerHTML = "";
    accounts.forEach(acc => {
        const email = acc.email;
        const isActive = email === activeAccount;
        
        const planInfo = getGooglePlanInfo(acc.limit);
        let storageInfoText = "";
        let pct = 0;
        
        if (acc.limit > 0) {
            pct = Math.min(100, Math.round((acc.usage / acc.limit) * 100));
            const formatStorage = (bytes) => {
                const GB = 1024 * 1024 * 1024;
                const TB = 1024 * GB;
                if (bytes >= TB) return `${(bytes / TB).toFixed(1)} TB`;
                return `${(bytes / GB).toFixed(1)} GB`;
            };
            storageInfoText = `${formatStorage(acc.usage)} / ${formatStorage(acc.limit)} used (${pct}%)`;
        } else {
            storageInfoText = "Storage info unavailable";
        }
        
        const card = document.createElement("div");
        card.className = "gdrive-account-card";
        card.style.display = "flex";
        card.style.flexDirection = "column";
        card.style.gap = "14px";
        card.style.background = "rgba(255,255,255,0.035)";
        card.style.padding = "18px";
        card.style.borderRadius = "16px";
        card.style.border = isActive ? "1.5px solid var(--color-accent)" : "1px solid rgba(255,255,255,0.08)";
        card.style.boxShadow = isActive ? "0 0 14px var(--color-accent-glow)" : "none";
        card.style.transition = "all 0.25s ease";
        card.style.marginBottom = "10px";
        
        const isFree = acc.limit <= 17 * 1024 * 1024 * 1024; // 17 GB or less is Free
        const tierClass = isFree ? "free-tier" : "premium-tier";
        
        card.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                <div style="display: flex; align-items: center; gap: 14px; min-width: 0; flex: 1;">
                    <input type="radio" name="active_gdrive" class="radio-active-gdrive" ${isActive ? "checked" : ""} data-email="${email}" style="cursor: pointer; width: 20px; height: 20px; accent-color: var(--color-accent); flex-shrink: 0;">
                    
                    <div class="gdrive-avatar-container ${tierClass}" style="width: 48px; height: 48px; flex-shrink: 0;">
                        ${acc.photo 
                            ? `<img class="gdrive-avatar-img" src="${acc.photo}" referrerpolicy="no-referrer">` 
                            : `<div class="gdrive-avatar-fallback" style="background-color: ${getAvatarColor(email)}">${email[0].toUpperCase()}</div>`
                        }
                    </div>
                    
                    <div style="display: flex; flex-direction: column; line-height: 1.35; min-width: 0; flex: 1;">
                        <span style="font-size: 1.05rem; color: var(--text-white); font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${acc.name || 'Unknown Name'}</span>
                        <span style="font-size: 0.85rem; color: var(--text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${email}</span>
                        <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px; flex-wrap: wrap;">
                            <span style="font-size: 0.82rem; color: #a1a1b5; font-weight: 500;">${planInfo.planName}</span>
                            ${planInfo.badgeHtml ? planInfo.badgeHtml : ""}
                            ${acc.fully_configured 
                                ? `<span style="font-size: 0.65rem; font-weight: 700; color: #2ecc71; background: rgba(46, 204, 113, 0.12); border: 1px solid rgba(46, 204, 113, 0.25); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center; gap: 3px;"><svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor" style="vertical-align: middle;"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> Fully Configured</span>`
                                : `<span style="font-size: 0.65rem; font-weight: 700; color: #e74c3c; background: rgba(231, 76, 60, 0.12); border: 1px solid rgba(231, 76, 60, 0.25); padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center; gap: 3px;"><svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor" style="vertical-align: middle;"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg> Not Configured</span>`
                            }
                        </div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 12px; flex-shrink: 0;">
                    <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">
                        <span style="font-size: 0.82rem; padding: 4px 10px; border-radius: 12px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); color: var(--text-white); font-weight: 600;">${planInfo.sizeText}</span>
                        ${apiBadgeHtml}
                    </div>
                    <button class="btn-delete-gdrive" data-email="${email}" style="background: none; border: none; color: #ff5555; cursor: pointer; font-size: 1.55rem; padding: 0 4px; line-height: 1; transition: color 0.15s ease;" title="Remove Account">&times;</button>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; width: 100%; margin-top: 4px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--text-muted);">
                    <span>Storage Space</span>
                    <span>${storageInfoText}</span>
                </div>
                <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; margin-top: 6px; overflow: hidden;">
                    <div style="width: ${pct}%; height: 100%; background: ${pct > 90 ? '#e74c3c' : 'var(--color-accent)'}; border-radius: 4px; box-shadow: 0 0 8px ${pct > 90 ? 'rgba(231,76,60,0.5)' : 'var(--color-accent-glow)'};"></div>
                </div>
            </div>
        `;
        
        card.querySelector("input[type='radio']").addEventListener("change", async (e) => {
            if (e.target.checked) {
                try {
                    const res = await fetch("/api/gdrive/select_account", {
                        method: "POST",
                        body: JSON.stringify({ email })
                    });
                    const resData = await res.json();
                    if (resData.success) {
                        loadGDriveAccounts();
                    } else {
                        alert(resData.error || "Failed to select account.");
                    }
                } catch (err) {
                    console.error(err);
                }
            }
        });
        
        card.querySelector(".btn-delete-gdrive").addEventListener("click", async () => {
            if (confirm(`Are you sure you want to remove Google account ${email}?`)) {
                try {
                    const res = await fetch("/api/gdrive/remove_account", {
                        method: "POST",
                        body: JSON.stringify({ email })
                    });
                    const resData = await res.json();
                    if (resData.success) {
                        loadGDriveAccounts();
                    } else {
                        alert(resData.error || "Failed to remove account.");
                    }
                } catch (err) {
                    console.error(err);
                }
            }
        });
        
        elGDriveAccountsList.appendChild(card);
    });
}

// Quick site switcher behavior
function switchProvider(newProvider) {
    if (activeProvider === newProvider) return;
    
    activeProvider = newProvider;
    localStorage.setItem("activeProvider", activeProvider);
    
    if (elProviderSelect) {
        elProviderSelect.value = activeProvider;
    }
    
    // Sync header quick switch toggle
    const elPillsContainer = document.querySelector(".browse-nav-pills");
    if (activeProvider === "onlinefix") {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.add("onlinefix-active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.add("active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.remove("active");
        if (elPillsContainer) elPillsContainer.style.display = "none";
    } else {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.remove("onlinefix-active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.add("active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.remove("active");
        if (elPillsContainer) elPillsContainer.style.display = "flex";
        elPillPopularMonth.innerText = "Top 50 Month";
        elPillPopularYear.style.display = "inline-block";
    }
    
    const elGoToSiteBtn = document.getElementById("btn-go-to-site");
    const elGoToSiteText = document.getElementById("go-to-site-text");
    const elCatalogGoToSiteBtn = document.getElementById("btn-catalog-go-to-site");
    const elCatalogGoToSiteText = document.getElementById("catalog-go-to-site-text");
    
    if (activeProvider === "onlinefix") {
        if (elGoToSiteBtn && elGoToSiteText) {
            elGoToSiteBtn.href = "https://online-fix.me/";
            elGoToSiteText.innerText = "Go to Online-Fix";
        }
        if (elCatalogGoToSiteBtn && elCatalogGoToSiteText) {
            elCatalogGoToSiteBtn.href = "https://online-fix.me/";
            elCatalogGoToSiteText.innerText = "Go to Online-Fix";
        }
    } else {
        if (elGoToSiteBtn && elGoToSiteText) {
            elGoToSiteBtn.href = "https://fitgirl-repacks.site/";
            elGoToSiteText.innerText = "Go to FitGirl";
        }
        if (elCatalogGoToSiteBtn && elCatalogGoToSiteText) {
            elCatalogGoToSiteBtn.href = "https://fitgirl-repacks.site/";
            elCatalogGoToSiteText.innerText = "Go to FitGirl";
        }
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
    const gofileProxy = localStorage.getItem("gofileProxy") === "true";
    const hideGDrive = localStorage.getItem("hideGDrive") !== "false"; // True by default
    
    if (elProviderSelect) {
        elProviderSelect.value = activeProvider;
    }
    if (elChkShowLogs) {
        elChkShowLogs.checked = showLogs;
        elChkShowLogs.addEventListener("change", () => {
            const val = elChkShowLogs.checked;
            elConsoleBox.parentElement.classList.toggle("hidden", !val);
            localStorage.setItem("showLogs", val ? "true" : "false");
        });
    }
    if (elChkRainbowBg) {
        elChkRainbowBg.checked = rainbowBg;
        elChkRainbowBg.addEventListener("change", () => {
            const val = elChkRainbowBg.checked;
            document.body.classList.toggle("rainbow-active", val);
            localStorage.setItem("rainbowBg", val ? "true" : "false");
        });
    }
    if (elChkGofileProxy) {
        elChkGofileProxy.checked = gofileProxy;
        elChkGofileProxy.addEventListener("change", () => {
            localStorage.setItem("gofileProxy", elChkGofileProxy.checked ? "true" : "false");
        });
    }
    if (elChkHideGDrive) {
        elChkHideGDrive.checked = hideGDrive;
        elChkHideGDrive.addEventListener("change", () => {
            const val = elChkHideGDrive.checked;
            document.querySelectorAll(".gdrive-ui-element").forEach(el => {
                el.style.display = val ? "none" : "";
            });
            localStorage.setItem("hideGDrive", val ? "true" : "false");
        });
    }
    document.querySelectorAll(".gdrive-ui-element").forEach(el => {
        el.style.display = hideGDrive ? "none" : "";
    });
    
    document.body.classList.toggle("rainbow-active", rainbowBg);
    elConsoleBox.parentElement.classList.toggle("hidden", !showLogs);
    
    const elPillsContainer = document.querySelector(".browse-nav-pills");
    if (activeProvider === "onlinefix") {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.add("onlinefix-active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.add("active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.remove("active");
        if (elPillsContainer) elPillsContainer.style.display = "none";
    } else {
        if (elSiteToggleTrigger) elSiteToggleTrigger.classList.remove("onlinefix-active");
        if (elLabelSiteFitGirl) elLabelSiteFitGirl.classList.add("active");
        if (elLabelSiteOnlineFix) elLabelSiteOnlineFix.classList.remove("active");
        if (elPillsContainer) elPillsContainer.style.display = "flex";
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
    
    const elGoToSiteBtn = document.getElementById("btn-go-to-site");
    const elGoToSiteText = document.getElementById("go-to-site-text");
    const elCatalogGoToSiteBtn = document.getElementById("btn-catalog-go-to-site");
    const elCatalogGoToSiteText = document.getElementById("catalog-go-to-site-text");
    
    if (activeProvider === "onlinefix") {
        if (elGoToSiteBtn && elGoToSiteText) {
            elGoToSiteBtn.href = "https://online-fix.me/";
            elGoToSiteText.innerText = "Go to Online-Fix";
        }
        if (elCatalogGoToSiteBtn && elCatalogGoToSiteText) {
            elCatalogGoToSiteBtn.href = "https://online-fix.me/";
            elCatalogGoToSiteText.innerText = "Go to Online-Fix";
        }
    } else {
        if (elGoToSiteBtn && elGoToSiteText) {
            elGoToSiteBtn.href = "https://fitgirl-repacks.site/";
            elGoToSiteText.innerText = "Go to FitGirl";
        }
        if (elCatalogGoToSiteBtn && elCatalogGoToSiteText) {
            elCatalogGoToSiteBtn.href = "https://fitgirl-repacks.site/";
            elCatalogGoToSiteText.innerText = "Go to FitGirl";
        }
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

// Render Screenshots Showcase + Grid Gallery
function renderScreenshots(screenshotsList, videosList) {
    console.log("renderScreenshots called with:", {screenshotsList, videosList});
    const elScreenshotsSection = document.getElementById("game-screenshots-section");
    const elScreenshotsContainer = document.getElementById("game-screenshots-container");
    const elMainScreenshotImg = document.getElementById("screenshot-main-img");
    const elMainVideoIframe = document.getElementById("screenshot-main-video");
    const elMainDirectVideo = document.getElementById("screenshot-main-direct-video");
    const elMainScreenshotShowcase = document.getElementById("screenshot-main-showcase-container");

    function playVideo(videoUrl) {
        const isDirect = videoUrl.includes(".webm") || videoUrl.includes(".mp4") || videoUrl.includes(".ogg") || videoUrl.includes("/store_trailers/");
        
        if (isDirect) {
            if (elMainDirectVideo) {
                elMainDirectVideo.src = videoUrl;
                elMainDirectVideo.muted = true;
                elMainDirectVideo.defaultMuted = true;
                elMainDirectVideo.autoplay = true;
                elMainDirectVideo.loop = true;
                elMainDirectVideo.playsInline = true;
                elMainDirectVideo.style.display = "block";
                
                // Attempt programmatical playback with auto-retry on interaction
                elMainDirectVideo.play().catch(e => {
                    console.log("Direct video autoplay blocked, setting up user interaction retry:", e);
                    const runPlay = () => {
                        elMainDirectVideo.play().catch(err => console.log("Subsequent play failed:", err));
                        document.removeEventListener("click", runPlay);
                        document.removeEventListener("keydown", runPlay);
                    };
                    document.addEventListener("click", runPlay);
                    document.addEventListener("keydown", runPlay);
                });
            }
            if (elMainVideoIframe) {
                elMainVideoIframe.src = "";
                elMainVideoIframe.style.display = "none";
            }
        } else {
            if (elMainVideoIframe) {
                elMainVideoIframe.src = videoUrl;
                elMainVideoIframe.style.display = "block";
            }
            if (elMainDirectVideo) {
                elMainDirectVideo.src = "";
                elMainDirectVideo.style.display = "none";
            }
        }
        if (elMainScreenshotImg) {
            elMainScreenshotImg.style.display = "none";
        }
    }

    function stopVideo() {
        if (elMainDirectVideo) {
            elMainDirectVideo.pause();
            elMainDirectVideo.src = "";
            elMainDirectVideo.style.display = "none";
        }
        if (elMainVideoIframe) {
            elMainVideoIframe.src = "";
            elMainVideoIframe.style.display = "none";
        }
    }

    if (elScreenshotsSection && elScreenshotsContainer) {
        elScreenshotsContainer.innerHTML = "";
        
        const hasVideos = videosList && videosList.length > 0;
        const hasScreenshots = screenshotsList && screenshotsList.length > 0;

        if (hasVideos || hasScreenshots) {
            // Setup default main preview
            if (hasVideos) {
                playVideo(videosList[0]);
            } else if (hasScreenshots) {
                const firstScreenshotUrl = `/api/proxy_image?url=${encodeURIComponent(screenshotsList[0])}`;
                if (elMainScreenshotImg) {
                    elMainScreenshotImg.src = firstScreenshotUrl;
                    elMainScreenshotImg.style.display = "block";
                    elMainScreenshotImg.onclick = () => {
                        openScreenshotModal(elMainScreenshotImg.src);
                    };
                }
                stopVideo();
            }

            if (elMainScreenshotShowcase) {
                elMainScreenshotShowcase.style.display = "block";
            }

            // 1. Render Video Thumbnails
            if (hasVideos) {
                videosList.forEach((videoUrl, idx) => {
                    const thumbWrapper = document.createElement("div");
                    thumbWrapper.className = "video-thumbnail-wrapper" + (idx === 0 ? " active" : "");
                    thumbWrapper.innerHTML = `
                        <div class="video-thumbnail-overlay">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                                <path d="M8 5v14l11-7z"/>
                            </svg>
                        </div>
                        <span style="font-size: 0.65rem; font-weight: 700; color: #fff; text-transform: uppercase;">Trailer</span>
                    `;
                    
                    thumbWrapper.addEventListener("click", () => {
                        playVideo(videoUrl);
                        elScreenshotsContainer.querySelectorAll(".video-thumbnail-wrapper, img").forEach(i => i.classList.remove("active"));
                        thumbWrapper.classList.add("active");
                    });
                    elScreenshotsContainer.appendChild(thumbWrapper);
                });
            }

            // 2. Render Screenshot Thumbnails
            if (hasScreenshots) {
                screenshotsList.forEach((src, idx) => {
                    const img = document.createElement("img");
                    const proxiedSrc = `/api/proxy_image?url=${encodeURIComponent(src)}`;
                    img.src = proxiedSrc;
                    img.alt = "Screenshot thumbnail";
                    if (!hasVideos && idx === 0) img.className = "active";
                    
                    img.addEventListener("click", () => {
                        stopVideo();
                        if (elMainScreenshotImg) {
                            elMainScreenshotImg.src = proxiedSrc;
                            elMainScreenshotImg.style.display = "block";
                            elMainScreenshotImg.onclick = () => {
                                openScreenshotModal(proxiedSrc);
                            };
                        }
                        elScreenshotsContainer.querySelectorAll(".video-thumbnail-wrapper, img").forEach(i => i.classList.remove("active"));
                        img.classList.add("active");
                    });
                    elScreenshotsContainer.appendChild(img);
                });
            }
            elScreenshotsSection.style.display = "block";
        } else {
            elScreenshotsSection.style.display = "none";
        }
    }
}

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

if (elWarpSkipBtn) {
    elWarpSkipBtn.addEventListener("click", async () => {
        try {
            await fetch("/api/skip_warp");
            fetchState();
        } catch (e) {
            console.error("Failed to skip WARP installer check:", e);
        }
    });
}

if (elWarpRetryBtn) {
    elWarpRetryBtn.addEventListener("click", async () => {
        try {
            await fetch("/api/retry_warp");
            fetchState();
        } catch (e) {
            console.error("Failed to retry WARP installer process:", e);
        }
    });
}

// Bind browse catalog button inside dashboard
const elBackToCatalogBtnDownload = document.getElementById("btn-back-to-catalog-download");
if (elBackToCatalogBtnDownload) {
    elBackToCatalogBtnDownload.addEventListener("click", () => {
        setViewState("catalog");
    });
}

// Bind floating mini download badge click and controls
const elMiniBadge = document.getElementById("floating-download-badge");
if (elMiniBadge) {
    const elClickArea = document.getElementById("floating-bar-click-area");
    if (elClickArea) {
        elClickArea.addEventListener("click", () => {
            setViewState("downloading");
        });
    }
    
    const playPauseBtn = document.getElementById("mini-btn-play-pause");
    if (playPauseBtn) {
        playPauseBtn.addEventListener("click", async (e) => {
            e.stopPropagation();
            const api = appState.is_running ? "/api/pause" : "/api/start";
            try {
                const response = await fetch(api, { method: "POST" });
                if (response.ok) {
                    fetchState();
                }
            } catch (e) {
                console.error("Error toggling download status from floating bar:", e);
            }
        });
    }
    
    const cancelBtn = document.getElementById("mini-btn-cancel");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", async (e) => {
            e.stopPropagation();
            if (confirm("Вы уверены, что хотите остановить и сбросить текущую загрузку?")) {
                try {
                    const response = await fetch("/api/reset", { method: "POST" });
                    if (response.ok) {
                        fetchState();
                    }
                } catch (e) {
                    console.error("Error resetting queue from floating bar:", e);
                }
            }
        });
    }
}

// Start Polling Loop
fetchState();
setInterval(fetchState, 1000);

// iOS-style Premium Selection Modal and Details Bottom Bar Integration
const elModalSaveDirInput = document.getElementById("modal-save-dir-input");
const elModalGameNameInput = document.getElementById("modal-game-name-input");
const elModalBrowseDirBtn = document.getElementById("modal-btn-browse-dir");
const elModalStartDownloadBtn = document.getElementById("modal-btn-start-download");
const elDetailsDownloadTriggerBtn = document.getElementById("btn-details-download-trigger");
const downloadConfigModal = document.getElementById("download-config-modal");

function populateModalMirrors(filteredMirrors) {
    const modalMirrorsList = document.getElementById("modal-mirrors-list");
    if (!modalMirrorsList) return;
    modalMirrorsList.innerHTML = "";
    
    filteredMirrors.forEach((m, idx) => {
        const row = document.createElement("div");
        row.className = "modal-mirror-row" + (idx === 0 ? " selected" : "");
        row.setAttribute("data-name", m.name);
        row.setAttribute("data-url", m.url);
        
        let meta = "";
        if (m.name.toLowerCase().includes("gofile")) meta = "High Speed Mirror (No VPN needed)";
        else if (m.name.toLowerCase().includes("torrent")) meta = "P2P BitTorrent Magnet Link";
        else if (m.name.toLowerCase().includes("qiwi")) meta = "Direct Speed Hoster";
        else if (m.name.toLowerCase().includes("pixeldrain")) meta = "Fast & Stable Mirror";
        
        row.innerHTML = `
            <div class="mirror-row-info">
                <span class="mirror-row-name">${m.name}</span>
                ${meta ? `<span class="mirror-row-meta">${meta}</span>` : ""}
            </div>
            <div class="mirror-row-check">✔</div>
        `;
        
        row.addEventListener("click", () => {
            document.querySelectorAll(".modal-mirror-row").forEach(r => r.classList.remove("selected"));
            row.classList.add("selected");
            
            // Sync with hidden original mirrors list
            const pills = document.querySelectorAll(".mirror-pill");
            pills.forEach(p => {
                if (p.innerText.trim() === m.name.trim()) {
                    p.click();
                }
            });
        });
        
        modalMirrorsList.appendChild(row);
    });
}

// Bind modal inputs folder browsing
if (elModalBrowseDirBtn && elModalSaveDirInput) {
    elModalBrowseDirBtn.addEventListener("click", async () => {
        elModalBrowseDirBtn.setAttribute("disabled", "true");
        try {
            const response = await fetch("/api/browse_folder");
            const data = await response.json();
            if (response.ok && data.success && data.path) {
                elModalSaveDirInput.value = data.path;
                elSaveDirInput.value = data.path;
            }
        } catch (e) {
            console.error("Error browsing folder inside modal:", e);
        } finally {
            elModalBrowseDirBtn.removeAttribute("disabled");
        }
    });
}

// 2-Step Setup Modal Wizard Logic
let modalStep = 1;
const elModalBtnBack = document.getElementById("modal-btn-back");
const elModalNextIcon = document.getElementById("modal-next-icon");
const elModalStartIcon = document.getElementById("modal-start-icon");
const elModalBtnText = document.getElementById("modal-btn-text");
const elModalStep1Container = document.getElementById("modal-step-1");
const elModalStep2Container = document.getElementById("modal-step-2");

function setModalStep(step) {
    modalStep = step;
    if (step === 1) {
        if (elModalStep1Container) elModalStep1Container.style.display = "block";
        if (elModalStep2Container) elModalStep2Container.style.display = "none";
        if (elModalBtnBack) elModalBtnBack.style.display = "none";
        if (elModalNextIcon) elModalNextIcon.style.display = "inline-block";
        if (elModalStartIcon) elModalStartIcon.style.display = "none";
        if (elModalBtnText) elModalBtnText.innerText = "Next";
    } else if (step === 2) {
        if (elModalStep1Container) elModalStep1Container.style.display = "none";
        if (elModalStep2Container) elModalStep2Container.style.display = "block";
        if (elModalBtnBack) elModalBtnBack.style.display = "block";
        if (elModalNextIcon) elModalNextIcon.style.display = "none";
        if (elModalStartIcon) elModalStartIcon.style.display = "inline-block";
        if (elModalBtnText) elModalBtnText.innerText = "Confirm & Start Download";
    }
}

// Bind Details Bottom Bar trigger
if (elDetailsDownloadTriggerBtn && downloadConfigModal) {
    elDetailsDownloadTriggerBtn.addEventListener("click", () => {
        // Sync original inputs to modal fields
        if (elModalGameNameInput) elModalGameNameInput.value = elGameNameInput.value;
        if (elModalSaveDirInput) elModalSaveDirInput.value = elSaveDirInput.value;
        
        // Reset to Step 1
        setModalStep(1);
        
        // Open modal with smooth transition
        downloadConfigModal.style.display = "flex";
        setTimeout(() => {
            downloadConfigModal.classList.add("active");
        }, 15);
    });
}

// Bind modal back button click
if (elModalBtnBack) {
    elModalBtnBack.addEventListener("click", () => {
        setModalStep(1);
    });
}

// Bind Modal Next / Start Download
if (elModalStartDownloadBtn && downloadConfigModal) {
    elModalStartDownloadBtn.addEventListener("click", () => {
        try {
            const gameTitle = elModalGameNameInput ? elModalGameNameInput.value.trim() : "";
            const downloadDir = elModalSaveDirInput ? elModalSaveDirInput.value.trim() : "";
            
            // Sync values to the original inputs
            if (elGameNameInput) elGameNameInput.value = gameTitle;
            if (elSaveDirInput) elSaveDirInput.value = downloadDir;
            
            if (modalStep === 1) {
                if (!downloadDir) {
                    alert("Please select a save directory first!");
                    return;
                }
                setModalStep(2);
            } else {
                confirmDownloadQueue(gameTitle, downloadDir);
            }
        } catch (e) {
            console.error("Error clicking Next button:", e);
            alert("Failed to proceed: " + e.message);
        }
    });
}

// Dismiss modal when clicking overlay background
if (downloadConfigModal) {
    downloadConfigModal.addEventListener("click", (e) => {
        if (e.target === downloadConfigModal) {
            downloadConfigModal.classList.remove("active");
            setTimeout(() => {
                downloadConfigModal.style.display = "none";
            }, 250);
        }
    });
}

// Google Translate API Integration
async function translateText(text) {
    if (!text || !text.trim()) return "";
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=ru&dt=t&q=${encodeURIComponent(text)}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error("Translation request failed");
    const data = await response.json();
    return data[0].map(item => item[0]).join("");
}

let originalDesc = "";
let translatedDesc = "";
let isDescTranslated = false;

const btnTranslateDesc = document.getElementById("btn-translate-desc");
if (btnTranslateDesc) {
    btnTranslateDesc.addEventListener("click", async (e) => {
        e.stopPropagation(); // Avoid collapsible trigger toggle
        const elText = document.getElementById("game-description");
        if (!elText) return;
        
        if (!originalDesc) {
            originalDesc = elText.innerText;
        }
        
        if (isDescTranslated) {
            elText.innerText = originalDesc;
            btnTranslateDesc.querySelector(".btn-translate-text").innerText = "Translate";
            isDescTranslated = false;
        } else {
            if (translatedDesc) {
                elText.innerText = translatedDesc;
                btnTranslateDesc.querySelector(".btn-translate-text").innerText = "Original";
                isDescTranslated = true;
            } else {
                btnTranslateDesc.innerHTML = "<span>🇷🇺</span> <span class='btn-translate-text'>Translating...</span>";
                btnTranslateDesc.setAttribute("disabled", "true");
                try {
                    translatedDesc = await translateText(originalDesc);
                    elText.innerText = translatedDesc;
                    btnTranslateDesc.querySelector(".btn-translate-text").innerText = "Original";
                    isDescTranslated = true;
                } catch (err) {
                    console.error("Translation error:", err);
                    alert("Translation failed. Check internet connection.");
                } finally {
                    btnTranslateDesc.innerHTML = "<span>🇷🇺</span> <span class='btn-translate-text'>" + (isDescTranslated ? "Original" : "Translate") + "</span>";
                    btnTranslateDesc.removeAttribute("disabled");
                }
            }
        }
    });
}

let originalFeatures = [];
let translatedFeatures = [];
let isFeaturesTranslated = false;

const btnTranslateFeatures = document.getElementById("btn-translate-features");
if (btnTranslateFeatures) {
    btnTranslateFeatures.addEventListener("click", async (e) => {
        e.stopPropagation(); // Avoid collapsible trigger toggle
        const elList = document.getElementById("repack-features-list");
        if (!elList) return;
        
        const listItems = Array.from(elList.querySelectorAll("li"));
        if (listItems.length === 0) return;
        
        if (originalFeatures.length === 0) {
            originalFeatures = listItems.map(li => li.innerText);
        }
        
        if (isFeaturesTranslated) {
            elList.innerHTML = originalFeatures.map(txt => `<li>${txt}</li>`).join("");
            btnTranslateFeatures.querySelector(".btn-translate-text").innerText = "Translate";
            isFeaturesTranslated = false;
        } else {
            if (translatedFeatures.length > 0) {
                elList.innerHTML = translatedFeatures.map(txt => `<li>${txt}</li>`).join("");
                btnTranslateFeatures.querySelector(".btn-translate-text").innerText = "Original";
                isFeaturesTranslated = true;
            } else {
                btnTranslateFeatures.setAttribute("disabled", "true");
                btnTranslateFeatures.innerHTML = "<span>🇷🇺</span> <span class='btn-translate-text'>Translating...</span>";
                const textToTranslate = originalFeatures.join("\n");
                try {
                    const translatedText = await translateText(textToTranslate);
                    translatedFeatures = translatedText.split("\n");
                    elList.innerHTML = translatedFeatures.map(txt => `<li>${txt}</li>`).join("");
                    btnTranslateFeatures.querySelector(".btn-translate-text").innerText = "Original";
                    isFeaturesTranslated = true;
                } catch (err) {
                    console.error("Translation error:", err);
                    alert("Translation failed. Check internet connection.");
                } finally {
                    btnTranslateFeatures.innerHTML = "<span>🇷🇺</span> <span class='btn-translate-text'>" + (isFeaturesTranslated ? "Original" : "Translate") + "</span>";
                    btnTranslateFeatures.removeAttribute("disabled");
                }
            }
        }
    });
}

function resetTranslationCache() {
    originalDesc = "";
    translatedDesc = "";
    isDescTranslated = false;
    originalFeatures = [];
    translatedFeatures = [];
    isFeaturesTranslated = false;
    
    if (btnTranslateDesc) {
        const textSpan = btnTranslateDesc.querySelector(".btn-translate-text");
        if (textSpan) textSpan.innerText = "Translate";
    }
    if (btnTranslateFeatures) {
        const textSpan = btnTranslateFeatures.querySelector(".btn-translate-text");
        if (textSpan) textSpan.innerText = "Translate";
    }
}
