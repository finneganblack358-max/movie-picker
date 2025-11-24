from flask import Blueprint, jsonify, render_template, current_app, request, redirect, session, url_for
import concurrent.futures
import requests
from moviequote_generator.core import MovieQuotes
from .models import MovieQuote, db

api = Blueprint('api', __name__)

@api.route("/")
def index():
    quotes = MovieQuotes()
    q = quotes.get_random_quote()

    quote_text = q.get("quote", "No quote")
    movie_name = q.get("movie", "Unknown movie")

    quote = MovieQuote(quote=quote_text, movie=movie_name)
    
    existing = MovieQuote.query.filter_by(quote=quote_text).first()
    if not existing:
        db.session.add(quote)
        db.session.commit()

    return render_template("index.html", quote=quote_text, movie=movie_name)

@api.route("/genres")
def genres():
    return render_template("genres.html")

def fetch_rating(movie, api_key):
    movie_id = movie['id']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={api_key}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            release_data = resp.json().get("results", [])
            movie['rating'] = next(
                (item['release_dates'][0]['certification']
                 for item in release_data
                 if item['iso_3166_1'] == 'US' and item['release_dates']),
                "Not Rated"
            )
        else:
            movie['rating'] = "Not Rated"
    except requests.RequestException:
        movie['rating'] = "Not Rated"
    return movie

@api.route("/trending")
def trending_movies():
    api_key = current_app.config["TMDB_API_KEY"]
    trending_url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"

    try:
        response = requests.get(trending_url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching trending movies: {e}", 500

    movies = response.json().get("results", [])

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        movies = list(executor.map(lambda m: fetch_rating(m, api_key), movies))

    return render_template("trending.html", movies=movies)

@api.route('/save-genres', methods=['POST'])
def save_genres():
    data = request.get_json()
    session['selected_genres'] = data.get('genres', [])
    return jsonify({"message": "saved"}), 200

@api.route("/for_you")
def for_you():
    genres = session.get('selected_genres', [])

    if not genres:
        return redirect(url_for('api.genres'))

    GENRE_MAP = {
        "Action": 28,
        "Animation": 16,
        "Comedy": 35,
        "Crime": 80,
        "Documentary": 99,
        "Drama": 18,
        "Fantasy": 14,
        "Family": 10751,
        "History": 36,
        "Horror": 27,
        "Music": 10402,
        "Mystery": 9648,
        "Romance": 10749,
        "Science Fiction": 878,
        "TV Movie": 10770,
        "Thriller": 53,
        "War": 10752,
        "Western": 37
    }

    genre_ids = [str(GENRE_MAP[g]) for g in genres if g in GENRE_MAP]
    if not genre_ids:
        return redirect(url_for('api.genres'))

    api_key = current_app.config["TMDB_API_KEY"]
    genre_param = ",".join(genre_ids)
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_param}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        movies = response.json().get("results", [])
    except requests.RequestException:
        movies = []

    return render_template("for_you.html", movies=movies)