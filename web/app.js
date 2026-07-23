// Global Elements
const elStartPauseBtn = document.getElementById("btn-start-pause");
const elExtractBtn = document.getElementById("btn-extract");
const elInstallBtn = document.getElementById("btn-install");
const elResetSessionBtn = document.getElementById("btn-reset-session");
const elResetSessionBtnDashboard = document.getElementById("btn-reset-session-dashboard");
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

// Haze Background Elements — Harmonoid AnimatedMeshGradient (WebGL mesh_gradient 1:1)
const elHazeRoot = document.getElementById("haze-background");
const elHazeSrcImg = document.getElementById("haze-src-img");
const elHazeMeshA = document.getElementById("haze-mesh-a");
const elHazeMeshB = document.getElementById("haze-mesh-b");
let activeHazeUrl = "";
let hazeMeshActiveIsA = true;
let lastHazePaletteKey = "";
let hazeApplyGeneration = 0;
let dynamicResetTimeout = null;
let hazeAnimRaf = 0;

/**
 * Open FitGirl through local reverse proxy (Python fetches via DoH).
 * Browser DNS in DE/RU is blocked — direct fitgirl-repacks.site fails;
 * localhost proxy serves the real site HTML+CSS+images.
 */
function getOpenBrowserUrl(originalUrl) {
    if (!originalUrl) return originalUrl;
    const u = String(originalUrl);
    if (u.includes("fitgirl-repacks.site") || u.includes("paste.fitgirl-repacks.site")) {
        // Absolute origin so target=_blank always hits our server, not a relative dead tab
        const origin = (typeof location !== "undefined" && location.origin)
            ? location.origin
            : "http://127.0.0.1:8000";
        return `${origin}/api/proxy_page?url=${encodeURIComponent(u)}`;
    }
    return originalUrl;
}

function getFitGirlHomeProxyUrl() {
    return getOpenBrowserUrl("https://fitgirl-repacks.site/");
}

// Download View Elements
const elActiveGameTitle = document.getElementById("active-game-title");
const elActiveGameSubtitle = document.getElementById("active-game-subtitle");
const elDownloadDirDisplay = document.getElementById("download-dir-display");
const elQueueContainer = document.getElementById("queue-list-container");
const elQueueCompletedCount = document.getElementById("queue-completed-count");

const elTotalProgressText = document.getElementById("total-progress-text");
const elTotalProgressTextSidebar = document.getElementById("total-progress-text-sidebar");
const elGlobalSpeed = document.getElementById("global-speed");
const elGlobalTimeLeft = document.getElementById("global-time-left");
const svgProgressCircleBar = document.querySelector(".progress-circle-bar");
const svgDashboardProgressBar = document.getElementById("dashboard-progress-bar");
const elCurrentFileLine = document.getElementById("current-file-progress-line");
const elCurrentFileName = document.getElementById("current-file-name");
const elCurrentFilePct = document.getElementById("current-file-pct");
const elCurrentFileSize = document.getElementById("current-file-size");
const elCurrentFileSpeed = document.getElementById("current-file-speed");

/** Active downloading/connecting file (or first waiting if idle). */
function getActiveDownloadFile(state) {
    const files = (state && state.files) || [];
    if (!files.length) return null;
    const idx = typeof state.active_index === "number" ? state.active_index : -1;
    if (idx >= 0 && idx < files.length) {
        const f = files[idx];
        if (f && ["downloading", "connecting", "copying"].includes(f.status)) return f;
    }
    const active = files.find((f) =>
        ["downloading", "connecting", "copying"].includes(f.status)
    );
    if (active) return active;
    // paused/idle: show first incomplete as context
    return files.find((f) => f.status !== "finished") || null;
}

function shortFileName(name, maxLen = 42) {
    const n = String(name || "").trim();
    if (!n) return "—";
    if (n.length <= maxLen) return n;
    const keep = maxLen - 1;
    const head = Math.ceil(keep * 0.55);
    const tail = keep - head;
    return n.slice(0, head) + "…" + n.slice(-tail);
}

/** Compact size for file line: always prefer MB/GB for readability. */
function formatFileSizePair(downloaded, total) {
    const d = Math.max(0, Number(downloaded) || 0);
    const t = Math.max(0, Number(total) || 0);
    if (t <= 0 && d <= 0) return "0 / ? MB";
    if (t <= 0) return `${formatBytes(d, 1)} / ?`;
    // Same unit for both when possible (prefer MB for mid-size parts)
    if (t < 1024 * 1024 * 1024) {
        const dm = d / (1024 * 1024);
        const tm = t / (1024 * 1024);
        return `${dm.toFixed(1)} / ${tm.toFixed(1)} MB`;
    }
    const dg = d / (1024 * 1024 * 1024);
    const tg = t / (1024 * 1024 * 1024);
    return `${dg.toFixed(2)} / ${tg.toFixed(2)} GB`;
}

function updateCurrentFileProgressLine(state) {
    const f = getActiveDownloadFile(state);
    const line = elCurrentFileLine;
    const elName = elCurrentFileName;
    const elPct = elCurrentFilePct;
    const elSize = elCurrentFileSize;
    const elSpeed = elCurrentFileSpeed;
    const elMiniRow = document.getElementById("mini-current-file-row");
    const elMiniName = document.getElementById("mini-current-file-name");
    const elMiniPct = document.getElementById("mini-current-file-pct");
    const elMiniSize = document.getElementById("mini-current-file-size");
    const elMiniSpeed = document.getElementById("mini-current-file-speed");

    if (!f) {
        if (line) line.classList.add("is-idle");
        if (elName) {
            elName.textContent = "No active file";
            elName.title = "";
        }
        if (elPct) elPct.textContent = "—";
        if (elSize) elSize.textContent = "—";
        if (elSpeed) elSpeed.textContent = "—";
        if (elMiniRow) elMiniRow.hidden = true;
        return;
    }

    const fullName = f.filename || "file";
    const downloaded = Number(f.downloaded) || 0;
    let total = Number(f.size) || 0;
    if (total <= 0 && f.type === "installer") total = 7468619;
    let pct = typeof f.progress === "number" ? f.progress : 0;
    if ((!pct || pct === 0) && total > 0 && downloaded > 0) {
        pct = Math.min(100, Math.floor((downloaded / total) * 100));
    }
    pct = Math.max(0, Math.min(100, Math.round(pct)));
    const fileSpeed = Number(f.speed) || 0;
    const isActive =
        f.status === "downloading" || f.status === "connecting" || f.status === "copying";
    const statusHint =
        f.status === "connecting"
            ? "connecting"
            : f.status === "copying"
              ? "copying"
              : f.status === "waiting"
                ? "queued"
                : f.status === "failed"
                  ? "failed"
                  : "";
    const short = shortFileName(fullName, 36);
    const sizeLabel = formatFileSizePair(downloaded, total);
    const speedLabel =
        isActive && fileSpeed > 0
            ? formatSpeed(fileSpeed)
            : f.status === "connecting"
              ? "…"
              : f.status === "waiting"
                ? "—"
                : "0.0 MB/s";
    const pctLabel =
        statusHint && f.status !== "downloading" ? `${pct}% · ${statusHint}` : `${pct}%`;

    if (line) line.classList.toggle("is-idle", f.status === "waiting" || f.status === "finished");
    if (elName) {
        elName.textContent = short;
        elName.title =
            `${fullName}` +
            (f.status ? ` (${f.status})` : "") +
            ` · ${sizeLabel}` +
            (fileSpeed > 0 ? ` · ${formatSpeed(fileSpeed)}` : "");
    }
    if (elPct) elPct.textContent = pctLabel;
    if (elSize) elSize.textContent = sizeLabel;
    if (elSpeed) elSpeed.textContent = speedLabel;

    if (elMiniRow && elMiniName && elMiniPct) {
        elMiniRow.hidden = false;
        elMiniName.textContent = shortFileName(fullName, 28);
        elMiniName.title = fullName;
        elMiniPct.textContent = `${pct}%`;
        if (elMiniSize) elMiniSize.textContent = sizeLabel;
        if (elMiniSpeed) elMiniSpeed.textContent = speedLabel;
    }
}

/**
 * Derive session phase from backend state.
 * ready    — session configured, nothing downloaded yet
 * paused   — partial progress, not running
 * downloading / starting — engine running
 * complete — every file finished (or 100%)
 * none     — no active session
 */
function getDownloadSessionInfo(state) {
    const files = (state && state.files) || [];
    const fileCount = files.length;
    const doneCount = files.filter(f => f.status === "finished").length;
    const failedCount = files.filter(f => f.status === "failed").length;
    const activeCount = files.filter(f =>
        f.status === "downloading" || f.status === "connecting" || f.status === "copying"
    ).length;
    const anyBytes = files.some(f => (f.downloaded || 0) > 0 || f.status === "finished");
    const pct = typeof state?.total_progress === "number" ? state.total_progress : 0;
    const anyProgress = anyBytes || pct > 0;
    const allDone = fileCount > 0 && doneCount === fileCount;
    const completeByProgress = fileCount > 0 && pct >= 100 && doneCount === fileCount;

    let phase = "none";
    if (state?.is_configured && fileCount > 0) {
        if (allDone || completeByProgress) {
            phase = "complete";
        } else if (state.is_running && activeCount > 0) {
            phase = "downloading";
        } else if (state.is_running) {
            phase = "starting";
        } else if (!anyProgress) {
            phase = "ready";
        } else {
            phase = "paused";
        }
    } else if (state?.is_configured && fileCount === 0) {
        phase = "ready";
    }

    return {
        phase,
        pct,
        fileCount,
        doneCount,
        failedCount,
        activeCount,
        anyProgress,
        allDone: allDone || completeByProgress,
        title: (state?.game_title || "").trim()
    };
}

function applyDownloadStatusBadge(elBadge, phase) {
    if (!elBadge) return;
    const styles = {
        ready: {
            text: "READY",
            bg: "rgba(52, 152, 219, 0.15)",
            border: "rgba(52, 152, 219, 0.4)",
            color: "#5dade2"
        },
        starting: {
            text: "STARTING",
            bg: "rgba(155, 89, 182, 0.15)",
            border: "rgba(155, 89, 182, 0.35)",
            color: "#be90d4"
        },
        downloading: {
            text: "DOWNLOADING",
            bg: "rgba(155, 89, 182, 0.15)",
            border: "rgba(155, 89, 182, 0.35)",
            color: "#be90d4"
        },
        paused: {
            text: "PAUSED",
            bg: "rgba(230, 126, 34, 0.15)",
            border: "rgba(230, 126, 34, 0.35)",
            color: "#f39c12"
        },
        complete: {
            text: "COMPLETE",
            bg: "rgba(46, 204, 113, 0.15)",
            border: "rgba(46, 204, 113, 0.4)",
            color: "#2ecc71"
        },
        none: {
            text: "IDLE",
            bg: "rgba(255, 255, 255, 0.06)",
            border: "rgba(255, 255, 255, 0.12)",
            color: "#a0a0b0"
        }
    };
    const s = styles[phase] || styles.none;
    elBadge.innerText = s.text;
    elBadge.style.background = s.bg;
    elBadge.style.borderColor = s.border;
    elBadge.style.color = s.color;
}

function setProgressCircle(offset, pctText) {
    if (svgProgressCircleBar) svgProgressCircleBar.style.strokeDashoffset = offset;
    if (svgDashboardProgressBar) svgDashboardProgressBar.style.strokeDashoffset = offset;
    if (elTotalProgressText) elTotalProgressText.innerText = pctText;
    if (elTotalProgressTextSidebar) elTotalProgressTextSidebar.innerText = pctText;
}

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
const openQueueGroups = new Set();
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

function updateWarpSettingsPanel(newState) {
    const elStatus = document.getElementById("warp-settings-status");
    const elInstall = document.getElementById("btn-warp-install");
    const elRotate = document.getElementById("btn-warp-rotate");
    if (!elStatus) return;

    const status = newState.warp_status || "unknown";
    const connected = !!newState.warp_connected;
    let label = "Cloudflare WARP: unknown";
    let color = "var(--text-muted)";

    if (status === "installing" || status === "checking") {
        label = status === "installing"
            ? "Downloading / installing Cloudflare WARP…"
            : "Checking Cloudflare WARP…";
        color = "#f5c542";
        if (elInstall) {
            elInstall.disabled = true;
            elInstall.innerText = "Working…";
        }
    } else if (status === "installed") {
        label = connected
            ? "✓ WARP installed and connected — auto IP rotate on Pixeldrain limit"
            : "✓ WARP installed (connecting…) — auto IP rotate on Pixeldrain limit";
        color = "#3dd68c";
        if (elInstall) {
            elInstall.disabled = true;
            elInstall.innerText = "Installed";
        }
        if (elRotate) elRotate.disabled = false;
    } else if (status === "error") {
        label = "WARP not ready: " + (newState.warp_error_message || "install failed");
        color = "#ff6b6b";
        if (elInstall) {
            elInstall.disabled = false;
            elInstall.innerText = "Download / Install WARP";
        }
    } else if (status === "skipped") {
        label = "WARP skipped at startup — install here to unlock high Pixeldrain speed";
        color = "#f5c542";
        if (elInstall) {
            elInstall.disabled = false;
            elInstall.innerText = "Download / Install WARP";
        }
    } else {
        if (elInstall) {
            elInstall.disabled = false;
            elInstall.innerText = "Download / Install WARP";
        }
    }

    elStatus.style.color = color;
    elStatus.innerText = label;
}

function handleWarpState(newState) {
    updateWarpSettingsPanel(newState);
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
        // installed or skipped — hide blocking modal
        elWarpModal.style.display = "none";
    }
}

// Update UI based on loaded state
function updateUI(newState) {
    handleWarpState(newState);
    
    // Pixeldrain free-cap: backend auto-rotates WARP; UI also kicks rotate ONCE
    // without waiting for the user to spam buttons (clicking did nothing useful before).
    if (newState.pixeldrain_limit_reached && !isShowingPixeldrainLimitAlert) {
        isShowingPixeldrainLimitAlert = true;
        const hasWarp = newState.warp_status === "installed";

        // Silent auto-kick immediately (no user click required)
        (async () => {
            try {
                if (hasWarp) {
                    console.log("[AUTO-WARP UI] pixeldrain_limit_reached → /api/warp/rotate");
                    await fetch("/api/warp/rotate", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: "{}",
                    });
                    // Backend already pause/resumes workers; just refresh UI after a bit
                    setTimeout(() => fetchState(), 10000);
                }
            } catch (e) {
                console.error("[AUTO-WARP UI] rotate failed", e);
            } finally {
                // Allow another auto-kick in 90s if still limited
                setTimeout(() => {
                    isShowingPixeldrainLimitAlert = false;
                    try { fetch("/api/clear_pixeldrain_limit"); } catch (_) {}
                }, 90000);
            }
        })();

        // Non-blocking toast only (don't freeze UI on modal that needs clicks)
        if (typeof Swal !== "undefined") {
            Swal.fire({
                toast: true,
                position: "top-end",
                timer: 6000,
                showConfirmButton: false,
                icon: hasWarp ? "info" : "warning",
                title: hasWarp
                    ? "Pixeldrain free-cap — auto WARP IP rotate…"
                    : "Pixeldrain free-cap — install WARP in Settings",
                background: "#040409",
                color: "#e2e2ec",
            });
        }
    }

    // 1. Manage setup vs download views
    syncViewState();
    
    const sessionInfo = getDownloadSessionInfo(newState);

    if (newState.is_configured) {
        // Always show session identity (even when idle / complete / not started)
        const displayTitle = sessionInfo.title || "Custom Repack";
        if (elActiveGameTitle) elActiveGameTitle.innerText = displayTitle;
        if (elActiveGameSubtitle) {
            elActiveGameSubtitle.innerText = newState.download_dir
                ? `Save directory: ${newState.download_dir}`
                : "Save directory: not set";
        }
        if (elDownloadDirDisplay) elDownloadDirDisplay.value = newState.download_dir || "";
        
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
        if (elDownloadMirrorBadge) {
            if (newState.active_mirror) {
                elDownloadMirrorBadge.innerText = `Mirror: ${newState.active_mirror}`;
                elDownloadMirrorBadge.style.display = "inline-block";
            } else {
                elDownloadMirrorBadge.style.display = "none";
            }
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
        
        // Sync Play/Pause Button & Status Badge from real session phase
        const elDownloadStatusBadge = document.getElementById("download-status-badge");
        applyDownloadStatusBadge(elDownloadStatusBadge, sessionInfo.phase);

        if (elStartPauseBtn) {
            if (sessionInfo.phase === "downloading" || sessionInfo.phase === "starting") {
                elStartPauseBtn.innerHTML = `
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                    </svg>
                    <span>Pause</span>
                `;
                elStartPauseBtn.classList.remove("btn-pulse");
                elStartPauseBtn.style.backgroundColor = "#e67e22";
                elStartPauseBtn.style.borderColor = "#d35400";
                elStartPauseBtn.disabled = false;
                elStartPauseBtn.style.opacity = "1";
            } else if (sessionInfo.phase === "complete") {
                elStartPauseBtn.innerHTML = `
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                    </svg>
                    <span>Downloaded</span>
                `;
                elStartPauseBtn.classList.remove("btn-pulse");
                elStartPauseBtn.style.backgroundColor = "rgba(46, 204, 113, 0.2)";
                elStartPauseBtn.style.borderColor = "rgba(46, 204, 113, 0.45)";
                // Keep enabled so user can re-trigger if needed; server will no-op empty work
                elStartPauseBtn.disabled = false;
                elStartPauseBtn.style.opacity = "1";
            } else if (sessionInfo.phase === "ready") {
                elStartPauseBtn.innerHTML = `
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M8 5v14l11-7z"/>
                    </svg>
                    <span>Start Download</span>
                `;
                elStartPauseBtn.classList.add("btn-pulse");
                elStartPauseBtn.style.backgroundColor = "";
                elStartPauseBtn.style.borderColor = "";
                elStartPauseBtn.disabled = false;
                elStartPauseBtn.style.opacity = "1";
            } else {
                // paused / partial
                elStartPauseBtn.innerHTML = `
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M8 5v14l11-7z"/>
                    </svg>
                    <span>Resume</span>
                `;
                elStartPauseBtn.classList.add("btn-pulse");
                elStartPauseBtn.style.backgroundColor = "";
                elStartPauseBtn.style.borderColor = "";
                elStartPauseBtn.disabled = false;
                elStartPauseBtn.style.opacity = "1";
            }
        }
        
        // 2. Overall Download Progress & Speeds
        const isDownloading = sessionInfo.phase === "downloading";
        if (isDownloading && newState.total_speed > 0) {
            if (smoothedSpeed === 0) {
                smoothedSpeed = newState.total_speed;
            } else {
                smoothedSpeed = 0.05 * newState.total_speed + 0.95 * smoothedSpeed;
            }
        } else if (!isDownloading && sessionInfo.phase !== "starting") {
            smoothedSpeed = 0;
        }

        if (elGlobalSpeed) {
            elGlobalSpeed.innerText = (isDownloading || sessionInfo.phase === "starting")
                ? formatSpeed(smoothedSpeed > 0 ? smoothedSpeed : newState.total_speed)
                : "0.0 MB/s";
        }

        const progressPct = Math.max(0, Math.min(100, Number(newState.total_progress) || 0));
        const offset = 283 - (283 * progressPct) / 100;
        setProgressCircle(offset, `${progressPct}%`);

        // Second line under overall progress: current file · file%
        updateCurrentFileProgressLine(newState);
        
        // ETA / status under progress ring
        if (elGlobalTimeLeft) {
            if (sessionInfo.phase === "complete") {
                elGlobalTimeLeft.innerText = "Complete";
            } else if (sessionInfo.phase === "ready") {
                elGlobalTimeLeft.innerText = "Not started";
            } else if (sessionInfo.phase === "paused") {
                elGlobalTimeLeft.innerText = "Paused";
            } else if (isDownloading && smoothedSpeed > 0) {
                let totalBytesLeft = 0;
                newState.files.forEach(f => {
                    if (f.status !== "finished") {
                        let expectedSize = f.size;
                        if (expectedSize <= 0) {
                            expectedSize = f.type === "installer" ? 7468619 : 524288000;
                        }
                        totalBytesLeft += Math.max(0, expectedSize - (f.downloaded || 0));
                    }
                });
                const totalSecondsLeft = Math.floor(totalBytesLeft / smoothedSpeed);
                elGlobalTimeLeft.innerText = formatTime(totalSecondsLeft);
            } else if (sessionInfo.phase === "starting") {
                elGlobalTimeLeft.innerText = "Starting…";
            } else {
                elGlobalTimeLeft.innerText = "Waiting…";
            }
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
        
        // 4. Completed items count (finished only — not "progressed")
        const completedCount = newState.files.filter(f => f.status === "finished").length;
        const failedCount = newState.files.filter(f => f.status === "failed").length;
        elQueueCompletedCount.innerText = failedCount > 0
            ? `${completedCount} / ${newState.files.length} done · ${failedCount} failed`
            : `${completedCount} / ${newState.files.length} completed`;
        
        // Helpers: treat finished files as fully downloaded for UI math
        const fileDownloadedBytes = (f) => {
            if (!f) return 0;
            if (f.status === "finished") {
                return (f.size && f.size > 0) ? f.size : (f.downloaded || 0);
            }
            return f.downloaded || 0;
        };
        const fileProgressPct = (f) => {
            if (!f) return 0;
            if (f.status === "finished") return 100;
            if (f.size > 0) return Math.min(100, Math.floor(((f.downloaded || 0) / f.size) * 100));
            return Math.min(100, f.progress || 0);
        };
        const statusLabel = (s) => {
            const map = {
                waiting: "Waiting",
                connecting: "Connecting",
                downloading: "Downloading",
                copying: "Copying",
                finished: "Done",
                failed: "Failed",
                paused: "Paused"
            };
            return map[s] || s;
        };
        
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
                    details.open = openQueueGroups.has(baseName);
                    
                    details.addEventListener("toggle", () => {
                        if (details.open) {
                            openQueueGroups.add(baseName);
                        } else {
                            openQueueGroups.delete(baseName);
                        }
                    });
                    
                    // Calculate group aggregates (finished parts count as full size)
                    const totalSize = groupItems.reduce((sum, item) => sum + (item.file.size || 0), 0);
                    const totalDownloaded = groupItems.reduce((sum, item) => sum + fileDownloadedBytes(item.file), 0);
                    const finishedInGroup = groupItems.filter(item => item.file.status === "finished").length;
                    const groupProgress = totalSize > 0
                        ? Math.min(100, Math.floor((totalDownloaded / totalSize) * 100))
                        : Math.floor((finishedInGroup / groupItems.length) * 100);
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
                    } else if (statuses.includes("failed") && !statuses.includes("downloading") && !statuses.includes("connecting")) {
                        overallStatus = "failed";
                    }
                    
                    let activeClass = (overallStatus === "downloading" || overallStatus === "connecting" || overallStatus === "copying") ? "active" : "";
                    const sizeText = totalSize > 0 ? formatBytes(totalSize) : "Pending...";
                    const speedText = overallStatus === "downloading" ? formatSpeed(groupSpeed) : "";
                    
                    details.innerHTML = `
                        <summary class="queue-group-summary ${activeClass}">
                            <div class="summary-header">
                                <span class="summary-toggle-icon">▸</span>
                                <div class="file-name" title="${baseName}">${baseName}</div>
                                <div class="file-badge game_part">${finishedInGroup}/${groupItems.length} parts</div>
                                <div class="file-progress-container">
                                    <div class="progress-bar-bg">
                                        <div class="progress-bar-fill status-${overallStatus}" style="width: ${groupProgress}%"></div>
                                    </div>
                                    <div class="file-progress-text">
                                        <span>${groupProgress}% · ${formatBytes(totalDownloaded)} / ${sizeText}</span>
                                        <span class="file-speed">${speedText}</span>
                                    </div>
                                </div>
                                <div class="file-status ${overallStatus}">${statusLabel(overallStatus)}</div>
                                <div class="file-actions">
                                    ${statuses.includes("failed") ? `<button class="btn btn-accent btn-retry-group">Retry failed</button>` : ""}
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
                        const childPct = fileProgressPct(childFile);
                        const childDl = fileDownloadedBytes(childFile);
                        
                        childItem.innerHTML = `
                            <div class="file-name" title="${childFile.filename}">${cleanFilename(childFile.filename)}</div>
                            <div class="file-progress-container">
                                <div class="progress-bar-bg">
                                    <div class="progress-bar-fill status-${childFile.status}" style="width: ${childPct}%"></div>
                                </div>
                                <div class="file-progress-text">
                                    <span>${childPct}% · ${formatBytes(childDl)} / ${childSizeText}</span>
                                    <span class="file-speed">${childSpeedText}</span>
                                </div>
                            </div>
                            <div class="file-status ${childFile.status}">${statusLabel(childFile.status)}</div>
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
                    const pct = fileProgressPct(file);
                    const dl = fileDownloadedBytes(file);
                    
                    item.innerHTML = `
                        <div class="file-name" title="${file.filename}">${cleanFilename(file.filename)}</div>
                        <div class="file-badge ${file.type}">${badgeText}</div>
                        <div class="file-progress-container">
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill status-${file.status}" style="width: ${pct}%"></div>
                            </div>
                            <div class="file-progress-text">
                                <span>${pct}% · ${formatBytes(dl)} / ${sizeText}</span>
                                <span class="file-speed">${speedText}</span>
                            </div>
                        </div>
                        <div class="file-status ${file.status}">${statusLabel(file.status)}</div>
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

// ---- Details page cache (memory + localStorage) so revisiting games is instant ----
const detailsPageCache = new Map();
const DETAILS_CACHE_STORAGE_KEY = "fg_details_cache_v9";
const DETAILS_CACHE_MAX = 40;

(function hydrateDetailsCache() {
    try {
        const raw = localStorage.getItem(DETAILS_CACHE_STORAGE_KEY);
        if (!raw) return;
        const obj = JSON.parse(raw);
        Object.entries(obj || {}).forEach(([k, v]) => {
            if (v && v.success) detailsPageCache.set(k, v);
        });
    } catch (_) {}
})();

function persistDetailsCache() {
    try {
        const obj = {};
        let n = 0;
        for (const [k, v] of detailsPageCache) {
            if (n++ >= DETAILS_CACHE_MAX) break;
            obj[k] = v;
        }
        localStorage.setItem(DETAILS_CACHE_STORAGE_KEY, JSON.stringify(obj));
    } catch (_) {}
}

function cacheKeyForUrl(url) {
    return (url || "").trim().replace(/\/+$/, "").toLowerCase();
}

/** Format repack size for UI: "55/55.1 GB" → "55–55.1 GB" (not progress-looking). */
function formatRepackSizeDisplay(sizeStr) {
    if (!sizeStr || sizeStr === "Unknown" || sizeStr === "—") return sizeStr || "";
    let s = String(sizeStr).trim();
    s = s.replace(
        /\s+(?:Download\s+Mirrors?|Filehoster|Genres?\/Tags?|Companies?|Languages?).*$/i,
        ""
    ).trim();
    const m = s.match(/^([\d]+(?:[.,][\d]+)?)\s*\/\s*([\d]+(?:[.,][\d]+)?)\s*([A-Za-z]+)?\s*$/);
    if (m) {
        const unit = (m[3] || "GB").trim();
        return `${m[1]}–${m[2]} ${unit}`;
    }
    // already en-dash form
    return s.replace(/\//g, "–");
}

/** Drop FitGirl "Included Bonus Content / Soundtracks" dumps from description text. */
function stripBonusContentFromDescription(text) {
    if (!text) return text;
    let out = String(text);
    // Cut from first bonus header to end
    out = out.replace(
        /(?:\n|^)\s*(?:•\s*)?(?:included\s+)?bonus\s+(?:content|soundtracks?|osts?|materials?|extras?)(?:\s*\([^)]*\))?\s*:?\s*\n[\s\S]*$/i,
        ""
    );
    out = out.replace(
        /(?:\n|^)\s*(?:•\s*)?включ[её]нн\w*\s+бонусн\w*[\s\S]*$/i,
        ""
    );
    const lines = out.split("\n");
    const cleaned = [];
    let skip = false;
    const isBonusHeader = (ln) => {
        const low = (ln || "").trim().toLowerCase().replace(/^[•·*\-–—]\s*/, "").replace(/:+\s*$/, "");
        if (/^(included\s+)?bonus\s+(content|soundtracks?|osts?|materials?|extras?)(\s*\([^)]*\))?$/.test(low)) return true;
        if (/included bonus/.test(low) && /(content|soundtrack|ost|non-audio|audio)/.test(low)) return true;
        return false;
    };
    const isResume = (ln) => {
        const low = (ln || "").trim().toLowerCase().replace(/:+\s*$/, "");
        return /^(game features|features|pc features|about this game|about the game|story|plot)$/.test(low);
    };
    for (const ln of lines) {
        if (isBonusHeader(ln)) { skip = true; continue; }
        if (skip) {
            if (isResume(ln)) { skip = false; cleaned.push(ln); }
            continue;
        }
        cleaned.push(ln);
    }
    return cleaned.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

function applyAnalyzeResult(url, data, gen = detailsOpenGeneration) {
    // Drop stale responses from a previous game click
    if (gen !== detailsOpenGeneration) {
        console.warn("Stale analyze result ignored", url);
        return;
    }
    // Shared apply path for network + cache hits
    if (data.type === "fitgirl_page") {
        // Always sanitize description (cache may predate bonus strip)
        if (data.description) data.description = stripBonusContentFromDescription(data.description);
// Populate metadata sidebar
                scrapedMetadata.original_size = data.original_size || "Unknown";
                scrapedMetadata.repack_size = data.repack_size || "Unknown";
                scrapedMetadata.cover_image = data.cover_image || "";
                
                elDetailsGameTitle.innerText = data.title || "Custom Repack";
                // Version pill removed from UI (v9.7 etc. is confusing noise in the header)
                if (elDetailsVersionBadge) {
                    elDetailsVersionBadge.style.display = "none";
                    elDetailsVersionBadge.innerText = "";
                }
                
                // Open in Browser URL mapping
                if (elBtnOpenBrowser) {
                    elBtnOpenBrowser.href = getOpenBrowserUrl(url);
                    elBtnOpenBrowser.style.display = "inline-block";
                }
                const btnOpenTop = document.getElementById("btn-open-browser-top");
                if (btnOpenTop) {
                    btnOpenTop.style.display = "none";
                    btnOpenTop.setAttribute("hidden", "");
                    btnOpenTop.setAttribute("aria-hidden", "true");
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
                
                // Reset translation caches for this game
                originalDesc = "";
                translatedDesc = "";
                isDescTranslated = false;
                originalFeatures = [];
                translatedFeatures = [];
                isFeaturesTranslated = false;

                // Render description / About the Game
                const descSection = document.getElementById("details-desc-section");
                if (descSection && elGameDescription) {
                    const cleanDesc = (data.description || "").trim();
                    if (cleanDesc) {
                        originalDesc = cleanDesc;
                        // prepareDetailsView hides this with display:none — always restore
                        elGameDescription.style.display = "block";
                        elGameDescription.innerHTML = cleanDesc.replace(/\n/g, "<br>");
                        descSection.style.display = "block";
                        descSection.classList.add("active");
                        // Auto-translate AFTER setting English source (don't mix features)
                        if (typeof translateText === "function") {
                            translateText(cleanDesc).then(translated => {
                                // Only apply if still viewing same description
                                if (originalDesc === cleanDesc && translated) {
                                    translatedDesc = translated;
                                    elGameDescription.style.display = "block";
                                    elGameDescription.innerHTML = translated.replace(/\n/g, "<br>");
                                    isDescTranslated = true;
                                    const btn = document.getElementById("btn-translate-desc");
                                    if (btn) btn.innerHTML = "<span>🇷🇺</span>";
                                }
                            }).catch(() => {});
                        }
                    } else {
                        elGameDescription.innerHTML = "";
                        elGameDescription.style.display = "none";
                        descSection.style.display = "none";
                        descSection.classList.remove("active");
                    }
                }
                
                // Render Repack Features list
                const featuresSection = document.getElementById("details-features-section");
                const featuresList = document.getElementById("repack-features-list");
                if (featuresSection && featuresList) {
                    if (data.repack_features && data.repack_features.length > 0) {
                        featuresList.innerHTML = "";
                        originalFeatures = data.repack_features.slice();
                        data.repack_features.forEach(feat => {
                            const li = document.createElement("li");
                            li.innerText = feat;
                            featuresList.appendChild(li);
                        });
                        featuresSection.style.display = "block";
                        // Keep features collapsed by default, but ensure list is visible when opened
                        featuresList.style.display = "block";
                    } else {
                        featuresList.innerHTML = "";
                        featuresSection.style.display = "none";
                    }
                }

                // Description always open; Repack Features collapsed by default
                const descHeader = document.getElementById("details-desc-header");
                if (descHeader) {
                    descHeader.onclick = () => {
                        descHeader.parentElement.classList.toggle("active");
                    };
                    if (data.description) {
                        descHeader.parentElement.classList.add("active");
                    }
                    const titleEl = descHeader.querySelector(".section-title");
                    if (titleEl) titleEl.innerText = "Game Description";
                }
                
                const featuresHeader = document.getElementById("details-features-header");
                if (featuresHeader) {
                    featuresHeader.onclick = () => {
                        featuresHeader.parentElement.classList.toggle("active");
                    };
                    featuresHeader.parentElement.classList.remove("active");
                    const titleEl = featuresHeader.querySelector(".section-title");
                    if (titleEl) titleEl.innerText = "Repack Features";
                }

                // Bind Sticky Top Header Buttons
                const btnBackTop = document.getElementById("btn-back-to-catalog-top");
                if (btnBackTop) {
                    btnBackTop.onclick = () => {
                        navigateBackToCatalog();
                    };
                }
                // Open-on-site control removed from details header (always keep hidden)
                const btnOpenBrowserTop = document.getElementById("btn-open-browser-top");
                if (btnOpenBrowserTop) {
                    btnOpenBrowserTop.style.display = "none";
                    btnOpenBrowserTop.setAttribute("hidden", "");
                    btnOpenBrowserTop.setAttribute("aria-hidden", "true");
                }

                // Render Screenshots & Videos Gallery (always after hard clear of previous game)
                clearDetailsMediaHard();
                if (gen !== detailsOpenGeneration) return;
                renderScreenshots(data.screenshots, data.videos);
                if (elGameScreenshotsSection) elGameScreenshotsSection.classList.remove("is-loading-media");
                const showcaseEl = document.getElementById("screenshot-main-showcase-container");
                if (showcaseEl) showcaseEl.classList.remove("is-loading");
                updateMiniBadge(appState);
                
                // Populate FitGirl website metadata fields
                let metaVisibleCount = 0;
                const showMetaRow = (row, el, value) => {
                    if (!row || !el) return;
                    if (value) {
                        el.innerText = value;
                        row.style.display = "grid";
                        metaVisibleCount++;
                    } else {
                        row.style.display = "none";
                    }
                };
                showMetaRow(document.getElementById("row-fg-genres"), document.getElementById("details-fg-genres"), data.genres_tags);
                showMetaRow(document.getElementById("row-fg-company"), document.getElementById("details-fg-company"), data.company);
                showMetaRow(document.getElementById("row-fg-languages"), document.getElementById("details-fg-languages"), data.languages);
                showMetaRow(
                    document.getElementById("row-fg-orig-size"),
                    document.getElementById("details-fg-orig-size"),
                    (data.original_size && data.original_size !== "Unknown") ? data.original_size : ""
                );
                showMetaRow(
                    document.getElementById("row-fg-repack-size"),
                    document.getElementById("details-fg-repack-size"),
                    (data.repack_size && data.repack_size !== "Unknown")
                        ? formatRepackSizeDisplay(data.repack_size)
                        : ""
                );
                const metaCard = document.querySelector(".details-meta-card");
                if (metaCard) metaCard.style.display = metaVisibleCount > 0 ? "block" : "none";
                
                // Update sticky bottom download bar — ALWAYS page repack size on details (not old session file sum)
                const detailsBottomBar = document.getElementById("details-bottom-bar");
                const detailsBottomSize = document.getElementById("details-bottom-size");
                if (detailsBottomSize) {
                    const rs = (data.repack_size && data.repack_size !== "Unknown")
                        ? data.repack_size
                        : (scrapedMetadata.repack_size !== "Unknown" ? scrapedMetadata.repack_size : "");
                    detailsBottomSize.innerText = formatRepackSizeDisplay(rs) || "—";
                }
                if (detailsBottomBar) setDetailsDownloadBarVisible(true);
                
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
                        if (detailsCoverCard) {
                            detailsCoverCard.style.display = "block";
                            detailsCoverCard.classList.remove("is-loading");
                            detailsCoverCard.classList.add("is-loaded");
                        }

                        elSetupCover.onerror = () => {
                            elSetupCover.src = "";
                            elSetupCover.style.display = "none";
                            elSetupCoverPlaceholder.style.display = "flex";
                            
                            if (detailsCoverImage) {
                                detailsCoverImage.src = "";
                                detailsCoverImage.style.display = "none";
                            }
                            if (detailsCoverPlaceholder) detailsCoverPlaceholder.style.display = "flex";
                            if (detailsCoverCard) detailsCoverCard.classList.remove("is-loaded", "is-loading");
                            clearDynamicBackground();
                        };
                        setHazeBackground(cachedUrl);
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
                    if (detailsCoverCard) {
                        detailsCoverCard.style.display = "none";
                        detailsCoverCard.classList.remove("is-loaded", "is-loading");
                    }
                    clearDynamicBackground();
                }

                // Show game title
                elGameNameInput.value = data.title;
                
                // Prefill default directory
                const defaultDir = appState.default_download_dir || "C:\\Games";
                elSaveDirInput.value = defaultDir;
                
                // Store mirrors list for provider switching
                scrapedMirrors = data.mirrors || [];
                
                const hideGDrive = localStorage.getItem("hideGDrive") !== "false";
                let filteredMirrors = (data.mirrors || []).filter(m => {
                    if (hideGDrive) {
                        const name = m.name.toLowerCase();
                        return !(name.includes("google") || name.includes("gdrive") || name.includes("drive") || name.includes("disk") || name.includes("диск") || name.includes("гугл"));
                    }
                    return true;
                });
                
                if (activeProvider === "onlinefix") {
                    filteredMirrors.sort((a, b) => (b.num_files || 0) - (a.num_files || 0));
                }

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
                    
                    // Populate modal mirrors — decrypt paste only when user opens Download
                    populateModalMirrors(filteredMirrors);
                    scrapedMirrors = filteredMirrors;
                } else {
                    elAnalyzeError.style.display = "block";
                    elAnalyzeError.innerText = "No download mirror links found on this page. Try copying direct links instead.";
                }

                // Description + screenshots already rendered above once (avoid double translate / flash)
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
    } else if (data.type === "online_fix_page" || (data.mirrors && data.title)) {
        if (data.title) elDetailsGameTitle.innerText = data.title;
        scrapedMetadata.original_size = data.original_size || "Unknown";
        scrapedMetadata.repack_size = data.repack_size || "Unknown";
        scrapedMetadata.cover_image = data.cover_image || "";
        if (data.description && elGameDescription) {
            const cleanDesc = stripBonusContentFromDescription(String(data.description));
            elGameDescription.innerHTML = cleanDesc.replace(/\n/g, "<br>");
            const descSection = document.getElementById("details-desc-section");
            if (descSection) descSection.style.display = "block";
        }
        renderScreenshots(data.screenshots || [], data.videos || []);
        if (data.mirrors && data.mirrors.length) {
            scrapedMirrors = data.mirrors;
            populateModalMirrors(data.mirrors);
        }
        const detailsBottomSize = document.getElementById("details-bottom-size");
        if (detailsBottomSize) {
            detailsBottomSize.innerText = (data.repack_size && data.repack_size !== "Unknown")
                ? formatRepackSizeDisplay(data.repack_size)
                : "—";
        }
        setDetailsDownloadBarVisible(true);
        setViewState("details");
    }
}

// URL Analysis trigger
elAnalyzeBtn.addEventListener("click", async () => {
    const url = elUrlTextarea.value.trim();
    if (!url) return;

    elAnalyzeSpinner.style.display = "inline-block";
    elAnalyzeBtnText.innerText = "Analyzing Link...";
    elAnalyzeBtn.setAttribute("disabled", "true");
    elAnalyzeError.style.display = "none";
    resetSetupDashboard();

    const key = cacheKeyForUrl(url);
    const finishUi = () => {
        hideDetailsPageLoader();
        elSetupDashboard.style.display = "grid";
        elAnalyzeSpinner.style.display = "none";
        elAnalyzeBtnText.innerText = "Analyze Link";
        elAnalyzeBtn.removeAttribute("disabled");
    };

    const genAtStart = detailsOpenGeneration;

    // Instant cache hit (already-opened games)
    if (detailsPageCache.has(key)) {
        try {
            applyAnalyzeResult(url, detailsPageCache.get(key), genAtStart);
        } catch (e) {
            console.warn("Cache apply failed, refetching", e);
            detailsPageCache.delete(key);
        } finally {
            if (genAtStart === detailsOpenGeneration) finishUi();
            else {
                elAnalyzeSpinner.style.display = "none";
                elAnalyzeBtnText.innerText = "Analyze Link";
                elAnalyzeBtn.removeAttribute("disabled");
            }
        }
        if (detailsPageCache.has(key) && genAtStart === detailsOpenGeneration) return;
        if (genAtStart !== detailsOpenGeneration) return;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 50000);

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url }),
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        // User already opened another game — discard this response
        if (genAtStart !== detailsOpenGeneration) {
            elAnalyzeSpinner.style.display = "none";
            elAnalyzeBtnText.innerText = "Analyze Link";
            elAnalyzeBtn.removeAttribute("disabled");
            return;
        }

        const data = await response.json();
        if (response.ok && data.success) {
            detailsPageCache.set(key, data);
            if (detailsPageCache.size > DETAILS_CACHE_MAX) {
                const first = detailsPageCache.keys().next().value;
                detailsPageCache.delete(first);
            }
            persistDetailsCache();
            applyAnalyzeResult(url, data, genAtStart);
        } else {
            elAnalyzeError.style.display = "block";
            elAnalyzeError.innerText = data.error || "Failed to analyze link. Check logs.";
            if (viewState === "details") {
                const msg = data.error || "Check logs.";
                if (typeof Swal !== "undefined") {
                    Swal.fire({
                        icon: "error",
                        title: /timed out|timeout|curl:\s*\(28\)/i.test(msg) ? "Site too slow / timed out" : "Failed to load game",
                        html: `<p style="text-align:left;font-size:0.88rem;word-break:break-word">${msg}</p>`,
                        showCancelButton: true,
                        confirmButtonText: "Retry",
                        cancelButtonText: "Back to catalog",
                        background: "rgba(14,14,22,0.97)",
                        color: "#eee",
                        confirmButtonColor: "#8b5cf6"
                    }).then(res => {
                        if (res.isConfirmed) elAnalyzeBtn.click();
                        else setViewState("catalog");
                    });
                } else {
                    alert("Failed to load game details: " + msg);
                    setViewState("catalog");
                }
            }
        }
    } catch (e) {
        clearTimeout(timeoutId);
        if (genAtStart !== detailsOpenGeneration) {
            elAnalyzeSpinner.style.display = "none";
            elAnalyzeBtnText.innerText = "Analyze Link";
            elAnalyzeBtn.removeAttribute("disabled");
            return;
        }
        console.error("Error analyzing:", e);
        const isAbort = e && e.name === "AbortError";
        elAnalyzeError.style.display = "block";
        elAnalyzeError.innerText = isAbort
            ? "Timeout loading page (50s). Try again or enable VPN."
            : "Connection error. Make sure Python server is running.";
        if (viewState === "details") {
            if (typeof Swal !== "undefined") {
                Swal.fire({
                    icon: "error",
                    title: isAbort ? "Timeout" : "Connection error",
                    text: isAbort ? "The repack page took too long." : "Could not reach server or site.",
                    showCancelButton: true,
                    confirmButtonText: "Retry",
                    cancelButtonText: "Back to catalog",
                    background: "rgba(14,14,22,0.97)",
                    color: "#eee",
                    confirmButtonColor: "#8b5cf6"
                }).then(res => {
                    if (res.isConfirmed) elAnalyzeBtn.click();
                    else setViewState("catalog");
                });
            } else {
                setViewState("catalog");
            }
        }
    } finally {
        if (genAtStart === detailsOpenGeneration) finishUi();
        else {
            elAnalyzeSpinner.style.display = "none";
            elAnalyzeBtnText.innerText = "Analyze Link";
            elAnalyzeBtn.removeAttribute("disabled");
        }
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
    if (elConfirmQueueBtn) {
        elConfirmQueueBtn.setAttribute("disabled", "true");
        elConfirmQueueBtn.innerText = "Resolving Mirror Paste...";
    }
    
    // Show checklist loading overlay
    if (elChecklistLoadingSpinner) elChecklistLoadingSpinner.style.display = "flex";
    if (elActiveMirrorBadge) elActiveMirrorBadge.style.display = "none";
    
    const MIRROR_TIMEOUT_MS = 75000; // PrivateBin + CF can be slow
    const maxAttempts = 2;
    let lastErr = null;
    let loaded = false;

    for (let attempt = 1; attempt <= maxAttempts && !loaded; attempt++) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), MIRROR_TIMEOUT_MS);
        try {
            if (elChecklistLoadingSpinner) {
                const p = elChecklistLoadingSpinner.querySelector("p");
                if (p) p.innerText = attempt > 1 ? `Decrypting mirror… retry ${attempt}/${maxAttempts}` : "Decrypting mirror paste…";
            }
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: mirrorUrl }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            const data = await response.json();
            if (response.ok && data.success) {
                rawFilesList = data.files || [];
                initCheckedFiles(rawFilesList);
                configureRussianSorting(rawFilesList);
                if (elActiveMirrorName) elActiveMirrorName.innerText = mirrorName;
                if (elActiveMirrorBadge) elActiveMirrorBadge.style.display = "inline-block";
                if (elConfirmQueueBtn) {
                    elConfirmQueueBtn.removeAttribute("disabled");
                    elConfirmQueueBtn.innerText = "Confirm and Start Download";
                }
                // Wider step-2 shell when files are ready
                const card = document.getElementById("download-config-card");
                if (card) card.classList.add("step-files-wide");
                updateChecklistSorted();
                loaded = true;
            } else {
                lastErr = data.error || "Unknown error";
            }
        } catch (e) {
            clearTimeout(timeoutId);
            console.error("Error loading mirror:", e);
            lastErr = e.name === "AbortError"
                ? "Timeout loading mirror links. The paste host is slow or blocked."
                : (e.message || "Failed to load mirror. Check internet / VPN.");
        }
    }

    if (!loaded) {
        const errMsg = String(lastErr || "Unknown error");
        const isDns = /could not resolve|resolve host|getaddrinfo|curl:\s*\(6\)/i.test(errMsg);
        const isTimeout = /timeout|timed out|abort/i.test(errMsg);
        if (typeof Swal !== "undefined") {
            Swal.fire({
                icon: isTimeout ? "warning" : "error",
                title: isDns ? "Mirror host unreachable" : (isTimeout ? "Mirror timed out" : "Mirror failed"),
                html: isDns
                    ? `<p style="text-align:left;margin:0 0 8px">Cannot reach paste host (DNS / ISP block).</p>
                       <p style="text-align:left;margin:0;color:var(--text-muted);font-size:0.85rem">Try another hoster, enable WARP/VPN, then retry.</p>`
                    : `<p style="text-align:left;word-break:break-word;font-size:0.88rem">${errMsg}</p>
                       <p style="text-align:left;margin-top:8px;color:var(--text-muted);font-size:0.82rem">Go Back and pick another mirror (e.g. Filehoster / fuckingfast).</p>`,
                showCancelButton: true,
                confirmButtonText: "Retry",
                cancelButtonText: "OK",
                background: "rgba(16,16,28,0.96)",
                color: "#eee",
                confirmButtonColor: "#9b59b6"
            }).then(res => {
                if (res.isConfirmed) loadMirrorLinks(mirrorUrl, mirrorName);
            });
        } else {
            alert("Error loading mirror links: " + errMsg);
        }
    }

    if (elChecklistLoadingSpinner) elChecklistLoadingSpinner.style.display = "none";
}

// Display config card for direct files/PrivateBin
function displayConfigCard(title, files, url = "") {
    activeMirrorName = "";
    if (elGameNameInput) elGameNameInput.value = title;
    
    const defaultDir = appState.default_download_dir || "C:\\Games";
    if (elSaveDirInput) elSaveDirInput.value = defaultDir;
    
    // Hide mirror selection since it's a direct paste
    if (elMirrorSelectSection) elMirrorSelectSection.style.display = "none";
    if (elActiveMirrorBadge) elActiveMirrorBadge.style.display = "none";
    
    // Set placeholder metadata
    scrapedMetadata.original_size = "N/A";
    scrapedMetadata.repack_size = "N/A";
    scrapedMetadata.cover_image = "";
    
    elDetailsGameTitle.innerText = title;
    elDetailsVersionBadge.style.display = "none";
    
    if (elBtnOpenBrowser && url) {
        elBtnOpenBrowser.href = getOpenBrowserUrl(url);
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
    
    const detailsBottomSize = document.getElementById("details-bottom-size");
    if (detailsBottomSize) detailsBottomSize.innerText = "Direct Link";
    setDetailsDownloadBarVisible(true);
    
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
    
    // Only override bottom size while the download config modal is open for THIS game's files.
    // Never let a previous session's rawFilesList overwrite the page repack size (caused 384GB bugs).
    const detailsBottomSize = document.getElementById("details-bottom-size");
    const downloadModal = document.getElementById("download-config-modal");
    const modalOpen = downloadModal && (
        downloadModal.classList.contains("active")
        || (downloadModal.style.display && downloadModal.style.display !== "none")
    );
    if (detailsBottomSize && modalOpen && rawFilesList && rawFilesList.length > 0) {
        let totalSelectedSize = 0;
        rawFilesList.forEach(f => {
            if (checkedFiles.has(f.filename) && f.size) {
                totalSelectedSize += f.size;
            }
        });
        if (totalSelectedSize > 0) {
            detailsBottomSize.innerText = formatBytes(totalSelectedSize);
        } else if (scrapedMetadata.repack_size && scrapedMetadata.repack_size !== "Unknown") {
            detailsBottomSize.innerText = formatRepackSizeDisplay(scrapedMetadata.repack_size);
        }
    }
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
const handleResetSession = async () => {
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
};

if (elResetSessionBtn) elResetSessionBtn.addEventListener("click", handleResetSession);
if (elResetSessionBtnDashboard) elResetSessionBtnDashboard.addEventListener("click", handleResetSession);

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

function setFloatingIslandVisible(el, visible) {
    if (!el) return;
    el.classList.toggle("is-visible", !!visible);
    el.setAttribute("aria-hidden", visible ? "false" : "true");
    // Inline styles must not fight CSS !important; class .is-visible owns display.
    el.style.removeProperty("display");
    // Kick liquid-glass backdrop capture when island appears
    if (visible && typeof window.refreshLiquidGlass === "function") {
        requestAnimationFrame(() => window.refreshLiquidGlass());
    }
}

/** True only when there is a real configured download queue (not ghost placeholders). */
function hasRealDownloadSession(state, sessionInfo) {
    if (!state || !state.is_configured) return false;
    const files = state.files || [];
    if (!files.length) return false;
    const info = sessionInfo || getDownloadSessionInfo(state);
    // Require a title or actual queue work — never show bare "Game Title" island
    if (info.phase === "none") return false;
    if (!info.title && !info.anyProgress && info.phase === "ready" && files.length === 0) return false;
    return true;
}

function updateMiniBadge(newState) {
    const elMiniBadge = document.getElementById("floating-download-badge");
    if (!elMiniBadge) return;

    const sessionInfo = getDownloadSessionInfo(newState);
    const showIsland = hasRealDownloadSession(newState, sessionInfo) && viewState !== "downloading";
    
    if (showIsland) {
        setFloatingIslandVisible(elMiniBadge, true);
        elMiniBadge.classList.add("dl-island", "is-compact-island");
        
        const elMiniTitle = document.getElementById("mini-game-title");
        const elMiniEta = document.getElementById("mini-game-eta");
        const elMiniStatus = document.getElementById("mini-game-status");
        const elMiniProgressBarFill = document.getElementById("mini-progress-bar-fill");
        const elMiniPct = document.getElementById("mini-game-pct");
        
        // Always show real game title when session exists (not only while downloading)
        if (elMiniTitle) {
            elMiniTitle.innerText = sessionInfo.title || "Download session";
        }
        
        const isDownloading = sessionInfo.phase === "downloading";
        const speedText = isDownloading
            ? formatSpeed(smoothedSpeed > 0 ? smoothedSpeed : newState.total_speed)
            : "0 MB/s";
        
        const totalBytes = newState.files ? newState.files.reduce((acc, f) => acc + (f.size || 0), 0) : 0;
        const downloadedBytes = newState.files ? newState.files.reduce((acc, f) => {
            if (f.status === "finished" && f.size > 0) return acc + f.size;
            return acc + (f.downloaded || 0);
        }, 0) : 0;
        const totalSizeText = totalBytes > 0 ? formatBytes(totalBytes) : "—";
        const downloadedSizeText = formatBytes(downloadedBytes);
        const pct = (typeof newState.total_progress === "number")
            ? Math.round(newState.total_progress)
            : (totalBytes > 0 ? Math.min(100, Math.floor((downloadedBytes / totalBytes) * 100)) : 0);
        
        // Status line: size + optional speed
        if (elMiniStatus) {
            if (sessionInfo.phase === "ready") {
                elMiniStatus.innerText = totalBytes > 0
                    ? `Not started · ${totalSizeText}`
                    : "Not started";
            } else if (sessionInfo.phase === "complete") {
                elMiniStatus.innerText = `${downloadedSizeText} / ${totalSizeText} · Done`;
            } else if (isDownloading) {
                elMiniStatus.innerText = `${downloadedSizeText} / ${totalSizeText} · ${speedText}`;
            } else {
                elMiniStatus.innerText = `${downloadedSizeText} / ${totalSizeText}`;
            }
        }
        
        // State chip: Ready / Paused / ETA / Done
        if (elMiniEta) {
            let stateLabel = "…";
            let stateClass = "is-idle";
            if (sessionInfo.phase === "complete") {
                stateLabel = "Done";
                stateClass = "is-done";
            } else if (sessionInfo.phase === "ready") {
                stateLabel = "Ready";
                stateClass = "is-idle";
            } else if (sessionInfo.phase === "downloading" && smoothedSpeed > 0) {
                const remainingBytes = Math.max(0, totalBytes - downloadedBytes);
                const etaSeconds = Math.max(0, remainingBytes / smoothedSpeed);
                stateLabel = formatTime(etaSeconds);
                stateClass = "is-running";
            } else if (sessionInfo.phase === "downloading" || sessionInfo.phase === "starting") {
                stateLabel = "Sync";
                stateClass = "is-running";
            } else if (sessionInfo.phase === "paused") {
                stateLabel = "Paused";
                stateClass = "is-paused";
            } else {
                stateLabel = "Idle";
                stateClass = "is-idle";
            }
            elMiniEta.innerText = stateLabel;
            elMiniEta.className = "floating-bar-eta " + stateClass;
        }
        
        if (elMiniPct) {
            elMiniPct.innerText = `${pct}%`;
        }
        
        if (elMiniProgressBarFill) {
            elMiniProgressBarFill.style.width = `${pct}%`;
        }

        // Second line on island: current file · its %
        updateCurrentFileProgressLine(newState);

        const playPauseBtn = document.getElementById("mini-btn-play-pause");
        if (playPauseBtn) {
            const running = sessionInfo.phase === "downloading" || sessionInfo.phase === "starting";
            let aria = "Start";
            if (running) aria = "Pause";
            else if (sessionInfo.phase === "paused") aria = "Resume";
            else if (sessionInfo.phase === "complete") aria = "Completed";
            else if (sessionInfo.phase === "ready") aria = "Start Download";
            playPauseBtn.setAttribute("aria-label", aria);
            playPauseBtn.title = aria;
            // Play / pause / done inside frosted disc
            const iconSvg = (path) =>
                `<span class="as-nav-center-ring" aria-hidden="true"></span>` +
                `<svg class="as-nav-center-icon" viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="${path}"/></svg>`;
            const PLAY = "M8 5v14l11-7z";
            const PAUSE = "M6 19h4V5H6v14zm8-14v14h4V5h-4z";
            const CHECK = "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z";
            if (sessionInfo.phase === "complete") {
                playPauseBtn.innerHTML = iconSvg(CHECK);
            } else if (running) {
                playPauseBtn.innerHTML = iconSvg(PAUSE);
            } else {
                playPauseBtn.innerHTML = iconSvg(PLAY);
            }
            playPauseBtn.classList.toggle("is-running", running);
            playPauseBtn.classList.toggle("is-paused", sessionInfo.phase === "paused");
            playPauseBtn.classList.toggle("is-done", sessionInfo.phase === "complete");
        }

        const elDetailsGameTitle = document.getElementById("details-game-title");
        const isViewingActiveGame = viewState === "details" &&
            elDetailsGameTitle &&
            sessionInfo.title &&
            elDetailsGameTitle.innerText === sessionInfo.title;
        
        if (isViewingActiveGame) {
            setDetailsDownloadBarVisible(false);
        } else if (viewState === "details") {
            setDetailsDownloadBarVisible(true);
        }
    } else {
        setFloatingIslandVisible(elMiniBadge, false);
        if (viewState === "details") {
            setDetailsDownloadBarVisible(true);
        }
    }
}

// ViewState Router
let viewState = "catalog"; // "catalog", "details", "downloading"

/**
 * Browser / mouse Back: stay in the SPA.
 * Opening details pushes history; Back returns to catalog instead of closing the tab.
 */
function setViewState(state, opts = {}) {
    const fromHistory = !!(opts && opts.fromHistory);
    const prev = viewState;
    viewState = state;
    syncViewState();
    updateMiniBadge(appState);

    if (fromHistory) return;
    try {
        if (state === "details" && prev !== "details") {
            history.pushState({ appView: "details" }, "", "#details");
        } else if (state === "catalog" && prev === "details") {
            // UI already navigated; keep hash in sync without extra stack entries
            if (history.state && history.state.appView === "details") {
                history.replaceState({ appView: "catalog" }, "", "#catalog");
            } else if (location.hash === "#details") {
                history.replaceState({ appView: "catalog" }, "", "#catalog");
            }
        }
    } catch (_) { /* ignore history errors */ }
}

/** Prefer history.back() so mouse/browser Back and UI Back share one path. */
function navigateBackToCatalog() {
    try {
        const elVideoIframe = document.getElementById("video-iframe");
        if (elVideoIframe) elVideoIframe.src = "";
        const elMainVideo = document.getElementById("screenshot-main-video");
        if (elMainVideo) elMainVideo.src = "";
        const elMainDirect = document.getElementById("screenshot-main-direct-video");
        if (elMainDirect) {
            try { elMainDirect.pause(); } catch (_) {}
            elMainDirect.removeAttribute("src");
            elMainDirect.load?.();
        }
    } catch (_) {}

    if (viewState === "details" && history.state && history.state.appView === "details") {
        history.back();
        return;
    }
    setViewState("catalog", { fromHistory: true });
    try {
        history.replaceState({ appView: "catalog" }, "", "#catalog");
    } catch (_) {}
}

window.addEventListener("popstate", (e) => {
    const appView = (e.state && e.state.appView) || "catalog";

    // Already on main catalog: Back must NOT leave the site / close the tab
    if (viewState === "catalog") {
        try {
            history.pushState({ appView: "catalog", root: true }, "", "#catalog");
        } catch (_) {}
        return;
    }

    if (appView === "details") {
        // Forward into details without content — bounce home
        if (viewState !== "details") {
            try { history.replaceState({ appView: "catalog" }, "", "#catalog"); } catch (_) {}
            setViewState("catalog", { fromHistory: true });
        }
        return;
    }

    // Back from details / download overlay → catalog (stay in app)
    if (viewState === "details" || viewState === "downloading") {
        try {
            const elVideoIframe = document.getElementById("video-iframe");
            if (elVideoIframe) elVideoIframe.src = "";
        } catch (_) {}
        setViewState("catalog", { fromHistory: true });
        // Keep a trap entry so another Back still stays on catalog
        try {
            history.pushState({ appView: "catalog", root: true }, "", "#catalog");
        } catch (_) {}
    }
});

// Seed history: catalog is the root. Extra push traps Back on main page.
try {
    history.replaceState({ appView: "catalog", root: true }, "", "#catalog");
    history.pushState({ appView: "catalog", root: true }, "", "#catalog");
} catch (_) {}

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
    const elDownloadBackdrop = document.getElementById("download-view-backdrop");

    // Hide sidebar completely in the new visual redesign
    const elSidebar = document.querySelector(".sidebar");
    if (elSidebar) elSidebar.style.display = "none";
    const elAppContainer = document.querySelector(".app-container");
    if (elAppContainer) elAppContainer.classList.remove("has-sidebar");

    if (viewState === "downloading") {
        // Keep catalog or details visible in the background
        elSetupView.classList.remove("hidden-view");
        
        // Show download dashboard as a floating modal overlay
        elDownloadView.classList.remove("hidden-view");
        elDownloadView.classList.add("active-overlay");
        if (elDownloadBackdrop) elDownloadBackdrop.style.display = "block";
        
        // Hide mini island while full download overlay is open
        setFloatingIslandVisible(elMiniBadge, false);
    } else {
        // Hide download overlay
        elDownloadView.classList.remove("active-overlay");
        elDownloadView.classList.add("hidden-view");
        if (elDownloadBackdrop) elDownloadBackdrop.style.display = "none";
        
        // updateMiniBadge decides visibility (real session only)
        updateMiniBadge(appState);
    }

    // Handle catalog background views based on background state
    let bgState = viewState;
    if (bgState === "downloading") {
        // Keep the previous view state in background if overlay is open
        bgState = "catalog";
    }

    if (bgState === "catalog") {
        elCatalogContainer.classList.remove("hidden-view");
        elGameDetailsContainer.classList.add("hidden-view");
        clearDynamicBackground();
        setDetailsDownloadBarVisible(false);
    } else if (bgState === "details") {
        elCatalogContainer.classList.add("hidden-view");
        elGameDetailsContainer.classList.remove("hidden-view");
    }
}

/**
 * Relative luminance (sRGB) — Flutter Color.computeLuminance().
 */
function colorLuminance(c) {
    const lin = (v) => {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
}

/* ============================================================
   Harmonoid AnimatedMeshGradient — WebGL port of mesh_gradient
   shader: lib/shaders/animated_mesh_gradient.frag
   options: frequency=5, amplitude=30, speed=2, grain=0
   ticker: time += 0.01 each frame (same as Flutter Ticker)
   ============================================================ */
const MESH_VERT = `
attribute vec2 a_pos;
void main() {
  gl_Position = vec4(a_pos, 0.0, 1.0);
}`;

// Exact algorithm from mesh_gradient animated_mesh_gradient.frag (Flutter → WebGL)
const MESH_FRAG = `
precision highp float;
uniform vec2 uSize;
uniform float uTime;
uniform float uFrequency;
uniform float uAmplitude;
uniform float uSpeed;
uniform float uGrain;
uniform vec3 uColor1;
uniform vec3 uColor2;
uniform vec3 uColor3;
uniform vec3 uColor4;

float S(float a, float b, float t) {
  return smoothstep(a, b, t);
}

mat2 Rot(float a) {
  float s = sin(a);
  float c = cos(a);
  return mat2(c, -s, s, c);
}

vec2 hash(vec2 p) {
  p = vec2(dot(p, vec2(2127.1, 81.17)), dot(p, vec2(1269.5, 283.37)));
  return fract(sin(p) * 43758.5453);
}

float noise(in vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  float n = mix(
    mix(dot(-1.0 + 2.0 * hash(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
        dot(-1.0 + 2.0 * hash(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
    mix(dot(-1.0 + 2.0 * hash(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
        dot(-1.0 + 2.0 * hash(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x),
    u.y);
  return 0.5 + 0.5 * n;
}

float grainNoise(vec2 p) {
  return fract(sin(dot(p * -1.0, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
  vec2 uv = gl_FragCoord.xy / uSize;
  float ratio = uSize.x / uSize.y;
  vec2 tuv = uv;
  tuv -= 0.5;

  float degree = noise(vec2(uTime * 0.1, tuv.x * tuv.y));
  tuv.y *= 1.0 / ratio;
  float deg = radians((degree - 0.5) * 720.0 + 180.0);
  tuv *= Rot(deg);
  tuv.y *= ratio;

  float frequency = uFrequency;
  float amplitude = uAmplitude;
  float speed = uTime * uSpeed;

  tuv.x += sin(tuv.y * frequency + speed) / amplitude;
  tuv.y += sin(tuv.x * frequency * 1.5 + speed) / (amplitude * 0.5);

  vec3 layer1 = mix(uColor1, uColor2, S(-0.3, 0.2, (tuv * Rot(radians(-5.0))).x));
  vec3 layer2 = mix(uColor3, uColor4, S(-0.3, 0.2, (tuv * Rot(radians(-5.0))).x));
  vec3 finalComp = mix(layer1, layer2, S(0.5, -0.3, tuv.y));
  vec3 grainedComp = finalComp + (finalComp * grainNoise(uv) * uGrain);
  gl_FragColor = vec4(grainedComp, 1.0);
}`;

/**
 * Adaptive haze quality — same shader / colors on every PC.
 * Powerful desktops keep full DPR + uncapped FPS.
 * Weak / thermal-limited GPUs automatically lower render resolution and
 * frame cadence only (visual style unchanged). Never permanently "downgrades"
 * a fast machine.
 */
const hazePerf = {
    // Full quality defaults (desktop / dGPU)
    maxDpr: 2,
    targetFps: 60,
    // Runtime adaptive
    dprCap: Math.min(window.devicePixelRatio || 1, 2),
    frameIntervalMs: 1000 / 60,
    samples: [],
    lastAdjust: 0,
    mode: "high" // high | balanced | low
};

function hazeRecordFrame(frameMs) {
    if (!Number.isFinite(frameMs) || frameMs <= 0 || frameMs > 200) return;
    hazePerf.samples.push(frameMs);
    if (hazePerf.samples.length > 45) hazePerf.samples.shift();
    const now = performance.now();
    if (now - hazePerf.lastAdjust < 1800 || hazePerf.samples.length < 20) return;
    hazePerf.lastAdjust = now;
    const avg = hazePerf.samples.reduce((a, b) => a + b, 0) / hazePerf.samples.length;
    const deviceMax = Math.min(window.devicePixelRatio || 1, 2);

    // ~60fps budget: keep full quality
    if (avg < 14) {
        hazePerf.mode = "high";
        hazePerf.dprCap = deviceMax;
        hazePerf.frameIntervalMs = 1000 / 60;
    } else if (avg < 22) {
        // Still looks fluid; slightly lower internal resolution only
        hazePerf.mode = "balanced";
        hazePerf.dprCap = Math.min(deviceMax, 1.25);
        hazePerf.frameIntervalMs = 1000 / 45;
    } else {
        // Laptop / iGPU pressure — same colors/shader, cheaper raster
        hazePerf.mode = "low";
        hazePerf.dprCap = 1;
        hazePerf.frameIntervalMs = 1000 / 30;
    }
}

function createMeshRenderer(canvas) {
    if (!canvas || !canvas.getContext) return null;
    const gl = canvas.getContext("webgl", {
        alpha: false,
        antialias: false,
        premultipliedAlpha: false,
        preserveDrawingBuffer: false,
        powerPreference: "high-performance",
        desynchronized: true
    });
    if (!gl) {
        console.warn("[haze] WebGL unavailable");
        return null;
    }

    function compile(type, src) {
        const sh = gl.createShader(type);
        gl.shaderSource(sh, src);
        gl.compileShader(sh);
        if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
            console.error("[haze] shader compile", gl.getShaderInfoLog(sh));
            return null;
        }
        return sh;
    }

    const vs = compile(gl.VERTEX_SHADER, MESH_VERT);
    const fs = compile(gl.FRAGMENT_SHADER, MESH_FRAG);
    if (!vs || !fs) return null;

    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
        console.error("[haze] program link", gl.getProgramInfoLog(prog));
        return null;
    }

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
        -1, -1,  1, -1,  -1, 1,
        -1,  1,  1, -1,   1, 1
    ]), gl.STATIC_DRAW);

    const aPos = gl.getAttribLocation(prog, "a_pos");
    const u = {
        size: gl.getUniformLocation(prog, "uSize"),
        time: gl.getUniformLocation(prog, "uTime"),
        frequency: gl.getUniformLocation(prog, "uFrequency"),
        amplitude: gl.getUniformLocation(prog, "uAmplitude"),
        speed: gl.getUniformLocation(prog, "uSpeed"),
        grain: gl.getUniformLocation(prog, "uGrain"),
        c1: gl.getUniformLocation(prog, "uColor1"),
        c2: gl.getUniformLocation(prog, "uColor2"),
        c3: gl.getUniformLocation(prog, "uColor3"),
        c4: gl.getUniformLocation(prog, "uColor4")
    };

    // Default AnimatedMeshGradientOptions() — visual identity unchanged
    const options = { frequency: 5, amplitude: 30, speed: 2, grain: 0 };
    let colors = [
        [0.2, 0.08, 0.24],
        [0.43, 0.17, 0.47],
        [0.14, 0.09, 0.24],
        [0.31, 0.13, 0.38]
    ];
    let time = 0;
    let running = false;
    let raf = 0;
    let lastFrameWall = 0;
    let lastDrawAt = 0;

    function resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, hazePerf.dprCap || 1);
        const w = Math.max(2, Math.floor(window.innerWidth * dpr));
        const h = Math.max(2, Math.floor(window.innerHeight * dpr));
        if (canvas.width !== w || canvas.height !== h) {
            canvas.width = w;
            canvas.height = h;
        }
        gl.viewport(0, 0, canvas.width, canvas.height);
    }

    function draw() {
        resize();
        gl.useProgram(prog);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

        gl.uniform2f(u.size, canvas.width, canvas.height);
        gl.uniform1f(u.time, time);
        gl.uniform1f(u.frequency, options.frequency);
        gl.uniform1f(u.amplitude, options.amplitude);
        gl.uniform1f(u.speed, options.speed);
        gl.uniform1f(u.grain, options.grain);
        gl.uniform3fv(u.c1, colors[0]);
        gl.uniform3fv(u.c2, colors[1]);
        gl.uniform3fv(u.c3, colors[2]);
        gl.uniform3fv(u.c4, colors[3]);

        gl.drawArrays(gl.TRIANGLES, 0, 6);
        lastDrawAt = performance.now();
    }

    function loop(now) {
        if (!running) return;
        raf = requestAnimationFrame(loop);

        // Pause entirely when tab/window not visible — free GPU on laptops
        if (typeof document !== "undefined" && document.hidden) return;

        const wall = typeof now === "number" ? now : performance.now();
        if (lastFrameWall && wall - lastFrameWall < (hazePerf.frameIntervalMs || 16.6) - 0.5) {
            return;
        }
        const dt = lastFrameWall ? (wall - lastFrameWall) : 16.6;
        lastFrameWall = wall;

        // Flutter Ticker: _delta += 0.01 each nominal frame — scale by real dt
        // so animation speed stays consistent when FPS is throttled.
        time += 0.01 * (dt / 16.6667);
        const t0 = performance.now();
        draw();
        hazeRecordFrame(performance.now() - t0);
    }

    return {
        setColors(rgbList) {
            // rgb 0-255 → 0-1 like painter color.red/255
            colors = rgbList.map(c => [
                Math.min(1, Math.max(0, c.r / 255)),
                Math.min(1, Math.max(0, c.g / 255)),
                Math.min(1, Math.max(0, c.b / 255))
            ]);
            while (colors.length < 4) colors.push(colors[colors.length - 1] || [0, 0, 0]);
            colors = colors.slice(0, 4);
            // One static redraw if not animating (inactive crossfade layer)
            if (!running) draw();
            else draw();
        },
        start() {
            if (running) return;
            running = true;
            lastFrameWall = 0;
            raf = requestAnimationFrame(loop);
        },
        stop() {
            running = false;
            if (raf) cancelAnimationFrame(raf);
            raf = 0;
        },
        isRunning() { return running; },
        draw,
        resize
    };
}

// Two mesh renderers for AnimatedSwitcher crossfade
let meshRendererA = null;
let meshRendererB = null;
let hazeCrossfadeStopTimer = 0;

function ensureMeshRenderers() {
    // Create both, but only keep the active layer animating (huge laptop win).
    if (!meshRendererA && elHazeMeshA) {
        meshRendererA = createMeshRenderer(elHazeMeshA);
    }
    if (!meshRendererB && elHazeMeshB) {
        meshRendererB = createMeshRenderer(elHazeMeshB);
    }
    // Start whichever is currently active
    const activeIsA = !elHazeMeshB || elHazeMeshA?.classList.contains("is-active") || !elHazeMeshB.classList.contains("is-active");
    if (activeIsA) {
        meshRendererA?.start();
        meshRendererB?.stop();
    } else {
        meshRendererB?.start();
        meshRendererA?.stop();
    }
    return !!(meshRendererA && meshRendererB);
}

/** After palette crossfade, stop the hidden mesh so only one WebGL loop runs. */
function hazeFinishCrossfade(activeIsA) {
    if (hazeCrossfadeStopTimer) {
        clearTimeout(hazeCrossfadeStopTimer);
        hazeCrossfadeStopTimer = 0;
    }
    // Match CSS opacity transition (~0.9s)
    hazeCrossfadeStopTimer = setTimeout(() => {
        hazeCrossfadeStopTimer = 0;
        if (activeIsA) {
            meshRendererA?.start();
            meshRendererB?.stop();
        } else {
            meshRendererB?.start();
            meshRendererA?.stop();
        }
    }, 950);
}

// Visibility / battery: freeze both meshes while hidden; resume active only.
if (typeof document !== "undefined") {
    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            meshRendererA?.stop();
            meshRendererB?.stop();
        } else {
            ensureMeshRenderers();
            const activeR = (elHazeMeshA?.classList.contains("is-active") ? meshRendererA : meshRendererB)
                || meshRendererA;
            activeR?.start();
            activeR?.draw();
        }
    });
}

/**
 * Harmonoid NowPlayingColorPaletteNotifier:
 * palette.where((e) => e.computeLuminance() < 0.5)
 * then order colors for AnimatedMeshGradient exactly as now_playing_background.dart
 */
function extractPaletteFromImage(imgElement, maxColors = 8) {
    const canvas = document.createElement("canvas");
    canvas.width = 32;
    canvas.height = 32;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    ctx.drawImage(imgElement, 0, 0, 32, 32);
    const data = ctx.getImageData(0, 0, 32, 32).data;
    const buckets = new Map();

    for (let i = 0; i < data.length; i += 4) {
        if (data[i + 3] < 180) continue;
        const r0 = data[i], g0 = data[i + 1], b0 = data[i + 2];
        const maxc = Math.max(r0, g0, b0);
        const minc = Math.min(r0, g0, b0);
        if (maxc < 18 || minc > 245) continue;
        const r = r0 >> 3, g = g0 >> 3, b = b0 >> 3;
        const key = (r << 10) | (g << 5) | b;
        buckets.set(key, (buckets.get(key) || 0) + 1);
    }

    const sorted = [...buckets.entries()].sort((a, b) => b[1] - a[1]);
    const raw = [];
    const tooClose = (a, b) => {
        const dr = a.r - b.r, dg = a.g - b.g, db = a.b - b.b;
        return (dr * dr + dg * dg + db * db) < 1400;
    };
    for (const [key] of sorted) {
        if (raw.length >= maxColors) break;
        const col = {
            r: ((key >> 10) & 31) * 8 + 4,
            g: ((key >> 5) & 31) * 8 + 4,
            b: (key & 31) * 8 + 4
        };
        if (raw.some(c => tooClose(c, col))) continue;
        raw.push(col);
    }

    // Harmonoid: luminance < 0.5 only (darker half of palette)
    let dark = raw.filter(c => colorLuminance(c) < 0.5);
    if (!dark.length) dark = raw.slice();
    if (!dark.length) {
        dark = [
            { r: 80, g: 30, b: 100 },
            { r: 160, g: 50, b: 90 },
            { r: 40, g: 50, b: 120 },
            { r: 110, g: 35, b: 85 }
        ];
    }

    // Keep dark character but ensure mesh is vividly visible (not black void).
    // Harmonoid paints full-screen mesh; near-black swatches look like "no animation".
    dark = dark.map(c => {
        let { r, g, b } = c;
        // floor so nothing collapses to black
        r = Math.max(r, 40);
        g = Math.max(g, 28);
        b = Math.max(b, 45);
        // boost saturation + mid lift
        const avg = (r + g + b) / 3;
        r = Math.min(255, Math.round((r - avg) * 1.35 + avg * 1.25 + 28));
        g = Math.min(255, Math.round((g - avg) * 1.35 + avg * 1.2 + 20));
        b = Math.min(255, Math.round((b - avg) * 1.35 + avg * 1.25 + 30));
        return { r, g, b };
    });

    // now_playing_background.dart switch on palette.length
    const p = dark;
    if (p.length === 1) return [p[0], p[0], p[0], p[0]];
    if (p.length === 2) return [p[1], p[0], p[1], p[0]]; // reversed[0], [0], reversed[0], [0]
    if (p.length === 3) return [p[2], p[0], p[2], p[1]];
    // else: reversed[0], [0], reversed[1], [1]
    return [p[p.length - 1], p[0], p[p.length - 2], p[1]];
}

function paletteKey(colors) {
    return colors.map(c => `${c.r},${c.g},${c.b}`).join("|");
}

/**
 * Apply palette with Harmonoid AnimatedSwitcher crossfade + live WebGL mesh.
 * opts.force — apply even if same key; opts.soft — longer/smoother tween (catalog page).
 */
function applyHazePalette(colors, opts = {}) {
    const force = !!(opts && opts.force);
    const soft = !!(opts && opts.soft);
    const key = paletteKey(colors);
    if (!force && key === lastHazePaletteKey && elHazeRoot && elHazeRoot.classList.contains("haze-active")) {
        return;
    }
    lastHazePaletteKey = key;
    ensureMeshRenderers();

    if (!elHazeRoot || !elHazeMeshA || !elHazeMeshB) {
        console.warn("[haze] DOM missing");
        return;
    }
    elHazeRoot.classList.remove("haze-idle");
    elHazeRoot.classList.add("haze-active");

    const nextCanvas = hazeMeshActiveIsA ? elHazeMeshB : elHazeMeshA;
    const prevCanvas = hazeMeshActiveIsA ? elHazeMeshA : elHazeMeshB;
    const nextR = hazeMeshActiveIsA ? meshRendererB : meshRendererA;
    const prevR = hazeMeshActiveIsA ? meshRendererA : meshRendererB;

    if (nextR) {
        nextR.setColors(colors);
        nextR.start();
        nextR._hasColors = true;
    }
    if (prevR && !prevR._hasColors) {
        prevR.setColors(colors);
        prevR._hasColors = true;
    }

    void nextCanvas.offsetWidth;
    nextCanvas.classList.add("is-active");
    prevCanvas.classList.remove("is-active");
    hazeMeshActiveIsA = !hazeMeshActiveIsA;
    if (typeof hazeFinishCrossfade === "function") hazeFinishCrossfade(hazeMeshActiveIsA);

    const p = colors[0];
    const s = colors[1] || colors[0];
    animateCSSColorVariables(
        `rgb(${p.r}, ${p.g}, ${p.b})`,
        `rgb(${s.r}, ${s.g}, ${s.b})`,
        soft ? 1600 : 1100
    );

    document.body.style.transition = soft
        ? "background-color 1.6s ease"
        : "background-color 1.2s ease";
    document.body.style.backgroundColor = `rgb(${Math.floor(p.r * 0.15)},${Math.floor(p.g * 0.12)},${Math.floor(p.b * 0.18)})`;
    elHazeRoot.style.backgroundColor = "#000";
}

function setHazeBackground(coverUrl) {
    if (dynamicResetTimeout) {
        clearTimeout(dynamicResetTimeout);
        dynamicResetTimeout = null;
    }
    if (!coverUrl) {
        clearDynamicBackground();
        return;
    }
    const stableKey = coverUrl.split("?")[0];
    if (activeHazeUrl === stableKey && elHazeRoot && elHazeRoot.classList.contains("haze-active") && lastHazePaletteKey) {
        return;
    }
    activeHazeUrl = stableKey;
    const gen = ++hazeApplyGeneration;
    ensureMeshRenderers();

    const fallback = [
        { r: 90, g: 35, b: 100 },
        { r: 160, g: 55, b: 90 },
        { r: 40, g: 50, b: 110 },
        { r: 120, g: 40, b: 80 }
    ];

    const applyFromImg = (img) => {
        if (gen !== hazeApplyGeneration) return;
        try {
            applyHazePalette(extractPaletteFromImage(img));
        } catch (e) {
            console.warn("[haze] palette extract failed", e);
            applyHazePalette(fallback);
        }
    };

    const img = new Image();
    if (/^https?:/i.test(coverUrl) || coverUrl.startsWith("/")) {
        img.crossOrigin = "anonymous";
    }
    img.onload = () => applyFromImg(img);
    img.onerror = () => {
        if (gen !== hazeApplyGeneration) return;
        applyHazePalette(fallback);
    };
    img.src = coverUrl;
}

function animateCSSColorVariables(targetPrimary, targetSecondary, duration = 400) {
    if (hazeAnimRaf) {
        cancelAnimationFrame(hazeAnimRaf);
        hazeAnimRaf = 0;
    }
    const startPrimary = getComputedStyle(document.documentElement).getPropertyValue("--color-primary").trim() || "#a83279";
    const startSecondary = getComputedStyle(document.documentElement).getPropertyValue("--color-secondary").trim() || "#9b59b6";

    function parseRgb(colorStr) {
        if (colorStr.startsWith("rgb")) {
            const m = colorStr.match(/\d+/g);
            if (m) return { r: parseInt(m[0], 10), g: parseInt(m[1], 10), b: parseInt(m[2], 10) };
        } else if (colorStr.startsWith("#")) {
            let hex = colorStr.slice(1);
            if (hex.length === 3) hex = hex.split("").map(x => x + x).join("");
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
    if (Math.abs(fromP.r - toP.r) < 3 && Math.abs(fromP.g - toP.g) < 3 && Math.abs(fromP.b - toP.b) < 3) return;

    const startTime = performance.now();
    function update(time) {
        const progress = Math.min((time - startTime) / duration, 1);
        const ease = progress < 0.5 ? 2 * progress * progress : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        const rP = Math.round(fromP.r + (toP.r - fromP.r) * ease);
        const gP = Math.round(fromP.g + (toP.g - fromP.g) * ease);
        const bP = Math.round(fromP.b + (toP.b - fromP.b) * ease);
        const rS = Math.round(fromS.r + (toS.r - fromS.r) * ease);
        const gS = Math.round(fromS.g + (toS.g - fromS.g) * ease);
        const bS = Math.round(fromS.b + (toS.b - fromS.b) * ease);
        document.documentElement.style.setProperty("--color-primary", `rgb(${rP}, ${gP}, ${bP})`);
        document.documentElement.style.setProperty("--color-secondary", `rgb(${rS}, ${gS}, ${bS})`);
        document.documentElement.style.setProperty("--color-primary-glow", `rgba(${rP}, ${gP}, ${bP}, 0.35)`);
        document.documentElement.style.setProperty("--color-secondary-glow", `rgba(${rS}, ${gS}, ${bS}, 0.28)`);
        document.documentElement.style.setProperty("--border-glow", `rgba(${rS}, ${gS}, ${bS}, 0.15)`);
        if (progress < 1) hazeAnimRaf = requestAnimationFrame(update);
        else hazeAnimRaf = 0;
    }
    hazeAnimRaf = requestAnimationFrame(update);
}

function clearDynamicBackground() {
    if (dynamicResetTimeout) clearTimeout(dynamicResetTimeout);
    hazeApplyGeneration++;
    activeHazeUrl = "";
    // Do NOT snap to purple — keep mesh running and re-sample catalog covers
    // (avoids idle blink on main page)
    if (viewState === "catalog") {
        scheduleCatalogPageHaze();
        dynamicResetTimeout = setTimeout(() => {
            if (elHazeSrcImg) {
                elHazeSrcImg.removeAttribute("src");
                elHazeSrcImg.removeAttribute("data-haze-src");
            }
            dynamicResetTimeout = null;
        }, 200);
        return;
    }

    ensureMeshRenderers();
    const idleColors = [
        { r: 55, g: 28, b: 48 },
        { r: 90, g: 40, b: 70 },
        { r: 35, g: 30, b: 55 },
        { r: 70, g: 35, b: 60 }
    ];
    applyHazePalette(idleColors, { force: true, soft: true });

    dynamicResetTimeout = setTimeout(() => {
        // Keep haze-active so opacity doesn't blink to idle 0.55
        if (elHazeRoot) {
            elHazeRoot.classList.add("haze-active");
            elHazeRoot.classList.remove("haze-idle");
        }
        if (elHazeSrcImg) {
            elHazeSrcImg.removeAttribute("src");
            elHazeSrcImg.removeAttribute("data-haze-src");
        }
        dynamicResetTimeout = null;
    }, 200);
}

// Kill duplicate declarations if any existed later in file for haze vars
// (lastHazePaletteKey / hazeApplyGeneration / dynamicResetTimeout re-declared near old block)

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

// Accent colors come only from haze palette (single path — no double-extract flicker)
function updateAccentFromImage(imgElement) {
    if (!imgElement || !imgElement.src) return;
    setHazeBackground(imgElement.src);
}

// Catalog Pagination and State Controls
let currentPage = 1;
let activeTab = "popular-month";
let searchQuery = "";
let activeProvider = "fitgirl";

// Adaptive catalog layout (cols × full rows = page size, no empty slots)
let catalogLayout = { cols: 6, rows: 3, pageSize: 18, gap: 12 };
// Full-list cache so we can re-slice when viewport / page size changes
const catalogFullCache = new Map();
const catalogPagesCache = new Map();

function getCatalogCacheKey(provider, page, query, tab, pageSize) {
    return `${provider}_${page}_${query || ''}_${tab || ''}_ps${pageSize || 0}`;
}
function getCatalogFullKey(provider, query, tab) {
    return `full_${provider}_${query || ''}_${tab || ''}`;
}

/**
 * Height-first catalog density:
 * pick 3 or 4 rows that EXACTLY fill available height, then derive cols from card width.
 * Incomplete last page rows are centered via flex + fixed --catalog-card-w.
 */
function computeCatalogLayout() {
    const wrapper = document.getElementById("games-grid-section") || elGamesGridContainer?.parentElement;
    if (!wrapper) {
        return { cols: 6, rows: 3, pageSize: 18, gap: 12, cardW: 150 };
    }

    const gap = 12;
    const rect = wrapper.getBoundingClientRect();
    const availW = Math.max(240, (wrapper.clientWidth || rect.width || window.innerWidth) - 24);
    const pills = document.getElementById("browse-nav-pills");
    const pillsVisible = pills && pills.style.display !== "none";
    const topChrome = pillsVisible ? 100 : 62;
    const botChrome = 78;
    const availH = Math.max(200, (wrapper.clientHeight || rect.height || window.innerHeight * 0.75) - topChrome - botChrome);

    const cardRatio = 4.15 / 3; // h/w
    let best = null;

    // Prefer 4 rows if cards stay readable; else 3. Size card HEIGHT to fill availH exactly.
    for (const rows of [4, 3, 2]) {
        const cardH = (availH - gap * (rows - 1)) / rows;
        const cardW = cardH / cardRatio;
        if (cardW < 108 || cardW > 220) continue;

        // How many full columns fit at this card width
        let cols = Math.floor((availW + gap) / (cardW + gap));
        cols = Math.max(3, Math.min(10, cols));

        // Recenter: use exact cardW from height (may leave side gutters — flex centers them)
        // If leftover width is huge, bump cols and slightly shrink width while keeping near-full height
        let useW = cardW;
        let useH = cardH;
        const widthIfCols = (availW - gap * (cols - 1)) / cols;
        if (widthIfCols < cardW * 0.92) {
            // cramped — reduce cols
            cols = Math.max(3, cols - 1);
        } else if (widthIfCols > cardW * 1.08 && cols < 10) {
            // can fit one more col with still-decent size
            const tryCols = cols + 1;
            const tryW = (availW - gap * (tryCols - 1)) / tryCols;
            const tryH = tryW * cardRatio;
            const usedH = tryH * rows + gap * (rows - 1);
            if (tryW >= 115 && usedH <= availH + 8) {
                cols = tryCols;
                useW = tryW;
                useH = tryH;
            } else {
                useW = Math.min(cardW, widthIfCols);
                useH = useW * cardRatio;
            }
        } else {
            // Prefer height-fill: keep cardH, cardW from height
            useW = cardW;
            useH = cardH;
        }

        const usedH = useH * rows + gap * (rows - 1);
        const leftover = Math.max(0, availH - usedH);
        const score =
            (rows >= 3 ? 300 : 80) +
            (rows === 4 ? 40 : 0) +
            (useW >= 130 && useW <= 190 ? 50 : 0) -
            leftover * 2.2 - // heavily punish empty bottom
            Math.abs(useW - 155) * 0.15;

        if (!best || score > best.score) {
            best = {
                cols,
                rows,
                pageSize: cols * rows,
                gap,
                cardW: Math.floor(useW * 10) / 10,
                cardH: useH,
                leftover,
                score
            };
        }
    }

    if (!best) {
        const cols = Math.max(3, Math.min(8, Math.floor(availW / 140)));
        const rows = 3;
        const cardW = (availW - gap * (cols - 1)) / cols;
        best = { cols, rows, pageSize: cols * rows, gap, cardW, score: 0 };
    }

    return {
        cols: best.cols,
        rows: best.rows,
        pageSize: best.pageSize,
        gap: best.gap,
        cardW: best.cardW
    };
}

function applyCatalogLayout() {
    const layout = computeCatalogLayout();
    catalogLayout = layout;
    if (elGamesGridContainer) {
        elGamesGridContainer.style.setProperty("--catalog-cols", String(layout.cols));
        elGamesGridContainer.style.setProperty("--catalog-gap", `${layout.gap}px`);
        elGamesGridContainer.style.setProperty("--catalog-card-w", `${layout.cardW}px`);
    }
    return layout;
}

/** Viewport-fixed Download dock helpers (element lives on <body>). */
function setDetailsDownloadBarVisible(visible) {
    const bar = document.getElementById("details-bottom-bar");
    if (!bar) return;
    // Ensure bar is a direct body child so fixed = viewport (not trapped by transform/overflow)
    if (bar.parentElement !== document.body) {
        document.body.appendChild(bar);
    }
    if (visible) {
        bar.classList.add("is-visible");
        bar.style.setProperty("display", "flex", "important");
        bar.setAttribute("aria-hidden", "false");
    } else {
        bar.classList.remove("is-visible");
        bar.style.setProperty("display", "none", "important");
        bar.setAttribute("aria-hidden", "true");
    }
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
            // Card may already be detached if user switched provider quickly
            if (!card.isConnected) return;
            const coverArea = card.querySelector(".card-cover-area");
            if (!coverArea) return;
            const img = document.createElement("img");
            img.className = "card-cover";
            img.src = cachedUrl;
            img.alt = "";
            img.draggable = false;
            img.decoding = "async";
            img.onload = () => {
                if (card.isConnected) applyCardDynamicAccent(img, card);
            };
            img.onerror = () => {
                if (!coverArea.isConnected) return;
                coverArea.innerHTML = `<div class="card-cover-placeholder">${GAMEPAD_SVG}</div>`;
            };
            // Replace placeholder without wiping if already has same image
            const existing = coverArea.querySelector("img.card-cover");
            if (existing && existing.src === cachedUrl) return;
            coverArea.replaceChildren(img);
        });
    }
    
    card.addEventListener("click", () => {
        elUrlTextarea.value = game.url;
        setViewState("details");
        showDetailsLoadingState(game.title, game.cover_image || "");
        // Tag analyze with generation so late responses can't paint wrong game
        elAnalyzeBtn.dataset.forGeneration = String(detailsOpenGeneration);
        elAnalyzeBtn.click();
    });
    
    return card;
}

function renderGamesList(results, popularList) {
    elGamesGridContainer.innerHTML = "";
    elGamesGridContainer.classList.remove("is-onlinefix-home");
    // Reset inline layout overrides
    elGamesGridContainer.style.display = "";
    elGamesGridContainer.style.flexDirection = "";
    elGamesGridContainer.style.gap = "";
    
    if (!results || results.length === 0) {
        elGamesGridContainer.innerHTML = `<div class="no-results-message">No repacks found.</div>`;
        return;
    }
    
    // Online-Fix home: popular marquee + square latest grid
    if (activeProvider === "onlinefix" && popularList && popularList.length > 0 && !searchQuery) {
        elGamesGridContainer.classList.add("is-onlinefix-home");
        
        const popSection = document.createElement("div");
        popSection.className = "popular-section";
        popSection.innerHTML = `
            <h3 class="section-title">Popular</h3>
            <div class="popular-slider-wrapper">
                <div class="popular-slider-scroll"></div>
            </div>
        `;
        
        const scrollTrack = popSection.querySelector(".popular-slider-scroll");
        // Duplicate for seamless marquee
        const doubleList = [...popularList, ...popularList];
        doubleList.forEach(game => {
            scrollTrack.appendChild(createGameCard(game));
        });
        
        elGamesGridContainer.appendChild(popSection);
        
        const staticTitle = document.createElement("h3");
        staticTitle.className = "section-title of-latest-title";
        staticTitle.innerText = "Latest Releases";
        elGamesGridContainer.appendChild(staticTitle);
        
        const staticGrid = document.createElement("div");
        staticGrid.className = "of-latest-grid";
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

/** Smooth staged loading progress for details fetch (0–99 until finish). */
let _detailsLoadPctTimer = 0;
let _detailsLoadPct = 0;

function setDetailsLoadPercent(pct, label) {
    _detailsLoadPct = Math.max(0, Math.min(99, Math.round(pct)));
    const elPct = document.getElementById("details-load-pct");
    const elBar = document.getElementById("details-load-bar-fill");
    const elLabel = document.getElementById("details-load-label");
    if (elPct) elPct.textContent = `${_detailsLoadPct}%`;
    if (elBar) elBar.style.width = `${_detailsLoadPct}%`;
    if (elLabel && label) elLabel.textContent = label;
}

function startDetailsLoadProgress() {
    stopDetailsLoadProgress(false);
    _detailsLoadPct = 0;
    setDetailsLoadPercent(4, "Connecting…");
    const stages = [
        { t: 400, p: 12, l: "Fetching page…" },
        { t: 1200, p: 28, l: "Fetching page…" },
        { t: 2500, p: 45, l: "Parsing repack…" },
        { t: 4500, p: 62, l: "Loading media…" },
        { t: 8000, p: 78, l: "Almost there…" },
        { t: 14000, p: 88, l: "Still loading…" },
        { t: 25000, p: 94, l: "Waiting for site…" }
    ];
    const start = performance.now();
    const tick = () => {
        const elapsed = performance.now() - start;
        let target = 4;
        let label = "Connecting…";
        for (const s of stages) {
            if (elapsed >= s.t) {
                target = s.p;
                label = s.l;
            }
        }
        // Ease toward target
        const next = _detailsLoadPct + Math.max(0.3, (target - _detailsLoadPct) * 0.08);
        setDetailsLoadPercent(Math.min(target, next), label);
        _detailsLoadPctTimer = requestAnimationFrame(tick);
    };
    _detailsLoadPctTimer = requestAnimationFrame(tick);
}

function stopDetailsLoadProgress(complete = true) {
    if (_detailsLoadPctTimer) {
        cancelAnimationFrame(_detailsLoadPctTimer);
        _detailsLoadPctTimer = 0;
    }
    if (complete) {
        setDetailsLoadPercent(100, "Done");
        const elPct = document.getElementById("details-load-pct");
        if (elPct) elPct.textContent = "100%";
        const elBar = document.getElementById("details-load-bar-fill");
        if (elBar) elBar.style.width = "100%";
    }
}

function hideDetailsPageLoader() {
    stopDetailsLoadProgress(true);
    const elDetailsLoader = document.getElementById("details-page-loader");
    if (elDetailsLoader) {
        elDetailsLoader.classList.remove("is-active");
        elDetailsLoader.style.display = "none";
        elDetailsLoader.setAttribute("aria-hidden", "true");
    }
    const detailsRoot = document.getElementById("game-details-container");
    if (detailsRoot) detailsRoot.classList.remove("is-details-loading");
}

/** Bumped on every details open — cancels stale analyze/media cycles. */
let detailsOpenGeneration = 0;
let activeMediaGeneration = 0;

/** Hard-clear showcase + thumbs so previous game never bleeds into the next. */
function clearDetailsMediaHard() {
    activeMediaGeneration++; // invalidate in-flight cycle timers / poster captures
    const imgA = document.getElementById("screenshot-main-img");
    const imgB = document.getElementById("screenshot-main-img-b");
    const video = document.getElementById("screenshot-main-direct-video");
    const iframe = document.getElementById("screenshot-main-video");
    const showcase = document.getElementById("screenshot-main-showcase-container");
    const thumbs = document.getElementById("game-screenshots-container");
    const progress = document.getElementById("media-cycle-progress");
    const fill = document.getElementById("media-cycle-progress-fill");
    [imgA, imgB].forEach((img) => {
        if (!img) return;
        try {
            img.onload = null;
            img.onerror = null;
            img.onclick = null;
            img.removeAttribute("src");
            img.src = "";
            img.classList.remove("is-active");
            img.style.opacity = "0";
            img.style.display = "block";
        } catch (_) {}
    });
    if (video) {
        try {
            video.pause();
            video.onended = null;
            video.ontimeupdate = null;
            video.onloadedmetadata = null;
            video.oncanplay = null;
            video.onerror = null;
            video.removeAttribute("src");
            video.load();
            video.controls = false;
            video.classList.remove("is-active");
        } catch (_) {}
    }
    if (iframe) {
        try {
            iframe.src = "";
            iframe.classList.remove("is-active");
        } catch (_) {}
    }
    if (thumbs) thumbs.innerHTML = "";
    if (showcase) {
        showcase.classList.remove("has-media", "preview-empty", "is-loading");
        showcase.style.removeProperty("height");
    }
    if (progress) progress.classList.remove("is-visible");
    if (fill) {
        fill.style.transition = "none";
        fill.style.width = "0%";
    }
    const section = document.getElementById("game-screenshots-section");
    if (section) {
        section.style.display = "none";
        section.classList.remove("is-loading-media");
    }
}

function showDetailsLoadingState(gameTitle, coverUrl = "") {
    detailsOpenGeneration += 1;
    clearDetailsMediaHard();
    const title = (gameTitle || "").trim() || "Loading…";
    elDetailsGameTitle.innerText = title;
    elDetailsVersionBadge.style.display = "none";
    if (elBtnOpenBrowser) elBtnOpenBrowser.style.display = "none";
    const btnOpenTop = document.getElementById("btn-open-browser-top");
    if (btnOpenTop) {
        btnOpenTop.style.display = "none";
        btnOpenTop.setAttribute("hidden", "");
    }
    elMetadataOriginalSize.innerText = "--";
    elMetadataRepackSize.innerText = "--";
    
    const detailsBottomSize = document.getElementById("details-bottom-size");
    if (detailsBottomSize) detailsBottomSize.innerText = "--";
    setDetailsDownloadBarVisible(false);
    
    // Reset metadata rows + hide empty meta card
    ["row-fg-genres", "row-fg-company", "row-fg-languages", "row-fg-orig-size", "row-fg-repack-size"].forEach(id => {
        const row = document.getElementById(id);
        if (row) row.style.display = "none";
    });
    const metaCard = document.querySelector(".details-meta-card");
    if (metaCard) metaCard.style.display = "none";

    const elVideoContainer = document.getElementById("details-video-container");
    const elVideoIframe = document.getElementById("video-iframe");
    if (elVideoIframe) elVideoIframe.src = "";
    if (elVideoContainer) elVideoContainer.style.display = "none";
    
    elSetupCover.src = "";
    elSetupCover.style.display = "none";
    elSetupCoverPlaceholder.style.display = "flex";

    const detailsCoverCard = document.getElementById("details-cover-card");
    const detailsCoverImage = document.getElementById("details-cover-image");
    const detailsCoverPlaceholder = document.getElementById("details-cover-placeholder");

    // Hide skeleton cover during load — full overlay instead of half-empty layout
    if (detailsCoverCard) {
        detailsCoverCard.classList.remove("is-loaded", "is-loading");
        detailsCoverCard.style.display = "none";
    }
    if (detailsCoverImage) {
        detailsCoverImage.removeAttribute("src");
        detailsCoverImage.src = "";
        detailsCoverImage.style.display = "none";
        detailsCoverImage.removeAttribute("data-loading");
    }
    if (detailsCoverPlaceholder) detailsCoverPlaceholder.style.display = "none";

    // Soft haze only — no broken cover flash
    if (coverUrl) {
        const proxied = coverUrl.startsWith("/api/") ? coverUrl : `/api/proxy_image?url=${encodeURIComponent(coverUrl)}`;
        getCachedImageUrl(proxied).then((cachedUrl) => {
            if (cachedUrl) setHazeBackground(cachedUrl);
        }).catch(() => {});
    } else {
        clearDynamicBackground();
    }
    
    if (elGameDescription) {
        elGameDescription.style.display = "none";
        elGameDescription.innerHTML = "";
    }
    const descSection = document.getElementById("details-desc-section");
    const featuresSection = document.getElementById("details-features-section");
    if (descSection) {
        descSection.style.display = "none";
        descSection.classList.remove("active");
    }
    if (featuresSection) {
        featuresSection.style.display = "none";
        featuresSection.classList.remove("active");
    }
    // Hard-reset media so previous game never flashes (dual layers + timers)
    clearDetailsMediaHard();
    
    elConfigCard.style.display = "none";
    elMirrorSelectSection.style.display = "none";
    
    const detailsRoot = document.getElementById("game-details-container");
    if (detailsRoot) detailsRoot.classList.add("is-details-loading");

    let elDetailsLoader = document.getElementById("details-page-loader");
    if (!elDetailsLoader) {
        elDetailsLoader = document.createElement("div");
        elDetailsLoader.id = "details-page-loader";
        elDetailsLoader.className = "details-page-loader";
        elDetailsLoader.innerHTML = `
            <div class="details-load-card">
                <div class="details-load-spinner" aria-hidden="true"></div>
                <div class="details-load-title" id="details-load-title">Loading</div>
                <div class="details-load-label" id="details-load-label">Preparing…</div>
                <div class="details-load-pct" id="details-load-pct">0%</div>
                <div class="details-load-bar" aria-hidden="true">
                    <div class="details-load-bar-fill" id="details-load-bar-fill" style="width:0%"></div>
                </div>
            </div>
        `;
        if (detailsRoot) detailsRoot.appendChild(elDetailsLoader);
    }
    const loadTitle = document.getElementById("details-load-title");
    if (loadTitle) loadTitle.textContent = title;
    elDetailsLoader.classList.add("is-active");
    elDetailsLoader.style.display = "flex";
    elDetailsLoader.setAttribute("aria-hidden", "false");
    elSetupDashboard.style.display = "none";
    startDetailsLoadProgress();
}

function updateCatalogPagination(hasNext) {
    if (hasNext) elBtnNextPage.removeAttribute("disabled");
    else elBtnNextPage.setAttribute("disabled", "true");
    elBtnPrevPage.disabled = (currentPage === 1);
    elPageIndicator.innerText = currentPage;
}

function renderCatalogPageFromFull(full) {
    const layout = applyCatalogLayout();
    const pageSize = layout.pageSize;
    const start = (currentPage - 1) * pageSize;
    const pageItems = (full.results || []).slice(start, start + pageSize);
    const hasNext = start + pageSize < (full.results || []).length;
    renderGamesList(pageItems, full.popular);
    updateCatalogPagination(hasNext);
    return pageItems.length;
}

async function fetchCatalogFullList() {
    const fullKey = getCatalogFullKey(activeProvider, searchQuery, activeTab);
    if (catalogFullCache.has(fullKey)) {
        return catalogFullCache.get(fullKey);
    }

    let response;
    if (searchQuery) {
        // Search is server-paged; fetch current server page only (still apply adaptive cols)
        response = await fetch("/api/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query: searchQuery,
                provider: activeProvider,
                page: currentPage
            })
        });
        const data = await response.json();
        if (!data.success) throw new Error(data.error || "search failed");
        // For search we do not full-cache across pages (server defines pages)
        return {
            results: data.results || [],
            popular: data.popular,
            has_next: !!data.has_next,
            serverPaged: true
        };
    }

    const type = (activeTab === "popular-year" ? "yearly" : "monthly");
    // Request a large page so we get the full popular list once, then client-slice
    response = await fetch(
        `/api/popular?provider=${activeProvider}&type=${type}&page=1&page_size=100`
    );
    const data = await response.json();
    if (!data.success) throw new Error(data.error || "popular failed");

    // If API still paginates, pull remaining pages into one list
    let all = Array.isArray(data.results) ? data.results.slice() : [];
    let page = 2;
    let hasNext = !!data.has_next;
    while (hasNext && page <= 8) {
        const r2 = await fetch(
            `/api/popular?provider=${activeProvider}&type=${type}&page=${page}&page_size=100`
        );
        const d2 = await r2.json();
        if (!d2.success || !d2.results?.length) break;
        all = all.concat(d2.results);
        hasNext = !!d2.has_next;
        page += 1;
    }

    const full = { results: all, popular: data.popular, serverPaged: false };
    catalogFullCache.set(fullKey, full);
    return full;
}

async function loadCatalogGames() {
    elGamesLoader.style.display = "flex";
    elGamesGridContainer.innerHTML = "";
    elSearchResultsTitle.style.display = "none";

    const layout = applyCatalogLayout();
    const pageSize = layout.pageSize;

    if (searchQuery) {
        elSearchResultsTitle.style.display = "block";
        elSearchResultsTitle.innerText = `Search results for: "${searchQuery}"`;
    }

    // Page-slice cache (depends on pageSize so resize invalidates naturally via key)
    const cacheKey = getCatalogCacheKey(activeProvider, currentPage, searchQuery, activeTab, pageSize);
    if (catalogPagesCache.has(cacheKey)) {
        const cached = catalogPagesCache.get(cacheKey);
        applyCatalogLayout();
        renderGamesList(cached.results, cached.popular);
        updateCatalogPagination(cached.has_next);
        elGamesLoader.style.display = "none";
        return;
    }

    try {
        const full = await fetchCatalogFullList();

        if (full.serverPaged) {
            // Search: show server page, still force even full rows when possible
            applyCatalogLayout();
            let items = full.results || [];
            // Trim to full rows only when we have a next page (avoid empty holes)
            if (full.has_next && items.length >= layout.cols) {
                const fullCount = Math.floor(items.length / layout.cols) * layout.cols;
                if (fullCount >= layout.cols * 2) items = items.slice(0, fullCount);
            }
            catalogPagesCache.set(cacheKey, {
                results: items,
                popular: full.popular,
                has_next: !!full.has_next
            });
            renderGamesList(items, full.popular);
            updateCatalogPagination(!!full.has_next);
        } else {
            const start = (currentPage - 1) * pageSize;
            const pageItems = (full.results || []).slice(start, start + pageSize);
            const hasNext = start + pageSize < (full.results || []).length;
            catalogPagesCache.set(cacheKey, {
                results: pageItems,
                popular: full.popular,
                has_next: hasNext
            });
            renderGamesList(pageItems, full.popular);
            updateCatalogPagination(hasNext);
        }
    } catch (e) {
        console.error("Load catalog games exception:", e);
        elGamesGridContainer.innerHTML = `<div class="error-text">Connection error loading catalog repacks.</div>`;
    } finally {
        elGamesLoader.style.display = "none";
        elBtnPrevPage.disabled = (currentPage === 1);
        elPageIndicator.innerText = currentPage;
        // After cards render: sample visible covers → page accent haze
        scheduleCatalogPageHaze();
    }
}

/** Aggregate dominant colors from covers currently on this catalog page. */
function scheduleCatalogPageHaze() {
    if (viewState !== "catalog") return;
    clearTimeout(window._catalogHazeTimer);
    window._catalogHazeTimer = setTimeout(() => updateCatalogPageHazeFromCovers(), 400);
}

function updateCatalogPageHazeFromCovers() {
    if (viewState !== "catalog") return;
    ensureMeshRenderers();
    const cards = elGamesGridContainer
        ? [...elGamesGridContainer.querySelectorAll(":scope > .game-card img.card-cover, .of-latest-grid img.card-cover")]
        : [];
    const samples = [];
    const tryExtract = (img) => {
        try {
            if (!img || !img.complete || !img.naturalWidth) return;
            const cols = extractPaletteFromImage(img, 6);
            if (cols && cols.length) samples.push(...cols);
        } catch (_) {}
    };
    let pending = 0;
    const finish = () => {
        if (viewState !== "catalog") return;
        if (!samples.length) {
            // Stable non-blinking idle (no purple snap)
            applyHazePalette([
                { r: 55, g: 28, b: 48 },
                { r: 90, g: 40, b: 70 },
                { r: 35, g: 30, b: 55 },
                { r: 70, g: 35, b: 60 }
            ], { force: true, soft: true });
            return;
        }
        // Bucket by coarse hue; weight dominant buckets higher
        const buckets = new Map();
        for (const c of samples) {
            const { h, s, l } = rgbToHsl(c.r, c.g, c.b);
            if (s < 0.12 || l < 0.08 || l > 0.82) continue; // skip grey/black/white
            const key = Math.round(h / 28) * 28; // ~13 hue bins
            const prev = buckets.get(key) || { n: 0, r: 0, g: 0, b: 0, s: 0 };
            prev.n += 1;
            prev.r += c.r;
            prev.g += c.g;
            prev.b += c.b;
            prev.s += s;
            buckets.set(key, prev);
        }
        let ranked = [...buckets.values()]
            .map(b => ({
                n: b.n,
                r: Math.round(b.r / b.n),
                g: Math.round(b.g / b.n),
                b: Math.round(b.b / b.n),
                s: b.s / b.n
            }))
            .sort((a, b) => b.n - a.n || b.s - a.s);
        if (!ranked.length) {
            ranked = samples.slice(0, 4).map(c => ({ ...c, n: 1 }));
        }
        // Build 4 mesh colors: dominant first, then next hues, fill with variants
        const mesh = [];
        for (const c of ranked) {
            if (mesh.length >= 4) break;
            mesh.push({ r: c.r, g: c.g, b: c.b });
        }
        while (mesh.length < 4) {
            const base = mesh[mesh.length % Math.max(1, mesh.length)] || { r: 80, g: 40, b: 70 };
            mesh.push({
                r: Math.min(255, Math.max(20, base.r + (mesh.length % 2 ? 25 : -15))),
                g: Math.min(255, Math.max(15, base.g + (mesh.length % 3 ? 10 : -20))),
                b: Math.min(255, Math.max(25, base.b + (mesh.length % 2 ? -10 : 20)))
            });
        }
        // Page key so page1 ≠ page2 without forced hard cut every poll
        applyHazePalette(mesh, { force: false, soft: true });
    };

    cards.forEach((img) => {
        if (img.complete && img.naturalWidth) {
            tryExtract(img);
        } else {
            pending++;
            img.addEventListener("load", () => {
                tryExtract(img);
                pending--;
                if (pending <= 0) finish();
            }, { once: true });
            img.addEventListener("error", () => {
                pending--;
                if (pending <= 0) finish();
            }, { once: true });
        }
    });
    if (pending <= 0) finish();
}

function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0, s = 0;
    const l = (max + min) / 2;
    if (max !== min) {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = ((g - b) / d + (g < b ? 6 : 0)); break;
            case g: h = ((b - r) / d + 2); break;
            default: h = ((r - g) / d + 4); break;
        }
        h *= 60;
    }
    return { h, s, l };
}

// Recompute grid density on resize / zoom so first page stays 3–4 full rows
let catalogResizeTimer = null;
let lastCatalogLayoutKey = "";
function onCatalogViewportChange() {
    if (viewState !== "catalog") return;
    clearTimeout(catalogResizeTimer);
    catalogResizeTimer = setTimeout(() => {
        const layout = computeCatalogLayout();
        const key = `${layout.cols}x${layout.rows}`;
        if (key === lastCatalogLayoutKey) {
            applyCatalogLayout();
            return;
        }
        lastCatalogLayoutKey = key;
        // Page size changed — drop page slices and re-render from full cache
        catalogPagesCache.clear();
        currentPage = 1;
        loadCatalogGames();
    }, 180);
}
window.addEventListener("resize", onCatalogViewportChange);
if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", onCatalogViewportChange);
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

function runCatalogSearch(q) {
    const query = (q || "").trim();
    if (!query) return;
    searchQuery = query;
    if (elSearchInput) elSearchInput.value = query;
    currentPage = 1;
    elPillPopularMonth.classList.remove("active");
    elPillPopularYear.classList.remove("active");
    loadCatalogGames();
}

function openSearchOverlay() {
    const overlay = document.getElementById("search-overlay");
    const input = document.getElementById("search-overlay-input");
    if (!overlay) return;
    overlay.classList.add("open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.classList.add("search-open");
    if (input) {
        input.value = searchQuery || (elSearchInput ? elSearchInput.value : "") || "";
        setTimeout(() => input.focus(), 60);
        const clearBtn = document.getElementById("btn-search-overlay-clear");
        if (clearBtn) clearBtn.style.display = input.value ? "flex" : "none";
    }
}

function closeSearchOverlay() {
    const overlay = document.getElementById("search-overlay");
    if (!overlay) return;
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.classList.remove("search-open");
}

const elBtnOpenSearch = document.getElementById("btn-open-search");
const elSearchOverlayInput = document.getElementById("search-overlay-input");
const elSearchOverlayBackdrop = document.getElementById("search-overlay-backdrop");
const elBtnSearchOverlayGo = document.getElementById("btn-search-overlay-go");
const elBtnSearchOverlayClear = document.getElementById("btn-search-overlay-clear");

if (elBtnOpenSearch) elBtnOpenSearch.addEventListener("click", openSearchOverlay);
if (elSearchOverlayBackdrop) elSearchOverlayBackdrop.addEventListener("click", closeSearchOverlay);
if (elBtnSearchOverlayGo) {
    elBtnSearchOverlayGo.addEventListener("click", () => {
        const q = elSearchOverlayInput ? elSearchOverlayInput.value.trim() : "";
        if (q) {
            closeSearchOverlay();
            runCatalogSearch(q);
        }
    });
}
if (elBtnSearchOverlayClear) {
    elBtnSearchOverlayClear.addEventListener("click", () => {
        if (elSearchOverlayInput) {
            elSearchOverlayInput.value = "";
            elSearchOverlayInput.focus();
        }
        elBtnSearchOverlayClear.style.display = "none";
    });
}
if (elSearchOverlayInput) {
    elSearchOverlayInput.addEventListener("input", () => {
        if (elBtnSearchOverlayClear) {
            elBtnSearchOverlayClear.style.display = elSearchOverlayInput.value ? "flex" : "none";
        }
    });
    elSearchOverlayInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            const q = elSearchOverlayInput.value.trim();
            if (q) {
                closeSearchOverlay();
                runCatalogSearch(q);
            }
        } else if (e.key === "Escape") {
            closeSearchOverlay();
        }
    });
}
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("search-open")) {
        closeSearchOverlay();
    }
});

if (elSearchInput) {
    elSearchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            runCatalogSearch(elSearchInput.value);
        }
    });
}

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
    navigateBackToCatalog();
});

// Settings Modal controls
elSettingsGearBtn.addEventListener("click", () => {
    elSettingsModal.style.display = "flex";
    setTimeout(() => {
        elSettingsModal.classList.add("active");
    }, 15);
    loadGDriveAccounts();
    // Refresh WARP status when opening settings
    fetch("/api/warp/status")
        .then((r) => r.json())
        .then((d) => {
            updateWarpSettingsPanel({
                warp_status: d.installed ? "installed" : (d.warp_status || "skipped"),
                warp_connected: !!d.connected,
                warp_error_message: d.warp_error_message || "",
            });
        })
        .catch(() => {});
    fetchState();
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

    const elCaptchaKey = document.getElementById("txt-captcha-api-key");
    if (elCaptchaKey) {
        const captcha_api_key = elCaptchaKey.value.trim();
        localStorage.setItem("captchaApiKey", captcha_api_key);
        try {
            await fetch("/api/set_captcha_key", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: captcha_api_key, provider: "auto" }),
            });
        } catch (e) {
            console.error("Failed to save captcha key:", e);
        }
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
        if (elGoToSiteBtn) {
            elGoToSiteBtn.href = "https://online-fix.me/";
            elGoToSiteBtn.title = "Open Online-Fix";
        }
        if (elGoToSiteText) elGoToSiteText.innerText = "Online-Fix";
        if (elCatalogGoToSiteBtn) {
            elCatalogGoToSiteBtn.href = "https://online-fix.me/";
            elCatalogGoToSiteBtn.title = "Open Online-Fix";
            elCatalogGoToSiteBtn.style.display = "";
        }
        if (elCatalogGoToSiteText) elCatalogGoToSiteText.innerText = "Online-Fix";
    } else {
        if (elGoToSiteBtn) {
            elGoToSiteBtn.href = "https://fitgirl-repacks.site/";
            elGoToSiteBtn.title = "Open FitGirl";
        }
        if (elGoToSiteText) elGoToSiteText.innerText = "FitGirl";
        if (elCatalogGoToSiteBtn) {
            elCatalogGoToSiteBtn.href = "https://fitgirl-repacks.site/";
            elCatalogGoToSiteBtn.title = "Open FitGirl";
            elCatalogGoToSiteBtn.style.display = "";
        }
        if (elCatalogGoToSiteText) elCatalogGoToSiteText.innerText = "FitGirl";
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
    const elCaptchaKeyInit = document.getElementById("txt-captcha-api-key");
    if (elCaptchaKeyInit) {
        elCaptchaKeyInit.value = localStorage.getItem("captchaApiKey") || "";
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
        if (elGoToSiteBtn) {
            elGoToSiteBtn.href = "https://online-fix.me/";
            elGoToSiteBtn.title = "Open Online-Fix";
        }
        if (elGoToSiteText) elGoToSiteText.innerText = "Online-Fix";
        if (elCatalogGoToSiteBtn) {
            elCatalogGoToSiteBtn.href = "https://online-fix.me/";
            elCatalogGoToSiteBtn.title = "Open Online-Fix";
            elCatalogGoToSiteBtn.style.display = "";
        }
        if (elCatalogGoToSiteText) elCatalogGoToSiteText.innerText = "Online-Fix";
    } else {
        // FitGirl is ISP-blocked in DE — always open via local DoH proxy (real site content)
        const fgHome = getFitGirlHomeProxyUrl();
        if (elGoToSiteBtn) {
            elGoToSiteBtn.href = fgHome;
            elGoToSiteBtn.title = "Open FitGirl (via local unblock proxy)";
        }
        if (elGoToSiteText) elGoToSiteText.innerText = "FitGirl";
        if (elCatalogGoToSiteBtn) {
            elCatalogGoToSiteBtn.href = fgHome;
            elCatalogGoToSiteBtn.title = "Open FitGirl (via local unblock proxy)";
            elCatalogGoToSiteBtn.style.display = "";
        }
        if (elCatalogGoToSiteText) elCatalogGoToSiteText.innerText = "FitGirl";
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
// Boot idle Harmonoid mesh — single active WebGL loop (second canvas is static until crossfade)
try {
    ensureMeshRenderers();
    const idle = [
        { r: 48, g: 22, b: 58 },
        { r: 110, g: 44, b: 120 },
        { r: 36, g: 24, b: 62 },
        { r: 78, g: 34, b: 98 }
    ];
    if (meshRendererA) meshRendererA.setColors(idle);
    if (meshRendererB) meshRendererB.setColors(idle);
    elHazeMeshA?.classList.add("is-active");
    elHazeMeshB?.classList.remove("is-active");
    meshRendererA?.start();
    meshRendererB?.stop();
    hazeMeshActiveIsA = true;
    // Debounced resize — avoid thrashing canvas reallocation on window drag
    let hazeResizeTimer = 0;
    window.addEventListener("resize", () => {
        if (hazeResizeTimer) clearTimeout(hazeResizeTimer);
        hazeResizeTimer = setTimeout(() => {
            hazeResizeTimer = 0;
            const active = hazeMeshActiveIsA ? meshRendererA : meshRendererB;
            active?.resize();
            active?.draw();
        }, 120);
    }, { passive: true });
} catch (e) {
    console.warn("[haze] boot failed", e);
}
loadCatalogGames();

// Render Screenshots Showcase + Grid Gallery
function renderScreenshots(screenshotsList, videosList) {
    // Kill any previous game's media cycle / dual-layer leftovers
    const mediaGen = ++activeMediaGeneration;
    const elScreenshotsSection = document.getElementById("game-screenshots-section");
    const elScreenshotsContainer = document.getElementById("game-screenshots-container");
    const elMainScreenshotImg = document.getElementById("screenshot-main-img");
    const elMainScreenshotImgB = document.getElementById("screenshot-main-img-b");
    const elMainVideoIframe = document.getElementById("screenshot-main-video");
    const elMainDirectVideo = document.getElementById("screenshot-main-direct-video");
    const elMainScreenshotShowcase = document.getElementById("screenshot-main-showcase-container");

    // Dual-layer image crossfade state (A/B ping-pong)
    let activeImgLayer = elMainScreenshotImg; // currently visible img
    let fadeImgLayer = elMainScreenshotImgB;  // next img (hidden)
    let mediaFadeToken = 0;
    const MEDIA_FADE_MS = 550;
    const isLive = () => mediaGen === activeMediaGeneration;

    // Drop torrent-stats / tracker banners / other junk
    const junkShotRe = /torrent-stats|torrentstats|kitty-kode|statspics|tracker-stats|favicon|gravatar|wp-includes|emoji/i;
    screenshotsList = (screenshotsList || []).filter(u => u && !junkShotRe.test(u));
    // Prefer full riotpixels (no .240p)
    screenshotsList = screenshotsList.map(u =>
        u.replace(/\.(jpg|jpeg|png|webp)\.(?:240p|400p|720p)\.(?:jpg|jpeg|png|webp)$/i, ".$1")
         .replace(/\.(?:240p|400p|720p)\.(jpg|jpeg|png|webp)$/i, ".$1")
    );
    videosList = (videosList || []).filter(Boolean);

    function normalizeVideoUrl(videoUrl) {
        // Keep microtrailer.webm / steam trailers as-is.
        // Rewriting to movie_max.mp4 caused 404 and silent autoplay failure.
        let playUrl = (videoUrl || "").trim();
        if (playUrl.startsWith("//")) playUrl = "https:" + playUrl;
        return playUrl;
    }

    function isDirectVideo(url) {
        const u = (url || "").toLowerCase();
        return u.includes(".webm") || u.includes(".mp4") || u.includes(".ogg") || u.includes("/store_trailers/");
    }

    function isYouTube(url) {
        return /youtube\.com|youtu\.be/i.test(url || "");
    }

    function youtubeId(url) {
        if (!url) return "";
        const m = url.match(/(?:embed\/|v=|youtu\.be\/|shorts\/)([A-Za-z0-9_-]{6,})/);
        return m ? m[1] : "";
    }

    function youtubeEmbedUrl(url) {
        const id = youtubeId(url);
        if (!id) return url;
        // muted autoplay so browsers allow it
        return `https://www.youtube.com/embed/${id}?autoplay=1&mute=1&rel=0&modestbranding=1&playsinline=1`;
    }

    function youtubePoster(url) {
        const id = youtubeId(url);
        return id ? `https://img.youtube.com/vi/${id}/hqdefault.jpg` : "";
    }

    function setLayerActive(el, on) {
        if (!el) return;
        if (on) el.classList.add("is-active");
        else el.classList.remove("is-active");
    }

    function deactivateAllMediaLayers({ keep = null } = {}) {
        [elMainScreenshotImg, elMainScreenshotImgB, elMainDirectVideo, elMainVideoIframe].forEach((el) => {
            if (!el || el === keep) return;
            setLayerActive(el, false);
        });
    }

    /**
     * Smart fit — prioritize FULL column width (user: less empty side space).
     * - Always use 100% of available width.
     * - Height = width / natural AR when it fits under maxH.
     * - If too tall: keep full width + maxH height, object-fit:cover (tiny crop, no bars).
     * - If AR matches exactly: object-fit:fill (no crop, no bars).
     */
    function fitShowcaseToSize(nw, nh) {
        if (!elMainScreenshotShowcase || !nw || !nh) return;
        const ar = nw / nh;
        const parent = elMainScreenshotShowcase.parentElement;
        // Prefer the media card / right column full inner width
        const maxW = Math.max(
            320,
            (parent && parent.clientWidth) || elMainScreenshotShowcase.clientWidth || 900
        );
        // Use more vertical room so 16:9 can stay full-width on laptops
        const maxH = Math.min(Math.max(360, window.innerHeight * 0.78), 1040);

        // Always claim full width of the column
        let w = maxW;
        let h = w / ar;
        let fitMode = "fill"; // perfect when box AR === media AR
        if (h > maxH) {
            h = maxH;
            // keep full width → box AR != media AR → cover avoids black bars
            fitMode = "cover";
        }
        w = Math.max(280, Math.round(w));
        h = Math.max(200, Math.round(h));

        elMainScreenshotShowcase.style.setProperty("--ss-ar", `${nw} / ${nh}`);
        elMainScreenshotShowcase.style.setProperty("width", "100%", "important");
        elMainScreenshotShowcase.style.setProperty("max-width", "100%", "important");
        elMainScreenshotShowcase.style.setProperty("height", h + "px", "important");
        elMainScreenshotShowcase.style.setProperty("min-height", "0", "important");
        elMainScreenshotShowcase.style.setProperty("max-height", "none", "important");
        // When cover mode, don't force image AR on the box (width 100% + fixed h)
        if (fitMode === "cover") {
            elMainScreenshotShowcase.style.setProperty("aspect-ratio", "auto", "important");
        } else {
            elMainScreenshotShowcase.style.setProperty("aspect-ratio", `${nw} / ${nh}`, "important");
        }
        elMainScreenshotShowcase.style.setProperty("margin-left", "0", "important");
        elMainScreenshotShowcase.style.setProperty("margin-right", "0", "important");

        [elMainScreenshotImg, elMainScreenshotImgB, elMainDirectVideo, elMainVideoIframe].forEach((el) => {
            if (!el) return;
            el.style.setProperty("object-fit", fitMode, "important");
            el.style.setProperty("object-position", "center center", "important");
            el.style.setProperty("width", "100%", "important");
            el.style.setProperty("height", "100%", "important");
            el.style.setProperty("left", "0", "important");
            el.style.setProperty("top", "0", "important");
            // keep layers in layout for opacity crossfade (not display:none)
            if (el.tagName === "IMG" || el.tagName === "VIDEO" || el.tagName === "IFRAME") {
                el.style.setProperty("display", "block", "important");
            }
        });
    }

    function fitShowcaseToNaturalSize(imgEl) {
        if (!imgEl) return;
        fitShowcaseToSize(imgEl.naturalWidth, imgEl.naturalHeight);
    }

    /**
     * Smooth crossfade to a still image.
     * Preloads into the inactive A/B layer, then swaps opacity — no hard cut.
     */
    function showMainScreenshot(proxiedSrc, { instant = false } = {}) {
        if (!elMainScreenshotImg && !elMainScreenshotImgB) return;
        // Ensure dual layers exist; fall back to single img
        const hasDual = !!(elMainScreenshotImg && elMainScreenshotImgB);
        const target = hasDual
            ? ((activeImgLayer && activeImgLayer.src && !instant) ? fadeImgLayer : (activeImgLayer || elMainScreenshotImg))
            : elMainScreenshotImg;
        if (!target) return;

        const token = ++mediaFadeToken;
        target.alt = "";
        target.style.cursor = "zoom-in";
        target.onclick = () => openScreenshotModal(proxiedSrc);

        const reveal = () => {
            if (token !== mediaFadeToken) return;
            fitShowcaseToNaturalSize(target);
            if (elMainScreenshotShowcase) {
                elMainScreenshotShowcase.classList.remove("preview-empty", "is-loading");
                elMainScreenshotShowcase.classList.add("has-media");
            }
            // Fade video/iframe out while image fades in
            if (elMainDirectVideo) {
                setLayerActive(elMainDirectVideo, false);
                try { elMainDirectVideo.pause(); } catch (_) {}
            }
            if (elMainVideoIframe) setLayerActive(elMainVideoIframe, false);

            if (hasDual && target !== activeImgLayer) {
                setLayerActive(target, true);
                setLayerActive(activeImgLayer, false);
                // swap roles after fade
                const prev = activeImgLayer;
                activeImgLayer = target;
                fadeImgLayer = prev;
            } else {
                setLayerActive(target, true);
                if (hasDual && fadeImgLayer && fadeImgLayer !== target) setLayerActive(fadeImgLayer, false);
                activeImgLayer = target;
                fadeImgLayer = hasDual
                    ? (target === elMainScreenshotImg ? elMainScreenshotImgB : elMainScreenshotImg)
                    : null;
            }
            // After fade, fully stop video so it doesn't keep decoding under the image
            setTimeout(() => {
                if (token !== mediaFadeToken) return;
                if (elMainDirectVideo && !elMainDirectVideo.classList.contains("is-active")) {
                    try {
                        elMainDirectVideo.removeAttribute("src");
                        elMainDirectVideo.load();
                        elMainDirectVideo.controls = false;
                    } catch (_) {}
                }
                if (elMainVideoIframe && !elMainVideoIframe.classList.contains("is-active")) {
                    elMainVideoIframe.src = "";
                }
            }, MEDIA_FADE_MS + 40);
            requestAnimationFrame(() => fitShowcaseToNaturalSize(target));
        };

        target.onload = reveal;
        target.onerror = () => {
            if (token !== mediaFadeToken) return;
            setLayerActive(target, false);
            if (elMainScreenshotShowcase) elMainScreenshotShowcase.classList.add("preview-empty");
        };

        // Same src already fully loaded
        if (target.src && target.src.endsWith(proxiedSrc.replace(/^\//, "")) === false) {
            /* always assign; browser may cache */
        }
        if (target.getAttribute("src") === proxiedSrc && target.complete && target.naturalWidth) {
            reveal();
        } else {
            // Start invisible if this is the incoming layer
            if (hasDual && target === fadeImgLayer) setLayerActive(target, false);
            target.src = proxiedSrc;
            if (target.complete && target.naturalWidth) reveal();
        }

        if (elMainScreenshotShowcase && !elMainScreenshotShowcase._ssResizeBound) {
            elMainScreenshotShowcase._ssResizeBound = true;
            window.addEventListener("resize", () => {
                const live = activeImgLayer || elMainScreenshotImg;
                if (live && live.naturalWidth) fitShowcaseToNaturalSize(live);
                else if (elMainDirectVideo && elMainDirectVideo.videoWidth) {
                    fitShowcaseToSize(elMainDirectVideo.videoWidth, elMainDirectVideo.videoHeight);
                }
            });
        }
    }

    function fallbackToFirstScreenshot() {
        if (!screenshotsList || !screenshotsList.length) {
            if (elMainScreenshotShowcase) elMainScreenshotShowcase.classList.add("preview-empty");
            return;
        }
        const firstScreenshotUrl = `/api/proxy_image?url=${encodeURIComponent(screenshotsList[0])}`;
        showMainScreenshot(firstScreenshotUrl, { instant: true });
        if (elScreenshotsContainer) {
            const firstImg = elScreenshotsContainer.querySelector("img.ss-thumb");
            if (firstImg) {
                elScreenshotsContainer.querySelectorAll(".video-thumbnail-wrapper, img").forEach(i => i.classList.remove("active"));
                firstImg.classList.add("active");
            }
        }
    }

    /** Steam trailer → official store thumbnail (different from screenshots). */
    function steamTrailerPoster(videoUrl) {
        const u = normalizeVideoUrl(videoUrl || "");
        if (!/steam/i.test(u)) return "";
        // .../steam/apps/12345/movie_max.mp4|movie480.webm|microtrailer.webm
        // → .../steam/apps/12345/movie.293x165.jpg
        const m = u.match(/^(https?:\/\/[^?#]*?\/steam\/apps\/\d+\/)/i);
        if (m) return m[1] + "movie.293x165.jpg";
        const m2 = u.match(/^(https?:\/\/[^?#]*?\/apps\/\d+\/)/i);
        if (m2 && /steam/i.test(u)) return m2[1] + "movie.293x165.jpg";
        return "";
    }

    /**
     * Capture a mid-frame (~50%) from a trailer as poster.
     * Uses same-origin /api/proxy_media so canvas is not CORS-tainted
     * (raw CDN videos almost always fail toDataURL → wrong first-screenshot fallback).
     */
    function captureVideoPoster(videoUrl) {
        return new Promise((resolve) => {
            const playUrl = normalizeVideoUrl(videoUrl);
            if (!playUrl) {
                resolve("");
                return;
            }
            if (!isDirectVideo(playUrl)) {
                resolve(youtubePoster(videoUrl) || steamTrailerPoster(videoUrl) || "");
                return;
            }
            // Prefer Steam official thumb when available (fast + distinct from screenshots)
            const steamThumb = steamTrailerPoster(playUrl);
            if (steamThumb) {
                // Still try mid-frame in background via proxy; start with steam thumb
                // Caller can set steam first then upgrade — we resolve steam immediately
                // for snappy UI, and also attempt mid-frame upgrade below.
            }

            const v = document.createElement("video");
            v.muted = true;
            v.playsInline = true;
            v.preload = "auto";
            v.crossOrigin = "anonymous";
            let settled = false;
            const finish = (url) => {
                if (settled) return;
                settled = true;
                try { v.removeAttribute("src"); v.load(); } catch (_) {}
                resolve(url || steamThumb || "");
            };
            const timer = setTimeout(() => finish(steamThumb || ""), 10000);

            // Same-origin proxy → canvas export works
            const proxied = `/api/proxy_media?url=${encodeURIComponent(playUrl)}`;

            v.addEventListener("loadedmetadata", () => {
                try {
                    const dur = v.duration;
                    // Prefer middle of trailer (user request); avoid first black frame
                    const t = (isFinite(dur) && dur > 0.6)
                        ? Math.max(0.4, Math.min(dur * 0.5, dur - 0.2))
                        : 1.0;
                    v.currentTime = t;
                } catch (_) {
                    clearTimeout(timer);
                    finish(steamThumb || "");
                }
            });
            v.addEventListener("seeked", () => {
                try {
                    const canvas = document.createElement("canvas");
                    const vw = v.videoWidth || 640;
                    const vh = v.videoHeight || 360;
                    if (vw < 2 || vh < 2) {
                        clearTimeout(timer);
                        finish(steamThumb || "");
                        return;
                    }
                    const scale = Math.min(1, 960 / Math.max(vw, 1));
                    canvas.width = Math.max(1, Math.round(vw * scale));
                    canvas.height = Math.max(1, Math.round(vh * scale));
                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
                    // Reject near-black first frames (failed seek / empty)
                    try {
                        const sample = ctx.getImageData(
                            Math.floor(canvas.width / 2),
                            Math.floor(canvas.height / 2),
                            1, 1
                        ).data;
                        const lum = 0.2126 * sample[0] + 0.7152 * sample[1] + 0.0722 * sample[2];
                        if (lum < 6) {
                            clearTimeout(timer);
                            finish(steamThumb || "");
                            return;
                        }
                    } catch (_) { /* ignore sample errors */ }
                    clearTimeout(timer);
                    finish(canvas.toDataURL("image/jpeg", 0.86));
                } catch (_) {
                    clearTimeout(timer);
                    finish(steamThumb || "");
                }
            });
            v.addEventListener("error", () => {
                clearTimeout(timer);
                finish(steamThumb || "");
            });
            v.src = proxied;
        });
    }

    function playVideo(videoUrl, { userLoop = false, showControls = null } = {}) {
        let playUrl = normalizeVideoUrl(videoUrl);
        const isDirect = isDirectVideo(playUrl);
        mediaFadeToken++; // cancel pending image fades
        // Auto-cycle: hide native controls so our progress bar is visible.
        // User click: show native controls.
        const useControls = (showControls === null) ? !!userLoop : !!showControls;

        if (isDirect) {
            if (elMainDirectVideo) {
                // Reset hard so re-click / autoplay always restarts
                try {
                    elMainDirectVideo.pause();
                    elMainDirectVideo.removeAttribute("src");
                    elMainDirectVideo.load();
                } catch (_) {}
                elMainDirectVideo.muted = true;
                elMainDirectVideo.defaultMuted = true;
                elMainDirectVideo.setAttribute("muted", "");
                elMainDirectVideo.autoplay = true;
                // Cycle mode needs 'ended' → no loop unless user clicked trailer
                elMainDirectVideo.loop = !!userLoop;
                if (userLoop) elMainDirectVideo.setAttribute("loop", "");
                else elMainDirectVideo.removeAttribute("loop");
                elMainDirectVideo.playsInline = true;
                elMainDirectVideo.setAttribute("playsinline", "");
                elMainDirectVideo.controls = useControls;
                elMainDirectVideo.preload = "auto";
                elMainDirectVideo.style.setProperty("display", "block", "important");
                elMainDirectVideo.style.setProperty("object-fit", "fill", "important");
                elMainDirectVideo.style.setProperty("background", "transparent", "important");
                // Fade video in; fade stills out
                setLayerActive(elMainDirectVideo, true);
                setLayerActive(elMainScreenshotImg, false);
                setLayerActive(elMainScreenshotImgB, false);
                setLayerActive(elMainVideoIframe, false);
                elMainDirectVideo.onloadedmetadata = () => {
                    fitShowcaseToSize(elMainDirectVideo.videoWidth || 16, elMainDirectVideo.videoHeight || 9);
                    if (elMainScreenshotShowcase) {
                        elMainScreenshotShowcase.classList.remove("preview-empty", "is-loading");
                        elMainScreenshotShowcase.classList.add("has-media");
                    }
                    elMainDirectVideo.play().catch(() => {
                        elMainDirectVideo.muted = true;
                        elMainDirectVideo.play().catch(() => {});
                    });
                };
                elMainDirectVideo.oncanplay = () => {
                    elMainDirectVideo.play().catch(() => {});
                };
                elMainDirectVideo.onerror = () => {
                    // If rewritten mp4 failed, try webm sibling once
                    if (/\.mp4($|\?)/i.test(playUrl)) {
                        const webm = playUrl.replace(/\.mp4/i, ".webm");
                        elMainDirectVideo.onerror = () => {
                            stopVideo({ hard: true });
                            fallbackToFirstScreenshot();
                        };
                        elMainDirectVideo.src = webm;
                        elMainDirectVideo.play().catch(() => {});
                        return;
                    }
                    if (/movie_max|movie480/i.test(playUrl) && /microtrailer/i.test(videoUrl || "")) {
                        elMainDirectVideo.onerror = () => {
                            stopVideo({ hard: true });
                            fallbackToFirstScreenshot();
                        };
                        elMainDirectVideo.src = videoUrl;
                        elMainDirectVideo.play().catch(() => {});
                        return;
                    }
                    stopVideo({ hard: true });
                    fallbackToFirstScreenshot();
                };
                elMainDirectVideo.src = playUrl;
                elMainDirectVideo.play().catch(() => {});
            }
            if (elMainVideoIframe) {
                elMainVideoIframe.src = "";
                setLayerActive(elMainVideoIframe, false);
            }
        } else {
            if (elMainVideoIframe) {
                elMainVideoIframe.src = isYouTube(videoUrl) ? youtubeEmbedUrl(videoUrl) : videoUrl;
                elMainVideoIframe.style.setProperty("display", "block", "important");
                elMainVideoIframe.style.setProperty("background", "#08080f", "important");
                setLayerActive(elMainVideoIframe, true);
                setLayerActive(elMainScreenshotImg, false);
                setLayerActive(elMainScreenshotImgB, false);
                setLayerActive(elMainDirectVideo, false);
                fitShowcaseToSize(16, 9);
            }
            if (elMainDirectVideo) {
                elMainDirectVideo.removeAttribute("src");
                setLayerActive(elMainDirectVideo, false);
            }
            if (elMainScreenshotShowcase) {
                elMainScreenshotShowcase.classList.remove("preview-empty", "is-loading");
                elMainScreenshotShowcase.classList.add("has-media");
            }
        }
        if (elMainScreenshotShowcase) elMainScreenshotShowcase.classList.remove("preview-empty");
    }

    function stopVideo({ hard = false } = {}) {
        if (elMainDirectVideo) {
            try { elMainDirectVideo.pause(); } catch (_) {}
            setLayerActive(elMainDirectVideo, false);
            elMainDirectVideo.controls = false;
            elMainDirectVideo.onerror = null;
            elMainDirectVideo.onloadedmetadata = null;
            elMainDirectVideo.oncanplay = null;
            if (hard) {
                try {
                    elMainDirectVideo.removeAttribute("src");
                    elMainDirectVideo.load();
                } catch (_) {}
            }
        }
        if (elMainVideoIframe) {
            setLayerActive(elMainVideoIframe, false);
            elMainVideoIframe.onerror = null;
            if (hard) elMainVideoIframe.src = "";
        }
    }

    if (elScreenshotsSection && elScreenshotsContainer) {
        elScreenshotsContainer.innerHTML = "";
        if (elMainScreenshotShowcase) elMainScreenshotShowcase.classList.remove("preview-empty");
        
        const hasVideos = videosList && videosList.length > 0;
        const hasScreenshots = screenshotsList && screenshotsList.length > 0;

        if (hasVideos || hasScreenshots) {
            if (elMainScreenshotShowcase) elMainScreenshotShowcase.style.display = "block";

            // --- Media cycle: trailer1 → trailer2 → … → shots → trailer1 (stops on user click) ---
            let mediaUserStopped = false;
            let mediaCycleTimer = null;
            let mediaShotIndex = 0;
            let mediaVideoIndex = 0;
            let progressRaf = 0;
            const SHOT_DWELL_MS = 4500;
            const shotProxied = hasScreenshots
                ? screenshotsList.map((src) => `/api/proxy_image?url=${encodeURIComponent(src)}`)
                : [];
            const elProgress = document.getElementById("media-cycle-progress");
            const elProgressFill = document.getElementById("media-cycle-progress-fill");

            function clearMediaCycle() {
                if (mediaCycleTimer) {
                    clearTimeout(mediaCycleTimer);
                    mediaCycleTimer = null;
                }
                if (progressRaf) {
                    cancelAnimationFrame(progressRaf);
                    progressRaf = 0;
                }
                if (elMainDirectVideo) {
                    elMainDirectVideo.ontimeupdate = null;
                }
            }

            function hideProgressBar() {
                if (elProgress) elProgress.classList.remove("is-visible");
                if (elProgressFill) {
                    elProgressFill.style.transition = "none";
                    elProgressFill.style.width = "0%";
                }
            }

            function setProgressPct(pct) {
                if (!elProgressFill) return;
                const p = Math.max(0, Math.min(100, pct));
                elProgressFill.style.width = p + "%";
            }

            /** Semi-transparent bar: linear for timed shots, live for video. */
            function startShotProgress(durationMs) {
                if (mediaUserStopped || !elProgress || !elProgressFill) return;
                elProgress.classList.add("is-visible");
                elProgressFill.style.transition = "none";
                setProgressPct(0);
                // Force reflow then animate to 100%
                void elProgressFill.offsetWidth;
                elProgressFill.style.transition = `width ${Math.max(200, durationMs)}ms linear`;
                requestAnimationFrame(() => setProgressPct(100));
            }

            function startVideoProgress() {
                if (mediaUserStopped || !elProgress || !elProgressFill || !elMainDirectVideo) return;
                elProgress.classList.add("is-visible");
                elProgressFill.style.transition = "none";
                setProgressPct(0);
                elMainDirectVideo.ontimeupdate = () => {
                    if (mediaUserStopped) return;
                    const d = elMainDirectVideo.duration;
                    if (!d || !isFinite(d) || d <= 0) return;
                    elProgressFill.style.transition = "none";
                    setProgressPct((elMainDirectVideo.currentTime / d) * 100);
                };
            }

            function markThumbActive(sel) {
                elScreenshotsContainer.querySelectorAll(".video-thumbnail-wrapper, img.ss-thumb")
                    .forEach((i) => i.classList.remove("active"));
                if (sel) sel.classList.add("active");
            }

            function markTrailerActive(idx) {
                const nodes = elScreenshotsContainer.querySelectorAll(".video-thumbnail-wrapper");
                markThumbActive(nodes[idx] || nodes[0] || null);
            }

            function playTrailerAt(idx, { fromUser = false } = {}) {
                if (!isLive() || !hasVideos) return;
                mediaVideoIndex = ((idx % videosList.length) + videosList.length) % videosList.length;
                clearMediaCycle();
                playVideo(videosList[mediaVideoIndex], {
                    userLoop: fromUser,
                    showControls: fromUser, // auto-cycle: no native chrome → custom bar visible
                });
                markTrailerActive(mediaVideoIndex);
                if (!fromUser && !mediaUserStopped && isLive()) {
                    wireTrailerEnded();
                    startVideoProgress();
                    if (elMainDirectVideo) {
                        elMainDirectVideo.loop = false;
                        elMainDirectVideo.removeAttribute("loop");
                    }
                } else {
                    hideProgressBar();
                }
            }

            function showShotAt(idx, { fromUser = false } = {}) {
                if (!isLive() || !shotProxied.length) return;
                mediaShotIndex = ((idx % shotProxied.length) + shotProxied.length) % shotProxied.length;
                const url = shotProxied[mediaShotIndex];
                clearMediaCycle();
                // Soft stop video (keep last frame under crossfade)
                stopVideo({ hard: false });
                showMainScreenshot(url, { instant: fromUser && !activeImgLayer?.src });
                const thumbs = elScreenshotsContainer.querySelectorAll("img.ss-thumb");
                markThumbActive(thumbs[mediaShotIndex] || null);
                if (!fromUser && !mediaUserStopped && isLive()) {
                    startShotProgress(SHOT_DWELL_MS);
                    mediaCycleTimer = setTimeout(() => {
                        if (mediaUserStopped || !isLive()) return;
                        if (mediaShotIndex >= shotProxied.length - 1) {
                            // After last shot → trailer 1 again (or first shot loop)
                            if (hasVideos) {
                                playTrailerAt(0);
                            } else {
                                showShotAt(0);
                            }
                        } else {
                            showShotAt(mediaShotIndex + 1);
                        }
                    }, SHOT_DWELL_MS);
                } else {
                    hideProgressBar();
                }
            }

            function wireTrailerEnded() {
                if (!elMainDirectVideo) return;
                elMainDirectVideo.onended = null;
                elMainDirectVideo.onended = () => {
                    if (mediaUserStopped || !isLive()) return;
                    // Trailer N finished → next trailer, then shots
                    if (mediaVideoIndex < videosList.length - 1) {
                        playTrailerAt(mediaVideoIndex + 1);
                    } else if (shotProxied.length) {
                        showShotAt(0);
                    } else if (hasVideos) {
                        playTrailerAt(0);
                    }
                };
            }

            function stopMediaCycleForUser() {
                mediaUserStopped = true;
                clearMediaCycle();
                hideProgressBar();
                if (elMainDirectVideo) elMainDirectVideo.onended = null;
            }

            // Build strip: trailer1…N FIRST, then shots
            const frag = document.createDocumentFragment();
            const trailerNodes = [];

            if (hasVideos) {
                videosList.forEach((videoUrl, vIdx) => {
                    const thumbWrapper = document.createElement("div");
                    thumbWrapper.className = "video-thumbnail-wrapper" + (vIdx === 0 ? " active" : "");
                    thumbWrapper.style.order = String(-100 + vIdx);
                    thumbWrapper.dataset.mediaKind = "trailer";
                    thumbWrapper.dataset.trailerIndex = String(vIdx);
                    const ytPoster = youtubePoster(videoUrl);
                    const steamPoster = steamTrailerPoster(videoUrl);
                    const coverFallback = (typeof scrapedMetadata !== "undefined" && scrapedMetadata.cover_image)
                        ? (scrapedMetadata.cover_image.startsWith("/api/")
                            ? scrapedMetadata.cover_image
                            : `/api/proxy_image?url=${encodeURIComponent(scrapedMetadata.cover_image)}`)
                        : "";
                    const initialPoster = ytPoster
                        ? ytPoster
                        : (steamPoster
                            ? `/api/proxy_image?url=${encodeURIComponent(steamPoster)}`
                            : coverFallback);
                    const label = videosList.length > 1 ? `Trailer ${vIdx + 1}` : "Trailer";
                    thumbWrapper.innerHTML = `
                        <img class="video-thumb-poster" alt="${label}" draggable="false" ${initialPoster ? `src="${initialPoster}"` : ""}>
                        <div class="video-thumbnail-overlay">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                                <path d="M8 5v14l11-7z"/>
                            </svg>
                        </div>
                        <span class="video-thumb-label">${label}</span>
                    `;
                    if (isDirectVideo(videoUrl) || /microtrailer|store_trailers|\.mp4|\.webm/i.test(videoUrl)) {
                        captureVideoPoster(videoUrl).then((posterUrl) => {
                            if (!posterUrl || !thumbWrapper.isConnected) return;
                            const img = thumbWrapper.querySelector(".video-thumb-poster");
                            if (!img) return;
                            img.src = posterUrl;
                        });
                    }

                    thumbWrapper.addEventListener("click", () => {
                        stopMediaCycleForUser();
                        mediaVideoIndex = vIdx;
                        playVideo(videoUrl, { userLoop: true, showControls: true });
                        markThumbActive(thumbWrapper);
                        hideProgressBar();
                    });
                    trailerNodes.push(thumbWrapper);
                    frag.appendChild(thumbWrapper);
                });
            }

            if (hasScreenshots) {
                shotProxied.forEach((proxiedSrc, idx) => {
                    const img = document.createElement("img");
                    img.className = "ss-thumb";
                    img.src = proxiedSrc;
                    img.alt = "";
                    img.loading = "lazy";
                    img.draggable = false;
                    img.style.order = String(idx + 1);
                    img.onerror = () => { img.style.display = "none"; };

                    img.addEventListener("click", () => {
                        stopMediaCycleForUser();
                        stopVideo({ hard: false });
                        showMainScreenshot(proxiedSrc);
                        mediaShotIndex = idx;
                        markThumbActive(img);
                        hideProgressBar();
                    });
                    frag.appendChild(img);
                });
            }

            elScreenshotsContainer.appendChild(frag);
            // Belt-and-suspenders: re-pin trailer nodes to absolute start of the strip
            trailerNodes.slice().reverse().forEach((n) => {
                elScreenshotsContainer.insertBefore(n, elScreenshotsContainer.firstChild);
            });
            elScreenshotsContainer.scrollLeft = 0;

            // Main stage: trailer1 → … → trailerN → shots → trailer1
            if (hasVideos) {
                playTrailerAt(0);
            } else if (hasScreenshots) {
                showShotAt(0);
            } else if (scrapedMetadata.cover_image) {
                const coverProxied = scrapedMetadata.cover_image.startsWith("/api/")
                    ? scrapedMetadata.cover_image
                    : `/api/proxy_image?url=${encodeURIComponent(scrapedMetadata.cover_image)}`;
                showMainScreenshot(coverProxied, { instant: true });
                hideProgressBar();
            } else {
                stopVideo({ hard: true });
                hideProgressBar();
                if (elMainScreenshotShowcase) {
                    elMainScreenshotShowcase.classList.remove("is-loading");
                    elMainScreenshotShowcase.classList.add("preview-empty");
                    elMainScreenshotShowcase.setAttribute("data-empty", "no-preview");
                }
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
            await fetch("/api/retry_warp", { method: "POST" });
            fetchState();
        } catch (e) {
            console.error("Failed to retry WARP installer process:", e);
        }
    });
}

// Settings → WARP install / rotate
const elWarpInstallBtn = document.getElementById("btn-warp-install");
const elWarpRotateBtn = document.getElementById("btn-warp-rotate");
if (elWarpInstallBtn) {
    elWarpInstallBtn.addEventListener("click", async () => {
        elWarpInstallBtn.disabled = true;
        elWarpInstallBtn.innerText = "Working…";
        try {
            await fetch("/api/warp/install", { method: "POST" });
            // poll status a few times while install runs
            for (let i = 0; i < 20; i++) {
                await new Promise((r) => setTimeout(r, 1500));
                fetchState();
                try {
                    const r = await fetch("/api/warp/status");
                    if (r.ok) {
                        const d = await r.json();
                        if (d.installed) break;
                    }
                } catch (_) { /* ignore */ }
            }
        } catch (e) {
            console.error("WARP install failed:", e);
            alert("WARP install request failed. Check logs / approve UAC if shown.");
        } finally {
            fetchState();
        }
    });
}
if (elWarpRotateBtn) {
    elWarpRotateBtn.addEventListener("click", async () => {
        elWarpRotateBtn.disabled = true;
        const prev = elWarpRotateBtn.innerText;
        elWarpRotateBtn.innerText = "Rotating…";
        try {
            const r = await fetch("/api/warp/rotate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: "{}",
            });
            if (!r.ok) throw new Error("HTTP " + r.status);
            // Backend force-rotates + restarts workers; poll until speed moves
            for (let i = 0; i < 12; i++) {
                await new Promise((res) => setTimeout(res, 1500));
                fetchState();
            }
            if (typeof Swal !== "undefined") {
                Swal.fire({
                    toast: true,
                    position: "top-end",
                    timer: 4000,
                    showConfirmButton: false,
                    icon: "success",
                    title: "WARP rotate done — reconnecting download",
                    background: "#040409",
                    color: "#e2e2ec",
                });
            }
        } catch (e) {
            console.error("WARP rotate failed:", e);
            alert("WARP rotate failed. Is Cloudflare WARP installed and connected?");
        } finally {
            elWarpRotateBtn.disabled = false;
            elWarpRotateBtn.innerText = prev || "Rotate IP now";
            fetchState();
        }
    });
}

// Bind browse catalog button inside dashboard
const elBackToCatalogBtnDownload = document.getElementById("btn-back-to-catalog-download");
if (elBackToCatalogBtnDownload) {
    elBackToCatalogBtnDownload.addEventListener("click", () => {
        navigateBackToCatalog();
    });
}

// Floating session pill: click body → download view; toggle → pause/resume
const elMiniBadge = document.getElementById("floating-download-badge");
if (elMiniBadge) {
    const openQueue = () => setViewState("downloading");
    const shell = document.getElementById("floating-bar-click-area");
    if (shell) {
        shell.addEventListener("click", (e) => {
            // don't open dashboard when pressing play/pause
            if (e.target.closest("#mini-btn-play-pause")) return;
            openQueue();
        });
    }

    const playPauseBtn = document.getElementById("mini-btn-play-pause");
    if (playPauseBtn) {
        playPauseBtn.addEventListener("click", async (e) => {
            e.stopPropagation();
            const api = appState.is_running ? "/api/pause" : "/api/start";
            try {
                const response = await fetch(api, { method: "POST" });
                if (response.ok) fetchState();
            } catch (err) {
                console.error("Error toggling download from floating bar:", err);
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
    const card = document.getElementById("download-config-card");
    if (step === 1) {
        if (elModalStep1Container) elModalStep1Container.style.display = "block";
        if (elModalStep2Container) elModalStep2Container.style.display = "none";
        if (elModalBtnBack) elModalBtnBack.style.display = "none";
        if (elModalNextIcon) elModalNextIcon.style.display = "inline-block";
        if (elModalStartIcon) elModalStartIcon.style.display = "none";
        if (elModalBtnText) elModalBtnText.innerText = "Next";
        if (card) card.classList.remove("step-files-wide");
    } else if (step === 2) {
        if (elModalStep1Container) elModalStep1Container.style.display = "none";
        if (elModalStep2Container) elModalStep2Container.style.display = "block";
        if (elModalBtnBack) elModalBtnBack.style.display = "block";
        if (elModalNextIcon) elModalNextIcon.style.display = "none";
        if (elModalStartIcon) elModalStartIcon.style.display = "inline-block";
        if (elModalBtnText) elModalBtnText.innerText = "Confirm & Start Download";
        if (card) card.classList.add("step-files-wide");
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
    elModalStartDownloadBtn.addEventListener("click", async () => {
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
                // Decrypt selected mirror only now (not on page open)
                if (!rawFilesList || rawFilesList.length === 0) {
                    const selected = document.querySelector(".modal-mirror-row.selected");
                    if (selected) {
                        const mUrl = selected.getAttribute("data-url");
                        const mName = selected.getAttribute("data-name") || "Mirror";
                        elModalStartDownloadBtn.setAttribute("disabled", "true");
                        try {
                            await loadMirrorLinks(mUrl, mName);
                        } finally {
                            elModalStartDownloadBtn.removeAttribute("disabled");
                        }
                    }
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

// Close button click handler inside modal card
const elCloseDownloadModalBtn = document.getElementById("btn-close-download-modal");
if (elCloseDownloadModalBtn && downloadConfigModal) {
    elCloseDownloadModalBtn.addEventListener("click", () => {
        downloadConfigModal.classList.remove("active");
        setTimeout(() => {
            downloadConfigModal.style.display = "none";
        }, 250);
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
            // Toggle to original (English)
            elText.innerText = originalDesc;
            btnTranslateDesc.innerHTML = "<span>🇬🇧</span>";
            isDescTranslated = false;
        } else {
            // Toggle to translation (Russian)
            if (translatedDesc) {
                elText.innerText = translatedDesc;
                btnTranslateDesc.innerHTML = "<span>🇷🇺</span>";
                isDescTranslated = true;
            } else {
                btnTranslateDesc.innerHTML = "<span>⏳</span>";
                btnTranslateDesc.setAttribute("disabled", "true");
                try {
                    translatedDesc = await translateText(originalDesc);
                    elText.innerText = translatedDesc;
                    btnTranslateDesc.innerHTML = "<span>🇷🇺</span>";
                    isDescTranslated = true;
                } catch (err) {
                    console.error("Translation error:", err);
                    btnTranslateDesc.innerHTML = "<span>🇬🇧</span>";
                    alert("Translation failed. Check internet connection.");
                } finally {
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
            // Toggle to original (English)
            elList.innerHTML = originalFeatures.map(txt => `<li>${txt}</li>`).join("");
            btnTranslateFeatures.innerHTML = "<span>🇬🇧</span>";
            isFeaturesTranslated = false;
        } else {
            // Toggle to translation (Russian)
            if (translatedFeatures.length > 0) {
                elList.innerHTML = translatedFeatures.map(txt => `<li>${txt}</li>`).join("");
                btnTranslateFeatures.innerHTML = "<span>🇷🇺</span>";
                isFeaturesTranslated = true;
            } else {
                btnTranslateFeatures.setAttribute("disabled", "true");
                btnTranslateFeatures.innerHTML = "<span>⏳</span>";
                const textToTranslate = originalFeatures.join("\n");
                try {
                    const translatedText = await translateText(textToTranslate);
                    translatedFeatures = translatedText.split("\n");
                    elList.innerHTML = translatedFeatures.map(txt => `<li>${txt}</li>`).join("");
                    btnTranslateFeatures.innerHTML = "<span>🇷🇺</span>";
                    isFeaturesTranslated = true;
                } catch (err) {
                    console.error("Translation error:", err);
                    btnTranslateFeatures.innerHTML = "<span>🇬🇧</span>";
                    alert("Translation failed. Check internet connection.");
                } finally {
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
        btnTranslateDesc.innerHTML = "<span>🇬🇧</span>";
    }
    if (btnTranslateFeatures) {
        btnTranslateFeatures.innerHTML = "<span>🇷🇺</span>";
    }
}

// Bind backdrop click to close floating download overlay
const elDownloadBackdrop = document.getElementById("download-view-backdrop");
if (elDownloadBackdrop) {
    elDownloadBackdrop.addEventListener("click", () => {
        setViewState("catalog");
    });
}

// Boot idle Harmonoid mesh so background is never a flat void
(function initIdleHazeMesh() {
    try {
        if (typeof applyHazePalette === "function") {
            // soft default until cover loads
            applyHazePalette([
                { r: 70, g: 28, b: 95 },
                { r: 130, g: 45, b: 120 },
                { r: 35, g: 18, b: 60 },
                { r: 95, g: 40, b: 100 }
            ]);
            if (elHazeRoot) {
                elHazeRoot.classList.add("haze-idle");
                elHazeRoot.classList.remove("haze-active");
            }
            lastHazePaletteKey = ""; // allow first real cover to apply
            activeHazeUrl = "";
        }
    } catch (e) { console.warn("idle haze", e); }
})();
