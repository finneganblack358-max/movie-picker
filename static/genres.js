document.addEventListener("DOMContentLoaded", () => {
    loadSavedGenres();

    // Toggle checkbox when clicking on div
    document.querySelectorAll(".category-checkbox").forEach(div => {
        div.addEventListener("click", e => {
            if (e.target.tagName !== "INPUT") {
                const checkbox = div.querySelector("input[type='checkbox']");
                if (checkbox) checkbox.checked = !checkbox.checked;
            }
        });
    });

    // Save button
    const saveGenresButton = document.getElementById("saveGenres");
    if (saveGenresButton) {
        saveGenresButton.addEventListener("click", async () => {
            const userGenres = getSelectedGenres();
            if (userGenres.length === 0) {
                alert("Please select at least one genre!");
                return;
            }
            await saveGenres(userGenres);
        });
    }
});

function getSelectedGenres() {
    return Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(box => box.value);
}

function loadSavedGenres() {
    const saved = getCookie("selectedGenres");
    if (!saved) return;

    try {
        const selectedGenres = JSON.parse(saved);
        selectedGenres.forEach(genre => {
            const checkbox = document.querySelector(`input[value="${genre}"]`);
            if (checkbox) checkbox.checked = true;
        });
    } catch (err) {
        console.error("Failed to parse saved genres cookie:", err);
    }
}

async function saveGenres(userGenres) {
    setCookie("selectedGenres", JSON.stringify(userGenres));

    try {
        const response = await fetch('/save-genres', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ genres: userGenres })
        });

        if (response.ok) {
            window.location.href = "/for_you";
        } else {
            alert("Failed to save genres. Please try again.");
        }
    } catch (err) {
        console.error("Error saving genres:", err);
        alert("An error occurred. Please try again.");
    }
}

// Simple cookie helpers
function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
}

function setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}
