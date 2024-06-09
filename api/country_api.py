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

country_blueprint = Blueprint('country_api', __name__)


# Examples
@country_blueprint.route('/example/country_data')
def example_country_data():
    """ Example to show that we can view data loaded in the data module's init """
    return jsonify(country_data)


@country_blueprint.route('/api/v1/countries', methods=["POST"])
def countries_post():
    """ posts data for new country then returns the country data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    if 'code' not in data:
        abort(400, "Missing country code")

    try:
        c = Country(name=data["name"], code=data["code"])
    except ValueError as exc:
        return repr(exc) + "\n"

    # add new user data to user_data
    # note that the created_at and updated_at are using timestamps
    country_data[c.id] = {
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at": c.created_at,
        "updated_at": c.updated_at
    }

    # note that the created_at and updated_at are using readable datetimes
    attribs = {
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at": datetime.fromtimestamp(c.created_at),
        "updated_at": datetime.fromtimestamp(c.updated_at)
    }

    return jsonify(attribs)


@country_blueprint.route('/api/v1/countries', methods=["GET"])
def countries_get():
    """ returns countires data """
    data = []

    for k, v in country_data.items():
        data.append({
            "id": v['id'],
            "name": v['name'],
            "code": v['code'],
            "created_at": datetime.fromtimestamp(v['created_at']),
            "updated_at": datetime.fromtimestamp(v['updated_at'])
        })

    return jsonify(data)


@country_blueprint.route('/api/v1/countries/<country_code>', methods=["GET"])
def countries_specific_get(country_code):
    """ returns specific country data """
    for k, v in country_data.items():
        if v['code'] == country_code:
            data = v

    c = {
        "id": data['id'],
        "name": data['name'],
        "code": data['code'],
        "created_at": datetime.fromtimestamp(data['created_at']),
        "updated_at": datetime.fromtimestamp(data['updated_at'])
    }

    return jsonify(c)


@country_blueprint.route('/api/v1/countries/<country_code>', methods=["PUT"])
def countries_put(country_code):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    c = {}

    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()
    for k, v in country_data.items():
        if v['code'] == country_code:
            c = v

    if not c:
        abort(400, "Country not found for code {}".format(country_code))

    # modify the values
    # only name is allowed to be modified
    for k, v in data.items():
        if k in ["name"]:
            c[k] = v

    # update country_data with the new name - print country_data out to confirm it if you want
    country_data[c['id']] = c

    attribs = {
        "id": c["id"],
        "name": c["name"],
        "code": c["code"],
        "created_at": datetime.fromtimestamp(c["created_at"]),
        "updated_at": datetime.fromtimestamp(c["updated_at"])
    }

    # print out the updated user details
    return jsonify(attribs)


@country_blueprint.route('/api/v1/countries/<country_code>/cities', methods=["GET"])
def countries_specific_cities_get(country_code):
    """ returns cities data of specified country """
    data = []
    wanted_country_id = ""

    for k, v in country_data.items():
        if v['code'] == country_code:
            wanted_country_id = v['id']

    for k, v in city_data.items():
        if v['country_id'] == wanted_country_id:
            data.append({
                "id": v['id'],
                "name": v['name'],
                "country_id": v['country_id'],
                "created_at": datetime.fromtimestamp(v['created_at']),
                "updated_at": datetime.fromtimestamp(v['updated_at'])
            })

    return jsonify(data)
