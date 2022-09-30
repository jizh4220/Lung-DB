
from flask import request
from flask_jwt_extended import create_access_token
from app import db
from app.user import user_bp
from app.user.models import User
from app.user.schema import UserSchema
from app.utils.responses import response_with
from app.utils import responses as resp


@user_bp.route('/register', methods=['POST'])
def create_user():
    """
    User Registration Route
    ---
    parameters:
        - in: body
          name: body
          schema:
            required:
                - username
                - password
            properties:
                username:
                    type: string
                    description: username
                    default: ""
                password:
                    type: string
                    description: password
                    default: ""
    responses:
        201:
            description: registration succeeded
            schema:
                properties:
                    code:
                        type: string
        422:
            description: registration failed
            schema:
                properties:
                    code:
                        type: string
                    message:
                        type: string
    """
    try:
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        user_schema = UserSchema()
        user = user_schema.load(data)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201)
    except:
        return response_with(resp.INVALID_INPUT_422)

@user_bp.route('/login',methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password'],current_user.password):
            access_token = create_access_token(identity=data['username'])
            return response_with(resp.SUCCESS_201,value={'message':'Logged in as {}'.format(current_user.username),"access_token":access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except:
        return response_with(resp.INVALID_INPUT_422)