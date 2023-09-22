from flask import Blueprint
from main.resources import HomePage, Login, Profile, UpdateProfile, ChangePassword, ResetRequest, ResetToken

main = Blueprint("main", __name__)

main.add_url_rule("/", view_func=HomePage.as_view("home"))
main.add_url_rule("/home", view_func=HomePage.as_view("home_page"))
main.add_url_rule("/login", view_func=Login.as_view("login"))
main.add_url_rule("/profile", view_func=Profile.as_view("profile"))
main.add_url_rule("/update_profile", view_func=UpdateProfile.as_view("update_profile"))
main.add_url_rule("/change_password", view_func=ChangePassword.as_view("change_password"))
main.add_url_rule("/reset_request", view_func=ResetRequest.as_view("reset_request"))
main.add_url_rule("/reset_token", view_func=ResetToken.as_view("reset_token"))

