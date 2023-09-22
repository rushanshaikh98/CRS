import json

from testing.test_user import test_login_success


def test_home_success(client, db, user):
    response = client.get("/home")
    assert response.json["data"] == "Hello World!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_enter_dates_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    response = client.get("/profile", headers={"Authorization": access_token})
    assert response.json["message"] == "Data fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_profile_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"name": "Update Profile", "email": "updateprofile@gmail.com", "city": "AHMEDABAD",
            "username": "update_profile"}
    response = client.post("/update_profile", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Profile Updated Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_profile_fail_email_already_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"name": "Update Profile", "email": "user@gmail.com", "city": "AHMEDABAD",
            "username": "update_profile"}
    response = client.post("/update_profile", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "user with this email id already exists please choose different email"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_profile_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"nam": "Update Profile", "email": "updateprofile@gmail.com", "city": "AHMEDABAD",
            "username": "update_profile"}
    response = client.post("/update_profile", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_profile_fail_invalid_city(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"name": "Update Profile", "email": "updateprofile@gmail.com", "city": "AHMED",
            "username": "update_profile"}
    response = client.post("/update_profile", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This city does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_profile_fail_username_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"name": "user1", "email": "updateprofile@gmail.com", "city": "AHMEDABAD",
            "username": "user1"}
    response = client.post("/update_profile", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "user with this username already exists please choose different username"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_password_change_success(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"current_password": "Rushan@123", "new_password": "Rush@123"}
    response = client.post("/change_password", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Password changed successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_password_change_fail_incorrect_password(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"current_password": "Rushan@13", "new_password": "Rush@123"}
    response = client.post("/change_password", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "invalid current password"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_password_change_fail_invalid_password(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"current_password": "Rushan@123", "new_password": "Rush123"}
    response = client.post("/change_password", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Password should have at least one of the symbols $@#%! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_password_change_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    data = {"current_pass": "Rushan@13", "new_password": "Rush@123"}
    response = client.post("/change_password", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reset_request_success(client, db, user):
    data = {"email": "user@gmail.com"}
    response = client.post("/reset_request", data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Mail sent!"
    assert response.json["status"] == "true"
    assert response.status_code == 200
    return response.json['data']


def test_reset_request_fail_email_not_found(client, db, user):
    data = {"email": "user999@gmail.com"}
    response = client.post("/reset_request", data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Email does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_reset_request_fail_invalid_keys(client, db, user):
    data = {"emai": "user999@gmail.com"}
    response = client.post("/reset_request", data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reset_token_success(client, db, user):
    token = test_reset_request_success(client, db, user)
    data = {"token": f'{token}', "new_password": 'Rushan@123'}
    response = client.post("/reset_token", data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "The password is changed successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_reset_token_fail_invalid_token(client, db, user):
    data = {"token": "abcd", "new_password": 'Rushan@123'}
    response = client.post("/reset_token", data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "That is an invalid or expired token!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reset_token_fail_invalid_keys(client, db, user):
    data = {"token1": "abcd", "new_password": 'Rushan@123'}
    response = client.post("/reset_token", data=json.dumps(data), content_type="application/json")
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_decorator_super_admin_required(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    response = client.get("/admins_list", headers={"Authorization": access_token})
    assert response.json["message"] == "Super admin only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_decorator_admin_required(client, db, user):
    access_token = test_login_success(client, db, user, email="user@gmail.com", password="Rushan@123")
    response = client.get("/verify_users_list", headers={"Authorization": access_token})
    assert response.json["message"] == "Admin only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_decorator_user_required(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    response = client.get("/bookings", headers={"Authorization": access_token})
    assert response.json["message"] == "For users only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403


def test_decorator_user_verified(client, db, user):
    data = {"car_id": "2"}
    access_token = test_login_success(client, db, user, email="user3@gmail.com", password="Rushan@123")
    response = client.post("/book_car", headers={"Authorization": access_token}, content_type="application/json",
                           data=json.dumps(data))
    assert response.json["message"] == "For verified users only!"
    assert response.json["status"] == "false"
    assert response.status_code == 403
