#!/usr/bin/python

from datetime import datetime
import uuid
import re
from data import country_data


class Country():
    """Representation of country """

    def __init__(self, *args, **kwargs):
        """ constructor """
        # super().__init__(*args, **kwargs)

        # defaults
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__name = ""
        self.__code = ""

        # Only allow name, code.
        # Note that setattr will call the setters for these attribs
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
            raise ValueError(
                "Invalid country name specified: {}".format(value))

    @property
    def code(self):
        """Getter for private prop code"""
        return self.__code

    @code.setter
    def code(self, value):
        """Setter for private prop code"""

        # ensure that the value is not spaces-only and is two uppercase alphabets only
        is_valid_code = len(value.strip()) > 0 and re.match(
            "^[A-Z][A-Z]$", value)
        if is_valid_code:
            self.__code = value
        else:
            raise ValueError(
                "Invalid country code specified: {}".format(value))

    # @classmethod
    # def from_json(cls, data):
    #     """Create a list of Country objects from JSON data."""
    #     country_data = json.loads(data)
    #     country_objects = []
    #     for country_entry in country_data.get('Country', []):
    #         country = cls(id=country_entry.get('id'),
    #                       name=country_entry.get('name'),
    #                       code=country_entry.get('code'),
    #                       created_at=country_entry.get('created_at'),
    #                       updated_at=country_entry.get('updated_at'))
    #         country_objects.append(country)
    #     return country_objects

    def update_country(self, **kwargs):
        """update existing country data"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid item: {key}")
        self.updated_at = datetime.now().timestamp()
