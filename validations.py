from models import User
import datetime
import re


class Validators:
    """Class for validating different variables"""

    @staticmethod
    def validate_username(field):
        """Method for validating the username and checking if it already exists

        Args
        ------------------
        field: It is the username entered by the user which needs to validated

        Returns
        ------------------
        True if the field is validated or raises a Validation error"""
        error = ""
        if " " not in field:
            user = User.query.filter_by(username=field).first()
            if user:
                error += 'Username is already taken! '
        else:
            error += 'Username cannot have spaces! '
        return error

    @staticmethod
    def validate_email(field):
        """Method for validating the email and checking if it already exists

        Args
        ------------------
        field: It is the email entered by the user which needs to validated

        Returns
        ------------------
        True if the field is validated or raises a Validation error"""
        error = ""
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pattern, field):
            user = User.query.filter_by(email=field).first()
            if user:
                error += 'Email is already taken! '
        else:
            error += 'Email address is not in proper format! '
        return error

    @staticmethod
    def validate_password(field):
        """Method for validating the password

        Args
        ------------------
        field: It is the pass entered by the  user which needs to validated

        Returns
        ------------------
        True if the field is validated or raises a Validation error"""

        passwd = field
        special_chars = ['$', '@', '#', '%']
        error = ""
        if len(passwd) < 6:
            error += 'Length should be at least 6! '

        if len(passwd) > 20:
            error += 'Length should be not be greater than 20! '

        if not any(char.isdigit() for char in passwd):
            error += 'Password should have at least one numeral! '

        if not any(char.isupper() for char in passwd):
            error += 'Password should have at least one uppercase letter! '

        if not any(char.islower() for char in passwd):
            error += 'Password should have at least one lowercase letter! '

        if not any(char in special_chars for char in passwd):
            error += 'Password should have at least one of the symbols $@#%! '

        return error

    @staticmethod
    def validate_rent_from(field):
        """Method for validating the entered dates

        Args
        ------------------
        field: It is the rent from date entered by the user which needs to validated

        Returns
        ------------------
        True if the field is validated or raises a Validation error"""
        error = ""
        if field < datetime.datetime.today():
            error = "The date cannot be in the past!"
        return error

    @staticmethod
    def validate_rent_till(rented_from, rented_till):

        """Method for validating the car ID and checking if it already exists

        Args
        ------------------
        rented_from: It is the car rent from date entered by the user which needs to validated
        rented_till: It is the car rent till date entered by the user which needs to validated

        Returns
        ------------------
        True if the field is validated or raises a Validation error"""
        error = ""
        if rented_till < datetime.datetime.today():
            error += "The date cannot be in the past!"
        elif rented_till < rented_from:
            error += "The rented till date cannot be less than the rented from date!"
        return error
