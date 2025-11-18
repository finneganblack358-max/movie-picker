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