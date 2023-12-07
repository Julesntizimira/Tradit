
from webdynamic.views import app_pages
from flask_login import login_required, current_user, logout_user
from models import storage
from models.user import User, Room
from flask import render_template, abort, session, url_for, redirect
import requests
from datetime import datetime
from models.genre import Genre
from models.author import Author
import json

@app_pages.route('/dashboard', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def dashboard():
    books_json = requests.get('http://127.0.0.1:5500/api/v1/books')
    books = books_json.json()

    bookList = json.dumps(books)

    wishes_json = requests.get('http://127.0.0.1:5500/api/v1/wishes')
    wishes = wishes_json.json()

    offers_json = requests.get('http://127.0.0.1:5500/api/v1/offers')
    offers = offers_json.json()
    genres = []
    authors = []
    
    genreList = storage.all(Genre).values()
    AuthorList = storage.all(Author).values()
    if genreList:
        for genre in genreList:
            genres.append(genre.to_dict())
    
    if AuthorList:
        for author in AuthorList:
            authors.append(author.to_dict())
    return render_template('dashboard.html', genres=genres, authors=authors, current_user=current_user, books=books, bookList=bookList, wishList=wishes, offerList=offers)

@app_pages.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app_pages.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_pages.login'))
