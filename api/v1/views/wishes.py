'''wishes Api'''
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

@app_views.route('/wishes', methods=['POST'], strict_slashes=False)
def add_to_wishlist():
    ''' add or remove a book from the wish list'''
    data = request.get_json()
    '''if not data or data.get('user_id') or data.get('book_id'):
        abort(404, 'Not a json format')'''
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    wishes = []
    wishList = book.wishes
    for obj in wishList:
        if obj.user_id == user.id:
            wishes.append(obj)
    if wishes:
        for wish in wishes:
            storage.delete(wish)
        return make_response(jsonify(message='Book removed to wishlist'), 201)
    else:
        wish = Wish(user_id=user_id, book_id=book_id)
        wish.save()
        return make_response(jsonify(message='Book added to wishlist'), 201)
    
@app_views.route('/wishes/users/<book_id>', methods=['GET'], strict_slashes=False)
def get_user_who_wish_book(book_id):
    '''get users who wish the book'''
    book = storage.get(Book, book_id)
    if not book:
        abort(404, 'user does not exist')
    wish_list = book.wishes
    wishes = []
    for wish in wish_list:
        user = storage.get(User, wish.user_id)
        wishes.append(user.to_dict())
    return make_response(jsonify(wishes))