from flask import jsonify, make_response, abort, request, abort
from api.v1.views import app_views
from models import storage
from models.author import Author


app_views.route('/authors', methods=['GET'], strict_slashes=False)
def get_author_list():
    '''get a authors list'''
    authorList = []
    for author in storage.all(Author).values():
        authorList.append(author.to_dict())
    return make_response(jsonify(authorList))

app_views.route('/authors/create', methods=['POST'], strict_slashes=False)
def add_to_author_list():
    '''add to genres list'''
    data = request.json()
    name = data.get('name')
    for author in storage.all(Author).values():
        if author.name.lower() == name.lower():
            author_dict = author.to_dict()
            return make_response(jsonify(author_dict), 201)
    new_author = Author(name=name)
    new_author.save()
    new_author_dict = new_author.to_dict()
    return make_response(jsonify(new_author_dict), 201)