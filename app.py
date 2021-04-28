import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json
import random

from auth.auth import AuthError, requires_auth

from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
def create_app():
    app = Flask(__name__)
    setup_db(app)

    # migrate = Migrate(app, db, compare_type=True)

    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,OPTIONS')
        return response

    # public view
    @app.route('/vehicles')
    def get_vehicles():
        vehicles = Vehicle.query.order_by(Vehicle.id).all()

        return jsonify({
            'success': True,
            'vehicles': [vehicle.format() for vehicle in vehicles]
        })
    # only salesrep, manager and owner have access
    @app.route('/vehicles', methods=['POST'])
    @requires_auth('post:vehicles')
    def add_vehicle(token):
        body = request.get_json()
        if body.get('make') == '' or body.get('model') == '':
            abort(422)

        try:
            new_vehicle = Vehicle(
                make=body['make'],
                model=body['model'],
                year=body['year'],
                color=body['color'])
            new_vehicle.insert()

            return jsonify({
                'success': True,
                'vehicle': new_vehicle.format()
            }), 200
        except:
            abort(400)

    # only salesrep, manager and owner have access
    @app.route('/vehicles/<vehicle_id>', methods=['PATCH'])
    @requires_auth('patch:vehicles')
    def update_vehicle(token, vehicle_id):
        body = request.get_json()
        make = body.get('make')
        model = body.get('model')
        year = body.get('year')
        color = body.get('color')

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
                'vehicle': vehicle.format()
            }), 200

        except:
            abort(400)

    # only manager and owner have access
    @app.route('/vehicles/<vehicle_id>', methods=['DELETE'])
    @requires_auth('delete:vehicles')
    def delete_vehicle(token, vehicle_id):
        vehicle = Vehicle.query.filter(Vehicle.id == vehicle_id).one()

        vehicle.delete()

        return jsonify({
            'success': True,
            'deleted-vehicle': vehicle.format()
        }), 200

    # only manager and owner have access
    @app.route('/sales')
    @requires_auth('get:sales')
    def get_sales(token):
        sales = Sale.query.order_by(Sale.id).all()

        return jsonify({
            'success': True, 
            'sales': [sale.format() for sale in sales]
            })

    # only manager or owner have access to this
    @app.route('/sales', methods=['POST'])
    @requires_auth('post:sales')
    def create_sale(token):
        body = request.get_json()
        if body.get('vehicle_id') == '' or body.get('customer_id') == '':
            abort(422)

        try:
            vehicle_id = body['vehicle_id']
            customer_id = body['customer_id']

            new_sale = Sale(
                vehicle_id = vehicle_id,
                customer_id = customer_id
            )

            new_sale.insert()

            return jsonify({
                'success': True,
                'sale_data': new_sale.format()
            }), 200
        
        except:
            abort(400)

    # # only owner has access to this
    # @app.route('/sales/<sale_id>', methods=['PATCH'])
    # def update_sale(sale_id):
    #     sale = Sale.query.filter(Sale.id == sale_id).one()

        
    # only owner has access to this
    @app.route('/sales/<sale_id>', methods=['DELETE'])
    @requires_auth('delete:sales')
    def delete_sale(token, sale_id):
        try:
            sale = Sale.query.filter(Sale.id == sale_id).one()
            if sale is None:
                abort(422)
            else: 
                sale.delete()
                return jsonify({
                    'success': True,
                    'sale_deleted': sale.format()
                }), 200
        except:
            abort(400)

    # only salesrep, manager and owner have access
    @app.route('/customers')
    @requires_auth('get:customers')
    def get_customers(token):
        customers = Customer.query.order_by(Customer.id).all()

        return jsonify({
            'success': True,
            'customers': [customer.format() for customer in customers]
        })

    # only salesrep, manager and owner have access
    @app.route('/customers', methods=['POST'])
    @requires_auth('post:customers')
    def create_customer(token):
        body = request.get_json()
        if body.get('first_name') == '' or body.get('last_name') == '':
            abort(422)

        try:
            new_customer = Customer(
                    first_name = body['first_name'],
                    last_name = body['last_name'],
                    phone_number = body['phone_number'],
                    address = body['address'],
                    city = body['city'],
                    state = body['state'],
                    zip_code = body['zip_code']
                )
            new_customer.insert()

            return jsonify({
                'success': True,
                'new_customer': new_customer.format()
            })
        except:
            abort(400)

    # only salesrep, manager and owner have access
    @app.route('/customers/<customer_id>', methods=['PATCH'])
    @requires_auth('patch:customers')
    def update_customer(token, customer_id):
        body = request.get_json()

        first_name = body.get('first_name')
        last_name = body.get('last_name')
        phone_number = body.get('phone_number')
        address = body.get('address')
        city = body.get('city')
        state = body.get('state')
        zip_code = body.get('zip_code')

        customer = Customer.query.filter(Customer.id == customer_id).one()

        if customer is None:
            abort(404)
        try:
            if first_name:
                customer.first_name = first_name
            if last_name:
                customer.last_name = last_name
            if phone_number:
                customer.phone_number = phone_number
            if address:
                customer.address = address
            if city:
                customer.city = city
            if state:
                customer.state = state
            if zip_code:
                customer.zip_code = zip_code
            
            customer.update()

            return jsonify({
                'success': True,
                'updated_customer': customer.format()
            }), 200

        except:
            abort(400)

    # only manager and owner can delete a customer
    @app.route('/customers/<customer_id>', methods=['DELETE'])
    @requires_auth('delete:customers')
    def delete_customer(token, customer_id):
        try:
            customer = Customer.query.filter(Customer.id == customer_id).one()

            if customer is None:
                abort(422)
            else:
                customer.delete()
                return jsonify({
                    'success': True,
                    'deleted_customer': customer.format()
                }), 200
        except:
            abort(400)
        
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method is not allowed'
        }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
    
    @app.errorhandler(AuthError)
    def hanle_auth_error(error):
        print(error)
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app

app = create_app()