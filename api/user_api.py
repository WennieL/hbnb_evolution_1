#!/usr/bin/python3

from flask import Blueprint, jsonify, request, abort
from datetime import datetime

# Import models
from models.user import User
from models.review import Review
from models.place import Place
from models.country import Country
from models.city import City
from models.amenity import Amenity

# Import data
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)

# Define the blueprint for user_api
user_blueprint = Blueprint('user_api', __name__)


@user_blueprint.route('/users', methods=["GET"])
def users_get():
    """returns all Users"""

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
def create_user():
    """ pcreate a new user"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    if not request.json:
        abort(400, "Not a JSON")

    # convert to python dict data type
    data = request.get_json()
    required_fields = ["first_name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        # use User class to create a new object and
        # access method: dict
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    # setdefault("User", []) provides a safety net
    # by initializing "User" if absent
    user_data.setdefault("User", [])
    # add new user data to user_data
    # note that the created_at and updated_at are using timestamps
    # data stored -> server side
    user_data["User"].append({
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at
    })

    # Prepare attributes to return, response to API request -> client side
    attribs = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "created_at": datetime.fromtimestamp(new_user.created_at),
        "updated_at": datetime.fromtimestamp(new_user.updated_at)
    }

    return jsonify(attribs), 201


@user_blueprint.route('/users/<user_id>', methods=["PUT"])
def users_put(user_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # Check if request contains JSON data
    if not request.json:
        abort(400, "Request must contain JSON data")

    # Get JSON data from request
    new_data = request.json

    # Check if user_id exists in user_data
    if user_id not in user_data:
        abort(404, f"User not found for id: {user_id}")

    # Get the user dictionary from user_data
    user = user_data[user_id]

    # Update user's first_name and last_name if provided in JSON data
    if "first_name" in new_data:
        user["first_name"] = new_data["first_name"]
    if "last_name" in new_data:
        user["last_name"] = new_data["last_name"]

    # Update user_data with the modified user
    user_data[user_id] = user

    # Prepare response attributes with updated timestamps as datetime objects
    attribs = {
        "id": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "created_at": datetime.fromtimestamp(user["created_at"]),
        "updated_at": datetime.fromtimestamp(user["updated_at"])
    }

    # Return JSON response with updated user attributes
    return jsonify(attribs), 200


# @user_blueprint.route('/users/<user_id>', methods=["DELETE"])
# def users_delete(user_id):
#     """Deletes an existing user by user_id"""

#     # Check if user_id exists in user_data
#     if user_id not in user_data:
#         abort(404, f"User not found: {user_id}")

#     # Remove user from user_data
#     deleted_user = user_data.pop(user_id)

#     # Prepare response with details of deleted user
#     attribs = {
#         "id": deleted_user["id"],
#         "first_name": deleted_user["first_name"],
#         "last_name": deleted_user["last_name"],
#         "email": deleted_user["email"],
#         "created_at": datetime.fromtimestamp(deleted_user["created_at"]),
#         "updated_at": datetime.fromtimestamp(deleted_user["updated_at"])
#     }

#     # Return JSON response with details of deleted user
#     return jsonify(attribs), 200
