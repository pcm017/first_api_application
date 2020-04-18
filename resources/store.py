from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):


    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Store not found'},404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message':'Store already exists'},400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {'message':'An internal server error occurred'},400
            return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':'Store Deleted'}
    
class StoreList(Resource):
    
    def get(self):
        stores = StoreModel.query.all()
        return {'stores':[store.json() for store in stores]}

