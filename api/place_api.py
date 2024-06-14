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


place_api = Blueprint('place_api', __name__)


@place_api.route('/example/places_amenties_raw')
def example_places_amenities_raw():
    """ Prints out the raw data for relationships between places and their amenities """
    return jsonify(place_to_amenity_data)


@place_api.route('/places_amenties', methods=["GET"])
def places_amenties():
    """ Prints out the relationships between places and their amenities using names """

    output = {}

    for place_key in place_to_amenity_data:
        place_name = place_data[place_key]['name']
        if place_name not in output:
            output[place_name] = []

        amenities_ids = place_to_amenity_data[place_key]
        for amenity_key in amenities_ids:
            amenity_name = amenity_data[amenity_key]['name']
            output[place_name].append(amenity_name)

    return jsonify(output)

# Q: how to make it unsorted?


@place_api.route('/places', methods=["GET"])
def place_amenties():
    """get all places data"""

    places_info = []

    for place_value in place_data.values():
        places_info.append({
            "id": place_value["id"],
            "host_user_id": place_value["host_user_id"],
            "city_id": place_value["city_id"],
            "name": place_value["name"],
            "description": place_value["description"],
            "address": place_value["address"],
            "latitude": place_value["latitude"],
            "longitude": place_value["longitude"],
            "number_of_rooms": place_value["number_of_rooms"],
            "bathrooms": place_value["bathrooms"],
            "price_per_night": place_value["price_per_night"],
            "max_guests": place_value["max_guests"],
            "created_at": datetime.fromtimestamp(place_value["created_at"]),
            "updated_at": datetime.fromtimestamp(place_value["updated_at"])
        })

    return jsonify(places_info), 200


@place_api.route('/places/<place_id>', methods=["GET"])
def place_info(place_id):
    """get sepecific info of a place"""
    for place_value in place_data.values():
        if place_value["id"] == place_id:
            found_place = place_value
            break
    else:
        abort(404, f"Place: {place_id} not found")

    place_info = {
        "id": found_place["id"],
        "host_user_id": found_place["host_user_id"],
        "city_id": found_place["city_id"],
        "name": found_place["name"],
        "description": found_place["description"],
        "address": found_place["address"],
        "latitude": found_place["latitude"],
        "longitude": found_place["longitude"],
        "number_of_rooms": found_place["number_of_rooms"],
        "bathrooms": found_place["bathrooms"],
        "price_per_night": found_place["price_per_night"],
        "max_guests": found_place["max_guests"],
        "created_at": datetime.fromtimestamp(found_place["created_at"]),
        "updated_at": datetime.fromtimestamp(found_place["updated_at"])
    }

    return jsonify(place_info), 200


@place_api.route('/places', methods=["POST"])
def create_place_info():
    """create a new place"""
    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()

    required_fields = ["name", "description", "address", "latitude", "longitude",
                       "number_of_rooms", "bathrooms", "price_per_night", "max_guests"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        new_place = Place(
            name=data["name"],
            description=data["description"],
            address=data["address"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            number_of_rooms=data["number_of_rooms"],
            bathrooms=data["bathrooms"],
            price_per_night=data["price_per_night"],
            max_guests=data["max_guests"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    if "Place" not in place_data:
        place_data["Place"] = []

    place_data["Place"].append({
        "id": new_place.id,
        "host_user_id": new_place.host_user_id,
        "city_id": new_place.city_id,
        "name": new_place.name,
        "description": new_place.description,
        "address": new_place.address,
        "latitude": new_place.latitude,
        "longitude": new_place.longitude,
        "number_of_rooms": new_place.number_of_rooms,
        "bathrooms": new_place.bathrooms,
        "price_per_night": new_place.price_per_night,
        "max_guests": new_place.max_guests,
        "created_at": new_place.created_at,
        "updated_at": new_place.updated_at
    })

    attribs = {
        "id": new_place.id,
        "host_user_id": new_place.host_user_id,
        "city_id": new_place.city_id,
        "name": new_place.name,
        "description": new_place.description,
        "address": new_place.address,
        "latitude": new_place.latitude,
        "longitude": new_place.longitude,
        "number_of_rooms": new_place.number_of_rooms,
        "bathrooms": new_place.bathrooms,
        "price_per_night": new_place.price_per_night,
        "max_guests": new_place.max_guests,
        "created_at": datetime.fromtimestamp(new_place.created_at),
        "updated_at": datetime.fromtimestamp(new_place.updated_at)
    }

    return jsonify(attribs), 200


@place_api.route('/places/<place_id>', methods=["PUT"])
def update_place_info(place_id):
    """update info of a place"""
    pass


@place_api.route('/places/<place_id>', methods=["DELETE"])
def delete_place_info(place_id):
    """dekete a place"""
    pass

# @place_api.route('/place/<city_id>', methods=["GET"])
# def places_in_a_specific_country(city_id):
#     """places within the countries"""
#     pass


# @place_api.route('/place/<host_user_id>', methods=["GET"])
# def place_owned_by_user(host_user_id):
#     """places are owned by which users"""


# @place_api.route('/place/<place_id>', methods=["GET"])
# def place_detail():
#     """specific info of a place"""
#     pass


# @place_api.route('/place/<', methods=["GET"])
# def
# """names of the owners of places with toilets"""
# pass
