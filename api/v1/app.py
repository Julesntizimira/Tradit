from flask import Flask, render_template, make_response, jsonify, url_for, redirect, session, abort, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import input_required, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models.user import User, Room
from models.book import Book
from models.author import Author
from models.genre import Genre
from models.wish import Wish
from models.comment import Comment
from models.offer import Offer
from models.message import Message
from models import storage
import json

from flask_socketio import join_room, leave_room, send, SocketIO, emit
import random
from string import ascii_uppercase

from api.v1.handleImage import handleImage


from api.v1.views import app_views

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SESSION_PROTECTION'] = 'strong'

socketio = SocketIO(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return storage.session.query(User).get(user_id)





    

class RegisterForm(FlaskForm):
    name = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Name"})
    address = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Address"})
    username = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    email = EmailField(validators=[input_required(), Email(message="Invalid email address")], render_kw={"placeholder":"Email"})
    password = PasswordField(validators=[input_required(), Length(min=4, max=20), ], render_kw={"placeholder":"Password"})
    file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = storage.session.query(User).filter(User.username == username.data).first()
        if existing_user_username:
            raise ValidationError("that username already exists please choose a different one" )

class LoginForm(FlaskForm):
    username = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
    remember = BooleanField("Remember Me")

class CommentForm(FlaskForm):
    text = StringField(validators=[input_required(), Length(max=500)], render_kw={"placeholder":"Type you comment"})
    submit = SubmitField("book")


class BookRegisterForm(FlaskForm):
    title  = StringField(validators=[input_required()], render_kw={"placeholder":"Title"})
    release_date = IntegerField(validators=[input_required()], render_kw={"placeholder":"Release date"})
    author = StringField(validators=[input_required(), Length(max=60)], render_kw={"placeholder":"Author"})
    genre = StringField(validators=[input_required(), Length(max=60)], render_kw={"placeholder":"Genre"})
    description  = StringField(validators=[input_required(), Length(max=500)], render_kw={"placeholder":"Short Description"})
    
  
    submit = SubmitField("Register")

    def validate_username(self, title):
        existing_user_username = storage.session.query(Book).filter(Book.title == title.data).first()
        if existing_user_username:
            raise ValidationError("that title already exists please choose a different one" )


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

def getBooks():
    books = []
    for book in storage.all(Book).values():
        books.append(book.to_dict())
    return json.dumps(books)

def getWishList():
    wishList = []
    for book in storage.session.query(Book).join(Wish).filter(Book.id == Wish.book_id).distinct(Book.id).all():
        wishList.append(book.to_dict())
    return json.dumps(wishList)

def getOfferList():
    OfferList = []
    for book in storage.session.query(Book).join(Offer).filter(Book.id == Offer.book_id).distinct(Book.id).all():
        OfferList.append(book.to_dict())
    return json.dumps(OfferList)


@app.route('/')
def landing():
    return render_template('landing1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    books = getBooks()
    wishList = getWishList()
    offerList = getOfferList()
    
    return render_template('dashboard.html', current_user=current_user, books=books, wishList=wishList, offerList=offerList)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book(book_id):
    form = CommentForm()
    book = storage.get(Book, book_id)
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
        return redirect(url_for('book', book_id=book_id))
    return render_template('book.html', book=book, genre=genrename, author=authorObj)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        file = form.file.data
        handleImage(file, form.name.data, 'profiles')
        new_user = User(username=form.username.data, password=hashed_password,  name=form.name.data, email=form.email.data, address=form.address.data)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/registerbook', methods=['GET', 'POST'])
@login_required
def registerBook():
    form = BookRegisterForm()
    if form.validate_on_submit():
        author_id = ""
        for obj in storage.session.query(Author).all():
            if form.author.data == obj.name or form.author.data in obj.name:
                author_id = obj.id
                break
        if author_id == "":
            new_author = Author(name=form.author.data)
            new_author.save()
            author_id = new_author.id

        genre_id = ""
        for obj in storage.session.query(Genre).all():
            if form.genre.data == obj.name or form.genre.data in obj.name:
                genre_id = obj.id
                break
        if genre_id == "":
            new_genre = Genre(name=form.genre.data)
            new_genre.save()
            genre_id = new_genre.id
        new_book = Book(title=form.title.data, description=form.description.data, release_date=form.release_date.data, author_id=author_id, genre_id=genre_id, user_id=current_user.id)
        new_book.save()
        return redirect(url_for('dashboard'))
    return render_template('registerbook.html', form=form)

@app.route('/item', methods=['GET', 'POST'])
@login_required
def itemInfos():
    return render_template('item.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    users = []
    for user in storage.session.query(User).all():
        if user.id != current_user.id:
            users.append(user)
    return render_template('users.html', users=users)


@app.route("/room/<user_id>")
@login_required
def room(user_id):
    user = storage.get(User, user_id)
    rooms = current_user.rooms
    
    user_room = None
    if rooms:
        for room in rooms:
            if room.users and user in room.users:
                user_room = room
                break

    if not user_room:
        user_room = Room(users=[current_user, user], members=2)
        user_room.save()

    if not user_room:
        abort(500)

    message_objs = user_room.messages
    messages = []
    for obj in message_objs:
        messages.append({'name': obj.name, 'message': obj.text})
    
    session["room"] = user_room.id
    session["name"] = current_user.username
    session['messages'] = messages
    return render_template("room.html", receiver=user.username, name=session.get("name"), code=user_room.id, messages=session.get('messages'))

@socketio.on("message")
def message(data):
    room = session.get("room")
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    session.get('messages').append(content)
    send(content, to=room)
    content['room_id'] = room
    content['text'] = content['message']
    del(content['message'])
    new_message = Message(**content)
    new_message.save()
    print(f"{session.get('name')} said: {data['data']}")




@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    join_room(room)
    send({'msg': 'clean'}, to=room)
    
    for msg in session.get('messages'):
        send(msg, to=room)
    send({"name": name, "message": f"{name} has entered the room"}, to=room)    
    
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    the_room = storage.get('Room', room)
    if the_room is not None:
        the_room.members -= 1
        if the_room.members <= 0:
            storage.delete(the_room)
            storage.save()
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")





if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5500', debug=True)