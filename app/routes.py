from app import app
from flask import session, request, jsonify, abort
from app.models import Manager
import json


@app.route('/login', methods=['POST'])
def login():
    if type(request.json) == str:
        login_data = json.loads(request.json)
    else:
        login_data = request.json

    if 'username' not in login_data or 'password' not in login_data:
        abort(400, description="Username or password missing!")

    username = login_data['username']
    password = login_data['password']

    target_manager = Manager.query.filter_by(username=username).first()

    if not target_manager:
        abort(401, description="Manager {} does not exist!".format(username))

    if not target_manager.check_password(password):
        abort(401, description="Password incorrect!")

    session['manager'] = target_manager.id
    return jsonify(manager=target_manager)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('manager', None)
    return jsonify(success=True)


@app.route('/checkout/tax', methods=['PATCH'])
def change_checkout_tax():
    pass


@app.route('/checkout', methods=['GET'])
def checkout():
    pass


@app.route('/checkout/discount', methods=['PATCH'])
def change_checkout_discount():
    pass


@app.route('/items', methods=['GET'])
def get_items():
    pass


@app.route('/item/restock', methods=['PATCH'])
def restock_item():
    pass


@app.route('/item/price', methods=['PATCH'])
def change_item_price():
    pass


@app.route('/item/discount', methods=['PATCH'])
def change_item_discount():
    pass


@app.route('/item/${itemid}', methods=['GET'])
def get_item_info(itemid):
    pass


@app.route('/receipts', methods=['GET'])
def get_receipts():
    pass


@app.route('/customers', methods=['GET'])
def get_customers():
    pass

