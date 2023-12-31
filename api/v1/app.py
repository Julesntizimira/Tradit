'''hold app to serve Apis'''
from flask import  Flask, jsonify, make_response
from api.v1.views import app_views
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

@app.after_request
def add_header(response):
    # Disable caching for all routes
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(404)
def not_found_error(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5500', debug=True)