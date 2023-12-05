from flask import jsonify, make_response, abort, request, abort
from api.v1.views import app_views
from models import storage
from models.message import Message
from models.user import User, Room
from datetime import datetime


def get_datetime(item):
    return datetime.strptime(item["date"], "%H:%M:%S")

@app_views.route('/messages/<room_id>', methods=['GET'], strict_slashes=False)
def get_messages(room_id):
    '''get a message list'''
    room = storage.get(Room, room_id)

    message_objs = room.messages
    messages = []
    for obj in message_objs:
        time = obj.date.strftime("%H:%M:%S")
        messages.append({'name': obj.name, 'message': obj.text, 'date': time})
    sorted_msg = sorted(messages, key=get_datetime)
    return make_response(jsonify(sorted_msg))


@app_views.route('/room/<user1_id>/user2_id>', methods=['GET'], strict_slashes=False)
def create_room(user1_id, user2_id):
    '''create or get a room between two users'''
    user1 = storage.get(User, user1_id)
    user2 = storage.get(User, user2_id)
    if not user1 or not user2:
        abort(400, 'user1 or user2 not found')
    for i in user1.rooms:
        if i in user2.rooms:
            room = i
            break
    if not room:
        room = Room(users=[user1, user2], mmbers=2)
        room.save()
    return make_response(jsonify(room.to_dict()), 201)
