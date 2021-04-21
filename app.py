import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json
import random

from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
setup_db(app)

migrate = Migrate(app, db, compare_type=True)

cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/vehicles')
def get_vehicles():
    vehicles = Vehicle.query.order_by(Vehicle.id).all()

    return jsonify({
        'success': True,
        'vehicles': [vehicle.format() for vehicle in vehicles]
    })

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    vehicle_data = request.get_json()

    make = vehicle_data['make']
    model = vehicle_data['model']
    year = vehicle_data['year']
    color = vehicle_data['color']

    new_vehicle = Vehicle(
        make=make,
        model=model,
        year=year,
        color=color)
    new_vehicle.insert()

    return jsonify({
        'success': True,
        'vehicle': [new_vehicle.format()]
    })

@app.route('/vehicles/<vehicle_id>', methods=['PATCH'])
def update_vehicle(vehicle_id):
    body = request.get_json()
    print(body.get('make'))
    make = body.get('make')
    model = body.get('model')
    year = body.get('year')
    color = body.get('color')
    print(make)
    vehicle = Vehicle.query.filter(Vehicle.id == vehicle_id).one()

    if vehicle is None:
        abort(404)
    try:
        if make:
            vehicle.make = make
        if model:
            vehicle.model = model
        if year:
            vehicle.year = year
        if color:
            vehicle.color = color
        
        vehicle.update()
        return jsonify({
            'success': True,
            'vehicle': [vehicle.format()]
        }), 200

    except:
        abort(400)

@app.route('/sales')
def get_sales():
    sales = Sale.query.order_by(Sale.id).all()

    return jsonify({
        'success': True, 
        'sales': [sale.format() for sale in sales]
        })

@app.route('/customers')
def get_customers():
    customers = Customer.query.order_by(Customer.id).all()

    return jsonify({
        'success': True,
        'customers': [customer.format() for customer in customers]
    })

if __name__ == '__main__':
    app.run()