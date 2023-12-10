from webdynamic.views import app_pages
from flask_login import login_required, current_user
from models import storage
from models.user import User, Room
from flask import render_template, abort, session, url_for
import requests
from datetime import datetime


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
    user = storage.get(User, user_id)
    if not user:
        abort(400, 'user not found')
    user_room = None
    url = f'http://127.0.0.1:5500/api/v1/room/create'
    data = {'user1_id': user.id, 'user2_id': current_user.id}
    room_resp = requests.post(url, json=data)
    user_room = room_resp.json()

    if not user_room:
        abort(500)
    room_id = user_room.get('id')
    resp = requests.get(f'http://127.0.0.1:5500/api/v1/messages/{room_id}')
    messages = resp.json()

    session["room"] = room_id
    session["name"] = current_user.username
    session["email"] = user.email
    return render_template("room.html", receiver=user.username, name=session.get("name"), code=room_id, messages=messages, current_user=current_user)



