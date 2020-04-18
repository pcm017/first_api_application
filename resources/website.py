from flask_restful import Resource,Api, reqparse
from flask import render_template, make_response
from models.item import ItemModel

class website(Resource):
    
    def get(self):
        items = ItemModel.get_all()
        itemList = [item.json() for item in items]
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("index.html",items= itemList),200,headers)