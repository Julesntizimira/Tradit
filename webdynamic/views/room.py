'''room view'''
from webdynamic.views import app_pages
from flask_login import login_required, current_user
from models import storage
from models.user import User, Room
from flask import render_template, abort, session, url_for, jsonify
from datetime import datetime


@app_pages.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def users():
    '''user'''
    users = []
    for user in storage.all(User).values():
        if user.id != current_user.id:
            users.append(user.to_dict())
    msg_list = []
    for room in current_user.rooms:
        message_objs = room.messages
        messages = []
        for obj in message_objs:
            receiver_id = None
            id = None
            if obj.name == current_user.username:
                for other_user in room.users:
                    if other_user.id != current_user.id:
                        receiver_id = other_user.id
                        break
            time = obj.date.strftime("%H:%M:%S")
            for user_obj in storage.all(User).values():
                if user_obj.username == obj.name:
                    id = user_obj.id
                    break
            messages.append({'name': obj.name, 'message': obj.text, 'date': time, 'user_id': id, 'receiver_id': receiver_id})
        sorted_msg = sorted(messages, key=get_datetime)
        if sorted_msg:
            msg_list.append(sorted_msg[-1])
    ordered_msg = sorted(msg_list, key=get_datetime, reverse=True)
    return render_template('users.html', users=users, current_user=current_user, rooms_updates=ordered_msg)

def get_datetime(item):
    return datetime.strptime(item["date"], "%H:%M:%S")

@app_pages.route("/room/<user_id>",  methods=['GET', 'POST'], strict_slashes=False)
@login_required
def room(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(400, 'user not found')

    room = None
    room = storage.session.query(Room).\
    filter(Room.users.any(User.id == user.id)).\
    filter(Room.users.any(User.id == current_user.id)).\
    first()

    if not room:
        room = Room(users=[user, current_user], members=2)
        room.save()
    if not room:
        abort(500)
    room_id = room.id

    session["room"] = room_id
    session["name"] = current_user.username
    session["email"] = user.email
    return render_template("room.html", receiver=user.username, name=session.get("name"), code=room_id, current_user=current_user)



