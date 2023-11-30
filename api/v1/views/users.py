from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User



user_attr = ['name', 'username', 'email', 'password', 'address']


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_Users():
    '''get user list'''
    user_list = []
    for user in storage.all('User').values():
        user_list.append(user.to_dict())
    return make_response(jsonify(user_list))

@app_views.route('/user/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    '''get user by id'''
    user_searched = storage.get(User, user_id)
    if user_searched is None:
        abort(404, description="Not found")
    else:
        return make_response(jsonify(user_searched.to_dict()), 200)
    
@app_views.route('/user/username/<username>', methods=['GET'], strict_slashes=False)
def get_user_by_username(username):
    '''get user by username'''
    for user in storage.all(User).values():
        if user.username == username:
            user_searched = user
            break
    if user_searched is None:
        abort(404, description="Not found")
    else:
        return make_response(jsonify(user_searched.to_dict()), 200)


@app_views.route('/user', methods=['POST'], strict_slashes=False)
def create_user():
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for att in user_attr:
        if att not in data.keys():
            abort(400, description=f"Missing {att}")
    for key in data.keys():
        if key not in user_attr:
            abort(400, description=f"unknown {key}")
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/user/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_infos(user_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    new_user = storage.get(User, user_id)
    if new_user is None:
        abort(404, description="Not Found")
    for key in data.keys():
        if key not in user_attr:
            abort(400, description=f"unknown {key}")
    for att, val in data.items():
        if att != 'id':
            setattr(new_user, att, val)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/user/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user_searched = storage.get(User, user_id)
    if user_searched is None:
        abort(404, description="Not found")
    else:
        storage.delete(user_searched)
        storage.save()
        return make_response(jsonify({}), 200)

@app_views.route('/user/<user_id>/rooms', methods=['GET'], strict_slashes=False)
def get_user_rooms(user_id):
    '''get user rooms'''
    user_searched = storage.get(User, user_id)
    if user_searched is None:
        abort(404, description="Not found")
    room_list = []
    for room in user_searched.rooms:
        room_list.append(room.to_dict())
    return make_response(jsonify(room_list))