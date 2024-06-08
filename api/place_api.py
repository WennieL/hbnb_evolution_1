#!/usr/bin/python3

from flask import Blueprint, jsonify, request, abort
from datetime import datetime

# Import your models
from models.user import User
from models.review import Review
from models.place import Place
from models.country import Country
from models.city import City
from models.amenity import Amenity

# Import your data (if needed)
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)


place_blueprint = Blueprint('place_api', __name__)