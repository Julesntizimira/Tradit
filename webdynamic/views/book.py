
from webdynamic.views import app_pages
from flask_login import login_required, current_user, logout_user
from models import storage
from models.book import Book
from models.author import Author
from models.comment import Comment
from models.genre import Genre
from flask import render_template, abort, session, url_for, redirect, flash
import requests
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField
from wtforms.validators import input_required, Length, ValidationError, Email
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.file import FileField, FileAllowed
from webdynamic.handleImage import handleImage
from models.user import User
from models.wish import Wish
import json


class CommentForm(FlaskForm):
    text = StringField(validators=[input_required(), Length(max=500)], render_kw={"placeholder":"Type you comment"})
    submit = SubmitField("book")


class BookRegisterForm(FlaskForm):
    title  = StringField(validators=[input_required()], render_kw={"placeholder":"Title"})
    release_date = IntegerField(validators=[input_required()], render_kw={"placeholder":"Release date"})
    author = StringField(validators=[input_required(), Length(max=60)], render_kw={"placeholder":"Author"})
    genre = StringField(validators=[input_required(), Length(max=60)], render_kw={"placeholder":"Genre"})
    description  = StringField(validators=[input_required(), Length(max=500)], render_kw={"placeholder":"Short Description"})
    file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField("Register")

@app_pages.route('/book/<book_id>', methods=['GET', 'POST'])
def book(book_id):
    form = CommentForm()
    book = storage.get(Book, book_id)
    wishes_json = requests.get(f'http://127.0.0.1:5500/api/v1/wishes/users/{book_id}')
    wish_users = wishes_json.json()
    
    offers_json = requests.get(f'http://127.0.0.1:5500/api/v1/offers/users/{book_id}')
    offer_users = offers_json.json()

    authors = storage.all(Author).values()
    for author in authors:
        if author.id == book.author_id:
            authorObj = author
    genres =  storage.all(Genre).values()
    for genre in genres:
        if genre.id == book.genre_id:
            genrename = genre.name
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, user_id=current_user.id, book_id=book_id)
        comment.save()
        return redirect(url_for('app_pages.book', book_id=book_id))
    
    return render_template('book.html', book=book, genre=genrename, current_user=current_user, author=authorObj, form=form, wishes=wish_users, offers=offer_users)


@app_pages.route('/registerbook', methods=['GET', 'POST'])
@login_required
def registerbook():
    form = BookRegisterForm()
    if form.validate_on_submit():
        genre_id = None
        author_id = None

        url = f'http://127.0.0.1:5500/api/v1/author/create/{form.author.data}'
        author_resp = requests.get(url)
        author = author_resp.json()
        author_id = author.get('id')
        
        url = f'http://127.0.0.1:5500/api/v1/genre/create/{form.genre.data}'
        genre_resp = requests.get(url)
        genre = genre_resp.json()
        genre_id = genre.get('id')

        if genre_id and author_id:
            print(genre_id, author_id)
            new_book = Book(title=form.title.data, description=form.description.data, release_date=form.release_date.data, author_id=author_id, genre_id=genre_id, user_id=current_user.id)
            new_book.save()
            file = form.file.data
            handleImage(file, new_book.id)
            return redirect(url_for('app_pages.dashboard'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return render_template('registerbook.html', form=form, )
