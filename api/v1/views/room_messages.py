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

@app_views.route('/message/create/<room_id>', methods=['POST'], strict_slashes=False)
def post_message_to_room(room_id):
    room = storage.get(Room, room_id)
    if room:
        content = request.get_json()
        date_time = datetime.strptime(content["date"], "%H:%M:%S")
        content['room_id'] = room_id
        content['text'] = content.get('message')
        content['date'] = date_time
        del(content['message'])
        new_message = Message(**content)
        new_message.save()
        storage.save()
        return make_response(jsonify({'status': 'stored'}), 201)

@app_views.route('/room/create', methods=['POST'], strict_slashes=False)
def create_room():
    '''create or get a room between two users'''
    data = request.get_json()
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')
    user1 = storage.get(User, user1_id)
    user2 = storage.get(User, user2_id)
    if not user1 or not user2:
        abort(400, 'user1 or user2 not found')
    room = None
    for i in user1.rooms:
        if i in user2.rooms:
            room = i
    if not room:
        room = Room(users=[user1, user2], members=2)
        room.save()
    return make_response(jsonify(room.to_dict()), 201)
