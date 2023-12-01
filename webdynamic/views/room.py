from webdynamic.views import app_pages
from flask_login import login_required, current_user
from models import storage
from models.user import User, Room
from flask import render_template, abort, session, url_for
import requests


@app_pages.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    resp = requests.get('http://127.0.0.1:5500/api/v1/users')
    users = resp.json()
    return render_template('users.html', users=users)


@app_pages.route("/room/<user_id>")
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



