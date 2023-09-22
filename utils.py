import os
import secrets
from flask import current_app
from PIL import Image
from flask_mail import Message
from app import mail


def save_picture(form_picture):
    """Method to save the documents submitted by the user. It takes an input as a se"""
    random_hex = secrets.token_hex(8)
    print(type(form_picture))
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    """
    Here first the picture path is saved in the folder and picture size is mentioned.
    """
    picture_path = os.path.join(current_app.root_path, 'static/id_proofs', picture_fn)
    # output_size = (500, 5000)
    picture = form_picture
    picture.save(picture_path)
    return picture_fn


def send_reset_email(user):
    """Method to send the reset password email"""
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''{token}'''
    mail.send(msg)
    return token
