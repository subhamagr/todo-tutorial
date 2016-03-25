import jwt
from datetime import datetime
from .. import app


def create_token(user_id):
    payload = {
        'id': user_id,
        'exp': datetime.utcnow() + app.config['TOKEN_EXPIRY'],
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
        return data
    except Exception:
        return None
