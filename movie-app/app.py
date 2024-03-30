#!/usr/bin/python3
from flask import Flask, jsonify, make_response, request, abort, url_for
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()

movies = [
           {
                'id': 1,
                'title': "The Shawshank Redemption",
                'director': "Frank Darabont",
                'release_year': 1994
            },
           {
                'id': 2,
                'title': "The Godfather",
                'director': "Francis Ford Coppola",
                'release_year': 1972
            },
           {
                'id': 3,
                'title': "The Dark Knight",
                'director': "Christopher Nolan",
                'release_year': 2008
            },
           {
                'id': 4,
                'title': "Pulp Fiction",
                'director': "Quentin Tarantino",
                'release_year': 1994
            },
           {
                'id': 5,
                'title': "Schindler's List",
                'director': "Steven Spielberg",
                'release_year': 1993
            }
    ]

@auth.verify_password
def verify_password(username, password):
    if username == 'waltertaya' and password == 'password123':
        return True
    return False

def make_public_movie(movie):
    new_movie = {}
    for field in movie:
        if field == 'id':
            new_movie['uri'] = url_for('get_movie', movie_id=movie['id'], _external=True)
        else:
            new_movie[field] = movie[field]
    return new_movie

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource Not Found'}), 404)

@app.route('/films/api/v1.0/movies', methods=['GET'])
@auth.login_required
def get_movies():
    return jsonify({'movies': [make_public_movie(movie) for movie in movies]})

@app.route('/films/api/v1.0/movies/<int:movie_id>', methods=['GET'])
@auth.login_required
def get_movie(movie_id):
    movie = [movie for movie in movies if movie['id'] == movie_id]
    if len(movie) == 0:
        abort(404)
    return jsonify({'movie': make_public_movie(movie[0])})

@app.route('/films/api/v1.0/movies', methods=['POST'])
@auth.login_required
def create_movie():
    if not request.json or not 'title' in request.json:
        """If the data isn't there, or if it is there, but we are missing a title item
          then we return an error code 400, which is the code for the bad request."""
        abort(400)
    movie = {
        'id': movies[-1]['id'] + 1,
        'title': request.json['title'], # The request.json will have the request data, but only if it came marked as JSON
        'director': request.json['director'],
        'release_year': request.json['release_year']
    }
    movies.append(movie)
    return jsonify({'movie': make_public_movie(movie)}), 201

@app.route('/films/api/v1.0/movies/<int:movie_id>', methods=['PUT'])
@auth.login_required
def update_movie(movie_id):
    movie = [movie for movie in movies if movie['id'] == movie_id]
    if len(movie) == 0:
        abort(404)
    if not request.json:
        abort(400)
    movie[0]['title'] = request.json.get('title', movie[0]['title'])
    movie[0]['director'] = request.json.get('director', movie[0]['director'])
    movie[0]['release_year'] = request.json.get('release_year', movie[0]['release_year'])
    return jsonify({'movie': make_public_movie(movie[0])})

@app.route('/films/api/v1.0/movies/<int:movie_id>', methods=['DELETE'])
@auth.login_required
def delete_movie(movie_id):
    movie = [movie for movie in movies if movie['id'] == movie_id]
    if len(movie) == 0:
        abort(404)
    movies.remove(movie[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
