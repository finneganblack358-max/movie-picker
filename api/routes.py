from flask import Blueprint, jsonify, render_template, current_app, request
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