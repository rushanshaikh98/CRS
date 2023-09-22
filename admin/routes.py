from flask import Blueprint
from admin.resources import CreateAdmins, AddCity, AddCompany, AddCategory, AddModel, UpdateModel, UpdateCompany, \
    UpdateCategory, UpdateCity, DeleteCity, DeleteCompany, DeleteCategory, DeleteModel, AdminList, DeleteAdmin, \
    DisplayUsersForVerification, VerifyUser, AcceptUser, RejectUser

admins = Blueprint("admins", __name__)

admins.add_url_rule("/create_admins", view_func=CreateAdmins.as_view("create_admins"))
admins.add_url_rule("/add_city", view_func=AddCity.as_view("add_city"))
admins.add_url_rule("/add_company", view_func=AddCompany.as_view("add_company"))
admins.add_url_rule("/add_category", view_func=AddCategory.as_view("add_category"))
admins.add_url_rule("/add_model", view_func=AddModel.as_view("add_model"))
admins.add_url_rule("/update_city", view_func=UpdateCity.as_view("update_city"))
admins.add_url_rule("/update_company", view_func=UpdateCompany.as_view("update_company"))
admins.add_url_rule("/update_category", view_func=UpdateCategory.as_view("update_category"))
admins.add_url_rule("/update_model", view_func=UpdateModel.as_view("update_model"))
admins.add_url_rule("/delete_city", view_func=DeleteCity.as_view("delete_city"))
admins.add_url_rule("/delete_company", view_func=DeleteCompany.as_view("delete_company"))
admins.add_url_rule("/delete_category", view_func=DeleteCategory.as_view("delete_category"))
admins.add_url_rule("/delete_model", view_func=DeleteModel.as_view("delete_model"))
admins.add_url_rule("/admins_list", view_func=AdminList.as_view("admins_list"))
admins.add_url_rule("/delete_admin", view_func=DeleteAdmin.as_view("delete_admin"))
admins.add_url_rule("/verify_users_list", view_func=DisplayUsersForVerification.as_view("verify_users_list"))
admins.add_url_rule("/verify_user", view_func=VerifyUser.as_view("verify_user"))
admins.add_url_rule("/accept_user", view_func=AcceptUser.as_view("accept_user"))
admins.add_url_rule("/reject_user", view_func=RejectUser.as_view("reject_user"))
