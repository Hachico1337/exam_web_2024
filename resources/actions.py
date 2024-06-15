from flask_restful import Api

from resources.routers import *
from .auth import *


def register_actions(app):
    api = Api(app)
    api.add_resource(AuthLogin, '/api/auth/login', strict_slashes=False)
    api.add_resource(RefreshToken, '/api/refresh', strict_slashes=False)
    api.add_resource(Books, '/api/books', strict_slashes=False)
    api.add_resource(WorkBook, '/api/book/<id>', strict_slashes=False)
    api.add_resource(UserInfo, '/api/user', strict_slashes=False)
    api.add_resource(WriteReview, '/api/review/<id>', strict_slashes=False)



