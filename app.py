#!/usr/bin/python3

from datetime import datetime
from flask import Flask, jsonify, request, abort

# Import models
from models.amenity import Amenity
from models.city import City
from models.country import Country
from models.place import Place
from models.review import Review
from models.user import User

# Import blueprints
from api.user_api import user_api
from api.country_api import country_api
from api.city_api import city_api
from api.amenity_api import amenity_api
from api.place_api import place_api
from api.review_api import review_api

# Import data
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)

# Initialize Flask app
app = Flask(__name__)


# Register blueprints - updated to unique prefixes
app.register_blueprint(user_api, url_prefix='/api/v1')
app.register_blueprint(country_api, url_prefix='/api/v1')
app.register_blueprint(city_api, url_prefix='/api/v1')
app.register_blueprint(amenity_api, url_prefix='/api/v1')
app.register_blueprint(place_api, url_prefix='/api/v1')
app.register_blueprint(review_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    """ Hello world """
    return 'Hello World'


@app.route('/', methods=["POST"])
def hello_world_post():
    """ Hello world endpoint for POST requests """
    # curl -X POST localhost:5000/
    return "hello world\n"


# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
