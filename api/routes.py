from flask import Blueprint, jsonify, render_template, request

api = Blueprint('api', __name__)

@api.route("/")
def index():
    return render_template("index.html")

@api.route("/genres")
def genres():
    return render_template("genres.html")

@api.route("/trending")
def trending():
    return render_template("trending.html")