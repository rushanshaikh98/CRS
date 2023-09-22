import json

from models import UserVerification
from .test_user import test_login_success


def test_create_admin_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "abc@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                    "username": "user11"}
    response = client.post("/create_admins", headers={"Authorization": access_token},
                           data=json.dumps(data), content_type="application/json")
    assert response.json["data"] == data
    assert response.json["message"] == "Admin Created Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_create_admin_fail_email_already_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "admin@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                    "username": "user11"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Email is already taken! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_admin_fail_invalid_email(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                    "username": "user11"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Email address is not in proper format! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_admin_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"names": "abc", "email": "rushan@gmail.com", "password": "Abc@123", "city": "AHMEDABAD",
                     "username": "user11"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_admin_fail_invalid_city(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc@123", "city": "AHMED",
                    "username": "user11"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This city does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_admin_fail_invalid_password(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc123", "city": "AHMED",
                    "username": "user11"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Password should have at least one of the symbols $@#%! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_admin_fail_invalid_username(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc123", "city": "AHMED",
                    "username": "user 1"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Username cannot have spaces! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_create_admin_fail_username_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"name": "abc", "email": "rushan@gmail.com", "password": "Abc123", "city": "AHMED",
                    "username": "admin1"}
    response = client.post("/create_admins", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Username is already taken! "
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_city_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"city": "surat"}
    response = client.post("/add_city", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "City Added Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_add_city_fail_name_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"city": "ahmedabad"}
    response = client.post("/add_city", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This city already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_city_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"city1": "suzuki"}
    response = client.post("/add_city", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_company_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"company_name": "Honda"}
    response = client.post("/add_company", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Company Added Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_add_company_fail_name_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"company_name": "suzuki"}
    response = client.post("/add_company", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This company already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_company_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"company_ne": "suzuki"}
    response = client.post("/add_company", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_category_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"category": "SUV"}
    response = client.post("/add_category", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Category Added Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_add_category_fail_name_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"category": "HATCHBACK"}
    response = client.post("/add_category", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This category already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_category_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"category_ne": "suzuki"}
    response = client.post("/add_category", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_model_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"model_name": "Fortune"}
    response = client.post("/add_model", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Model Added Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 201


def test_add_model_fail_name_exists(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"model_name": "SWIFT"}
    response = client.post("/add_model", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This model already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_add_model_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"model_ne": "suzuki"}
    response = client.post("/add_model", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_city_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "city_name": "baroda"}
    response = client.post("/update_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "City Updated Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_city_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 5, "city_name": "baroda"}
    response = client.post("/update_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "City id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_city_fail_name_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "city_name": "ahmedabad"}
    response = client.post("/update_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "City already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_city_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "city_nam": "ahmedabad"}
    response = client.post("/update_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_company_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "company_name": "toyota"}
    response = client.post("/update_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Company Updated Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_company_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 11, "company_name": "suzuki"}
    response = client.post("/update_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Company id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_company_fail_name_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "company_name": "suzuki"}
    response = client.post("/update_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Company already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_company_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "company_nam": "ahmedabad"}
    response = client.post("/update_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_category_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "category_name": "suv"}
    response = client.post("/update_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Category Updated Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_category_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 12, "category_name": "suv"}
    response = client.post("/update_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Category id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_category_fail_name_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "category_name": "hatchback"}
    response = client.post("/update_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Category already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_category_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "category_nam": "ahmedabad"}
    response = client.post("/update_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_model_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "model_name": "fortune"}
    response = client.post("/update_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Model Updated Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_update_model_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 11, "model_name": "suv"}
    response = client.post("/update_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Model id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_update_model_fail_name_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "model_name": "swift"}
    response = client.post("/update_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Model already exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_update_model_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1, "model_nam": "ahmedabad"}
    response = client.post("/update_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_city_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 2}
    response = client.post("/delete_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "City Deleted Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_city_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.post("/delete_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "City id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_city_fail_has_users(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/delete_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "City cannot be deleted as it has users!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_city_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/delete_city", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_company_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 2}
    response = client.post("/delete_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Company deleted Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_company_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.post("/delete_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Company id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_company_fail_has_cars(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/delete_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Company cannot be deleted as our company owns some cars of this company"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_company_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/delete_company", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_category_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 2}
    response = client.post("/delete_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Category Deleted Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_category_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.post("/delete_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Category id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_category_fail_has_cars(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/delete_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Category cannot be deleted as our company owns some cars of this category!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_category_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/delete_category", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_model_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 2}
    response = client.post("/delete_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Model Deleted Successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_model_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.post("/delete_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Model id does not exists!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_model_fail_has_cars(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/delete_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Model cannot be deleted as our company owns some cars of this model!"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_delete_model_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/delete_model", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_get_admin_list_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    response = client.get("/admins_list", content_type="application/json", headers={"Authorization": access_token})
    assert response.json["message"] == "Admins list fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_get_admin_list_fail_no_admins(client, db, user, app):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    from models import User
    with app.app_context():
        admin_object = User.query.filter_by(id=1).first()
        db.session.delete(admin_object)
        db.session.commit()
    response = client.get("/admins_list", content_type="application/json", headers={"Authorization": access_token})
    assert response.json["message"] == "There are no admins right now!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_admin_success(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/delete_admin", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Admin deleted successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_delete_admin_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"id": 2}
    response = client.post("/delete_admin", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Admin id does not exist!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_delete_admin_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="superadmin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/delete_admin", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_get_verification_list_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    response = client.get("/verify_users_list", content_type="application/json",
                          headers={"Authorization": access_token})
    assert response.json["message"] == "Verification records fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_get_verification_list_fail_no_requests(client, db, user, app):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    with app.app_context():
        user_object = UserVerification.query.filter_by(id=1).first()
        db.session.delete(user_object)
        db.session.commit()
    response = client.get("/verify_users_list", headers={"Authorization": access_token})
    assert response.json["message"] == "No users left for verification!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_verify_user_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.get("/verify_user", data=json.dumps(data), content_type="application/json",
                          headers={"Authorization": access_token})
    assert response.json["message"] == "User verification record fetched successfully!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_verify_user_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.get("/verify_user", data=json.dumps(data), content_type="application/json"
                          , headers={"Authorization": access_token})
    assert response.json["message"] == "This user id has no requests for verification!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_verify_user_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.get("/verify_user", data=json.dumps(data), content_type="application/json",
                          headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_accept_user_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.post("/accept_user", data=json.dumps(data), content_type="application/json",
                          headers={"Authorization": access_token})
    assert response.json["message"] == "User successfully verified!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_accept_user_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/accept_user", data=json.dumps(data), content_type="application/json"
                          , headers={"Authorization": access_token})
    assert response.json["message"] == "This user id has no requests for verification!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_accept_user_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/accept_user", data=json.dumps(data), content_type="application/json"
                           , headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400


def test_reject_user_success(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": 3}
    response = client.post("/reject_user", data=json.dumps(data), content_type="application/json",
                          headers={"Authorization": access_token})
    assert response.json["message"] == "User successfully rejected!"
    assert response.json["status"] == "true"
    assert response.status_code == 200


def test_reject_user_fail_id_not_exist(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"id": 1}
    response = client.post("/reject_user", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "This user id has no requests for verification!"
    assert response.json["status"] == "false"
    assert response.status_code == 404


def test_reject_user_fail_invalid_keys(client, db, user):
    access_token = test_login_success(client, db, user, email="admin@gmail.com", password="Rushan@123")
    data = {"i": 1}
    response = client.post("/reject_user", data=json.dumps(data), content_type="application/json",
                           headers={"Authorization": access_token})
    assert response.json["message"] == "Please enter proper data"
    assert response.json["status"] == "false"
    assert response.status_code == 400
