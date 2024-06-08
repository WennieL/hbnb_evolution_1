#!/usr/bin/python3

from datetime import datetime
from flask import Flask, jsonify, request, abort

# Import your models
from models.amenity import Amenity
from models.city import City
from models.country import Country
from models.place import Place
from models.review import Review
from models.user import User

# Import your blueprints
from api.user_api import user_blueprint
from api.country_api import country_blueprint
from api.city_api import city_blueprint
from api.amenity_api import amenity_blueprint
from api.place_api import place_blueprint
from api.review_api import review_blueprint

# Import your data (if needed)
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)

# Initialize Flask app
app = Flask(__name__)

# Register your blueprints
app.register_blueprint(user_blueprint, url_prefix='/api/v1/')
app.register_blueprint(country_blueprint, url_prefix='/api/v1/')
app.register_blueprint(city_blueprint, url_prefix='/api/v1/')
app.register_blueprint(amenity_blueprint, url_prefix='/amenity')
app.register_blueprint(place_blueprint, url_prefix='/place')
app.register_blueprint(review_blueprint, url_prefix='/review')


@app.route('/')
def hello_world():
    """ Hello world """
    return 'Hello World'


@app.route('/', methods=["POST"])
def hello_world_post():
    """ Hello world endpoint for POST requests """
    # curl -X POST localhost:5000/
    return "hello world\n"


# Examples
@app.route('/example/country_data')
def example_country_data():
    """ Example to show that we can view data loaded in the data module's init """
    return jsonify(country_data)


@app.route('/example/cities')
def example_cities():
    """ Example route to showing usage of the City model class """

    # We will be appending dictionaries to the list instead of City objects
    # This is so we can print them out on the webpage
    # If there is no need to display the data, we can consider storing the City objects themselves
    cities_list = []

    # the 'hello' and 'world' params below will be filtered off in City constructor
    cities_list.append(City(name="Gotham", hello="hello").__dict__)
    cities_list.append(City(name="Metropolis", world="world").__dict__)

    # Validation: The city with the invalid name is not appended to the list
    try:
        cities_list.append(City(name="#$%^&**", country_id=2).__dict__)
    except ValueError as exc:
        # This is printed internally in the server output. Not shown on website.
        print("City creation Error - ", exc)

    # Validation: The city with the invalid country_id is not appended to the list
    try:
        cities_list.append(City(name="Duckburg", country_id=1234).__dict__)
    except ValueError as exc:
        print("City creation Error - ", exc)

    # Note that private attributes have a weird key format. e.g. "_City__country_id"
    # This shows that the output of the City object's built-in __dict__ is not usable as-is

    return cities_list


@app.route('/example/places_amenties_raw')
def example_places_amenities_raw():
    """ Prints out the raw data for relationships between places and their amenities """
    return jsonify(place_to_amenity_data)


@app.route('/example/places_amenties_prettified_example')
def example_places_amenties_prettified():
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


@app.route('/example/places_reviews')
def example_places_reviews():
    """ prints out reviews of places """

    output = {}

    for key in review_data:
        row = review_data[key]
        place_id = row['place_id']
        place_name = place_data[place_id]['name']
        if place_name not in output:
            output[place_name] = []

        reviewer = user_data[row['commentor_user_id']]

        output[place_name].append({
            "review": row['feedback'],
            "rating": str(row['rating'] * 5) + " / 5",
            "reviewer": reviewer['first_name'] + " " + reviewer['last_name']
        })

    return jsonify(output)

# Consider adding other test routes to display data for:
# - the places within the countries
# - which places are owned by which users
# - names of the owners of places with toilets


# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
