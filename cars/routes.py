from flask import Blueprint
from cars.resources import CreateCars, UpdateCar, DeleteCar, BookCar, CarTakingList, CarTakingListLate, CarTaken, \
    CarDeliveryList, CarDeliveryListLate, CarReturnReview, CarMaintenance, PaymentSuccess, PaymentCancel

cars = Blueprint("cars", __name__)

cars.add_url_rule("/create_cars", view_func=CreateCars.as_view("create_cars"))
cars.add_url_rule("/update_car", view_func=UpdateCar.as_view("update_car"))
cars.add_url_rule("/delete_car", view_func=DeleteCar.as_view("delete_car"))
cars.add_url_rule("/book_car", view_func=BookCar.as_view("book_car"))
cars.add_url_rule("/car_taking_list", view_func=CarTakingList.as_view("car_taking_list"))
cars.add_url_rule("/car_taking_list_late", view_func=CarTakingListLate.as_view("car_taking_list_late"))
cars.add_url_rule("/car_taken", view_func=CarTaken.as_view("car_taken"))
cars.add_url_rule("/car_delivery_list", view_func=CarDeliveryList.as_view("car_delivery_list"))
cars.add_url_rule("/car_delivery_list_late", view_func=CarDeliveryListLate.as_view("car_delivery_list_late"))
cars.add_url_rule("/car_return_review", view_func=CarReturnReview.as_view("car_return_review"))
cars.add_url_rule("/car_maintenance", view_func=CarMaintenance.as_view("car_maintenance"))
cars.add_url_rule("/success", view_func=PaymentSuccess.as_view("success"))
cars.add_url_rule("/cancel", view_func=PaymentCancel.as_view("cancel"))
