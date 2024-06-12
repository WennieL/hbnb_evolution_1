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
def update_city_data():
    """update data of a specific city"""
    pass


@city_api.route('/city/delete/<city_id>', methods=["DELETE"])
def delete_a_city():
    """delete a specific city"""
    pass
