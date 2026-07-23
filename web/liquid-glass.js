/**
 * Minimal structure helper for frosted chrome.
 * Does NOT wrap .dl-session-shell (session info must stay visible).
 */
(function () {
    "use strict";

    function boot() {
        // Only wrap pagination if needed for flex; session pill is self-contained
        document.querySelectorAll(".floating-pagination-capsule").forEach((el) => {
            el.classList.add("liquid-glass");
        });
        document.querySelectorAll(".dl-session-shell, .as-nav-pill-shell").forEach((el) => {
            el.classList.add("liquid-glass");
            // Never wrap session info into .lg-content
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }

    window.refreshLiquidGlass = boot;
})();
