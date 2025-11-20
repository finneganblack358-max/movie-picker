function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
}

function setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

document.addEventListener("DOMContentLoaded", () => {
    const saved = getCookie("selectedGenres");
    if (saved) {
        try {
            const selectedGenres = JSON.parse(saved);
            selectedGenres.forEach(genre => {
                const checkbox = document.querySelector(`input[type="checkbox"][value="${genre}"]`);
                if (checkbox) checkbox.checked = true;
            });
        } catch (err) {
            console.error("Cookie parse error:", err);
        }
    }
});

function getGenres() {
    const boxes = document.querySelectorAll('input[type="checkbox"]:checked');
    return Array.from(boxes).map(box => box.value);
}

const saveGenresButton = document.getElementById("saveGenres");

saveGenresButton.addEventListener("click", async () => {
    const userGenres = getGenres();

    if (userGenres.length === 0) {
        alert("Please select at least one genre!");
        return;
    }

    setCookie("selectedGenres", JSON.stringify(userGenres));

    try {
        const response = await fetch('/save-genres', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ genres: userGenres })
        });

        if (response.ok) {
            window.location.href = "/for_you";
        } else {
            alert("Failed to save genres. Please try again.");
        }
    } catch (error) {
        console.error("Error saving genres:", error);
        alert("An error occurred. Please try again.");
    }
});