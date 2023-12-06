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


app_views.route('/author/create/<author_name>', methods=['GET'], strict_slashes=False)
def post_author(author_name):
    '''post author'''
    for author in storage.all(Author).values():
        name = author.name
        if name.lower() == author_name.lower() or name.lower() in author_name.lower() or author_name.lower() in name.lower():
            return make_response(jsonify(author.to_dict()))
    new_author = Author(name=author_name)
    new_author.save()
    return make_response(jsonify(new_author.to_dict()))
