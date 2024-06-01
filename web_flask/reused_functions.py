#!/usr/bin/env python3
"""Contains functions that are reused in different modules of the app"""

from datetime import datetime
import random
import string
from flask_mail import Message

def time_diff_from_now(timestamp):
    """
    Calculates the time difference between the current
    time and a given timestamp
    """
    datetime_obj = datetime.fromisoformat(timestamp)
    current_datetime = datetime.utcnow()
    time_diff = current_datetime - datetime_obj
    return time_diff.total_seconds()


def generate_verification_code(length=6):
    """ generate an email verifictaion code """
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.digits,
                                  k=length))


def send_code(email, verification_code, message, f_app):
    """ send the email verification code """
    msg = Message('Verification ePermit',
                sender='chiegody254@gmail.com',
                recipients=[email])
    msg.body = f'{message}: {verification_code}'
    f_app.extensions['mail'].send(msg)
