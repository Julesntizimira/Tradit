from flask import  Flask, render_template, jsonify, make_response
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

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