import json


def test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123"):

    login_data = {"email": f"{email}", "password": f"{password}"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Logged in Successfully"
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return f'Bearer {response.json["data"]["access_token"]}'


def test_login_invalid_keys(client, db, user):
    login_data = {"emails": "admin@gmail.com", "password": "Rushan@123"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_login_invalid_email(client, db, user):
    login_data = {"email": "admin123@gmail.com", "password": "abc"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "email doesn't exists"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_login_invalid_password(client, db, user):
    login_data = {"email": "admin@gmail.com", "password": "123"}
    response = client.post("/login", data=json.dumps(login_data), content_type="application/json")
    assert response.json["message"] == "Incorrect Password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_success(client, db, user):
    register_data = {"name": "abc", "email": "abc@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                     "username": "user11"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["data"] == register_data
    assert response.json["message"] == "User Register Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_registration_fail_email_already_exists(client, db, user):
    register_data = {"name": "abc", "email": "admin@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                     "username": "user11"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Email is already taken! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_email(client, db, user):
    register_data = {"name": "abc", "email": "@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                     "username": "user11"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Email address is not in proper format! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_keys(client, db, user):
    register_data = {"names": "abc", "email": "rushan@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                     "username": "user11"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_city(client, db, user):
    register_data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc@123", "city": "AHMED",
                     "username": "user11"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "This city does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_password(client, db, user):
    register_data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc123", "city": "AHMED",
                     "username": "user11"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Password should have at least one of the symbols $@#%! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_invalid_username(client, db, user):
    register_data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc123", "city": "AHMED",
                     "username": "user 1"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Username cannot have spaces! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_registration_fail_username_exists(client, db, user):
    register_data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc123", "city": "AHMED",
                     "username": "admin1"}
    response = client.post("/registration", data=json.dumps(register_data), content_type="application/json")
    assert response.json["message"] == "Username is already taken! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_verification_already_verified(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    response = client.post("/apply_verification", headers={"Authorization": access_token},
                           content_type="application/json")
    assert response.json["message"] == "Your are already verified!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_verification_wait_for_previous_review(client, db, user):
    access_token = test_login_success(client, db, user, email="user2@gmail.com", password="Rushan@123")
    response = client.post("/apply_verification", headers={"Authorization": access_token},
                           content_type="application/json")
    assert response.json["message"] == "Please wait for your previous request to be reviewed!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_verification_apply_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    fp = '/home/rushan/Downloads/Rushan_photo.jpg'
    response = client.post("/apply_verification", headers={"Authorization": access_token},
                           data={"file": open(fp, "rb")}, content_type="multipart/form-data")
    assert response.json["message"] == "Successfully Applied for verification!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_verification_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    fp = '/home/rushan/Downloads/Rushan_photo.jpg'
    response = client.post("/apply_verification", headers={"Authorization": access_token},
                           data={"image": open(fp, "rb")}, content_type="multipart/form-data")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_enter_dates_invalid_rent_from(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    date_data = {"rent_from": "2022/07/23", "rent_till": "2022/07/23", "city_delivery_id": 1}
    response = client.post("/taking_dates", headers={"Authorization": access_token},
                           data=json.dumps(date_data), content_type="application/json")
    assert response.json["message"] == "The date cannot be in the past!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_enter_dates_invalid_rent_till(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    date_data = {"rent_from": "2022/12/31", "rent_till": "2022/12/30", "city_delivery_id": 1}
    response = client.post("/taking_dates", headers={"Authorization": access_token},
                           data=json.dumps(date_data), content_type="application/json")
    assert response.json["message"] == "The rented till date cannot be less than the rented from date!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_enter_dates_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    date_data = {"rent_fro": "2022/07/27", "rent_till": "2022/07/26", "city_delivery_id": 1}
    response = client.post("/taking_dates", headers={"Authorization": access_token},
                           data=json.dumps(date_data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_enter_dates_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    date_data = {"rent_from": "2022/12/30", "rent_till": "2022/12/31", "city_delivery_id": 1}
    response = client.post("/taking_dates", headers={"Authorization": access_token},
                           data=json.dumps(date_data), content_type="application/json")
    assert response.json["message"] == "Dates entered successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_bookings_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    response = client.get("/bookings", headers={"Authorization": access_token})
    assert response.json["message"] == "Booking records fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_bookings_fail_no_bookings(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    response = client.get("/bookings", headers={"Authorization": access_token})
    assert response.json["message"] == "No Booking records for this user!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_cancel_booking_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "1"}
    response = client.post("/cancel_booking", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Booking cancelled successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_cancel_booking_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking": "1"}
    response = client.post("/cancel_booking", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_cancel_booking_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "100"}
    response = client.post("/cancel_booking", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "No booking with this booking id for this user!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_cancel_booking_fail_date_passed(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "2"}
    response = client.post("/cancel_booking", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "You cannot cancel the booking at this time!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_pay_fine_success(client, db, user, mocker):
    mocker.patch('users.resources.stripe.PaymentIntent.create', return_value={'url': 'cars'})
    mocker.patch('users.resources.stripe.checkout.Session.create', return_value={'url': 'cars'})
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "1"}
    response = client.post("/pay_fine", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "click on following link to complete the payment"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_pay_fine_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking": "1"}
    response = client.post("/pay_fine", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_pay_fine_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "100"}
    response = client.post("/pay_fine", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "No booking with this booking id!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_fine_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "1"}
    response = client.get("/fine_success", headers={"Authorization": access_token},
                        data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Fine paid successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_fine_cancel(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    data = {"booking_id": "1"}
    response = client.get("/fine_cancel", headers={"Authorization": access_token},
                        data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Payment Cancelled. Please try again!"
    assert response.json["status"] == "true"
    assert response.status_code == 200
