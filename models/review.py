#!/usr/bin/python3

from datetime import datetime
import uuid
from data import review_data


class Review():
    """Representation of place"""

    def __init__(self, **kwargs):
        """ constructor """

        # defaults
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__commentor_user_id = ""
        self.__place_id = ""
        self.__feedback = ""
        self.__rating = 0.0

        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    @property
    def commentor_user_id(self):
        """Getter for private __commentor_user_id"""
        return self.__commentor_user_id

    @commentor_user_id.setter
    def reviews(self, value):
        """Setter for private __commentor_user_id"""
        if value in review_data:
            self.__commentor_user_id = value
        else:
            raise ValueError(f"Commentor User ID is not found: {value}")

    @property
    def place_id(self):
        """Getter for private __place_id"""
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        """Setter for private __place_id"""
        if value in review_data:
            self.__place_id = value
        else:
            raise ValueError(f"Place ID is not found: {value}")

    @property
    def feedback(self):
        """Getter for private __place_id"""
        return self.__feedback

    @feedback.setter
    def __feedback(self, value):
        """Setter for private __feedback"""
        if isinstance(value, str):
            self.__feedback = value
        else:
            raise ValueError(f"Feedback is not found: {value}")

    @property
    def rating(self):
        """Getter for private __rating"""
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Setter for private rating"""
        if isinstance(value, (int, float)) and 0.0 <= value <= 1.0:
            self.__rating = value
        else:
            raise ValueError(f"Rating is not found: {value}")


# create a review
# update a review
# delete a eview
# save a reivew
