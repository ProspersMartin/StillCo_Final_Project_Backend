"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Client, Orders, Service_catalog
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)


# *************************************************************************************
# ******************************   JWT/ LOGIN METHOD   ********************************
# *************************************************************************************
app.config['JWT_SECRET_KEY'] = '$8455&843AM735I33!'
jwt = JWTManager(app)

#                 # Provide a method to create access tokens.
#                 # The create_jwt() function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    client_check = Client.query.filter_by(email=email, password=password).first()
    if client_check == None:

        return jsonify({"msg": "Bad email or password"}), 401

#         # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email)}
    return jsonify(ret), 200
# *************************************************************************************




@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


# *************************************************************************************
# *******************************   CLIENT METHODS   **********************************
# *************************************************************************************


# *******************************  CLIENT (GENERAL)  **********************************
# *************************************************************************************
@app.route('/client', methods=['POST', 'GET'])
# @jwt_required
def handle_client():
    """
    Create client and retrieve all clients
    """

# *******************   POST REQUEST    *******************
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)

        client1 = Client(name=body['name'], email=body['email'], password=body['password'])
        db.session.add(client1)
        db.session.commit()
        return jsonify(client1.serialize()), 200

# *******************   GET REQUEST    *******************
    if request.method == 'GET':
        all_clients= Client.query.all()
        all_clients = list(map(lambda x: x.serialize(), all_clients))
        return jsonify(all_clients), 200

    return "Invalid Method", 404


# **************************  INDIVIDUAL/SPECIFIC CLIENT  *****************************
# *************************************************************************************
@app.route('/client/<int:client_id>', methods=['PUT', 'GET', 'DELETE'])
@jwt_required
def get_single_client(client_id):
    """
    Single client
    """

# *******************   PUT REQUEST    *******************
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        client1 = Client.query.get(client_id)
        if client1 is None:
            raise APIException('Client not found', status_code=404)

        if "email" in body:
            client1.email = body["email"]
        if "password" in body:
            client1.password = body["password"]
        if "client_login_status" in body:
            client1.client_login_status = body["client_login_status"]

        db.session.commit()
        return jsonify(client1.serialize()), 200

# *******************   GET REQUEST    *******************
    if request.method == 'GET':
        client1 = Client.query.get(client_id)
        if client1 is None:
            raise APIException('Client not found', status_code=404)

        return jsonify(client1.serialize()), 200

# *******************   DELETE REQUEST    *******************
    if request.method == 'DELETE':
        client1 = Client.query.get(client_id)
        if client1 is None:
            raise APIException('Client not found', status_code=404)

        db.session.delete(client1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404
# *************************************************************************************




# *************************************************************************************
# *******************************   ORDERS METHODS   **********************************
# *************************************************************************************


# *******************************  ORDERS (GENERAL)  **********************************
# *************************************************************************************#
@app.route('/orders', methods=['POST', 'GET'])
def handle_orders():
    """
    Create orders and retrieve all orders
    """

# *******************   POST REQUEST    *******************
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object",
                               status_code=400)

        if 'client_email' not in body:
            raise APIException('You need to specify client_email', status_code=400)
        # if 'total' not in body:
        #     raise APIException('You need to specify the total', status_code=400)
        # if 'order_number' not in body:
        #     raise APIException('You need to specify the order number', status_code=400)
        # if 'date_created' not in body:
        #     raise APIException('You need to specify the date created', status_code=400)
        # if 'assigned_consultant' not in body:
        #     raise APIException('You need to specify the assigned_consultant', status_code=400)
        items = body['items']
        for item in items:
            order1 = Orders(
                client_email=item.client_email,
                total=item.price)
            db.session.add(order1)



        db.session.commit()
        return "ok", 200

# *******************   GET REQUEST    *******************
    if request.method == 'GET':
        all_orders = Orders.query.all()
        all_orders = list(map(lambda x: x.serialize(), all_orders))
        return jsonify(all_orders), 200

    return "Invalid Method", 404



# **************************  INDIVIDUAL/SPECIFIC ORDER  ******************************
# *************************************************************************************
@app.route('/orders/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_order(id):
    """
    Single order
    """

# *******************   PUT REQUEST    *******************
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        order1 = Orders.query.get(id)
        if order1 is None:
            raise APIException('Order not found', status_code=404)

        if "client_email" in body:
            order1.client_email = body["client_email"]
        if "payment_status" in body:
            order1.payment_status = body["payment_status"]
        if "meeting_type" in body:
            order1.meeting_type = body["meeting_type"]
        if "assigned_consultant" in body:
            order1.assigned_consultant = body["assigned_consultant"]
        if "order_status" in body:
            order1.order_status = body["order_status"]
        if "order_notes" in body:
            order1.order_notes = body["order_notes"]
        if "order_issues" in body:
            order1.order_issues = body["order_issues"]
        if "date_completed" in body:
            order1.date_completed = body["date_completed"]
        if "total" in body:
            order1.total = body["total"]

        db.session.commit()
        return jsonify(order1.serialize()), 200

# *******************   GET REQUEST    *******************
    if request.method == 'GET':
        order1 = Orders.query.get(id)
        if order1 is None:
            raise APIException('Order not found', status_code=404)

        return jsonify(order1.serialize()), 200

# *******************   DELETE REQUEST    *******************
    if request.method == 'DELETE':
        order1 = Orders.query.get(id)
        if order1 is None:
            raise APIException('Order not found', status_code=404)

        db.session.delete(order1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404




# *************************************************************************************
# *******************************  SERVICES METHODS   *********************************
# *************************************************************************************

# ******************************   SERVICES (GENERAL)   *******************************
# *************************************************************************************
@app.route('/services', methods=['POST', 'GET'])
def handle_service_catalog():
    """
    Retrieve all Services
    """

# *******************   POST REQUEST    *******************
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object",
                               status_code=400)

        if 'service_name' not in body:
            raise APIException('You need to specify the service', status_code=400)
        if 'assigned_consultant' not in body:
            raise APIException('You need to specify the assigned consultant', status_code=400)
        if 'description' not in body:
            raise APIException('You need to specify the description', status_code=400)
        if 'price' not in body:
            raise APIException('You need to specify the price', status_code=400)
        if 'service_type' not in body:
            raise APIException('You need to specify the service type', status_code=400)
        if 'package' not in body:
            raise APIException('You need to specify the package', status_code=400)


        service1 = Service_catalog(service_name=body['service_name'], assigned_consultant=body['assigned_consultant'],
           description=body['description'], price=body['price'], service_type=body['service_type'], package=body['package'])

        db.session.add(service1)
        db.session.commit()
        return "ok", 200

# *******************   GET REQUEST    *******************
    if request.method == 'GET':
        all_services = Service_catalog.query.all()
        all_services = list(map(lambda x: x.serialize(), all_services))
        return jsonify(all_services), 200

    return "Invalid Method", 404



# **************************  INDIVIDUAL/SPECIFIC SERVICE  ******************************
# *************************************************************************************
@app.route('/services/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_service(id):
    """
    Single service
    """

# *******************   PUT REQUEST    *******************
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        service1 = Service_catalog.query.get(id)
        if service1 is None:
            raise APIException('Service not found', status_code=404)

        if "assigned_consultant" in body:
            service1.assigned_consultant = body["assigned_consultant"]
        if "service_name" in body:
            service1.service = body["service_name"]
        if "description" in body:
            service1.description = body["description"]
        if "price" in body:
            service1.price = body["price"]
        if "service_type" in body:
            service1.service_type = body["service_type"]
        if "package" in body:
            service1.package = body["package"]

        db.session.commit()
        return jsonify(service1.serialize()), 200

# *******************   GET REQUEST    *******************
    if request.method == 'GET':
        service1 = Service_catalog.query.get(id)
        if service1 is None:
            raise APIException('Service not found', status_code=404)
        return jsonify(service1.serialize()), 200

# *******************   DELETE REQUEST    *******************
    if request.method == 'DELETE':
        service1 = Service_catalog.query.get(id)
        if service1 is None:
            raise APIException('Service not found', status_code=404)
        db.session.delete(service1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
