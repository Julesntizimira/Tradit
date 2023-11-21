from flask import Flask, render_template, make_response, jsonify, url_for, redirect, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField
from wtforms.validators import input_required, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models.user import User
from models.book import Book
from models.author import Author
from models.genre import Genre
from models import storage

from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase




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

class BookRegisterForm(FlaskForm):
    title  = StringField(validators=[input_required()], render_kw={"placeholder":"Title"})
    release_date = IntegerField(validators=[input_required()], render_kw={"placeholder":"Release date"})
    author = StringField(validators=[input_required(), Length(max=60)], render_kw={"placeholder":"Author"})
    genre = StringField(validators=[input_required(), Length(max=60)], render_kw={"placeholder":"Genre"})
    description  = StringField(validators=[input_required(), Length(max=500)], render_kw={"placeholder":"Short Description"})
    
  
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = storage.session.query(User).filter(User.username == username.data).first()
        if existing_user_username:
            raise ValidationError("that username already exists please choose a different one" )


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

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
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
        new_book = Book(title=form.title.data, release_date=form.release_date.data, author_id=author_id, genre_id=genre_id, user_id=current_user.id)
        new_book.save()
        return redirect(url_for('/itemInfos'))
    return render_template('registerbook.html', form=form)

@app.route('/item', methods=['GET', 'POST'])
@login_required
def itemInfos():
    return render_template('item.html')




rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/home", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")





if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5500', debug=True)