import json

from models import Rented
from .test_user import test_login_success


def test_create_car_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ01EX786", "company_id": "1", "category_id": "1", "model_id": "1", "city_id": "1",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Added Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_create_car_fail_some_vals_not_int(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ01EX786", "company_id": "1", "category_id": "1", "model_id": "1", "city_id": "1",
            "color": "WHITE", "ppd": "abc", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Some values must be integers"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_car_fail_car_id_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX9709", "company_id": "1", "category_id": "1", "model_id": "1", "city_id": "1",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car with this id already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_car_fail_company_id_not_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ01EX786", "company_id": "100", "category_id": "1", "model_id": "1", "city_id": "1",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Company with this id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_create_car_fail_category_id_not_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ01EX786", "company_id": "1", "category_id": "100", "model_id": "1", "city_id": "1",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Category with this id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_create_car_fail_city_id_not_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ01EX786", "company_id": "1", "category_id": "1", "model_id": "1", "city_id": "100",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "City with this id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_create_car_fail_model_id_not_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ01EX786", "company_id": "1", "category_id": "1", "model_id": "100", "city_id": "1",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Model with this id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_create_car_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_i": "GJ01EX786", "company_id": "1", "category_id": "1", "model_id": "1", "city_id": "1",
            "color": "WHITE", "ppd": "1000", "min_rent": "1200", "deposit": "5000", "mileage": "10"}
    response = client.post("/create_cars", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_car_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX9709", "city_id": "1", "color": "WHITE", "ppd": "1000", "min_rent": "1200",
            "deposit": "5000", "mileage": "10", "status": "true"}
    response = client.post("/update_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Updated Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_car_fail_car_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX979", "city_id": "1", "color": "WHITE", "ppd": "1000", "min_rent": "1200",
            "deposit": "5000", "mileage": "10"}
    response = client.post("/update_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car with this id does not exist"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_car_fail_city_id_not_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX9709", "city_id": "100", "color": "WHITE", "ppd": "1000", "min_rent": "1200",
            "deposit": "5000", "mileage": "10"}
    response = client.post("/update_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "City with this id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_car_fail_some_vals_not_int(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX9709", "city_id": "1", "color": "WHITE", "ppd": "1000", "min_rent": "1200",
            "deposit": "abc", "mileage": "10"}
    response = client.post("/update_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Some values must be integers"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_car_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": "GJ27EX9709", "city_id": "1", "color": "WHITE", "ppd": "1000", "min_rent": "1200",
            "deposit": "5000", "mileage": "10"}
    response = client.post("/update_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_car_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX1"}
    response = client.post("delete_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Deleted Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_car_fail_car_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX979"}
    response = client.post("delete_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car with this id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_car_fail_car_booked_by_user(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "GJ27EX9709"}
    response = client.post("delete_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "This car cannot be deleted as it is booked by a someone!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_delete_car_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"i": "GJ27EX9709"}
    response = client.post("/delete_car", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_book_car_fail_no_dates_entered(client, db, user):
    access_token = test_login_success(client, db, user, email="user5@gmail.com", password="Rushan@123")
    data = {"car_id": "1"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "You dont have entered the dates!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_book_car_fail_dates_passed(client, db, user):
    access_token = test_login_success(client, db, user, email="user4@gmail.com", password="Rushan@123")
    data = {"car_id": "1"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter the dates again as they have become past!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_book_car_fail_already_booked(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"car_id": "1"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Sorry! This car is already booked!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_book_car_fail_already_have_booking(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"car_id": "2"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Sorry! You already have a booking for this time period " \
                                       "and you can only book a single at given time!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_book_car_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user6@gmail.com", password="Rushan@123")
    data = {"car_id": "2"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "click on following link to complete the payment"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_book_car_fail_fine_pending(client, db, user):
    access_token = test_login_success(client, db, user, email="user7@gmail.com", password="Rushan@123")
    data = {"car_id": "2"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "You first need the to pay your previous fine to book a car!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_book_car_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"id": "2"}
    response = client.post("/book_car", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_book_payment_success(client, db, user, mocker):
    mocker.patch('cars.resources.stripe.PaymentIntent.create',return_value={'url':'sefdghcjtfjg'})
    access_token = test_login_success(client, db, user, email="user6@gmail.com", password="Rushan@123")
    data = {"car_id": "2"}
    response = client.get("/success", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Booked Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_book_payment_cancel(client, db, user):
    access_token = test_login_success(client, db, user, email="user6@gmail.com", password="Rushan@123")
    data = {"car_id": "2"}
    response = client.get("/cancel", headers={"Authorization": access_token},
                    data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Payment Cancelled. Please try again!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_taking_list_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    response = client.get("/car_taking_list", headers={"Authorization": access_token})
    assert response.json["message"] == "Records fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_taking_list_late_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    response = client.get("/car_taking_list_late", headers={"Authorization": access_token})
    assert response.json["message"] == "Records fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_taking_list_fail_no_bookings(client, db, user, app):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    with app.app_context():
        rows = Rented.query.all()
        for row in rows:
            db.session.delete(row)
        db.session.commit()
    response = client.get("/car_taking_list", headers={"Authorization": access_token})
    assert response.json["message"] == "There are no bookings for today!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_car_taking_list_late_fail_no_bookings(client, db, user, app):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    with app.app_context():
        rows = Rented.query.all()
        for row in rows:
            db.session.delete(row)
        db.session.commit()
    response = client.get("/car_taking_list_late", headers={"Authorization": access_token})
    assert response.json["message"] == "There are no previous bookings which are pending!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_car_taken_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"booking_id": "1"}
    response = client.post("/car_taken", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Taken!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_taken_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": "1"}
    response = client.post("/car_taken", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_car_taken_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"booking_id": "100"}
    response = client.post("/car_taken", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "There are not bookings with this booking id!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_car_delivery_list_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    response = client.get("/car_delivery_list", headers={"Authorization": access_token})
    assert response.json["message"] == "Records fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_delivery_list_late_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    response = client.get("/car_delivery_list_late", headers={"Authorization": access_token})
    assert response.json["message"] == "Records fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_delivery_list_fail_no_bookings(client, db, user, app):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    with app.app_context():
        rows = Rented.query.all()
        for row in rows:
            db.session.delete(row)
        db.session.commit()
    response = client.get("/car_delivery_list", headers={"Authorization": access_token})
    assert response.json["message"] == "There are no car returns for today!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_car_delivery_list_late_fail_no_bookings(client, db, user, app):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    with app.app_context():
        rows = Rented.query.all()
        for row in rows:
            db.session.delete(row)
        db.session.commit()
    response = client.get("/car_delivery_list_late", headers={"Authorization": access_token})
    assert response.json["message"] == "There are no car returns for previous days!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_car_maintenance_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "2", "description": "desc"}
    response = client.post("/car_maintenance", headers={"Authorization": access_token},
                  data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Added to maintenance successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_car_maintenance_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": "2", "description": "desc"}
    response = client.post("/car_maintenance", headers={"Authorization": access_token},
                  data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_car_maintenance_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"car_id": "200", "description": "desc"}
    response = client.post("/car_maintenance", headers={"Authorization": access_token},
                  data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "There are no cars with this id!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_car_return_review_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"booking_id": "1", "said_date": "1", "said_time": "1", "proper_condition": "1",
            "fine": 0, "description": "desc"}
    response = client.post("/car_return_review", headers={"Authorization": access_token},
                  data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Car Return Reviewed Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_car_return_review_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"booking": "1", "said_date": "1", "said_time": "1", "proper_condition": "1",
            "fine": 0, "description": "desc"}
    response = client.post("/car_return_review", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_car_return_review_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"booking_id": "200", "said_date": "1", "said_time": "1", "proper_condition": "1",
            "fine": 0, "description": "desc"}
    response = client.post("/car_return_review", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "There are not bookings with this booking id!"
    assert response.json["status"] == "false"
    assert response.status_code == 404
