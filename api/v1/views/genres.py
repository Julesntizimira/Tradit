'''genres Api'''
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.genre import Genre


@app_views.route('/genres', methods=['GET'], strict_slashes=False)
def get_genres():
    ''' get all genres present in storage'''
    genreList = []
    for genre in storage.all(Genre).values():
        genreList.append(genre.to_dict())
    return make_response(jsonify(genreList))

@app_views.route('/genre/<genre_id>', methods=['GET'], strict_slashes=False)
def get_genre(genre_id):
    ''' get genre by id'''
    genre = storage.get(Genre, genre_id)
    if genre:
        return make_response(jsonify(genre.to_dict()), 201)
    return make_response(jsonify({}), 200)

@app_views.route('/genre/new/<name>', methods=['POST'], strict_slashes=False)
def add_to_genres(name):
    '''add to genre'''
    for genre in storage.all(Genre).values():
        if genre.name.lower() == name.lower():
            return make_response(jsonify(genre.to_dict()), 200)
    new_genre = Genre(name=name)
    new_genre.save()
    return make_response(jsonify(new_genre.to_dict()), 201)