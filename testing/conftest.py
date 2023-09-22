import os

from app import bcrypt
import pytest
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import User, City, UserVerification, CarCompany, CarCategories, CarModels, Car, Rented, Temporary
import datetime
load_dotenv()


@pytest.fixture(scope="session")
def app():
    from app import create_app

    return create_app()


@pytest.fixture(scope="function", autouse=True)
def db(app):
    from app import db
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['TESTING'] = True

    db.init_app(app)
    print("-------Creating Tables------")
    with app.app_context():
        db.create_all(app=app)
    Migrate(app, db)
    db.init_app(app)
    yield db
    print("-------Dropping Tables------")
    with app.app_context():
        db.drop_all(app=app)


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def user(app, db):
    with app.app_context():
        city_object = City(city="AHMEDABAD")
        city_object.save_to_db()
        city_object = City(city="DIU")
        city_object.save_to_db()
        password = bcrypt.generate_password_hash("Rushan@123").decode('utf-8')
        user_object = User(name="Admin", username="admin1", email="admin@gmail.com", password=password,
                           city_id=1, is_admin=True)
        user_object.save_to_db()
        user_object = User(name="User", username="user1", email="user@gmail.com", password=password,
                           city_id=1, is_verified=True)
        user_object.save_to_db()
        user_object = User(name="User", username="user2", email="user2@gmail.com", password=password,
                          city_id=1)
        user_object.save_to_db()
        user_object = User(name="User", username="user3", email="user3@gmail.com", password=password,
                           city_id=1)
        user_object.save_to_db()
        user_object = User(name="User", username="user4", email="user4@gmail.com", password=password,
                           city_id=1, is_verified=True)
        user_object.save_to_db()
        user_object = User(name="User", username="user5", email="user5@gmail.com", password=password,
                           city_id=1, is_verified=True)
        user_object.save_to_db()
        user_object = User(name="User", username="user6", email="user6@gmail.com", password=password,
                           city_id=1, is_verified=True)
        user_object.save_to_db()
        user_object = User(name="User", username="user7", email="user7@gmail.com", password=password,
                           city_id=1, is_verified=True, fine_pending=True)
        user_object.save_to_db()
        user_object = User(name="SuperAdmin", username="super_admin", email="superadmin@gmail.com", password=password,
                           city_id=1, is_admin=True, is_super_admin=True)
        user_object.save_to_db()
        row = UserVerification(user_id=3, id_proof="default.jpg", approval="", date=datetime.date.today())
        db.session.add(row)
        db.session.commit()
        company_object = CarCompany(company_name="SUZUKI")
        company_object.save_to_db()
        company_object = CarCompany(company_name="MINI")
        company_object.save_to_db()
        category_object = CarCategories(category="HATCHBACK")
        category_object.save_to_db()
        category_object = CarCategories(category="SMALL")
        category_object.save_to_db()
        model_object = CarModels(model_name="SWIFT")
        model_object.save_to_db()
        model_object = CarModels(model_name="COOPER")
        model_object.save_to_db()
        car_object = Car(car_id="GJ27EX9709", company_id=1, category_id=1,  model_id=1, color="WHITE", mileage=11,
                         ppd=1000, min_rent=1200, deposit=5000, city_id=1)
        car_object.save_to_db()
        car_object = Car(car_id="GJ27EX1", company_id=1, category_id=1, model_id=1, color="WHITE", mileage=11,
                         ppd=1000, min_rent=1200, deposit=5000, city_id=1)
        car_object.save_to_db()
        rent_object = Rented(carID=1, user_id=2, booking_time=datetime.date.today(),
                             rented_from="2022/12/30", rented_till="2022/12/31", city_taken_id=1, city_delivery_id=1,
                             fine=100)
        db.session.add(rent_object)
        db.session.commit()
        rent_object = Rented(carID=1, user_id=2, booking_time=datetime.date.today(),
                             rented_from=datetime.date.today(),
                             rented_till=datetime.date.today()+datetime.timedelta(days=2),
                             city_taken_id=1, city_delivery_id=1)
        db.session.add(rent_object)
        db.session.commit()
        rent_object = Rented(carID=1, user_id=6, booking_time=datetime.date.today(),
                             rented_from=datetime.date.today() - datetime.timedelta(days=2),
                             rented_till=datetime.date.today() + datetime.timedelta(days=2),
                             city_taken_id=1, city_delivery_id=1)
        db.session.add(rent_object)
        db.session.commit()
        rent_object = Rented(carID=1, user_id=7, booking_time=datetime.date.today(),
                             rented_from=datetime.date.today() - datetime.timedelta(days=2),
                             rented_till=datetime.date.today(),
                             city_taken_id=1, city_delivery_id=1, car_taken=True)
        db.session.add(rent_object)
        rent_object = Rented(carID=1, user_id=6, booking_time=datetime.date.today(),
                             rented_from=datetime.date.today() - datetime.timedelta(days=2),
                             rented_till=datetime.date.today() - datetime.timedelta(days=1),
                             city_taken_id=1, city_delivery_id=1, car_taken=True)
        db.session.add(rent_object)
        db.session.commit()
        temp_object = Temporary(user_id=2, rent_from="2022/12/30", rent_till="2022/12/31", city_id=1)
        db.session.add(temp_object)
        db.session.commit()
        temp_object = Temporary(user_id=5, rent_from="2022/5/20", rent_till="2022/5/22", city_id=1)
        db.session.add(temp_object)
        db.session.commit()
        temp_object = Temporary(user_id=8, rent_from="2022/12/30", rent_till="2022/12/31", city_id=1)
        db.session.add(temp_object)
        db.session.commit()
        temp_object = Temporary(user_id=7, rent_from="2022/12/20", rent_till="2022/12/22", city_id=1)
        db.session.add(temp_object)
        db.session.commit()
        return user_object
