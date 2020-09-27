import json

from flask import session, request, jsonify, abort

from app import app, db
from app.models import Manager, Checkout, Item, Receipt, Customer


def validate_session():
    if 'manager' not in session or not session['manager']:
        abort(401, description="You do not have permission for this action!")

    if not Manager.query.get(session['manager']):
        abort(401, description="You do not have permission for this action!")


@app.route('/login', methods=['POST'])
def login():
    if type(request.json) == str:
        login_data = json.loads(request.json)
    else:
        login_data = request.json

    if 'username' not in login_data or 'password' not in login_data:
        abort(400, description="Incomplete request! Fields required: username, password")

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


@app.route('/session', methods=['GET'])
def check_session():
    if 'manager' not in session or not session['manager']:
        return jsonify(current_user=None)

    manager = Manager.query.get(session['manager'])

    if not manager:
        return jsonify(current_user=None)

    return jsonify(current_user=manager)


@app.route('/checkout/<checkoutid>', methods=['GET'])
def get_checkout(checkoutid):
    try:
        id_ = int(checkoutid)
    except ValueError:
        abort(400, description="Checkout id must be a positive integer!")
        return
    checkout = Checkout.query.get(id_)

    if not checkout:
        abort(400, description="Checkout id {} does not exist!".format(id_))

    return jsonify(checkout=checkout)


@app.route('/checkout/<checkoutid>', methods=['PATCH'])
def edit_checkout(checkoutid):
    validate_session()

    if type(request.json) == str:
        checkout_data = json.loads(request.json)
    else:
        checkout_data = request.json

    if 'discount' not in checkout_data or 'tax_rate' not in checkout_data:
        abort(400, description="Incomplete request! Fields required: discount, tax_rate")
    try:
        discount = float(checkout_data['discount'])
        tax_rate = float(checkout_data['tax_rate'])
        id_ = int(checkoutid)
    except ValueError:
        abort(400, description="Discount rate must be a float number in range [0.0, 1.0]!")
        return

    if not (0 <= discount <= 1):
        abort(400, description="Discount rate must be in range [0.0, 1.0]!")

    if tax_rate < 0:
        abort(400, description="Tax rate must a positive float number!")

    checkout = Checkout.query.get(id_)

    if not checkout:
        abort(400, description="Checkout id {} does not exist!".format(id_))

    checkout.discount = discount
    checkout.tax_rate = tax_rate
    db.session.commit()
    return jsonify(checkout=checkout)


@app.route('/items', methods=['GET'])
def get_items():
    validate_session()

    items = Item.query.all()

    return jsonify(items=items)


@app.route('/item/<itemid>', methods=['DELETE'])
def delete_item(itemid):
    validate_session()

    try:
        item_id = int(itemid)
    except ValueError:
        abort(400, description="Item id must be a positive integer!")
        return

    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)


@app.route('/item', methods=['POST'])
def add_item():
    validate_session()

    if type(request.json) == str:
        item_data = json.loads(request.json)
    else:
        item_data = request.json

    if 'name' not in item_data or 'stock' not in item_data or 'price' not in item_data or 'discount' not in item_data:
        abort(400, description="Incomplete request! Fields required: name, discount, stock, price")

    try:
        discount = float(item_data['discount'])
        stock = int(item_data['stock'])
        price = float(item_data['price'])
        name = str(item_data['name'])
    except ValueError:
        abort(400, description="Discount rate must be a float number in range [0.0, 1.0], stock number must be an "
                               "integer, price must be a positive float number and item id must be a positive integer!")
        return

    if not (0 <= discount <= 1):
        abort(400, description="Discount rate must be in range [0.0, 1.0]!")

    if price < 0:
        abort(400, description="Price must be a non-negative float number!")

    item = Item(name=name, discount=discount, price=price, stock=stock)
    db.session.add(item)
    db.session.commit()
    return jsonify(item=item)


@app.route('/item/<itemid>', methods=['PATCH'])
def edit_item(itemid):
    validate_session()

    if type(request.json) == str:
        item_data = json.loads(request.json)
    else:
        item_data = request.json

    if 'discount' not in item_data or 'stock' not in item_data or 'price' not in item_data:
        abort(400, description="Incomplete request! Fields required: discount, stock, price")
    try:
        discount = float(item_data['discount'])
        stock = int(item_data['stock'])
        price = float(item_data['price'])
        id_ = int(itemid)
    except ValueError:
        abort(400, description="Discount rate must be a float number in range [0.0, 1.0], stock number must be an "
                               "integer, price must be a positive float number and item id must be a positive integer!")
        return

    if not (0 <= discount <= 1):
        abort(400, description="Discount rate must be in range [0.0, 1.0]!")

    item = Item.query.get(id_)

    if not item:
        abort(400, description="Item id {} does not exist!".format(id_))

    item.price = price
    item.discount = discount
    item.stock = stock
    db.session.commit()
    return jsonify(item=item)


@app.route('/item/<itemid>', methods=['GET'])
def get_item(itemid):
    try:
        item_identifier = int(itemid)
    except ValueError:
        item_identifier = str(itemid)

    if type(item_identifier) == str:
        item = Item.query.filter_by(name=item_identifier).first()
    else:
        item = Item.query.get(item_identifier)

    if not item:
        abort(400, description="Item with name or id {} does not exist!".format(item_identifier))

    return jsonify(item=item)


@app.route('/receipts', methods=['GET'])
def get_receipts():
    validate_session()

    receipts = Receipt.query.all()

    return jsonify(receipts=receipts)


@app.route('/customers', methods=['GET'])
def get_customers():
    validate_session()

    customers = Customer.query.all()

    return jsonify(customers=customers)
