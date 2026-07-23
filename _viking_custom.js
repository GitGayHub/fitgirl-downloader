function cloudflareCallback(token) {
    turnstile.remove(captchaId);
    document.getElementById("captcha-download").remove();
    document.getElementById("download-link").classList.remove("hidden");

    let dotCount = 0;
    const intervalId = setInterval(() => {
        document.getElementById("download-link").textContent += ".";
        dotCount++;
        if (dotCount >= 10) {
            clearInterval(intervalId);
        }
    }, 1000);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
        setTimeout(function () {
            clearInterval(intervalId);
            var response = JSON.parse(xhr.responseText);
            if (response.link) {
                document.getElementById("download-link").textContent = "Download";
                document.getElementById("download-link").href = response.link;

                document.getElementById("download-parallel")?.classList.remove("hidden");

                if (
                    response.link.toLowerCase().endsWith(".mkv") ||
                    response.link.toLowerCase().endsWith(".mp4") ||
                    response.link.toLowerCase().endsWith(".ogg") ||
                    response.link.toLowerCase().endsWith(".webm")
                ) {
                    document.getElementById("file-information").classList.add("hidden");
                    document.getElementById("embed-code").classList.remove("hidden");
                    document.querySelector(".video-js").classList.remove("hidden");
                    document.querySelector("video").src = response.link;
                    document.querySelector("video").dispatchEvent(new Event("srcChanged"));
                }

                if (response.files) {
                    response.files.forEach((file) => {
                        document.getElementById("archive").classList.remove("hidden");

                        const fileElement = document.createElement("a");
                        fileElement.textContent = addSpacesAroundSlashes(file.name) + " - " + formatFileSize(file.size);
                        fileElement.title = addSpacesAroundSlashes(fileElement.textContent);
                        fileElement.href = response.linkArchive + file.name;
                        fileElement.target = "_blank";
                        document.getElementById("archive").appendChild(fileElement);
                        document.getElementById("archive").appendChild(document.createElement("br"));
                    });
                }
            } else {
                if (response.error) {
                    document.getElementById("download-link").textContent = "Error : " + response.error;
                } else {
                    document.getElementById("download-link").textContent = "Error : please contact us";
                }
            }
        }, 0000);
    };
    xhr.send("cf-turnstile-response=" + encodeURIComponent(token));
}

var files = [];
var links = [];
var doneFiles = 0;
var currentSize = 0;
var totalSize = 0;

if (document.getElementById("file")) {
    // Get the element that will handle the drag and drop
    const dropArea = document.getElementById("file").parentNode;

    // Prevent the default behavior of the browser when a file is dragged over the drop area
    dropArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        e.stopPropagation();
    });

    // Change the drop area's style when a file is dragged over it
    dropArea.addEventListener("dragenter", (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropArea.style.border = "3px dashed #000";
    });

    // Change the drop area's style when a file is dragged out of it
    dropArea.addEventListener("dragleave", (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropArea.style.border = "none";
    });

    dropArea.addEventListener(
        "drop",
        function (e) {
            e.preventDefault();
            e.stopPropagation();
            dropArea.style.border = "2px dashed transparent";

            document.getElementById("file").files = e.dataTransfer.files;
            var event = new Event("change");
            document.getElementById("file").dispatchEvent(event);
        },
        false,
    );

    document.getElementById("file").addEventListener("change", handleChange);
    document.getElementById("folder").addEventListener("change", handleChange);
}

function handleChange(e) {
    files = Array.from(e.target.files);
    files.forEach(function (file) {
        totalSize += file.size;
    });

    document.getElementById("progress-global").querySelector(".totalSize").innerText = (totalSize / 1024 / 1024).toFixed(2);
    document.getElementById("progress-global").querySelector(".totalFiles").innerText = files.length;

    document.getElementById("progress-current").style.display = "block";
    if (files.length > 1) {
        document.getElementById("progress-global").style.display = "block";
    }

    if (typeof uploadCloudflare !== "undefined") uploadNextFileCloudflare();
    else uploadNextFile();
}

if (document.getElementById("links")) {
    document.getElementById("links").addEventListener(
        "change",
        function (e) {
            links = document.getElementById("links").value.split("\n");

            document.getElementById("progress-current").style.display = "block";

            uploadNextLink();
        },
        false,
    );
}

async function getServer() {
    const response = await fetch(urlGetServer);
    const data = await response.json();
    return data.server;
}

async function getServerCloudflare(size) {
    const formData = new FormData();
    formData.append("size", size);
    const response = await fetch(urlGetUploadUrl, { method: "POST", body: formData });
    const data = await response.json();

    uploadId = data.uploadId;
    key = data.key;
    partSize = data.partSize;
    numberParts = data.numberParts;
    urls = data.urls;

    return data.urls;
}

async function completeUpload(file) {
    const formData = new FormData();
    formData.append("name", file.name);
    formData.append("user", document.getElementById("user").value);
    if (document.getElementById("path")) formData.append("path", document.getElementById("path").value);
    if (document.getElementById("pathPublicShare")) formData.append("pathPublicShare", document.getElementById("pathPublicShare").value);
    formData.append("uploadId", uploadId);
    formData.append("key", key);
    etags.forEach((etag, index) => {
        formData.append(`parts[${index}][PartNumber]`, etag.PartNumber);
        formData.append(`parts[${index}][ETag]`, etag.ETag);
    });
    const page = await fetch(urlCompleteUpload, { method: "POST", body: formData });
    const response = await page.json();

    if (response.url) {
        var link = document.createElement("a");
        link.setAttribute("target", "_blank");
        link.setAttribute("href", response.url);
        link.setAttribute("title", response.name + " - " + formatFileSize(response.size));
        link.textContent = file.name;
        document.getElementById("results").appendChild(link);
        document.getElementById("results").appendChild(document.createElement("br"));
        document.getElementById("results").style.display = "block";
    } else {
        document.getElementById("results").style.display = "block";
        document.getElementById("results").innerHTML += "Error : " + file.name + "<br>";
    }
}

let lastUpdateTime = 0;
function uploadNextLink() {
    document.getElementById("upload-buttons").classList.add("hidden");
    document.getElementById("infos").classList.add("hidden");
    if (links.length > 0) {
        var link = links.shift();
        var formData = new FormData();
        formData.append("link", link);
        formData.append("user", document.getElementById("user").value);
        if (document.getElementById("path")) formData.append("path", document.getElementById("path").value);
        if (document.getElementById("pathPublicShare")) formData.append("pathPublicShare", document.getElementById("pathPublicShare").value);
        getServer().then((server) => {
            fetch(server, {
                method: "POST",
                body: formData,
            })
                .then((response) => {
                    const newResponse = response.clone();
                    const reader = newResponse.body.getReader();
                    return new ReadableStream({
                        start(controller) {
                            return pump();
                            function pump() {
                                return reader.read().then(({ done, value }) => {
                                    if (done) {
                                        controller.close();
                                        return;
                                    }
                                    try {
                                        var file = JSON.parse(new TextDecoder().decode(value));
                                        if (file.progress) {
                                            const now = Date.now();
                                            if (now - lastUpdateTime >= 500) {
                                                percentage = file.progress.replace("%", "");
                                                const timeDiff = (now - lastTime) / 1000;
                                                const currentLoaded = file.current;
                                                const loadedDiff = currentLoaded - lastLoaded;
                                                if (timeDiff > 0) {
                                                    speed = loadedDiff / timeDiff;
                                                }
                                                lastLoaded = currentLoaded;
                                                lastTime = now;
                                                const speedMbps = (speed / (1024 * 1024)).toFixed(2);
                                                document.getElementById("progress-current").querySelector(".speed").innerText = speedMbps;
                                                document.getElementById("progress-current").querySelector(".fileName").innerText = file.name;
                                                document.getElementById("progress-current").querySelector("progress").value = percentage;
                                                document.getElementById("progress-current").querySelector(".currentSize").innerText = (file.current / 1024 / 1024).toFixed(2);
                                                document.getElementById("progress-current").querySelector(".totalSize").innerText = (file.total / 1024 / 1024).toFixed(2);
                                                lastUpdateTime = now;
                                            }
                                        } else {
                                            document.getElementById("results").style.display = "block";
                                            document.getElementById("results").innerHTML +=
                                                "<a target='_blank' title='" +
                                                file.name +
                                                " - " +
                                                formatFileSize(file.size) +
                                                "' href='" +
                                                file.url +
                                                "'>" +
                                                file.name +
                                                "</a><br>";
                                            uploadNextLink();
                                        }
                                    } catch (error) {
                                        const decodedValue = new TextDecoder().decode(value);
                                        if (decodedValue.includes("can not download link") || decodedValue.includes("file not saved")) {
                                            document.getElementById("results").style.display = "block";
                                            document.getElementById("results").innerHTML += "Error : " + link + "<br>";
                                            uploadNextLink();
                                        }
                                    }
                                    controller.enqueue(value);
                                    return pump();
                                });
                            }
                        },
                    });
                })
                .then((stream) => new Response(stream));
        });
    } else {
        document.getElementById("progress-current").style.display = "none";
    }
}

var xhr;
function uploadNextFile() {
    document.getElementById("upload-buttons").classList.add("hidden");
    document.getElementById("infos").classList.add("hidden");
    if (files.length > 0) {
        doneFiles++;
        document.getElementById("progress-global").querySelector(".doneFiles").innerText = doneFiles;

        var file = files.shift();
        document.getElementById("progress-current").querySelector(".fileName").innerText = file.name;

        xhr = new XMLHttpRequest();
        var formData = new FormData();
        formData.append("file", file);
        formData.append("user", document.getElementById("user").value);
        if (document.getElementById("path")) formData.append("path", document.getElementById("path").value);
        if (document.getElementById("pathPublicShare")) formData.append("pathPublicShare", document.getElementById("pathPublicShare").value);

        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                var percentage = Math.round((e.loaded * 100 * 10) / e.total) / 10;
                document.getElementById("progress-current").querySelector("progress").value = percentage;
                document.getElementById("progress-current").querySelector(".currentSize").innerText = (e.loaded / 1024 / 1024).toFixed(2);
                document.getElementById("progress-current").querySelector(".totalSize").innerText = (e.total / 1024 / 1024).toFixed(2);

                currentSizeAndLoaded = currentSize + e.loaded;
                percentageGlobal = Math.round((currentSizeAndLoaded * 100 * 10) / totalSize) / 10;
                document.getElementById("progress-global").querySelector(".currentSize").innerText = (currentSizeAndLoaded / 1024 / 1024).toFixed(2);
                document.getElementById("progress-global").querySelector("progress").value = percentageGlobal;
            }
        };

        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    if (xhr.responseText.includes("file not saved")) {
                        document.getElementById("results").style.display = "block";
                        document.getElementById("results").innerHTML += "Error : " + file.name + "<br>";
                    } else {
                        var response = JSON.parse(xhr.responseText);
                        document.getElementById("results").style.display = "block";
                        document.getElementById("results").innerHTML +=
                            "<a target='_blank' title='" + response.name + " - " + formatFileSize(response.size) + "' href='" + response.url + "'>" + response.name + "</a><br>";

                        currentSize += parseInt(response.size);
                    }
                } else {
                    document.getElementById("results").style.display = "block";
                    document.getElementById("results").innerHTML += "Error : " + file.name + "<br>";
                }

                uploadNextFile();
            }
        };

        getServer().then((server) => {
            xhr.open("POST", server);
            xhr.send(formData);
        });
    } else {
        document.getElementById("progress-current").style.display = "none";
        document.getElementById("progress-global").style.display = "none";
    }
}

uploadId = "";
key = "";
partSize = "";
numberParts = "";
urls = "";
offset = "";
function uploadNextFileCloudflare() {
    document.getElementById("upload-buttons").classList.add("hidden");
    document.getElementById("infos").classList.add("hidden");
    if (files.length > 0) {
        doneFiles++;
        document.getElementById("progress-global").querySelector(".doneFiles").innerText = doneFiles;

        var file = files.shift();
        document.getElementById("progress-current").querySelector(".fileName").innerText = file.name;

        partNumber = 1;
        offset = 0;
        etags = [];
        getServerCloudflare(file.size).then((urls) => {
            uploadNextPart(file);
        });
    } else {
        document.getElementById("progress-current").style.display = "none";
        document.getElementById("progress-global").style.display = "none";
    }
}

let lastLoaded = 0;
let lastTime = Date.now();
let speed = 0;

function uploadNextPart(file, retryCount = 0) {
    const maxRetries = 2;

    if (urls.length == 0) {
        completeUpload(file);
        uploadNextFileCloudflare();
        return false;
    }

    url = urls.shift();
    part = file.slice(offset, offset + partSize);

    xhr = new XMLHttpRequest();
    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const now = Date.now();
            if (now - lastUpdateTime >= 500) {
                const timeDiff = (now - lastTime) / 1000;
                const loadedDiff = e.loaded - lastLoaded;

                if (timeDiff > 0) {
                    speed = loadedDiff / timeDiff;
                }

                lastLoaded = e.loaded;
                lastTime = now;

                const speedMbps = (speed / (1024 * 1024)).toFixed(2);
                document.getElementById("progress-current").querySelector(".speed").innerText = speedMbps;

                var percentage = Math.round(((offset + e.loaded) * 100 * 10) / file.size) / 10;
                document.getElementById("progress-current").querySelector("progress").value = percentage;
                document.getElementById("progress-current").querySelector(".currentSize").innerText = ((offset + e.loaded) / 1024 / 1024).toFixed(2);
                document.getElementById("progress-current").querySelector(".totalSize").innerText = (file.size / 1024 / 1024).toFixed(2);

                currentSizeAndLoaded = currentSize + e.loaded;
                percentageGlobal = Math.round((currentSizeAndLoaded * 100 * 10) / totalSize) / 10;
                document.getElementById("progress-global").querySelector(".currentSize").innerText = (currentSizeAndLoaded / 1024 / 1024).toFixed(2);
                document.getElementById("progress-global").querySelector("progress").value = percentageGlobal;

                lastUpdateTime = now;
            }
        }
    };

    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4) {
            const etag = xhr.getResponseHeader("Etag");
            if (etag) {
                offset += partSize;
                currentSize += part.size;
                etags.push({
                    PartNumber: partNumber++,
                    ETag: etag,
                });
                uploadNextPart(file);
            } else {
                if (retryCount <= maxRetries) {
                    setTimeout(() => {
                        urls.unshift(url);
                        uploadNextPart(file, retryCount + 1);
                    }, 10000);
                } else {
                    document.getElementById("results").style.display = "block";
                    document.getElementById("results").innerHTML += "Error : " + file.name + "<br>";
                }
            }
        }
    };
    xhr.open("PUT", url);
    xhr.send(part);
}

["contextmenu", "click", "mousedown"].forEach((event) => {
    document.getElementById("download-link")?.addEventListener(event, function (e) {
        document.querySelector("video")?.pause();
    });

    document.getElementById("download-parallel")?.addEventListener(event, function (e) {
        document.querySelector("video")?.pause();
    });
});

window.addEventListener("turbo:before-visit", function (e) {
    if (xhr && xhr.readyState < 4) {
        xhr.abort();
    }

    var video = document.querySelector("video");
    if (video) {
        video.remove();
    }
});

function formatFileSize(size) {
    size = parseFloat(size);
    const units = ["B", "KB", "MB", "GB", "TB"];
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return `${size.toFixed(2)} ${units[unitIndex]}`;
}

function numberFormat(number, decimals, decimalSeparator, thousandSeparator) {
    let rounded = Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
    let parts = rounded.toFixed(decimals).toString().split(".");
    let integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousandSeparator);
    if (decimals === 0) {
        return integerPart;
    }
    let decimalPart = parts[1] || "";
    return integerPart + decimalSeparator + decimalPart;
}

if (window.self !== window.top) {
    const body = document.querySelector("body");
    const nav = document.querySelector("nav");
    const footer = document.querySelector("footer");
    const menu = document.getElementById("menu");
    const accountBar = document.querySelector(".account-bar");
    const filename = document.querySelector("h2");
    const size = document.getElementById("size");
    const downloadLink = document.getElementById("download-link");
    const downloadParallel = document.getElementById("download-parallel");
    const box = document.querySelector(".box");
    const embedCode = document.getElementById("embed-code");

    if (menu) {
        menu.classList.add("hidden");
    }
    if (footer) {
        footer.remove();
    }
    if (embedCode) {
        embedCode.classList.add("hidden");
    }

    document.querySelector("video").addEventListener("srcChanged", function () {
        if (body) {
            body.style.backgroundColor = "transparent";
        }
        if (nav) {
            nav.classList.add("hidden");
        }
        if (accountBar) {
            accountBar.classList.add("hidden");
        }
        if (filename) {
            filename.classList.add("hidden");
        }
        if (size) {
            size.classList.add("hidden");
        }
        if (downloadLink) {
            downloadLink.classList.add("hidden");
        }
        if (downloadParallel) {
            downloadParallel.classList.add("hidden");
        }
        if (box) {
            box.classList.remove("box");
        }
        if (embedCode) {
            embedCode.classList.add("hidden");
        }
    });
}

async function downloadFileInChunks(url, filename, numChunks = 4) {
    try {
        const response = await fetch(url, { method: "HEAD" });
        if (!response.ok) throw new Error("Impossible to get files informations");
        const fileSize = parseInt(response.headers.get("content-length"), 10);
        const chunkSize = Math.ceil(fileSize / numChunks);

        const cacheName = "file-download-cache";
        const cache = await caches.open(cacheName);

        const progressBar = document.querySelector("progress");
        const currentSize = document.querySelector(".currentSize");
        const totalSize = document.querySelector(".totalSize");
        let totalDownloaded = 0;
        totalSize.innerText = formatFileSize(fileSize);

        function updateProgressBar(downloadedBytes) {
            totalDownloaded += downloadedBytes;
            progressBar.value = `${(totalDownloaded / fileSize) * 100}`;
            currentSize.innerText = formatFileSize(totalDownloaded);
        }

        const chunks = [];
        for (let i = 0; i < numChunks; i++) {
            const start = i * chunkSize;
            const end = i === numChunks - 1 ? fileSize - 1 : (i + 1) * chunkSize - 1;
            chunks.push(downloadChunkWithProgress(cache, url, start, end, i, updateProgressBar));
        }

        await Promise.all(chunks);

        const combinedBlob = await combineChunksFromCache(cache, numChunks);

        const link = document.createElement("a");
        link.href = URL.createObjectURL(combinedBlob);
        link.download = filename;
        link.click();

        await caches.delete(cacheName);
    } catch (error) {
        console.error("Download error:", error);
        document.getElementById("download-link")?.classList.remove("hidden");
        document.getElementById("download-parallel-progress")?.classList.add("hidden");
        document.getElementById("download-parallel")?.classList.remove("hidden");
        if (document.getElementById("download-parallel")) document.getElementById("download-parallel").innerText = "Error, try normal download";
    }
}

async function downloadChunkWithProgress(cache, url, start, end, index, onProgress) {
    const headers = { Range: `bytes=${start}-${end}` };
    const response = await fetch(url, { headers });

    if (!response.ok) throw new Error(`Chunk ${index} failed`);

    const reader = response.body.getReader();
    let receivedLength = 0;
    const chunks = [];

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        chunks.push(value);
        receivedLength += value.length;

        if (onProgress) onProgress(value.length);
    }

    const blob = new Blob(chunks);

    const cacheKey = `chunk-${index}`;
    await cache.put(cacheKey, new Response(blob));
}

async function combineChunksFromCache(cache, numChunks) {
    const chunks = [];
    for (let i = 0; i < numChunks; i++) {
        const cacheKey = `chunk-${i}`;
        const response = await cache.match(cacheKey);
        if (!response) throw new Error(`Chunk ${i} not found in cache`);
        const blob = await response.blob();
        chunks.push(blob);
    }
    return new Blob(chunks, { type: "application/octet-stream" });
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
    } catch (err) {
        console.error("error during copy to clipboard : ", err);
    }
}

function copyLinksToClipboard(select) {
    var listing = "";
    var files = document.getElementById("results").getElementsByTagName("a");
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var filename = file.getAttribute("title").split("-")[0].trim();
        var size = file.getAttribute("title").split("-")[1].trim();
        if (select.value == "with filename") {
            listing = listing + file.href + "#" + filename + "\n";
        } else if (select.value == "with filename and size") {
            listing = listing + file.href + "#" + filename + " - " + size + "\n";
        } else {
            listing = listing + file.href + "\n";
        }
    }

    copyToClipboard(listing);

    select.selectedIndex = 0;
    select.options[0].textContent = "Copied";

    setTimeout(function () {
        select.options[0].textContent = "Copy links";
    }, 3000);
}

function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function addSpacesAroundSlashes(text) {
    return text.replace(/\//g, " / ");
}

const preferredTheme = getCookie("theme") || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
document.documentElement.setAttribute("data-theme", preferredTheme);
if (!getCookie("theme")) {
    setCookie("theme", preferredTheme, 3650);
}

document.getElementById("toggle-theme").addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    setCookie("theme", newTheme, 3650);
    location.reload();
});

document.getElementById("download-link")?.addEventListener("click", (event) => {
    if (event.target.textContent == "Download") {
        event.target.textContent = "Downloading ...";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    element = document.querySelector(".js-choice");
    if (element) {
        choices = new Choices(element, { addChoices: true, searchResultLimit: -1, shouldSort: false, searchPlaceholderValue: "Type Folder/Subfolder" });
    }
});

function handleFolderChange(selectElement) {
    document.querySelectorAll("option").forEach((option) => {
        option.text = addSpacesAroundSlashes(option.text);
    });

    if (typeof choices !== "undefined") {
        choices.refresh();
    }
}

document.querySelectorAll("option").forEach((option) => {
    option.text = addSpacesAroundSlashes(option.text);
});

var videoElement = document.querySelector("video");
if (videoElement) {
    var player = videojs(videoElement);

    player.ready(function () {
        document.addEventListener("keydown", function (event) {
            var currentTime = player.currentTime();
            var newTime;

            if (event.key === "ArrowRight") {
                newTime = currentTime + 30;
                player.currentTime(Math.min(newTime, player.duration()));
            } else if (event.key === "ArrowLeft") {
                newTime = currentTime - 30;
                player.currentTime(Math.max(newTime, 0));
            }
        });
    });

    player.on("play", function () {
        var overlay = document.getElementById("video-text-overlay");

        if (overlay) {
            overlay.style.display = "block";
            setTimeout(function () {
                document.getElementById("video-text-overlay").remove();
            }, 10000);
        }
    });

    player.on("error", function () {
        var error = player.error();
        if (error && (error.code === 3 || error.code === 4 || error.code === 5)) {
            document.getElementById("video-container").remove();
            document.getElementById("file-information").classList.remove("hidden");
            document.getElementById("embed-code").classList.add("hidden");
        }
    });
}
