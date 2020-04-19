import os #Access to OS environment variable

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.website import website
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///mydatabase.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
# The secret key is used to sign the JWTs. That means that when the application receives the JWT, 
# it can check whether it was signed with the same secret key.
# If it was, it means that this app made that JWT, and therefore should accept it as valid (given that it is a valid JWT).
# If it wasn't, then it's some other app's JWT and we should reject it.
app.secret_key = 'pratik'
api = Api(app)

jwt = JWT(app,authenticate,identity)

#Item has inherited methods from Resource

api.add_resource(StoreList,'/stores')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/createUser')
api.add_resource(website,'/')

if __name__ == "__main__":
    
    db.init_app(app)
    app.run(port=5000,debug=True)