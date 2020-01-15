from flask import request,jsonify
from flask_restful import Resource,reqparse
import sqlite3
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                       type=float,
                       required=True,help='This attribute cannot be left blank.'
                       )


    @jwt_required()
    def get(self,name):
        item = ItemModel.find_item(name)
        return item.json(),200 if item else 404  #200 is for status OK
                                                   #404 for resource not found

    def post(self,name):
        item = ItemModel.find_item(name)
        if item:
            return {'message':'The item {} is already exists.'.format(name)},400   #400 for resource already exists.
        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'])                                                                         #Bad request
        item.insert()
        return item.json() ,201          #201 resource is created.

    def delete(self,name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_query= "DELETE from items where name=?"
        cursor.execute(delete_query,(name,))

        connection.commit()
        connection.close()

        return {'mesage':'Item has been deleted.'}

    def put(self,name):
        item = ItemModel.find_item(name)
        data= Item.parser.parse_args()
        updated_item = ItemModel(name,data['price'])
        if item is None:
            updated_item.insert()
        else:
            updated_item.update()
        return updated_item.json()



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        res = cursor.execute(query)
        items = res.fetchall()

        return {'items':items},200
