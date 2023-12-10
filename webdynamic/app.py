from flask import Flask, make_response, jsonify, session, send_from_directory
from webdynamic.views import app_pages
from flask_login import LoginManager
from models import storage
from models.user import User
from models.message import Message
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room, send, emit
from datetime import datetime
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
socketio = SocketIO(app, cors_allowed_origins="*")
app.register_blueprint(app_pages)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "app_pages.login"


@login_manager.user_loader
def load_user(user_id):
    url = f'http://127.0.0.1:5500/api/v1/user/{user_id}'
    resp = requests.get(url)
    data = resp.json()
    user = User(**data)
    return user


@socketio.on("message")
def message(data):
    room = session.get("room")
    content = {
        "name": session.get("name"),
        "message": data["data"],
        "date": datetime.now().strftime("%H:%M:%S")
    }
    send(content, to=room)
    url = f'http://127.0.0.1:5500/api/v1/message/create/{room}'
    resp = requests.post(url, json=content)
    if resp.status_code == 201:
        print(f"{session.get('name')} said: {data.get('data')}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    join_room(room)
    '''send({'msg': 'clean'}, to=room)'''
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

@app.errorhandler(404)
def not_found_error(error):
    '''not found page'''
    return make_response(jsonify({'Error': 'Not found'}), 404)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5200', debug=True,  use_reloader=True)
