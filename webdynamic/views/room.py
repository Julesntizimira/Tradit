from webdynamic.views import app_pages
from flask_login import login_required, current_user
from models import storage
from models.user import User, Room
from models.message import Message
from flask import render_template, abort, session, url_for, redirect
import requests
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField
from wtforms.validators import input_required, Length, ValidationError, Email
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.file import FileField, FileAllowed

class MessageForm(FlaskForm):
    text = StringField(validators=[input_required(), Length(max=1000)], render_kw={"placeholder":"Type you message"})
    submit = SubmitField("room")

@app_pages.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def users():
    users = []
    users_resp = requests.get(f'http://127.0.0.1:5500/api/v1/users')
    userList = users_resp.json()
    for user in userList:
        if user['id'] != current_user.id:
            users.append(user)
    every_room_last_message = []
    current_user_id = current_user.id
    resp = requests.get(f'http://127.0.0.1:5500/api/v1/rooms/user/{current_user_id}')
    every_room_last_message = resp.json()

    return render_template('users.html', users=users, current_user=current_user, rooms_updates=every_room_last_message)

def get_datetime(item):
    return datetime.strptime(item["date"], "%H:%M:%S")

@app_pages.route("/room/<user_id>",  methods=['GET', 'POST'], strict_slashes=False)
@login_required
def room(user_id):
    form = MessageForm()
    user = storage.get(User, user_id)
    if not user:
        abort(400, 'user not found')

    room = storage.session.query(Room).\
    filter(Room.users.any(User.id == user_id)).\
    filter(Room.users.any(User.id == current_user.id)).\
    first()
    if not room:
        room = Room(users=[user, current_user], members=2)
        room.save()
    room_id = room.id

    message_objs = room.messages
    messages = []
    for obj in message_objs:
        time = obj.date.strftime("%H:%M:%S")
        messages.append({'name': obj.name, 'message': obj.text, 'date': time})
    sorted_msg = sorted(messages, key=get_datetime)

    if form.validate_on_submit():
        date_time = datetime.now()
        new_message = Message(text=form.text.data, room_id=room_id, name=current_user.username, date=date_time)
        new_message.save()
        return redirect(url_for('app_pages.room', user_id=user_id))
    return render_template("room.html", form=form, receiver=user.username, messages=sorted_msg, name=current_user.username, code=room_id, current_user=current_user)