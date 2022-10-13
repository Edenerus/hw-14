from flask import Flask, jsonify
from utils import *

app = Flask(__name__)


@app.route('/movie/<title>')
def search_movie(title):
    return get_movie_by_title(title)


@app.route('/movie/<int:year_one>/to/<int:year_two>')
def search_by_year(year_one, year_two):
    return jsonify(get_movie_by_year(year_one, year_two))


@app.route('/rating/<category>')
def search_by_rating(category):
    return jsonify(get_movie_by_rating(category))


@app.route('/genre/<genre>')
def search_by_genre(genre):
    return jsonify(get_movie_by_genre(genre))


if __name__ == '__main__':
    app.run(debug=True)
