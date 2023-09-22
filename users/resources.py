import os
import stripe
from flask_restful import Resource
from flask import request
from app import bcrypt, db
from models import User, City, UserVerification, Temporary, Rented
from flask_jwt_extended import jwt_required, get_jwt_identity
from validations import Validators
from utils import save_picture
import datetime
from decorators import user_required
from flask_api import status


class Registration(Resource):

    def post(self):
        user_json = request.get_json()
        try:
            error = Validators.validate_email(user_json['email'])
            if len(error) > 0:
                return {"data": [],
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            error = Validators.validate_username(user_json['username'])
            if len(error) > 0:
                return {"data": user_json,
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            error = Validators.validate_password(user_json['password'])
            if len(error) > 0:
                return {"data": [],
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            city = City.query.filter_by(city=user_json["city"].replace(" ", "").upper()).first()
            if not city:
                return {"data": [],
                        "message": "This city does not exist!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            hashed_password = bcrypt.generate_password_hash(user_json['password']).decode('utf-8')
            user_object = User(name=user_json['name'], username=user_json['username'], email=user_json['email'],
                               password=hashed_password, city_id=city.id)
            user_object.save_to_db()
            return {"data": user_json,
                    "message": "User Register Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            print(user_json)
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class ApplyForVerification(Resource):
    decorators = [jwt_required(), user_required()]

    def post(self):
        try:
            record = User.query.filter_by(id=get_jwt_identity()).filter_by(is_verified=True).first()
            if record:
                return {"data": [],
                        "message": "Your are already verified!",
                        "status": "false"
                        }, status.HTTP_403_FORBIDDEN
            record = UserVerification.query.filter_by(user_id=get_jwt_identity()).all()
            if record:
                if record[-1].approval == "":
                    return {"data": [],
                            "message": "Please wait for your previous request to be reviewed!",
                            "status": "false"
                            }, status.HTTP_403_FORBIDDEN
            picture_file = save_picture(request.files['file'])
            row = UserVerification(user_id=get_jwt_identity(), id_proof=picture_file, approval="",
                                   date=datetime.datetime.today())
            db.session.add(row)
            db.session.commit()
            return {"data": [picture_file],
                    "message": "Successfully Applied for verification!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class EnterDates(Resource):
    decorators = [jwt_required(), user_required()]

    def post(self):
        user_json = request.get_json()
        try:
            rent_from = datetime.datetime.strptime((user_json['rent_from']), '%Y/%m/%d')
            rent_till = datetime.datetime.strptime((user_json['rent_till']), '%Y/%m/%d')
            error = Validators.validate_rent_from(rent_from)
            if len(error) > 0:
                return {"data": [],
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            error = Validators.validate_rent_till(rent_from, rent_till)
            if len(error) > 0:
                return {"data": [],
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            record = Temporary.query.filter_by(user_id=get_jwt_identity()).first()
            if record:
                record.rent_from = rent_from
                record.rent_till = rent_till
                record.city_id = user_json['city_delivery_id']
                db.session.commit()
            else:
                new = Temporary(user_id=get_jwt_identity(), rent_from=rent_from,
                                rent_till=rent_till, city_id=user_json['city_delivery_id'])
                db.session.add(new)
                db.session.commit()
            return {"data": [],
                    "message": "Dates entered successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class CancelBooking(Resource):
    decorators = [jwt_required(), user_required()]

    def post(self):
        user_json = request.get_json()
        try:
            record = Rented.query.filter_by(booking_id=user_json['booking_id']).filter_by(user_id=get_jwt_identity()) \
                .first()
            if record:
                if record.rented_from > datetime.datetime.today():
                    record.final_status = "false"
                    db.session.commit()
                    return {"data": [],
                            "message": "Booking cancelled successfully!",
                            "status": "true"
                            }, status.HTTP_200_OK
                else:
                    return {"data": [],
                            "message": "You cannot cancel the booking at this time!",
                            "status": "false"
                            }, status.HTTP_403_FORBIDDEN
            return {"message": "No booking with this booking id for this user!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class Bookings(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        orders = Rented.query.filter_by(user_id=get_jwt_identity()).order_by(Rented.booking_time.desc()).all()
        record = {}
        if orders:
            for order in orders:
                record[order.booking_id] = {"car_id": f"{order.user_id}", "From": f"{order.rented_from}",
                                            "To": f"{order.rented_till}"}
        else:
            return {"data": [],
                    "message": "No Booking records for this user!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND
        return {"data": record,
                "message": "Booking records fetched successfully!",
                "status": "true"
                }, status.HTTP_200_OK


class PayFine(Resource):
    decorators = [jwt_required(), user_required()]

    def post(self):
        user_json = request.get_json()
        try:
            record = Rented.query.filter_by(booking_id=user_json['booking_id']).first()
            if not record:
                return {"message": "No booking with this booking id!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            user = User.query.filter_by(id=record.user_id).first()
            invoice = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Fine Payment',
                        },
                        'unit_amount': int(record.fine * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                # both url  will be called from frontend side
                success_url=os.environ.get('HOST') + '/fine_success',
                cancel_url=os.environ.get('HOST') + '/fine_cancel',
            )
            card_obj = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": "4242424242424242",
                    "exp_month": 7,
                    "exp_year": 2023,
                    "cvc": "123",
                },
            )
            customer = stripe.Customer.create(
                email=user.email, payment_method=card_obj.id
            )
            stripe.PaymentIntent.create(
                customer=customer.id,
                payment_method=card_obj.id,
                currency="inr",
                amount=int(record.fine * 100),
                description='Car Booking Rent'
            )

            return {"data": invoice["url"],
                    "message": "click on following link to complete the payment",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class FinePaymentSuccess(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        user_json = request.get_json()
        record = Rented.query.filter_by(booking_id=user_json['booking_id']).first()
        user = User.query.filter_by(id=record.user_id).first()
        record.fine_paid = True
        user.fine_pending = False
        db.session.commit()
        return {"data": [],
                "message": "Fine paid successfully!",
                "status": "true"
                }, status.HTTP_200_OK


class FinePaymentCancel(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        return {"data": [],
                "message": "Payment Cancelled. Please try again!",
                "status": "true"
                }, status.HTTP_200_OK
