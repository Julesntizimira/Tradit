'''room and message Api'''
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
    '''post message Api'''
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
        return make_response(jsonify({'status': 'stored'}), 201)
    else:
        abort(404, 'room not found')

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

    # Use session query to filter rooms based on user ids
    room = storage.session.query(Room).\
        filter(Room.users.any(User.id == user1_id)).\
        filter(Room.users.any(User.id == user2_id)).\
        first()

    if not room:
        room = Room(users=[user1, user2], members=2)
        room.save()

    return make_response(jsonify(room.to_dict()), 201)

@app_views.route('rooms/user/<user_id>', methods=['GET'], strict_slashes=False)
def get_last_message_of_every_room(user_id):
    '''get a last message of every room'''
    user = storage.get(User, user_id)
    msg_list = []
    if not user:
        abort(404, 'user not found')
    else:
        for room in user.rooms:
            message_objs = room.messages
            messages = []
            for obj in message_objs:
                receiver_id = None
                id = None
                if obj.name == user.username:
                    for other_user in room.users:
                        if other_user.id != user.id:
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
        return make_response(jsonify(ordered_msg), 200)
