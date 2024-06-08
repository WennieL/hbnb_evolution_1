#!/usr/bin/python

from datetime import datetime
import uuid
import re
from data import country_data


class City():
    """Representation of a city,
     containing basic details such as name and associated country."""

    def __init__(self, *args, **kwargs):
        """ constructor """
        # super().__init__(*args, **kwargs)

        # defaults
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__name = ""
        self.__country_id = ""

        # Only allow country_id, name.
        # Note that setattr will call the setters for these 2 attribs
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    @property
    def name(self):
        """Getter for private prop name"""
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search(
            "^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError("Invalid city name specified: {}".format(value))

    @property
    def country_id(self):
        """Getter for private prop country_id"""
        return self.__country_id

    @country_id.setter
    def country_id(self, value):
        """Setter for private prop country_id"""

        # ensure that the specified country id actually exists before setting
        if value in country_data:
            self.__country_id = value
        else:
            raise ValueError("Invalid country_id specified: {}".format(value))

    # @classmethod
    # def from_json(cls, data):
    #     """Create a City object from JSON data."""
    #     city_data = json.loads(data)
    #     city_objects = []
    #     for city_entry in city_data.get('City', []):
    #         city = cls(id=city_entry.get('id'),
    #                    country_id=city_entry.get('country_id'),
    #                    name=city_entry.get('name'),
    #                    created_at=city_entry.get('created_at'),
    #                    updated_at=city_entry.get('updated_at'))
    #         city_objects.append(city)
    #     return city_objects

    def update_city(self, **kwargs):
        """update an existing city data"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid item: {key}")
        self.updated_at = datetime.now().timestamp()
