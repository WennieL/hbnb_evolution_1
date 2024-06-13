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


city_api = Blueprint('city_api', __name__, url_prefix="/api/v1")


@city_api.route('/cities', methods=["GET"])
def get_cities():
    """return all cities """
    cities_info = []

    for city_value in city_data.values():
        cities_info.append({
            "id": city_value["id"],
            "country_id": city_value["country_id"],
            "name": city_value["name"],
            "created_at": datetime.fromtimestamp(city_value["created_at"]),
            "updated_at": datetime.fromtimestamp(city_value["updated_at"])
        })

    return jsonify(cities_info)


@city_api.route('/countries/<country_code>/cities', methods=["GET"])
def countries_specific_cities_get(country_code):
    """ returns all cities data of a specified country """

    cities_data = []
    found_country_id = None

    for country_value in country_data.values():
        if country_value["code"] == country_code:
            found_country_id = country_value["id"]
            break

    if not found_country_id:
        abort(404, f"Country: {country_code} is not found")

    for city_value in city_data.values():
        if city_value["country_id"] == found_country_id:
            cities_data.append({
                "id": city_value["id"],
                "country_id": city_value["country_id"],
                "name": city_value["name"],
                "created_at": datetime.fromtimestamp(city_value["created_at"]),
                "updated_at": datetime.fromtimestamp(city_value["updated_at"])
            })

    return jsonify(cities_data), 200


@city_api.route('/city/create', methods=["POST"])
def create_new_city():
    """create a new city to a specific country"""

    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()
    required_fields = ["name", "country_id"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        new_city = City(
            name=data["name"],
            country_id=data["country_id"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    if "City" not in city_data:
        city_data["City"] = []

    city_data["City"].append({
        "id": new_city.id,
        "country_id": new_city.country_id,
        "name": new_city.name,
        "created_at": new_city.created_at,
        "updated_at": new_city.updated_at
    })

    attribs = {
        "id": new_city.id,
        "country_id": new_city.country_id,
        "name": new_city.name,
        "created_at": datetime.fromtimestamp(new_city.created_at),
        "updated_at": datetime.fromtimestamp(new_city.updated_at)
    }

    return jsonify(attribs), 200


@city_api.route('/city/update/<city_id>', methods=["PUT"])
def update_city_data(city_id):
    """update data of a specific city"""
    if not request.json:
        abort(400, "not JSON file")

    new_data = request.get_json()
    for city_value in city_data.values():
        if city_value["id"] == city_id:
            found_city_data = city_value
            break
    else:
        abort(404, "City ID not found: {city_id}")

    if "name" in new_data:
        found_city_data["name"] = new_data["name"]

    attribs = {
        "id": found_city_data["id"],
        "country+id": found_city_data["country_id"],
        "name": found_city_data["name"],
        "created_at": datetime.fromtimestamp(found_city_data["created_at"]),
        "updated_at": datetime.fromtimestamp(found_city_data["updated_at"])
    }

    return jsonify(attribs), 200


@city_api.route('/city/delete/<city_id>', methods=["DELETE"])
def delete_a_city(city_id):
    """delete a specific city"""
    for city_value in city_data.values():
        if city_value["id"] == city_id:
            delete_data = city_value
            break
    else:
        abort(404, f"City not found: {city_id}")

    city_info = {
        "id": delete_data["id"],
        "country+id": delete_data["country_id"],
        "name": delete_data["name"],
        "created_at": datetime.fromtimestamp(delete_data["created_at"]),
        "updated_at": datetime.fromtimestamp(delete_data["updated_at"])
    }

    return jsonify(city_info), 200
