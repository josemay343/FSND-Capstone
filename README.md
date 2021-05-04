# City Cars Dealership API Backend

## Motivation for project

The dealership API utilizes the skills learned throughout the Udacity FullStack Web Developer nanodegree which covered the following areas:
- SQL and Data Modeling for the Web
- API developement and Documentation
- Identity and Access Management
- Server Deployment, Containerization and Testing

This project served as a foundation in understanding backend architectures.

Application is running on Heroku at: https://dealership.herokuapp.com/

## Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

Before going any further, please check that you have Python installed by running the command:
```bash
python --version
```

Also, make sure you have PIP installed by running the command:
```bash
pip --version
```

## Virtual Enviornment

It is good practice and recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Using Virtualenv: virtualenv is a tool to create isolated Python environments.

To install run the command:
```bash
pip install virtualenv
```
Verify the installation:
```bash
virtualenv --version
```

Basic Usage:
To create a virtual environment, navigate to the desired project directory and run the command:
```bash
virtualenv venv
```
In this case `venv` is the name of your virtual environment and it can be anything depending on your needs.
`virtualenv venv` will create a new folder `venv` within your current directory and will contain all python files and any other packages that you have installed with pip.

Once the virtualenv has been created, it needs to be activated by using the command:
```bash
source venv/bin/activate
```

Once this is setup, any package that you installed will be placed within this isolated python environment

`Note`: when you are done working with the virtualenv, run the command below to deactivate:
```bash
deactivate
```

## PIP Dependencies

Once you have your virtual environment up and running, install dependencies by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server (Locally)

From within the project directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

Setting the FLASK_ENV to `development` will enable debug mode and flask run will enable the interactive debugger and reloader. The reloader will detect any file changes and automatically restart the server.

To run the server, execute:

```bash
flask run
```

The `setup.sh` file contains all enviroment variables required by the app.
run the command within the project directory to load the variables:

```bash
source setup.sh
```

### Testing the API endpoints(Locally)

From the project directory, run the command:

```bash
dropdb dealership_test
createdb dealership_test
psql dealership_test < dealership.psql
python test_app.py
```
Test the endpoints via CURL or Postman at http://127.0.0.1:5000/

## Running the server(Heroku)

The app is live on Heroku at: https://dealership.herokuapp.com/

### Testing the API endpoints(Heroku)

Use CURL or Postman to test the endpoints on Heroku at: https://dealership.herokuapp.com/

## API

### Vehicle Endpoints

#### `GET /vehicles`
- Fetches a list of all vehicles. If no vehicles on database, return an emtpy array.
- Request Arguments: None
- Permissions: None, public access
- Response body:
    - Status code 200 and json `{'success': True,'vehicles': [vehicles]}` where vehicles is a list containing all vehicles in the database or status code with details of failure.

#### `POST /vehicles`
- Creates a new vehicle and stores it in the database. Returns a 400 if the body passed is incorrect.
- Request Arguments:
    - `'make'`: A string for the make of the vehicle, e.g., Honda, Toyota, etc...
    - `'model'`: A string for the model of the vehicle, e.g., Civic, Corolla, etc...
    - `'year'`: An integer for the vehicle manufactured year.
    - `'color'`: A string for the vehicle's color.
- Permissions:
    - `'post:vehicles'`
- Response body:
    - Status code 200 and json `{'success': True, 'vehicle': new_vehicle}` where vehicle is an array for the recently created vehicle or status code with details of failure.

#### `PATCH /vehicles/<vehicle_id>`
- Updates an existing vehicle. Returns 404 if `<vehicle_id>` is not found.
- Request Arguments, at least one has to be passed:
    - `'make'`: A string for the make of the vehicle, e.g., Honda, Toyota, etc...
    - `'model'`: A string for the model of the vehicle, e.g., Civic, Corolla, etc...
    - `'year'`: An integer for the vehicle manufactured year.
    - `'color'`: A string for the vehicle's color.
- Permissions:
    - `'patch:vehicles'`
- Response body:
    - Status code 200 and json `{'success': True, 'vehicle': vehicle}` where vehicle is an array for the recently updated vehicle or status code with details of failure.

#### `DELETE /vehicles/<vehicle_id>`
- Deletes an existing vehicle. Returns 404 if the `<vehicle_id>` is not found.
- Request Arguments: None
- Permissions:
    - `'delete:vehicles'`
- Response body:
    - Status code 200 and json `{'success': True, 'deleted-vehicle': vehicle}` where delete-vehicle is an array for the recently deleted vehicle or status code with details of failure.

### Sales Endpoint

#### `GET /sales`
- Fetches a list of all sales. If no sales on database, return an emtpy array.
- Request Arguments: None
- Permissions:
    - `'get:sales'`
- Response body:
    - Status code 200 and json `{'success': True, 'sales': [sales]}` where sales is a list containing all sales in the database or status code with details of failure.

#### `POST /sales`
- Creates a new vehicle and stores it in the database. Returns a 400 if the body passed is incorrect.
- Request Arguments:
    - `'vehicle_id'`: An Integer representing the vehicle ID.
    - `'customer_id'`: An Integer representing the customer ID.
- Permissions:
    - `'post:sales'`
- Response body:
    - Status code 200 and json `{'success': True, 'sale_data': new_sale}` where sale_data is an array for the recently created sale or status code with details of failure.

#### `DELETE /sales/<sales_id>`
- Deletes an existing sale entry. Returns 404 if the `<sale_id>` is not found.
- Request Arguments: None
- Permissions:
    - `'delete:sales'`
- Response body:
    - Status code 200 and json `{'success': True, 'sale_deleted': sale}` where sale_deleted is an array for the recently deleted sale or status code with details of failure.

### Customers Endpoint

#### `GET /customers`
- Fetches a list of all customers. If no customers on database, return an emtpy array.
- Request Arguments: None
- Permissions:
    - `'get:customers'`
- Response body:
    - Status code 200 and json `{'success': True, 'customers': [customer]}` where customers is a list containing all customers in the database or status code with details of failure.

#### `POST /customers`
- Creates a new customer and stores it in the database. Returns a 400 if the body passed is incorrect.
- Request Arguments:
    - `'first_name'`: A string for the customer's first name.
    - `'last_name'`: A string for the customer's last name.
    - `'phone_number'`: A string for the customer's phone number.
    - `'address'`: A string for the customer's address.
    - `'city'`: A string for the customer's city.
    - `'state'`: A string for the customer's state.
    - `'zip_code'`: An Integer for the customer's zip code.
- Permissions:
    - `'post:customers'`
- Response body:
    - Status code 200 and json `{'success': True, 'new_customer': customer}` where new_customer is an array for the recently created customer or status code with details of failure.

#### `PATCH /customers/<customer_id>`
- Updates an existing customer and stores it in the database. Returns 404 if `<customer_id>` is not found.
- Request Arguments, at least one has to be passed:
    - `'first_name'`: A string for the customer's first name.
    - `'last_name'`: A string for the customer's last name.
    - `'phone_number'`: A string for the customer's phone number.
    - `'address'`: A string for the customer's address.
    - `'city'`: A string for the customer's city.
    - `'state'`: A string for the customer's state.
    - `'zip_code'`: An Integer for the customer's zip code.
- Permissions:
    - `'patch:customers'`
- Response body:
    - Status code 200 and json `{'success': True, 'updated_customer': customer}` where updated_customer is an array for the recently updated customer or status code with details of failure.

#### `DELETE /customers/<customer_id>`
- Deletes an existing customer. Returns 404 if the `<customer_id>` is not found.
- Request Arguments: None
- Permissions:
    - `'delete:customers'`
- Response body:
    - Status code 200 and json `{'success': True, 'deleted_customer': customer}` where deleted_customer is an array for the recently deleted customer or status code with details of failure.

## Authentication

### Permissions
- `post:vehicles`: creates a vehicle
- `patch:vehicles`: updates existing vehicle
- `delete:vehicles`: deletes a vehicle
- `get:sales`: retrieves all sales
- `post:sales`: create a sales
- `delete:sales`: delete a sales
- `get:customers`: retrieves all customers
- `post:customers`: creates a customer
- `patch:customers`: updates a customer
- `delete:customers`: deletes a customer

### Roles
1. Sales Representative
    - Can create, update, and delete vehicles
    - Can get, create, and update customers
    - Permissions:
        - `post:vehicles`
        - `patch:vehicles`
        - `delete:vehicles`
        - `get:customers`
        - `post:customers`  
        - `patch:customers`
2. Manager
    - All permissions from the sales representative and...
    - Can delete customers
    - Can get, create sales
    - Permissions:
        - `delete:customers`
        - `get:sales`
        - `post:sales`
        - `post:vehicles`
        - `patch:vehicles`
        - `delete:vehicles`
        - `get:customers`
        - `post:customers`  
        - `patch:customers`

3. Owner
    - All permissions from the manager and...
    - Can delete sales
    - Permissions:
        - `delete:sales`
        - `delete:customers`
        - `get:sales`
        - `post:sales`
        - `post:vehicles`
        - `patch:vehicles`
        - `delete:vehicles`
        - `get:customers`
        - `post:customers`  
        - `patch:customers`

## Tokens

Tokens are provided in the setup.sh file. Run the command below to load the into your environment:

```bash
source setup.sh
```

1. Sales Representative
    See setup.sh, SALES_REP

2. Manager
    See setup.sh, MANAGER
    
3. Owner
    See setup.sh, OWNER
      