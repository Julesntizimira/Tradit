from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.book import Book
from models.genre import Genre



book_attr = ['title', 'release_date', 'author_id', 'genre_id', 'user_id', 'description']


@app_views.route('/books', methods=['GET'], strict_slashes=False)
def get_books():
    book_list = []
    for book in storage.all('Book').values():
        book_list.append(book.to_dict())
    return make_response(jsonify(book_list))

@app_views.route('/book/<book_id>', methods=['GET'], strict_slashes=False)
def get_book_by_id(book_id):
    '''get a book by id'''
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        return make_response(jsonify(book_searched.to_dict()), 200)
    
@app_views.route('/book/search/<book_title>', methods=['GET'], strict_slashes=False)
def get_book_searched(book_title):
    '''get a book searched'''
    book_searched = []
    title = book_title.lower()
    for book in storage.all(Book).values():
        for arg in title.split(' '):
            if arg in book.title.lower():
                if book_title not in book_searched:
                    book_searched.append(book.title)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        return make_response(jsonify(book_searched.to_dict()), 200)
    
@app_views.route('/book/title/<book_title>', methods=['GET'], strict_slashes=False)
def get_book_by_title(book_title):
    '''get a book by title'''
    book_searched = storage.get('Book', book_title)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        return make_response(jsonify(book_searched.to_dict()), 200)


@app_views.route('/book', methods=['POST'], strict_slashes=False)
def create_book():
    '''register new book'''
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for att in book_attr:
        if att not in data.keys():
            abort(400, description=f"Missing {att}")
    for key in data.keys():
        if key not in book_attr:
            abort(400, description=f"unknown {key}")
    for book in storage.all(Book).values():
        if book.title.lower() == data.get('title'):
            return make_response(jsonify(book.to_dict()), 200)
    new_book = Book(**data)
    new_book.save()
    return make_response(jsonify(new_book.to_dict()), 201)


@app_views.route('/book/<book_id>', methods=['PUT'], strict_slashes=False)
def update_book(book_id):
    '''update a book'''
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    new_book = storage.get(Book, book_id)
    if new_book is None:
        abort(404, description="Not Found")
    for key in data.keys():
        if key not in book_attr:
            abort(400, description=f"unknown {key}")
    for att, val in data.items():
        if att != 'id':
            setattr(new_book, att, val)
    new_book.save()
    return make_response(jsonify(new_book.to_dict()), 201)


@app_views.route('/book/<book_id>', methods=['DELETE'], strict_slashes=False)
def delete_book_by_id(book_id):
    '''delete a book by id'''
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        storage.delete(book_searched)
        storage.save()
        return make_response(jsonify({}), 200)

@app_views.route('/book/<book_id>/genres', methods=['GET'], strict_slashes=False)
def get_book_genre(book_id):
    '''get book genre'''
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        genre = storage.get(Genre, book_searched.genre_id)
        return make_response(jsonify(genre.to_dict()), 200)
    
@app_views.route('/book/<book_id>/comments', methods=['GET'], strict_slashes=False)
def get_book_comments(book_id):
    '''get book comments'''
    book_searched = storage.get(Book, book_id)
    if book_searched is None:
        abort(404, description="Not found")
    else:
        comments = []
        for comment in book_searched.comments:
            comments.append(comment.to_dict())
        return make_response(jsonify(comments), 200)
