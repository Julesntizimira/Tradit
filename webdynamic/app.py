'''Tradit web flask app Module'''
from flask import Flask, make_response, jsonify, session
from webdynamic.views import app_pages
from flask_login import LoginManager
from models import storage
from models.user import User, Room
from models.message import Message
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room, send, emit
from datetime import datetime, timedelta
from flask_session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)

socketio = SocketIO(app, cors_allowed_origins="*")

@app.after_request
def add_header(response):
    '''Disable caching for all routes'''
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

app.register_blueprint(app_pages)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "app_pages.login"


@login_manager.user_loader
def load_user(user_id):
    '''load user'''
    user = storage.get(User, user_id)
    return user

def get_datetime(item):
    '''get datetime'''
    return datetime.strptime(item["date"], "%H:%M:%S")

def save_message(content):
    '''save message in background'''
    new_message = Message(text=content['message'], name=content['name'], room_id=content['room_id'], date=datetime.strptime(content['date'], "%H:%M:%S"))
    new_message.save()

@socketio.on("message")
def message(data):
    '''emit message'''
    room = session.get("room")
    content = {
        "name": session.get("name"),
        "message": data["data"],
        "date":  datetime.now().strftime("%H:%M:%S"),
        "room_id": room
    }
    socketio.start_background_task(save_message, content)
    emit("message", content, room=room)
    print(f"{session.get('name')} said: {data.get('data')}")

@socketio.on("connect")
def connect(auth):
    '''connect message'''
    room = session.get("room")
    name = session.get("name")
    
    join_room(room)
    send({'msg': 'clean'}, to=room)

    user_room = storage.get(Room, room)
    message_objs = user_room.messages
    messages = []
    for obj in message_objs:
        time = obj.date.strftime("%H:%M:%S")
        messages.append({'name': obj.name, 'message': obj.text, 'date': time})
    sorted_msg = sorted(messages, key=get_datetime)
    for msg in sorted_msg:
        emit("message", msg, room=room) 
    send({"name": name, "message": f"{name} has entered the room"}, to=room)  
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    '''disconnect'''
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

@app.errorhandler(404)
def not_found_error(error):
    '''not found page'''
    return make_response(jsonify({'Error': 'Not found'}), 404)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5200', debug=True,  use_reloader=True)
