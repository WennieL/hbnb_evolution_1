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

country_api = Blueprint('country_api', __name__)


# Examples
@country_api.route('/example/country_data')
def example_country_data():
    """ Example to show that we can view data loaded in the data module's init """
    return jsonify(country_data)


@country_api.route('/countries', methods=["GET"])
def countries_get():
    """ returns all countires data """

    countries_info = []
    for country_value in country_data.values():
        countries_info.append({
            "id": country_value["id"],
            "name": country_value["name"],
            "code": country_value["code"],
            "created_at": datetime.fromtimestamp(country_value["created_at"]),
            "updated_at": datetime.fromtimestamp(country_value["updated_at"])
        })

    return jsonify(countries_info), 200


@country_api.route('/countries/<country_code>', methods=["GET"])
def countries_specific_get(country_code):
    """ returns specific country data """

    for country_value in country_data.values():
        if country_value['code'] == country_code:
            data = country_value

    country_info = {
        "id": data['id'],
        "name": data['name'],
        "code": data['code'],
        "created_at": datetime.fromtimestamp(data['created_at']),
        "updated_at": datetime.fromtimestamp(data['updated_at'])
    }

    return jsonify(country_info), 200


@country_api.route('/countries', methods=["POST"])
def create_new_country():
    """ posts data for new country then returns the country data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'
    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()
    country_list = data.get("Country")

    for data in country_list:
       # Check for required fields in each country data
        required_fields = ["name", "code"]
        for field in required_fields:
            if field not in data:
                abort(400, f"Missing data: {field}")
        try:
            new_country = Country(
                name=data["name"],
                code=data["code"]
            )
        except ValueError as exc:
            abort(400, repr(exc))

        if "Country" not in country_data:
            country_data["Country"] = []

        country_data["Country"].append({
            "id": new_country.id,
            "name": new_country.name,
            "code": new_country.code,
            "created_at": new_country.created_at,
            "updated_at": new_country.updated_at
        })
        attribs = {
            "id": new_country.id,
            "name": new_country.name,
            "code": new_country.code,
            "created_at": datetime.fromtimestamp(new_country.created_at),
            "updated_at": datetime.fromtimestamp(new_country.updated_at)
        }
    return jsonify(attribs), 200


@country_api.route('/countries/<country_code>', methods=["PUT"])
def update_country(country_code):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'
    if not request.json:
        abort(400, "Not a JSON")

    new_data = request.get_json()

    # Search for the country with the specified country_code
    for country_value in country_data.values():
        if country_value["code"] == country_code:
            found_country_data = country_value
            break
    else:
        abort(404, f"Country not found: {country_code}")

    # Update country attributes if new data is provided
    if "name" in new_data:
        found_country_data["name"] = new_data["name"]
    if "code" in new_data:
        found_country_data["code"] = new_data["code"]

    # Prepare response attributes with updated timestamps as datetime objects
    attribs = {
        "id": found_country_data["id"],
        "name": found_country_data["name"],
        "code": found_country_data["code"],
        "created_at": datetime.fromtimestamp(found_country_data["created_at"]),
        "updated_at": datetime.fromtimestamp(found_country_data["updated_at"])
    }

    return jsonify(attribs), 200


@country_api.route('/countries/<country_code>', methods=["DELETE"])
def delete_country(country_code):
    """Deletes an existing user by user_id"""

    keys_to_delete = []

    for country_key, country_value in list(country_data.items()):
        if country_value["code"] == country_code:
            keys_to_delete.append(country_key)

    if not keys_to_delete:
        abort(404, f"Place not found with ID: {country_code}")

    # Remove the place(s) from the dictionary
    for country_key in keys_to_delete:
        del country_data[country_key]

    # Return a confirmation message
    return jsonify({"message": f"Country: {country_code} has been deleted."}), 204
