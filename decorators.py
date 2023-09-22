from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User
from flask_api import status


def super_admin_required():
    """ A decorator for checking whether a user is super admin or not"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.filter_by(id=get_jwt_identity()).first()
            if user.is_super_admin:
                return fn(*args, **kwargs)
            else:
                return {"data": [],
                        "message": "Super admin only!",
                        "status": "false"
                        }, status.HTTP_403_FORBIDDEN
        return decorator
    return wrapper


def admin_required():
    """ A decorator for checking whether a user is admin or not"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.filter_by(id=get_jwt_identity()).first()
            if user.is_admin:
                return fn(*args, **kwargs)
            else:
                return {"data": [],
                        "message": "Admin only!",
                        "status": "false"
                        }, status.HTTP_403_FORBIDDEN
        return decorator
    return wrapper


def user_required():
    """ A decorator for checking whether a user is normal user or not"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.filter_by(id=get_jwt_identity()).first()
            if not user.is_super_admin and not user.is_admin:
                return fn(*args, **kwargs)
            else:
                return {"data": [],
                        "message": "For users only!",
                        "status": "false"
                        }, status.HTTP_403_FORBIDDEN
        return decorator
    return wrapper


def user_verified():
    """ A decorator for checking whether a user is verified or not"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.filter_by(id=get_jwt_identity()).first()
            if user.is_verified:
                return fn(*args, **kwargs)
            else:
                return {"data": [],
                        "message": "For verified users only!",
                        "status": "false"
                        }, status.HTTP_403_FORBIDDEN
        return decorator
    return wrapper
