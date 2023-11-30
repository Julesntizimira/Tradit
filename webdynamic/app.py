from flask import Flask, make_response, jsonify
from webdynamic.views import app_pages
from flask_login import LoginManager
from models import storage
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.register_blueprint(app_pages)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)


@app.errorhandler(404)
def not_found_error(error):
    '''not found page'''
    return make_response(jsonify({'Error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5200', debug=True)