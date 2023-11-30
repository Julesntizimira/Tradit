from flask import jsonify, make_response, abort, request, abort
from api.v1.views import app_views
from models import storage
from models.book import Book
from models.offer import Offer
from models.user import User


@app_views.route('/offers', methods=['GET'], strict_slashes=False)
def get_offerlist():
    '''get a offer list'''
    offer_list = []
    offers = storage.session.query(Book).join(Offer).filter(Book.id == Offer.book_id).distinct(Book.id).all()
    for book in offers:
        offer_list.append(book.to_dict())
    return make_response(jsonify(offer_list))

@app_views.route('/offers/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_offers(user_id):
    '''get users offers'''
    user = storage.get(User, user_id)
    if not user:
        abort(404, 'user does not exist')
    offer_list = []
    offers = storage.session.query(Book).join(Offer).filter(Book.id == Offer.book_id).join(User).filter(Offer.user_id == user_id).all()
    for book in offers:
        offer_list.append(book.to_dict())
    return make_response(jsonify(offer_list))

@app_views.route('/offers/<book_id>/<user_id>', methods=['POST'], strict_slashes=False)
def add_to_offerlist(book_id, user_id):
    ''' add a book from the offer list'''
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    offer = Offer(user_id=user_id, book_id=book_id)
    offer.save()
    return make_response(201)

@app_views.route('/offers/<book_id>/<user_id>', methods=['PUT'], strict_slashes=False)
def remove_to_offerlist(book_id, user_id):
    '''remove book from the offer list'''
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    offer = storage.session.query(Offer).join(Book).filter(Book.id == Offer.book_id).Join(User).filter(Offer.user_id == User.id).first()
    if offer:
        storage.delete(offer)
    return make_response(201)
