from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

def new_access_token(public_id):
    return create_access_token(identity=public_id)

def new_refresh_token(public_id):
    return create_refresh_token(identity=public_id)


class ValidateToken(Resource):
    @jwt_required()
    def post(self):
        return {"response": "success", "message": "Access token is valid"}, 200


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        return {"response": "success", "access_token": str(new_access_token(get_jwt_identity()))}, 200