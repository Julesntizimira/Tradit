from flask import jsonify, make_response, abort, request, abort
from api.v1.views import app_views
from models import storage
from models.genre import Genre


app_views.route('/genres', methods=['GET'], strict_slashes=False)
def get_genre_list():
    '''get a genres list'''
    genreList = []
    for genre in storage.all(Genre).values():
        genreList.append(genre.to_dict())
    return make_response(jsonify(genreList))

app_views.route('/genres/create', methods=['POST'], strict_slashes=False)
def add_to_genre_list():
    '''add to genres list'''
    data = request.json()
    name = data.get('name')
    for genre in storage.all(Genre).values():
        if genre.name.lower() == name.lower():
            genre_dict = genre.to_dict()
            return make_response(jsonify(genre_dict), 201)
    new_genre = Genre(name=name)
    new_genre.save()
    new_genre_dict = new_genre.to_dict()
    return make_response(jsonify(new_genre_dict), 201)