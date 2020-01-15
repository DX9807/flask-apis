from flask import request,jsonify
from flask_restful import Resource,reqparse
from models.store import StoreModel


class Store(Resource):

    def get(self,name):
        store = StoreModel.query.filter_by(name = name).first()

        if store:
            return store.json()
        return {'message':'Store not found'}


    def post(self,name):

        store = StoreModel.query.filter_by(name = name).first()

        if store:
            return {'message':'Store already exists'}
        else:
            store = StoreModel(name)
            store.save_to_db()
        return store.json()

    def delete(self,name):
        store = StoreModel.query.filter_by(name = name).first()

        if not store:
            return {'message':name+' store not found'}
        else:
            store.delete_from_db()
        return {'message':'Store deleted'}



class StoreList(Resource):

    def get(self):
        stores = StoreModel.query.all()
        return {'stores':[store.json() for store in stores]}
