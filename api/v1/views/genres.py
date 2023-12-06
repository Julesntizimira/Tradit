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

app_views.route('/genre/create/<genre_name>', methods=['GET'], strict_slashes=False)
def post_genre(genre_name):
    '''post a genre'''
    for genre in storage.all(Genre).values():
        name = genre.name
        if name.lower() == genre_name.lower() or name.lower() in genre_name.lower() or genre_name.lower() in name.lower():
            return make_response(jsonify(genre.to_dict()))
    new_genre = Genre(name=genre_name)
    new_genre.save()
    return make_response(jsonify(new_genre.to_dict()))