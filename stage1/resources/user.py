import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type= str ,required=True,help='This attribute is must!')
    parser.add_argument('password',type= str ,required=True,help='This attribute is must!')


    def post(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        user = UserRegister.parser.parse_args()
        username = user['username']

        if UserModel.find_by_username(username):
            return {'message':'User already exists!'},401

        insert_query = "INSERT INTO users VALUES (Null,?,?)"
        cursor.execute(insert_query,(user['username'],user['password']))
        connection.commit()
        connection.close()
        return user
