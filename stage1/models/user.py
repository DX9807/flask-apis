import sqlite3

class UserModel:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select = "SELECT * FROM users where username=?"
        res = cursor.execute(select,(username,))
        row = res.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user


    @classmethod
    def find_by_userid(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select = "SELECT * FROM users where id=?"
        res = cursor.execute(select,(_id,))
        row = res.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
