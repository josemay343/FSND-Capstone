import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_name = 'dealership'
# database_path = "postgresql://{}@{}/{}".format(
#     'yosef', 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JSON_SORT_KEYS'] = False
    db.app = app
    db.init_app(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    year = db.Column(db.Integer)
    color  = db.Column(db.String)
    vehicle = db.relationship('Sale', cascade='all,delete-orphan', backref='vehicle', lazy=True)

    # def __repr__(self):
    #     return f'<Vehicle ID: {self.id}, Make: {self.make}, Year: {self.year}>'
    def __init__(self, make, model, year, color):
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    def insert(self):
        db.session.add(self)
        db.session.commit()  

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color
        }
        
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    customer = db.relationship('Sale', cascade='all,delete-orphan', backref='customer', lazy=True)


    def __repr__(self):
        return f'Customer ID: {self.id}, First name: {self.first_name}, Phone#: {self.phone_number}'

    def insert(self):
        db.session.add(self)
        db.session.commit()  

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code
        }
class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def __repr__(self):
        return f'Sale ID: {self.id}, Vehicle ID: {self.vehicle_id}, Customer ID: {self.customer_id}'

    def insert(self):
        db.session.add(self)
        db.session.commit()  

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'sale_id': self.id,
            'customer_id': self.customer_id,
            'vehicle_id': self.vehicle_id,
        }