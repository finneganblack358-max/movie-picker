let watchLaterList = [];

const watchLaterButtons = document.querySelectorAll('button.watch-later');

watchLaterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const movieCard = button.closest('.movie-card');
        const movieTitle = movieCard.getAttribute('data-title');

        if (watchLaterList.includes(movieTitle)) {
            watchLaterList = watchLaterList.filter(title => title !== movieTitle);
            button.classList.remove('added');
        } else {
            watchLaterList.push(movieTitle);
            button.classList.add('added');
        }

        saveWatchLater();
        console.log(watchLaterList);
    });
});

function saveWatchLater() {
    fetch('/save-watch-later', {
        method: 'POST',
        headers: { 
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ movies: watchLaterList })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server saved:", data);
    })
    .catch(err => {
        console.error("Error saving watch later:", err);
    });
}