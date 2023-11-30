from flask import jsonify, make_response, abort, request, abort
from api.v1.views import app_views
from models import storage
from models.book import Book
from models.wish import Wish
from models.user import User


@app_views.route('/wishes', methods=['GET'], strict_slashes=False)
def get_wishlist():
    '''get a wish list'''
    wish_list = []
    wishes = storage.session.query(Book).join(Wish).filter(Book.id == Wish.book_id).distinct(Book.id).all()
    for book in wishes:
        wish_list.append(book.to_dict())
    return make_response(jsonify(wish_list))

@app_views.route('/wishes/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_wishes(user_id):
    '''get users wishes'''
    user = storage.get(User, user_id)
    if not user:
        abort(404, 'user does not exist')
    wish_list = []
    wishes = storage.session.query(Book).join(Wish).filter(Book.id == Wish.book_id).join(User).filter(Wish.user_id == user_id).all()
    for book in wishes:
        wish_list.append(book.to_dict())
    return make_response(jsonify(wish_list))

@app_views.route('/wishes/<book_id>/<user_id>', methods=['POST'], strict_slashes=False)
def add_to_wishlist(book_id, user_id):
    ''' add a book from the wish list'''
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    wish = Wish(user_id=user_id, book_id=book_id)
    wish.save()
    return make_response(201)

@app_views.route('/wishes/<book_id>/<user_id>', methods=['PUT'], strict_slashes=False)
def remove_to_wishlist(book_id, user_id):
    '''remove book from the wish list'''
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    wish = storage.session.query(Wish).join(Book).filter(Book.id == Wish.book_id).Join(User).filter(Wish.user_id == User.id).first()
    if wish:
        storage.delete(wish)
    return make_response(201)
