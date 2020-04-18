from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    #The below is applicable only for POST and PUT methods
    parser = reqparse.RequestParser()
    
    parser.add_argument('price',required=True,type=float,help='This field cannot be left blank')
    parser.add_argument('store_id',required=True,type=int,help='Every item needs a store id')
    
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404
        #Learn: next & filter --> Next is to be used to select the first item, Filter is to iterate a sequence

    def post(self,name):
        data = Item.parser.parse_args()
        if StoreModel.find_by_id(data['store_id']) and ItemModel.find_by_name(name): #Dedupe at Item Level is okay, but dedupe at Store and Item Level
            return {'message':"An item with name '{}' already exists for the store".format(name)}, 400
        
      
        
        item = ItemModel(name,**data)
        
        try:
            item.save_to_db()
        except:
            return {"message":"An internal server error occurred"}, 500
        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message':'Item {} has been deleted from the database'.format(name)}


    def put(self,name):
        data = Item.parser.parse_args()
        
        #item = ItemModel[]
        
        item = ItemModel.find_by_name(name)
        #Now the Item above will have the properties of ItemModel 
        #It can be select by {Item.Price}
        if item:
                item.price = data['price']
        else:
                item = ItemModel(name,**data)
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        items = ItemModel.get_all()
        return {'items': [item.json() for item in items] }#Items JSONS
        #Second Method
        #return {'items': list(map(lambda x: x.json(),items))}

