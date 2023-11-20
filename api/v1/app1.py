#!/usr/bin/python3
from models.user import User
from models.book import Book
from models.comment import Comment
from flask import Flask, request
import json


app = Flask(__name__)

@app.route("/")
def all_data():
    from models import storage
    all_dict = []
    for val in storage.all():
        com_dict = {
                'comment': val[0].text,
                'user': val[1].name,
                'book': val[2].name
                }
        all_dict.append(com_dict)
    return json.dumps(all_dict, indent=4)


@app.route("/books")
def books():
    from models import storage
    all_books = []
    for val in storage.all(Book):
        comment_list = []
        for comment in val.get_comments():
            comment_list.append(comment.text)
        book_dict = {
                'id': val.id,
                'description': val.description, 
                'name': val.name,
                'comments': comment_list

                }
        all_books.append(book_dict)
    return json.dumps(all_books, indent=4)


@app.route("/books/<int:n>")
def books_by_number(n):
    from models import storage
    n = int(n)
    allbooks = storage.all(Book)
    if n > len(allbooks):
        return {}
    mybook = allbooks[n]
    comment_list = []
    for comment in mybook.get_comments():
        comment_list.append(comment.text)
    book_dict = {
            'id': mybook.id,
            'description': mybook.description,
            'name': mybook.name,
            'comments': comment_list
            }
    return json.dumps(book_dict, indent=4)


@app.route("/books/", methods=['POST'])
def books_post():
    book_added = Book(request.form['title'], request.form['description'], request.form['release_date'], request.form['author_id'], request.form['genre_id'], request.form['user_id'])
    book_added.save()
    return json.dumps({'message': f"{book_added.title} is successifully added"}, indent=4)


if __name__ == "__main__":
    app.run(debug=True)
