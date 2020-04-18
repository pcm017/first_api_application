from werkzeug.security import safe_str_cmp
from models.user import UserModel
import sqlite3


#username_query = 

# users = [
#     User(1,"Bob","asdf")
# ]

# #You create separate mapping so that you don't have to iterate the list above every time and can index directly.
# username_mapping = { u.username: u for u in users}

# userid_mapping = { u.id:u for u in users }

#Authenticate a user 
def authenticate(username,password):
    #.get method is beneficial it can send default value as well
    user = UserModel.find_by_username(username)
    if user and  safe_str_cmp(user.password,password):
        return user

#JWT 
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
