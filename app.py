from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    login_manager.init_app(app)
    JWTManager(app)
    Migrate(app, db)
    db.init_app(app)
    mail.init_app(app)
    from users.routes import users
    from main.routes import main
    from admin.routes import admins
    from cars.routes import cars
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(admins)
    app.register_blueprint(cars)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
