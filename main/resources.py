from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from models import User, City
from validations import Validators
from utils import send_reset_email
from flask_api import status


class HomePage(Resource):
    def get(self):
        return {'data': 'Hello World!',
                'status': 'true'}, status.HTTP_200_OK


class Login(Resource):

    def post(self):
        login_json_data = request.get_json()
        try:
            user = User.query.filter_by(email=login_json_data["email"]).first()
            if not user:
                return {"data": [],
                        "message": "email doesn't exists",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            if bcrypt.check_password_hash(user.password, login_json_data["password"]):
                access_token = create_access_token(identity=user.id)
                return {"data": {"access_token": access_token},
                        "message": "Logged in Successfully",
                        "status": "true"
                        }, status.HTTP_200_OK
            else:
                return {"data": [],
                        "message": "Incorrect Password",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
        except (KeyError, AttributeError) as err:
            print(err)
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class Profile(Resource):
    decorators = [jwt_required()]

    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        return {"data": {"name": user.name, "email": user.email, "username": user.username, "city": user.city.city},
                "message": "Data fetched successfully!",
                "status": "true"
                }, status.HTTP_200_OK


class UpdateProfile(Resource):
    decorators = [jwt_required()]

    def post(self):
        profile_json_data = request.get_json()
        user = User.query.filter_by(id=get_jwt_identity()).first()
        try:
            user_obj = User.query.filter(User.email == profile_json_data['email'], User.id != user.id).first()
            if user_obj:
                return {"data": [],
                        "message": "user with this email id already exists please choose different email",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            user_obj = User.query.filter(User.username == profile_json_data['username'], User.id != user.id).first()
            if user_obj:
                return {"data": [],
                        "message": "user with this username already exists please choose different username",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            city = City.query.filter_by(city=profile_json_data["city"].replace(" ", "").upper()).first()
            if not city:
                return {"data": [],
                        "message": "This city does not exist!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            user.name = profile_json_data["name"]
            user.email = profile_json_data["email"]
            user.username = profile_json_data["username"]
            user.city_id = city.id
            db.session.commit()
            return {"data": [],
                    "message": "Profile Updated Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class ChangePassword(Resource):
    decorators = [jwt_required()]

    def post(self):
        password_json_data = request.get_json()
        user = User.query.filter_by(id=get_jwt_identity()).first()
        try:
            if bcrypt.check_password_hash(user.password, password_json_data["current_password"]):
                error = ""
                error += Validators.validate_password(password_json_data["new_password"])
                if len(error) > 0:
                    return {"message": f"{error}",
                            "status": "false"
                            }, status.HTTP_400_BAD_REQUEST

                user.password = bcrypt.generate_password_hash(password_json_data["new_password"]).decode('utf-8')
                db.session.commit()
            else:
                return {"data": [],
                        "message": "invalid current password",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            return {"data": [],
                    "message": "Password changed successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class ResetRequest(Resource):

    def post(self):
        json_data = request.get_json()
        try:
            user = User.query.filter_by(email=json_data['email']).first()
            if not user:
                return {"data": [],
                        "message": "Email does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            return {"data": send_reset_email(user),
                    "message": "Mail sent!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class ResetToken(Resource):

    def post(self):
        json_data = request.get_json()
        try:
            user = User.verify_reset_token(json_data['token'])
            if not user:
                return {"data": [],
                        "message": "That is an invalid or expired token!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            hashed_password = bcrypt.generate_password_hash(json_data['new_password']).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return {"data": [],
                    "message": "The password is changed successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
