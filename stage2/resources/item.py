from flask import request,jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_claims,
                                get_jwt_identity,
                                jwt_optional,
                                fresh_jwt_required
                                )
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                       type=float,
                       required=True,help='This attribute cannot be left blank.'
                       )

    parser.add_argument('store_id',
                       type=float,
                       required=True,help='Every item needs to be stored in a particular store.'
                       )



    @jwt_required
    def get(self,name):
        item = ItemModel.find_item(name)
        return item.json(),200 if item else 404  #200 is for status OK
                                                   #404 for resource not found
    @fresh_jwt_required
    def post(self,name):
        item = ItemModel.find_item(name)
        if item:
            return {'message':'The item {} is already exists.'.format(name)},400   #400 for resource already exists.
        data = Item.parser.parse_args()
        item = ItemModel(name,**data)                                                                         #Bad request
        item.save_to_db()
        return item.json() ,201          #201 resource is created.

    @jwt_required
    def delete(self,name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin priviliges required'}

        item = ItemModel.find_item(name)

        if item:
            item.delete_from_db()
            return {'message':'Item deleted'}
        return {'message':'Item not found'}

    def put(self,name):
        item = ItemModel.find_item(name)

        data= Item.parser.parse_args()

        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()



class ItemList(Resource):
    @jwt_optional
    def get(self):
        current_user = get_jwt_identity()
        items = [x.json() for x in ItemModel.query.all()]

        if current_user:
            return items

        return {
                'items':[item['name'] for item in items],
                'message':'You need to login for more information.'
               }
