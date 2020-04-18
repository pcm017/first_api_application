import sqlite3
from flask_restful import Resource,Api, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field cannot be blank")
    parser.add_argument('password',type=str,required=True,help="This field cannot be blank")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'User already exists'},400
        else:
            user = UserModel(**data) #For each of the keys in data, username = value and password = value
            user.save_to_db()
            
            return {"message":"user has been created successfully"},201
