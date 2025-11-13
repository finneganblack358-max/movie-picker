from flask import Blueprint, jsonify, request, current_app, render_template
from api.models import db, Movie
import requests

api = Blueprint("api", __name__)

@api.route("/")
def index():
    return render_template("index.html")

@api.route("/movies", methods=["GET"])
def get_movies():
    query = request.args.get("query", "Inception")
    api_key = current_app.config["TMDB_API_KEY"]

    url = f"https://api.themoviedb.org/3/search/movie"
    params = {"api_key":api_key, "query": query}
    response = requests.get(url, params=params)

    return jsonify(response.json())

@api.route("/movies/save", methods=["POST"])
def save_movie():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Movie title is required"}), 400

    new_movie = Movie(
        title=data["title"],
        description=data.get("description", "")
    )

    db.session.add(new_movie)
    db.session.commit()

    return jsonify({"message": f"Movie '{new_movie.title}' saved successfully!"}), 201

@api.route("/movies/local", methods=["GET"])
def get_saved_movies():
    movies = Movie.query.all()
    result = [{"id": m.id, "title": m.title, "description": m.description} for m in movies]
    return jsonify(result)