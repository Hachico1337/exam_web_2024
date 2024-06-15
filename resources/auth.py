from flask_restful import Resource
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from database.models import Users


class AuthLogin(Resource):
    def post(self):
        try:
            login = request.form.get('login')
            password = request.form.get('password')
            user = Users.find_by_login(login)
            if not user or not check_password_hash(user.password_hash, password):
                return make_response(jsonify({'message': 'not correct data'}), 401)
            else:
                token = create_access_token(identity=user.id)
                return make_response(jsonify({'message': 'success', 'token': token}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}))


class RefreshToken(Resource):
    """
    обновление токена авторизации
    """
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        token = create_access_token(identity=user)
        return make_response(jsonify({'message': 'success', 'access_token': token}), 200)
