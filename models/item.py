from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.String(80))

    store_id = db.Column(db.Integer,db.ForeignKey('stores.id')) #Stores which is table name and id which is column Name
    store = db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name,'price':self.price}

    @classmethod 
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #### Because it is going to return an ItemModel instead of dict

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self): #Renamed to save_to_db since it doesn't insert but just saves it
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect("mydatabase.db")
        # cursor = connection.cursor()
        
        # query = "INSERT INTO items VALUES (?,?)"
        # cursor.execute(query,(self.name,self.price))
        
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def updateItem(self):
    #     connection = sqlite3.connect("mydatabase.db")
    #     cursor = connection.cursor()
        
    #     query = "UPDATE items SET price = ? WHERE name =?;"
    #     cursor.execute(query,(self.price,self.price,))
        
    #     connection.commit()
    #     connection.close()
