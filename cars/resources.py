import os

import stripe
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from decorators import admin_required, user_required, user_verified
from models import User, City, Car, CarModels, CarCategories, CarCompany, Rented, Temporary, Maintenance
import datetime
from flask_api import status


class CreateCars(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        car_json_data = request.get_json()
        try:
            if not car_json_data['ppd'].isnumeric() or not car_json_data['min_rent'].isnumeric() or\
                    not car_json_data['deposit'].isnumeric() or not car_json_data['mileage'].isnumeric():
                return {"data": [],
                        "message": "Some values must be integers",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            # cars = Car.query.filter_by(car_id=car_json_data['car_id'].replace(" ", "").upper()).first()
            # if cars:
            #     return {"data": [],
            #             "message": "Car with this id already exists!",
            #             "status": "false"
            #             }, status.HTTP_400_BAD_REQUEST
            cars = CarCompany.query.filter_by(id=car_json_data['company_id'].replace(" ", "").upper()).first()
            if not cars:
                return {"data": [],
                        "message": "Company with this id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            cars = CarCategories.query.filter_by(id=car_json_data['category_id'].replace(" ", "").upper()).first()
            if not cars:
                return {"data": [],
                        "message": "Category with this id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            cars = CarModels.query.filter_by(id=car_json_data['model_id'].replace(" ", "").upper()).first()
            if not cars:
                return {"data": [],
                        "message": "Model with this id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            cars = City.query.filter_by(id=car_json_data['city_id'].replace(" ", "").upper()).first()
            if not cars:
                return {"data": [],
                        "message": "City with this id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            car_object = Car(company_id=car_json_data['company_id'], category_id=car_json_data['category_id'],
                             model_id=car_json_data['model_id'], mileage=car_json_data['mileage'],
                             ppd=car_json_data['ppd'], color=car_json_data['color'].replace(" ", "").upper(),
                             min_rent=car_json_data['min_rent'], city_id=car_json_data['city_id'],
                             deposit=car_json_data['deposit'])
            car_object.save_to_db()
            return {"data": [],
                    "message": "Car Added Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class UpdateCar(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        car_json_data = request.get_json()
        try:
            car = Car.query.filter_by(id=car_json_data['car_id'].replace(" ", "").upper()).first()
            if not car:
                return {"data": [],
                        "message": "Car with this id does not exist",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            if not car_json_data['ppd'].isnumeric() or not car_json_data['min_rent'].isnumeric() or\
                    not car_json_data['deposit'].isnumeric() or not car_json_data['mileage'].isnumeric():
                return {"data": [],
                        "message": "Some values must be integers",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            cars = City.query.filter_by(id=car_json_data['city_id'].replace(" ", "").upper()).first()
            if not cars:
                return {"data": [],
                        "message": "City with this id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            car.color = car_json_data['color'].replace(" ", "").upper()
            car.mileage = car_json_data['mileage']
            car.ppd = car_json_data['ppd']
            car.min_rent = car_json_data['min_rent']
            car.deposit = car_json_data['deposit']
            car.city_id = car_json_data['city_id']
            car.status = car_json_data['status']
            db.session.commit()
            return {"data": [],
                    "message": "Car Updated Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteCar(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        car_json_data = request.get_json()
        try:
            car = Car.query.filter_by(id=car_json_data['car_id'].replace(" ", "").upper()).first()
            if not car:
                return {"data": [],
                        "message": "Car with this id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            record = Rented.query.filter_by(carID=car.id).filter(Rented.final_status == "true").first()
            if record:
                if record.rented_from > datetime.datetime.today():
                    return {"data": [],
                            "message": "This car cannot be deleted as it is booked by a someone!",
                            "status": "false"
                            }, status.HTTP_403_FORBIDDEN
            db.session.delete(car)
            db.session.commit()
            return {"data": [],
                    "message": "Car Deleted Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}
stripe.api_key = stripe_keys['secret_key']


class BookCar(Resource):

    decorators = [jwt_required(), user_required(), user_verified()]

    def post(self):
        car_json_data = request.get_json()
        try:
            dates = Temporary.query.filter_by(user_id=get_jwt_identity()).first()
            if not dates:
                return {"data": [],
                        "message": "You dont have entered the dates!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            if dates.rent_from < datetime.datetime.today():
                return {"data": [],
                        "message": "Please enter the dates again as they have become past!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            customer = User.query.filter_by(id=get_jwt_identity()).first()
            if not customer.fine_pending:
                user = Temporary.query.filter_by(user_id=get_jwt_identity()).first()
                rented_cars = Rented.query.filter(user.rent_from <= Rented.rented_till) \
                    .filter(user.rent_till >= Rented.rented_from).filter_by(carID=car_json_data['car_id']) \
                    .filter(Rented.final_status == "true").all()
                record = Rented.query.filter(user.rent_from <= Rented.rented_till) \
                    .filter(user.rent_till >= Rented.rented_from).filter_by(user_id=get_jwt_identity()) \
                    .filter(Rented.final_status == "true").all()
                if rented_cars:
                    return {"data": [],
                            "message": "Sorry! This car is already booked!",
                            "status": "false"
                            }, status.HTTP_400_BAD_REQUEST
                elif record:
                    return {"data": [],
                            "message": "Sorry! You already have a booking for this time period and you can only book "
                                       "a single at given time!",
                            "status": "false"
                            }, status.HTTP_403_FORBIDDEN

                else:
                    dates = Temporary.query.filter_by(user_id=get_jwt_identity()).first()
                    customer = User.query.filter_by(id=get_jwt_identity()).first()
                    rent = Rented(carID=car_json_data['car_id'], user_id=get_jwt_identity(), booking_time=datetime
                                  .datetime.now(), rented_from=dates.rent_from, rented_till=dates.rent_till,
                                  city_taken_id=customer.city_id, city_delivery_id=dates.city_id)

                    db.session.add(rent)
                    db.session.commit()
                    return {"data": [],
                            "message": "Car Booked Successfully!",
                            "status": "true"
                            }, status.HTTP_200_OK
                    # car = Car.query.filter_by(id=car_json_data['car_id']).first()
                    # days = int(str(dates.rent_till - dates.rent_from).split(" ")[0])
                    # if days <= 1:
                    #     amount = car.min_rent
                    # else:
                    #     amount = days*car.ppd
                    # invoice = stripe.checkout.Session.create(
                    #     payment_method_types=['card'],
                    #     line_items=[{
                    #         'price_data': {
                    #             'currency': 'inr',
                    #             'product_data': {
                    #                 'name': 'Car Booking',
                    #             },
                    #             'unit_amount': int(amount * 100),
                    #         },
                    #         'quantity': 1,
                    #     }],
                    #     mode='payment',
                    #     # both url  will be called from frontend side
                    #     success_url=os.environ.get('HOST') + '/success',
                    #     cancel_url=os.environ.get('HOST') + '/cancel',
                    # )
                    # # card_obj = stripe.PaymentMethod.create(
                    # #     type="card",
                    # #     card={
                    # #         "number": "4242424242424242",
                    # #         "exp_month": 7,
                    # #         "exp_year": 2023,
                    # #         "cvc": "123",
                    # #     },
                    # # )
                    # customer = stripe.Customer.create(
                    #     email=customer.email, payment_method='pm_card_visa'
                    # )
                    # stripe.PaymentIntent.create(
                    #     customer=customer.id,
                    #     payment_method='pm_card_visa',
                    #     currency="inr",
                    #     amount=int(amount * 100),
                    #     description='Car Booking Rent'
                    # )
                    # return {"data": invoice["url"],
                    #         "message": "click on following link to complete the payment",
                    #         "status": "true"
                    #         }, status.HTTP_200_OK
            else:
                return {"data": [],
                        "message": "You first need the to pay your previous fine to book a car!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
        except (KeyError, AttributeError) as err:
            print(err)
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class PaymentSuccess(Resource):
    # decorators = [jwt_required(), user_required()]

    def get(self):
        car_json_data = request.get_json()
        print(car_json_data)
        dates = Temporary.query.filter_by(user_id=get_jwt_identity()).first()
        customer = User.query.filter_by(id=get_jwt_identity()).first()
        rent = Rented(carID=car_json_data['car_id'], user_id=get_jwt_identity(), booking_time=datetime
                      .datetime.now(), rented_from=dates.rent_from, rented_till=dates.rent_till,
                      city_taken_id=customer.city_id, city_delivery_id=dates.city_id)

        db.session.add(rent)
        db.session.commit()
        return {"data": [],
                "message": "Car Booked Successfully!",
                "status": "true"
                }, status.HTTP_200_OK


class PaymentCancel(Resource):
    decorators = [jwt_required(), user_required()]

    def get(self):
        return {"data": [],
                "message": "Payment Cancelled. Please try again!",
                "status": "true"
                }, status.HTTP_200_OK


class CarTakingList(Resource):

    decorators = [jwt_required(), admin_required()]

    def get(self):
        record = {}
        admin = User.query.filter_by(id=get_jwt_identity()).first()
        orders = Rented.query.filter_by(city_taken_id=admin.city_id).filter_by(final_status="true") \
            .filter_by(rented_from=datetime.date.today()).filter_by(car_taken=False).all()
        if orders:
            for order in orders:
                record[order.booking_id] = {"car_id": f"{order.user_id}", "From": f"{order.rented_from}",
                                        "To": f"{order.rented_till}"}
            return {"data": record,
                    "message": "Records fetched successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        else:
            return {"data": [],
                    "message": "There are no bookings for today!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND


class CarTakingListLate(Resource):

    decorators = [jwt_required(), admin_required()]

    def get(self):
        record = {}
        admin = User.query.filter_by(id=get_jwt_identity()).first()
        orders = Rented.query.filter_by(city_taken_id=admin.city_id).filter_by(final_status="true")\
            .filter(Rented.rented_from < datetime.date.today()).filter(Rented.rented_till > datetime.date.today())\
            .filter_by(car_taken=False).all()
        if orders:
            for order in orders:
                record[order.booking_id] = {"car_id": f"{order.user_id}", "From": f"{order.rented_from}",
                                        "To": f"{order.rented_till}"}
            return {"data": record,
                    "message": "Records fetched successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        else:
            return {"data": [],
                    "message": "There are no previous bookings which are pending!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND


class CarTaken(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        car_json = request.get_json()
        try:
            record = Rented.query.filter_by(booking_id=car_json['booking_id']).first()
            if not record:
                return {"data": [],
                        "message": "There are not bookings with this booking id!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            record.car_taken = True
            db.session.commit()
            return {"data": [],
                    "message": "Car Taken!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class CarDeliveryList(Resource):

    decorators = [jwt_required(), admin_required()]

    def get(self):
        record = {}
        admin = User.query.filter_by(id=get_jwt_identity()).first()
        orders = Rented.query.filter_by(city_delivery_id=admin.city_id).filter_by(final_status="true")\
            .filter_by(rented_till=datetime.date.today()).filter_by(car_taken=True)\
            .filter_by(car_delivery=False).all()
        if orders:
            for order in orders:
                record[order.booking_id] = {"car_id": f"{order.user_id}", "From": f"{order.rented_from}",
                                        "To": f"{order.rented_till}"}
            return {"data": record,
                    "message": "Records fetched successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        else:
            return {"data": [],
                    "message": "There are no car returns for today!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND


class CarDeliveryListLate(Resource):

    decorators = [jwt_required(), admin_required()]

    def get(self):
        record = {}
        admin = User.query.filter_by(id=get_jwt_identity()).first()
        orders = Rented.query.filter_by(city_delivery_id=admin.city_id).filter_by(final_status="true")\
            .filter(Rented.rented_till < datetime.date.today()).filter_by(car_taken=True)\
            .filter_by(car_delivery=False).all()
        if orders:
            for order in orders:
                record[order.booking_id] = {"car_id": f"{order.user_id}", "From": f"{order.rented_from}",
                                        "To": f"{order.rented_till}"}
            return {"data": record,
                    "message": "Records fetched successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        else:
            return {"data": [],
                    "message": "There are no car returns for previous days!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND


class CarMaintenance(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        car_json = request.get_json()
        try:
            car = Car.query.filter_by(id=car_json['car_id']).first()
            if not car:
                return {"data": [],
                        "message": "There are no cars with this id!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            record = Maintenance(carID=car_json['car_id'], date=datetime.datetime.utcnow(),
                                 description=car_json['description'], user_id=get_jwt_identity())
            db.session.add(record)
            car.status = False
            db.session.commit()
            return {"data": [],
                    "message": "Car Added to maintenance successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class CarReturnReview(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        car_json = request.get_json()
        try:
            record = Rented.query.filter_by(booking_id=car_json['booking_id']).first()
            if not record:
                return {"data": [],
                        "message": "There are not bookings with this booking id!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            record.said_date = bool(int(car_json['said_date']))
            record.said_time = bool(int(car_json['said_time']))
            record.proper_condition = bool(int(car_json['proper_condition']))
            record.description = car_json['description']
            record.fine = car_json['fine']
            if car_json['fine'] > 0:
                user = User.query.filter_by(id=record.user_id).first()
                user.fine_pending = True
            record.car_delivery = True
            db.session.commit()
            return {"data": [],
                    "message": "Car Return Reviewed Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            print(err)
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
