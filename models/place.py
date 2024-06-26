#!/usr/bin/python3

from datetime import datetime
import uuid
import re
from data import place_data, user_data, city_data, review_data, place_to_amenity_data


class Place():
    """Representation of place"""

    def __init__(self, **kwargs):
        """ constructor """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__host_user_id = ""
        self.__city_id = ""
        self.__name = ""
        self.__description = ""
        self.__address = ""
        self.__latitude = 0.0
        self.__longitude = 0.0
        self.__number_of_rooms = 0
        self.__bathrooms = 0
        self.__price_per_night = 0
        self.__max_guests = 0

        # Initialize instance attributes from kwargs if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid item: {key}")

    @property
    def host_user_id(self):
        """pass"""
        return self.__host_user_id

    @host_user_id.setter
    def host_user_id(self, value):
        """Setter for host user id"""
        if isinstance(value, str):
            self.__host_user_id = value
        else:
            raise ValueError(f"Invalid Host User ID: {value}")

    @property
    def city_id(self):
        """pass"""
        return self.__city_id

    @city_id.setter
    def city_id(self, value):
        """Setter for host user id"""
        if isinstance(value, str):
            self.__city_id = value
        else:
            raise ValueError(f"Invalid City ID: {value}")

    @property
    def name(self):
        """Getter for private name"""
        return self.__name

    @name.setter
    def name(self, value):
        """setter for private name"""

        # ensure that the value is not spaces-only and is alphabets + spaces only

        if len(value.strip()) > 0 and re.match("^(?=.+)[a-zA-Z ]+$", value):
            self.__name = value
        else:
            raise ValueError(f"Invalid place name specified: {value}")

    @property
    def description(self):
        """Getter for private description"""
        return self.__description

    @description.setter
    def description(self, value):
        """Setter for private description"""
        if isinstance(value, str) and value.strip():
            self.__description = value
        else:
            raise ValueError(f"Invalid description specified: {value}")

    @property
    def address(self):
        """Getter for private address"""
        return self.__address

    @address.setter
    def address(self, value):
        """Setter for private address"""
        if isinstance(value, str) and value.strip():
            self.__address = value
        else:
            raise ValueError(f"Invalid address specified: {value}")

    @property
    def latitude(self):
        """Getter for private latitude"""
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for private latitude"""
        # ensure that the value is not None, positive or
        # negative float only and at least 1 char input

        if isinstance(value, (float, int)):
            self.__latitude = value
        else:
            raise ValueError(f"Invalid latitude specified: {value}")

    @property
    def longitude(self):
        """Getter for private longitude"""
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for private longitude"""
        # ensure that the value is not None, positive or
        # negative float only and at least 1 char input

        if isinstance(value, (float, int)):
            self.__longitude = value
        else:
            raise ValueError(f"Invalid longitude specified: {value}")

    @property
    def number_of_rooms(self):
        """Getter for private number_of_rooms"""
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        """Setter for private number_of_rooms"""
        # ensure that the value is positive int

        if isinstance(value, int) and value > 0:
            self.__number_of_rooms = value
        else:
            raise ValueError(f"Invalid number_of_rooms specified: {value}")

    @property
    def bathrooms(self):
        """Getter for private bathrooms"""
        return self.__bathrooms

    @bathrooms.setter
    def bathrooms(self, value):
        """Setter for private bathrooms"""
        if isinstance(value, int) and value >= 0:
            self.__bathrooms = value
        else:
            raise ValueError(f"Invalid bathrooms specified: {value}")

    @property
    def price_per_night(self):
        """Getter for private price_per_night"""
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        """Setter for private longitude"""
        # ensure that the value is 0 or positive int or float
        if isinstance(value, (float, int)) and value >= 0:
            self.__price_per_night = float(value)
        else:
            raise ValueError(f"Invalid price_per_night specified: {value}. ")

    @property
    def max_guests(self):
        """Getter for private max_guests"""
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, value):
        """Setter for private max_guests"""
        # ensure that the value is positive int only

        if isinstance(value, int) and value > 0:
            self.__max_guests = value
        else:
            raise ValueError(
                f"Invalid max_guests specified: {value}. Guest(s) must be a positive integer.")
