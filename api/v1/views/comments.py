from flask import jsonify, make_response, abort, request, abort
from api.v1.views import app_views
from models import storage
from models.book import Book
from models.comment import Comment
from models.user import User



@app_views.route('/comment', methods=['POST'], strict_slashes=False)
def add_comment():
    ''' add a book from the wish list'''
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('book_id') or not data.get('text'):
        abort(400, 'user, book or text Missing')
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    book = storage.get(Book, book_id)
    if not user:
        abort(404, 'user does not exist')
    if not book:
        abort(404, 'book does not exist')
    text = data.get('text')
    comment = Comment(user_id=user_id, book_id=book_id, text=text)
    comment.save()
    return make_response(201)