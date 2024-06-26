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
from data import FileStorage
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)

# Import utility function
from utils import pretty_json

# Define the blueprint for user_api
user_api = Blueprint('user_api', __name__)


@user_api.route('/users', methods=["GET"])
def users_get():
    """return all Users"""
    users_info = []

    for user_value in user_data.values():
        users_info.append({
            "id": user_value["id"],
            "first_name": user_value['first_name'],
            "last_name": user_value['last_name'],
            "email": user_value['email'],
            "password": user_value['password'],
            "created_at": datetime.fromtimestamp(user_value['created_at']).isoformat(),
            "updated_at": datetime.fromtimestamp(user_value['updated_at']).isoformat()
        })

    return pretty_json(users_info), 200


@user_api.route('/users/<user_id>', methods=["GET"])
def users_specific_get(user_id):
    """returns specified user"""

    for user_value in user_data.values():
        if user_value["id"] == user_id:
            data = user_value
            break
    else:
        abort(404, f"User: {user_id} not found")

    user_info = {
        "id": data["id"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "password": data["password"],
        "created_at": datetime.fromtimestamp(data["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(data["updated_at"]).isoformat()
    }

    return pretty_json(user_info), 200


@user_api.route('/users', methods=["POST"])
def create_new_user():
    """create a new user"""

    if not request.json:
        abort(400, "Request must contain JSON data")

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

    user_data[new_user.id] = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "password": new_user.password,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at
    }

    try:
        FileStorage.save_model_data("user_data.json", user_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "created_at": datetime.fromtimestamp(new_user.created_at).isoformat(),
        "updated_at": datetime.fromtimestamp(new_user.updated_at).isoformat()
    }

    # Use 201 Created status for successful creation
    return pretty_json(attribs), 201


@user_api.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """ updates existing user data using specified id """

    # Check if request contains JSON data
    if not request.json:
        abort(400, "Request must contain JSON data")

    # Get JSON data from request
    new_data = request.get_json()

    for user_value in user_data.values():
        # for user_value in user_data.get("User", []):
        if user_value["id"] == user_id:
            found_user_data = user_value
            break
    else:
        abort(404, f"User ID not found: {user_id}")

    # Update user's first_name and last_name if provided in JSON data
    if "first_name" in new_data:
        found_user_data["first_name"] = new_data["first_name"]
    if "last_name" in new_data:
        found_user_data["last_name"] = new_data["last_name"]

    try:
        FileStorage.save_model_data("user_data.json", user_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": found_user_data["id"],
        "first_name": found_user_data["first_name"],
        "last_name": found_user_data["last_name"],
        "email": found_user_data["email"],
        "created_at": datetime.fromtimestamp(found_user_data["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(found_user_data["updated_at"]).isoformat()
    }

    # Return JSON response with updated user attributes
    return pretty_json(attribs), 200


@user_api.route('/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    """Deletes an existing user by user_id"""

    keys_to_delete = []

    for user_key, user_value in list(user_data.items()):
        if user_value["id"] == user_id:
            keys_to_delete.append(user_key)

    if not keys_to_delete:
        abort(404, f"User not found with ID: {user_id}")

    for user_key in keys_to_delete:
        del user_data[user_key]

    try:
        FileStorage.save_model_data("user_data.json", user_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    return pretty_json({"message": f"User {user_id} has been deleted."}), 204
