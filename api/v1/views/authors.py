from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.author import Author



@app_views.route('/authors', methods=['GET'], strict_slashes=False)
def get_authors():
    ''' get all genres present in storage'''
    authorList = []
    for author in storage.all(Author).values():
        authorList.append(author.to_dict())
    return make_response(jsonify(authorList))

@app_views.route('/author/<author_id>', methods=['GET'], strict_slashes=False)
def get_author(author_id):
    ''' get author by id'''
    author = storage.get(Author, author_id)
    if author:
        return make_response(jsonify(author.to_dict()), 201)
    return make_response(jsonify({}), 200)

@app_views.route('/author/new/<name>', methods=['POST'], strict_slashes=False)
def add_to_authors(name):
    '''add to authors'''
    for author in storage.all(Author).values():
        if author.name.lower() == name.lower():
            return make_response(jsonify(author.to_dict()), 200)
    new_author = Author(name=name)
    new_author.save()
    return make_response(jsonify(new_author.to_dict()), 201)



