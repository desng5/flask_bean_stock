from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app import db
from datetime import datetime
from app.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify(email, password):
    user = db.session.execute(db.Select(User).where(User.email==email)).scalars().one_or_none()
    if user is not None and user.check_password(password):
        return user
    return None

@basic_auth.error_handler
def handle_error(status):
    return {'error': 'Incorrect email and/or password'}, status

@token_auth.verify_token
def verify(token):
    user = db.session.execute(db.select(User).where(User.token == token)).scalars().one_or_none()
    if user is not None and user.token_expiration > datetime.utcnow():
        return user
    return None

@token_auth.error_handler
def handle_error(status):
    return {'error': 'Invalid or expired token'}, status