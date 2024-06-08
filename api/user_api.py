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

# Define the blueprint for user_api
user_blueprint = Blueprint('user_api', __name__)


@user_blueprint.route('/users', methods=["GET"])
def users_get():
    """returns all Users"""
    if not user_data:
        abort(404, description="No user exist")

    users_info = []
    for user_key, user in user_data.items():
        users_info.append({
            "id": user['id'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
            "password": user['password'],
            "created_at": datetime.fromtimestamp(user['created_at']),
            "updated_at": datetime.fromtimestamp(user['updated_at'])
        })

    return jsonify(users_info)


@user_blueprint.route('/users/<user_id>', methods=["GET"])
def users_specific_get(user_id):
    """returns specified user"""
    user = user_data.get(user_id)
    if not user:
        abort(404, description="User not found")

    user_info = {
        "id": user['id'],
        "first_name": user['first_name'],
        "last_name": user['last_name'],
        "email": user['email'],
        "password": user['password'],
        "created_at": datetime.fromtimestamp(user['created_at']),
        "updated_at": datetime.fromtimestamp(user['updated_at'])
    }

    return jsonify(user_info)


@user_blueprint.route('/users', methods=["POST"])
def users_post():
    """ posts data for new user then returns the user data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # print(request.content_type)

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    try:
        u = User(first_name=data["first_name"], last_name=data["last_name"],
                 email=data["email"], password=data["password"])
    except ValueError as exc:
        return repr(exc) + "\n"

    # add new user data to user_data
    # note that the created_at and updated_at are using timestamps
    user_data[u.id] = {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "created_at": u.created_at,
        "updated_at": u.updated_at
    }

    # note that the created_at and updated_at are using readable datetimes
    attribs = {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "created_at": datetime.fromtimestamp(u.created_at),
        "updated_at": datetime.fromtimestamp(u.updated_at)
    }

    return jsonify(attribs)


@user_blueprint.route('/users/<user_id>', methods=["PUT"])
def users_put(user_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()

    if user_id not in user_data:
        abort(400, "User not found for id {}".format(user_id))

    u = user_data[user_id]

    # modify the values
    for k, v in data.items():
        # only first_name and last_name are allowed to be modified
        if k in ["first_name", "last_name"]:
            u[k] = v

    # update user_data with the new name - print user_data out to confirm it if you want
    user_data[user_id] = u

    attribs = {
        "id": u["id"],
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"],
        "created_at": datetime.fromtimestamp(u["created_at"]),
        "updated_at": datetime.fromtimestamp(u["updated_at"])
    }

    # print out the updated user details
    return jsonify(attribs)
