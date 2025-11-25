document.addEventListener("DOMContentLoaded", () => {
    const watchLaterButtons = document.querySelectorAll('button.watch-later');


    fetch('/get-watch-later')
        .then(res => res.json())
        .then(data => {
            watchLaterButtons.forEach(button => {
                const movieCard = button.closest('.movie-card');
                const movieTitle = movieCard.getAttribute('data-title');

                if (data.movies.some(m => m.title === movieTitle)) {
                    button.classList.add('added');
                    button.textContent = '✓ Watch Later';
                }
            });
        })
        .catch(err => console.error("Error loading watch later:", err));


    watchLaterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const movieCard = button.closest('.movie-card');
            const movieTitle = movieCard.getAttribute('data-title');
            const moviePoster = movieCard.getAttribute('data-poster');

            fetch('/toggle-watch-later', {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: movieTitle, poster_path: moviePoster })
            })
            .then(res => res.json())
            .then(data => {
                if (data.action === 'added') {
                    button.classList.add('added');
                    button.textContent = '✓ Watch Later';
                } else {
                    button.classList.remove('added');
                    button.textContent = 'Watch Later';
                }
            })
            .catch(err => console.error("Error toggling watch later:", err));
        });
    });
});

function deleteMovie(button) {
    const title = button.closest('.movie-card').getAttribute('data-title');
    
    fetch('/delete-from-watch-later', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title })
    })
    .then(res => res.json())
    .then(data => {
        window.location.href = '/watch_later';
    })
    .catch(err => console.error("Error deleting movie:", err));
}

function resetAll() {
    if (confirm('Are you sure you want to delete all movies from Watch Later?')) {
        fetch('/reset-watch-later', {
            method: 'POST',
            headers: { "Content-Type": "application/json" }
        })
        .then(res => res.json())
        .then(data => {
            window.location.href = '/watch_later';
        })
        .catch(err => console.error("Error resetting watch later:", err));
    }
}