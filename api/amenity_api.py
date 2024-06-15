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


amenity_api = Blueprint('amenity_api', __name__)


@amenity_api.route('/amenities', methods=["GET"])
def amenities_get():
    """return all amenities"""
    amenities_info = []

    for amenity_value in amenity_data.values():
        amenity_id = amenity_value["id"]
        amenities_info.append({
            "id": amenity_id,
            "name": amenity_value['name'],
            "created_at": datetime.fromtimestamp(amenity_value['created_at']),
            "updated_at": datetime.fromtimestamp(amenity_value['updated_at'])
        })

    return jsonify(amenities_info), 200


@amenity_api.route('/amenities/<amenity_id>', methods=["GET"])
def amenity_specific_get(amenity_id):
    """returns specified amenity"""

    for amenity_value in amenity_data.values():
        if amenity_value["id"] == amenity_id:
            data = amenity_value
            break
    else:
        abort(404, f"Amenity: {amenity_id} not found")

    amenity_info = {
        "id": amenity_id,
        "name": data['name'],
        "created_at": datetime.fromtimestamp(amenity_value['created_at']),
        "updated_at": datetime.fromtimestamp(amenity_value['updated_at'])
    }

    return jsonify(amenity_info), 200


@amenity_api.route('/amenities', methods=["POST"])
def create_new_amenity():
    """create a new amenity"""

    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()

    required_fields = ["name"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        new_amenity = Amenity(name=data["name"])
    except ValueError as exc:
        abort(400, repr(exc))

    if "Amenity" not in amenity_data:
        amenity_data["Amenity"] = []

    amenity_data["Amenity"].append({
        "id": new_amenity.id,
        "name": new_amenity.name,
        "created_at": new_amenity.created_at,
        "updated_at": new_amenity.updated_at
    })

    attribs = {
        "id": new_amenity.id,
        "name": new_amenity.name,
        "created_at": datetime.fromtimestamp(new_amenity.created_at),
        "updated_at": datetime.fromtimestamp(new_amenity.updated_at)
    }
    return jsonify(attribs), 200


@amenity_api.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):
    """ updates existing amenity data using specified id """

    if not request.json:
        abort(400, "Request must contain JSON data")

    update_data = request.get_json()

    for amenity_value in amenity_data.values():
        if amenity_value["id"] == amenity_id:
            found_amenity_data = amenity_value
            break
    else:
        abort(404, f"Amenity ID not found: {amenity_id}")

    if "name" in update_data:
        found_amenity_data["name"] = update_data["name"]

    amenity_data[amenity_id] = found_amenity_data

    attribs = {
        "id": found_amenity_data["id"],
        "name": found_amenity_data["name"],
        "created_at": datetime.fromtimestamp(found_amenity_data["created_at"]),
        "updated_at": datetime.fromtimestamp(found_amenity_data["updated_at"])
    }

    return jsonify(attribs), 200


@amenity_api.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an existing amenity by amenity_id"""

    keys_to_delete = []

    for amenity_key, amenity_value in list(amenity_data.items()):
        if amenity_value["id"] == amenity_id:
            keys_to_delete.append(amenity_key)

    if not keys_to_delete:
        abort(404, f"Amenity not found with ID: {amenity_id}")

    for amenity_key in keys_to_delete:
        del amenity_data[amenity_key]

    # Return a confirmation message
    return jsonify({"message": f"Amenity {amenity_id} has been deleted."}), 204
