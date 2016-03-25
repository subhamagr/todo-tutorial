from jwt_helper import parse_token
from . import InvalidApiUsage
from app import login_manager
from app.schema import User
from flask import g


@login_manager.request_loader
def request_loader(request):
    print 'Inside'
    token = request.headers.get('Authorization')
    token_data = parse_token(token)
    if token_data:
        user = User.query.get(token_data['id'])
        g.user = user
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    raise InvalidApiUsage('Bad credentials', status_code=401, payload=None)
