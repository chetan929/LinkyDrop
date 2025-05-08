function getCSRFToken() {
    let csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : "";
}

function downloadVideo() {
    let videoUrl = document.getElementById("videoUrl").value.trim();
    let errorMessage = document.getElementById("error-message");
    let downloadMessage = document.getElementById("download-message");
    let downloadButton = document.querySelector("button");

    // Clear previous messages
    errorMessage.textContent = "";
    downloadMessage.textContent = "";

    if (!videoUrl) {
        errorMessage.textContent = "❌ Please enter a video link!";
        errorMessage.style.color = "red";
        return;
    }

    // Disable button and show loading
    downloadButton.disabled = true;
    downloadButton.textContent = "Processing...";
    downloadMessage.textContent = "⏳ Processing...";
    downloadMessage.style.color = "blue";

    fetch("/download/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("❌ Server error or video not found.");
        }

        // Try to extract filename from headers
        const disposition = response.headers.get("Content-Disposition");
        let filename = "video.mp4";
        if (disposition && disposition.includes("filename=")) {
            const match = disposition.match(/filename\*=UTF-8''(.+)|filename="?(.+?)"?$/);
            filename = decodeURIComponent(match?.[1] || match?.[2] || filename);
        }

        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        if (!blob || blob.size === 0) {
            throw new Error("❌ Video could not be downloaded.");
        }

        const downloadLink = document.createElement("a");
        const url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = filename;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        downloadLink.remove();
        URL.revokeObjectURL(url);

        downloadMessage.textContent = "✅ Download Complete!";
        downloadMessage.style.color = "green";
    })
    .catch(error => {
        downloadMessage.textContent = error.message;
        downloadMessage.style.color = "red";
    })
    .finally(() => {
        downloadButton.disabled = false;
        downloadButton.textContent = "Download";
    });
}
