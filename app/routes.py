import json

from flask import session, request, jsonify, abort
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import Manager, Checkout, Item, Receipt, Customer


@app.errorhandler(400)
def data_error(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(401)
def credential_error(e):
    return jsonify(error=str(e)), 401


# validate session
def validate_session():
    if 'manager' not in session or not session['manager']:
        abort(401, description="You do not have permission for this action!")

    if not Manager.query.get(session['manager']):
        abort(401, description="You do not have permission for this action!")


# validate and login Manager
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
    session.modified = True
    return jsonify(manager=target_manager)


# log out Manager
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('manager', None)
    return jsonify(success=True)


# check Session
@app.route('/session', methods=['GET'])
def check_session():
    if 'manager' not in session:
        return jsonify(current_user=None)

    manager = Manager.query.get(session.get('manager'))

    if not manager:
        return jsonify(current_user=None)

    return jsonify(current_user=manager)


# get checkout information given id
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


# edit checkout information given id
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

    try:
        db.session.commit()
    except IntegrityError as e:
        print(e)
        abort(400, description="Checkout failed (valid discount and tax_rate)?")
        return

    return jsonify(checkout=checkout)


# get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()

    return jsonify(items=items)


# delete item given id
@app.route('/item/<itemid>', methods=['DELETE'])
def delete_item(itemid):
    validate_session()

    try:
        item_id = int(itemid)
    except ValueError:
        abort(400, description="Item id must be a positive integer!")
        return

    item = Item.query.get(item_id)

    if not item:
        abort(400, description="Item {} does not exist!".format(item_id))

    db.session.delete(item)
    try:
        db.session.commit()
    except IntegrityError as e:
        print(e)
        abort(400, description="Item deletion failed!")
        return
    return jsonify(success=True)


# add item given valid info
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

    prev_item = Item.query.filter_by(name=name).first()

    if prev_item:
        abort(400, description="Item with name {} already exists!".format(name))

    item = Item(name=name, discount=discount, price=price, stock=stock)
    db.session.add(item)
    try:
        db.session.commit()
    except IntegrityError as e:
        print(e)
        abort(400, description="Item creation failed!")
        return
    return jsonify(item=item)


# edit item info given valid id and info
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
    try:
        db.session.commit()
    except IntegrityError as e:
        print(e)
        abort(400, description="Item modification failed!")
        return
    return jsonify(item=item)


# get item given id
@app.route('/item/<itemid>', methods=['GET'])
def get_item(itemid):
    try:
        item_identifier = int(itemid)
    except ValueError:
        item_identifier = str(itemid)

    item = None
    if type(item_identifier) == int:
        item = Item.query.get(item_identifier)

    if not item:
        item = Item.query.filter_by(name=str(item_identifier)).first()

    if not item:
        abort(400, description="Item with name or id {} does not exist!".format(item_identifier))

    return jsonify(item=item)


# purchase and update item given valid id and quantity
@app.route('/item/purchase', methods=['POST'])
def purchase_item():
    if type(request.json) == str:
        item_data = json.loads(request.json)
    else:
        item_data = request.json

    if 'id' not in item_data or 'amount' not in item_data:
        abort(400, description="Incomplete request! Fields required: name, discount, stock, price")

    try:
        itemid = int(item_data['id'])
        buy_amount = int(item_data['amount'])
    except ValueError:
        abort(400, description="Item id and buy amount must be positive integers!")
        return

    if itemid <= 0 or buy_amount <= 0:
        abort(400, description="Item id and buy amount must be positive integers!")

    item = Item.query.get(itemid)

    if buy_amount > item.stock:
        abort(400, description="Amount requested exceeded total item stock!")

    item.stock = item.stock - buy_amount
    try:
        db.session.commit()
    except IntegrityError as e:
        print(e)
        abort(400, description="Item purchase failed!")
        return
    return jsonify(item=item)


# get all receipts
@app.route('/receipts', methods=['GET'])
def get_receipts():
    validate_session()

    receipts = Receipt.query.all()

    return jsonify(receipts=receipts)


# get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    validate_session()

    customers = Customer.query.all()

    return jsonify(customers=customers)
