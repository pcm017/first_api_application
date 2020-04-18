from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate,identity
import requests

app = Flask(__name__)
# The secret key is used to sign the JWTs. That means that when the application receives the JWT, 
# it can check whether it was signed with the same secret key.
# If it was, it means that this app made that JWT, and therefore should accept it as valid (given that it is a valid JWT).
# If it wasn't, then it's some other app's JWT and we should reject it.
app.secret_key = 'pratik'
api = Api(app)

jwt = JWT(app,authenticate,identity)

items = []

#Item has inherited methods from Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',required=True,type=float,help='This field cannot be left blank')
    
    @jwt_required()
    def get(self,name):
        #Learn: next & filter --> Next is to be used to select the first item, Filter is to iterate a sequence
        item = next(filter(lambda x: x['name']==name,items),None)
        return {'item':item}, 200 if item else 404

    def post(self,name):
        if next(filter(lambda x: x['name']==name,items),None):
            return {'message':"An item with name '{}' already exists".format(name)}, 400
        #Request.get_json() picks up the body of the request.
        data = Item.parser.parse_args()
        #data = request.get_json()
        item = {'name':name,'price':data['price']}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name']!=name,items))
        return {'message':'item {} has been deleted'.format(name)}

    def put(self,name):
        #data = request.get_json()
        data = Item.parser.parse_args()
        item = next(filter(lambda x:x['name']==name,items),None)
        if item is None:
            item = {'name':name,'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        if not items:
            return {'items':None}, 404
        else:
            return {'items':items}

class testWhatsapp(Resource):
    def post(self):
        data = request.get_json()
        headers = {'api-key':'Aef70d5de137e365ebd28bd188c652dd4'}
        r = requests.post('https://api.kaleyra.io/v1/HXAP1661930066IN/messages',params=data,headers=headers)
        return {'response':r.text}
        


api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(testWhatsapp,'/message')

app.run(port=5000,debug=True)