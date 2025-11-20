from flask import Blueprint, jsonify, render_template, current_app, request, redirect, session, url_for
import requests

api = Blueprint('api', __name__)

@api.route("/")
def index():
    return render_template("index.html")

@api.route("/genres")
def genres():
    return render_template("genres.html")

@api.route("/trending")
def trending_movies():
    api_key = current_app.config["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])
        
        return render_template("trending.html", movies=movies)
    else:
        return f"Error fetching trending movies: {response.status_code}", response.status_code
    
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
    "Science-Fiction": 878,
    "TV-Movie": 10770,
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

    response = requests.get(url)
    movies = []
    if response.status_code == 200:
        data = response.json()
        movies.extend(data.get("results", []))

    return render_template("for_you.html", movies=movies)