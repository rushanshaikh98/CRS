from flask import Blueprint
from .resources import Registration, ApplyForVerification, EnterDates, Bookings, CancelBooking, PayFine, \
    FinePaymentSuccess, FinePaymentCancel

users = Blueprint("users", __name__)

users.add_url_rule("/registration", view_func=Registration.as_view("registration"))
users.add_url_rule("/apply_verification", view_func=ApplyForVerification.as_view("apply_verification"))
users.add_url_rule("/taking_dates", view_func=EnterDates.as_view("taking_dates"))
users.add_url_rule("/bookings", view_func=Bookings.as_view("bookings"))
users.add_url_rule("/cancel_booking", view_func=CancelBooking.as_view("cancel_booking"))
users.add_url_rule("/pay_fine", view_func=PayFine.as_view("pay_fine"))
users.add_url_rule("/fine_success", view_func=FinePaymentSuccess.as_view("fine_success"))
users.add_url_rule("/fine_cancel", view_func=FinePaymentCancel.as_view("fine_cancel"))
