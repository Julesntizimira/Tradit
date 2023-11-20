from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.book import Book
from models.genre import Genre

@app_views.route('/books', methods=['GET'], strict_slashes=False)
def get_books():
    book_list = []
    for book in storage.all('Book').values():
        book_list.append(book.to_dict())
    return make_response(jsonify(book_list))

@app_views.route('/books/<book_id>', methods=['GET'], strict_slashes=False)
def get_book_by_id(book_id):
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        return make_response(jsonify(book_searched.to_dict()), 200)


@app_views.route('/books', methods=['POST'], strict_slashes=False)
def create_book():
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    book_attr = ['title', 'release_date', 'author_id', 'genre_id', 'user_id', 'description']
    for att in book_attr:
        if att not in data.keys():
            abort(400, description=f"Missing {att}")
    new_book = Book(**data)
    new_book.save()
    return make_response(jsonify(new_book.to_dict()), 201)


@app_views.route('/books/<book_id>', methods=['PUT'], strict_slashes=False)
def update_book(book_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    new_book = storage.get(Book, book_id)
    if new_book is None:
        abort(404, description="Not Found")
    for att, val in data.items():
        if att != 'id':
            setattr(new_book, att, val)
    new_book.save()
    return make_response(jsonify(new_book.to_dict()), 201)


@app_views.route('/books/<book_id>', methods=['DELETE'], strict_slashes=False)
def delete_book_by_id(book_id):
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        storage.delete(book_searched)
        storage.save()
        return make_response(jsonify({}), 200)

@app_views.route('/books/<book_id>/genres', methods=['GET'], strict_slashes=False)
def get_book_genre(book_id):
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        genre = storage.get(Genre, book_searched.genre_id)
        return make_response(jsonify(genre.to_dict()), 200)
