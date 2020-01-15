from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_refresh_token_required
from flask_restful import Resource,reqparse
from models.user import UserModel


parser = reqparse.RequestParser()
parser.add_argument('username',type= str ,required=True,help='This attribute is must!')
parser.add_argument('password',type= str ,required=True,help='This attribute is must!')



class UserRegister(Resource):

    def post(self):

        data = parser.parse_args()
        username = data['username']

        user = UserModel.find_by_username(username)
        if user:
            return {'mesaage':'User already exists'}
        else:
            user= UserModel(data['username'],data['password'])
            user.save_to_db()
        return user.json()


class User(Resource):

    @classmethod
    def get(cls,user_id):

        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message':'User not found'},404
        return user.json()

    @classmethod
    def delete(cls,user_id):

        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message':'User not found'},404
        user.delete_from_db()
        return {'message':user.username+' deleted'}


class UserLogin(Resource):

    def post(self):

        data = parser.parse_args()
        username = data['username']

        user = UserModel.find_by_username(username)

        if user and user.username == data['username'] and user.password == data['password']:
            access_token = create_access_token(identity = user.id ,fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
               "access_token":access_token,
               "refresh_token":refresh_token
           },200
        return {
           "message":"Invalid credentials"
        }


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {'access_token':new_token}
