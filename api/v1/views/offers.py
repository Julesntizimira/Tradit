'''offers Api'''
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

@app_views.route('/offers', methods=['POST'], strict_slashes=False)
def add_to_offerlist():
    ''' add or remove a book from the offer list'''
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    offers = []
    offerList = book.offers
    for obj in offerList:
        if obj.user_id == user.id:
            offers.append(obj)
    if offers:
        for offer in offers:
            storage.delete(offer)
        return make_response(jsonify(message='Book removed to offerlist'), 201)
    else:
        offer = Offer(user_id=user_id, book_id=book_id)
        offer.save()
        return make_response(jsonify(message='Book removed to offerlist'),201)
    
@app_views.route('/offers/users/<book_id>', methods=['GET'], strict_slashes=False)
def get_user_who_offer_book(book_id):
    '''get users who are offering the book'''
    book = storage.get(Book, book_id)
    if not book:
        abort(404, 'user does not exist')
    offer_list = book.offers
    offers = []
    for offer in offer_list:
        user = storage.get(User, offer.user_id)
        offers.append(user.to_dict())
    return make_response(jsonify(offers))
