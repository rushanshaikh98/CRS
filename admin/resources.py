from flask_restful import Resource
from flask import request, url_for
from flask_jwt_extended import jwt_required
from app import db, bcrypt
from models import User, City, CarCompany, Car, CarModels, CarCategories, UserVerification
from validations import Validators
from decorators import super_admin_required, admin_required
from flask_api import status


class CreateAdmins(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            error = Validators.validate_email(admin_json['email'])
            if len(error) > 0:
                return {"data": [],
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            error = Validators.validate_username(admin_json['username'])
            if len(error) > 0:
                return {"data": admin_json,
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            error = Validators.validate_password(admin_json['password'])
            if len(error) > 0:
                return {"data": [],
                        "message": f"{error}",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            city = City.query.filter_by(city=admin_json["city"].replace(" ", "").upper()).first()
            if not city:
                return {"data": [],
                        "message": "This city does not exist!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            hashed_password = bcrypt.generate_password_hash(admin_json['password']).decode('utf-8')
            admin_object = User(name=admin_json['name'], username=admin_json['username'], email=admin_json['email'],
                               password=hashed_password, city_id=city.id, is_admin=True)
            admin_object.save_to_db()
            return {"data": admin_json,
                    "message": "Admin Created Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class AddCity(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            city = City.query.filter_by(city=admin_json["city"].replace(" ", "").upper()).first()
            if city:
                return {"data": [],
                        "message": "This city already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            admin_object = City(city=admin_json['city'].replace(" ", "").upper())
            admin_object.save_to_db()
            return {"data": [],
                    "message": "City Added Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class AddCompany(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            company = CarCompany.query.filter_by(company_name=admin_json["company_name"].replace(" ", "").upper()).first()
            if company:
                return {"data": [],
                        "message": "This company already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            admin_object = CarCompany(company_name=admin_json['company_name'].replace(" ", "").upper())
            admin_object.save_to_db()
            return {"data": [],
                    "message": "Company Added Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class AddCategory(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            category = CarCategories.query.filter_by(category=admin_json["category"].replace(" ", "").upper()).first()
            if category:
                return {"data": [],
                        "message": "This category already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            admin_object = CarCategories(category=admin_json['category'].replace(" ", "").upper())
            admin_object.save_to_db()
            return {"data": [],
                    "message": "Category Added Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class AddModel(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            model = CarModels.query.filter_by(model_name=admin_json["model_name"].replace(" ", "").upper()).first()
            if model:
                return {"data": [],
                        "message": "This model already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            admin_object = CarModels(model_name=admin_json['model_name'].replace(" ", "").upper())
            admin_object.save_to_db()
            return {"data": [],
                    "message": "Model Added Successfully!",
                    "status": "true"
                    }, status.HTTP_201_CREATED
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class UpdateCity(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            city_id = City.query.filter_by(id=admin_json["id"]).first()
            if not city_id:
                return {"data": [],
                        "message": "City id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            city = City.query.filter_by(city=admin_json["city_name"].replace(" ", "").upper()).first()
            if city:
                return {"data": [],
                        "message": "City already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            city_id.city = admin_json["city_name"].replace(" ", "").upper()
            db.session.commit()
            return {"data": [],
                    "message": "City Updated Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class UpdateCompany(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            company_id = CarCompany.query.filter_by(id=admin_json["id"]).first()
            if not company_id:
                return {"data": [],
                        "message": "Company id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            company = CarCompany.query.filter_by(company_name=admin_json["company_name"].replace(" ", "").upper()).first()
            if company:
                return {"data": [],
                        "message": "Company already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            company_id.company_name = admin_json["company_name"].replace(" ", "").upper()
            db.session.commit()
            return {"data": [],
                    "message": "Company Updated Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class UpdateCategory(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            category_id = CarCategories.query.filter_by(id=admin_json["id"]).first()
            if not category_id:
                return {"data": [],
                        "message": "Category id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            category = CarCategories.query.filter_by(category=admin_json["category_name"].replace(" ", "").upper())\
                .first()
            if category:
                return {"data": [],
                        "message": "Category already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            category_id.category = admin_json["category_name"].replace(" ", "").upper()
            db.session.commit()
            return {"data": [],
                    "message": "Category Updated Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            print(err)
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class UpdateModel(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            model_id = CarModels.query.filter_by(id=admin_json["id"]).first()
            if not model_id:
                return {"data": [],
                        "message": "Model id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            model = CarModels.query.filter_by(model_name=admin_json["model_name"].replace(" ", "").upper())\
                .first()
            if model:
                return {"data": [],
                        "message": "Model already exists!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            model_id.model_name = admin_json["model_name"].replace(" ", "").upper()
            db.session.commit()
            return {"data": [],
                    "message": "Model Updated Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteCity(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            city_id = City.query.filter_by(id=admin_json["id"]).first()
            if not city_id:
                return {"data": [],
                        "message": "City id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            users = User.query.filter_by(city_id=admin_json["id"]).first()
            if users:
                return {"data": [],
                        "message": "City cannot be deleted as it has users!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            db.session.delete(city_id)
            db.session.commit()
            return {"data": [],
                    "message": "City Deleted Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteCompany(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            company_id = CarCompany.query.filter_by(id=admin_json["id"]).first()
            if not company_id:
                return {"data": [],
                        "message": "Company id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            cars = Car.query.filter_by(company_id=admin_json["id"]).first()
            if cars:
                return {"data": [],
                        "message": "Company cannot be deleted as our company owns some cars of this company",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            db.session.delete(company_id)
            db.session.commit()
            return {"data": [],
                    "message": "Company deleted Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteCategory(Resource):
    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            category_id = CarCategories.query.filter_by(id=admin_json["id"]).first()
            if not category_id:
                return {"data": [],
                        "message": "Category id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            cars = Car.query.filter_by(category_id=admin_json["id"]).first()
            if cars:
                return {"data": [],
                        "message": "Category cannot be deleted as our company owns some cars of this category!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            db.session.delete(category_id)
            db.session.commit()
            return {"data": [],
                    "message": "Category Deleted Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DeleteModel(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            model_id = CarModels.query.filter_by(id=admin_json["id"]).first()
            if not model_id:
                return {"data": [],
                        "message": "Model id does not exists!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            cars = Car.query.filter_by(model_id=admin_json["id"]).first()
            if cars:
                return {"data": [],
                        "message": "Model cannot be deleted as our company owns some cars of this model!",
                        "status": "false"
                        }, status.HTTP_400_BAD_REQUEST
            db.session.delete(model_id)
            db.session.commit()
            return {"data": [],
                    "message": "Model Deleted Successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class AdminList(Resource):
    decorators = [jwt_required(), super_admin_required()]

    def get(self):
        admins = {}
        admins_list = User.query.filter_by(is_admin=True).filter_by(is_super_admin=False).all()
        if not admins_list:
            return {"data": [],
                    "message": "There are no admins right now!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND
        for admin in admins_list:
            admins[admin.id] = {f"{admin.username}": f"{admin.email}"}
        return {"data": admins,
                "message": "Admins list fetched successfully!",
                "status": "true"
                }, status.HTTP_200_OK


class DeleteAdmin(Resource):

    decorators = [jwt_required(), super_admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            admin_id = User.query.filter_by(id=admin_json["id"]).\
                filter_by(is_admin=True).filter_by(is_super_admin=False).first()
            if not admin_id:
                return {"data": [],
                        "message": "Admin id does not exist!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            db.session.delete(admin_id)
            db.session.commit()
            return {"data": [],
                    "message": "Admin deleted successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class DisplayUsersForVerification(Resource):

    decorators = [jwt_required(), admin_required()]

    def get(self):
        user_requests = {}
        users_list = db.session.query(UserVerification, User).filter(UserVerification.user_id == User.id)\
            .filter(UserVerification.approval == "").all()
        if users_list:
            for user in users_list:
                user_requests[user.User.username] = {f"{user.User.email}": f"{user.UserVerification.id_proof}"}
            return {"data": user_requests,
                    "message": "Verification records fetched successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        else:
            return {"data": [],
                    "message": "No users left for verification!",
                    "status": "false"
                    }, status.HTTP_404_NOT_FOUND


class VerifyUser(Resource):

    decorators = [jwt_required(), admin_required()]

    def get(self):
        admin_json = request.get_json()
        try:
            user_ver = UserVerification.query.filter_by(user_id=admin_json['id'])\
                .filter(UserVerification.approval == "").first()
            if not user_ver:
                return {"data": [],
                        "message": "This user id has no requests for verification!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            user = User.query.filter_by(id=admin_json['id']).first()
            image_file = url_for('static', filename='id_proofs/' + user_ver.id_proof)
            return {"data": {"Name": f"{user.name}", "Username": f"{user.username}", "Email": f"{user.email}",
                    "id_proof": f"{image_file}"},
                    "message": "User verification record fetched successfully!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class AcceptUser(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            user_ver = UserVerification.query.filter_by(user_id=admin_json['id'])\
                .filter(UserVerification.approval == "").first()
            if not user_ver:
                return {"data": [],
                        "message": "This user id has no requests for verification!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            user = User.query.filter_by(id=admin_json['id']).first()
            user.is_verified = True
            user_ver.approval = "true"
            db.session.commit()
            return {"data": [],
                    "message": "User successfully verified!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST


class RejectUser(Resource):

    decorators = [jwt_required(), admin_required()]

    def post(self):
        admin_json = request.get_json()
        try:
            user_ver = UserVerification.query.filter_by(user_id=admin_json['id'])\
                .filter(UserVerification.approval == "").first()
            if not user_ver:
                return {"data": [],
                        "message": "This user id has no requests for verification!",
                        "status": "false"
                        }, status.HTTP_404_NOT_FOUND
            user_ver.approval = "false"
            db.session.commit()
            return {"data": [],
                    "message": "User successfully rejected!",
                    "status": "true"
                    }, status.HTTP_200_OK
        except (KeyError, AttributeError) as err:
            return {"data": [],
                    "message": "Please enter proper data",
                    "status": "false"
                    }, status.HTTP_400_BAD_REQUEST
