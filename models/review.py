#!/usr/bin/python3

from datetime import datetime
import uuid
from data import review_data


class Review:
    """Representation of a review"""

    def __init__(self, **kwargs):
        """Constructor for Review"""
        self.id = str(uuid.uuid4())  # Generate unique ID
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.__commentor_user_id = ""
        self.__place_id = ""
        self.__feedback = ""
        self.__rating = 0.0

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    @property
    def commentor_user_id(self):
        """Getter for commentor_user_id"""
        return self.__commentor_user_id

    @commentor_user_id.setter
    def commentor_user_id(self, value):
        """Setter for commentor_user_id"""
        self.__commentor_user_id = value

    @property
    def place_id(self):
        """Getter for place_id"""
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        """Setter for place_id"""
        self.__place_id = value

    @property
    def feedback(self):
        """Getter for feedback"""
        return self.__feedback

    @feedback.setter
    def feedback(self, value):
        """Setter for feedback"""
        if isinstance(value, str):
            self.__feedback = value
        else:
            raise ValueError("Feedback must be a string")

    @property
    def rating(self):
        """Getter for rating"""
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Setter for rating"""
        if isinstance(value, (int, float)) and 0.0 <= value <= 5.0:
            self.__rating = value
        else:
            raise ValueError("Rating must be a number between 0 and 5")
