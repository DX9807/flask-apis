from models.user import UserModel


def authenticate(username,password):
    user = UserModel.find_by_username(username)
    print(user)
    if user and user.password==password:
        return user
    return {'message':'User not found.'},404


def identity(payload):
    userid = payload['identity']
    return UserModel.find_by_userid(userid)
