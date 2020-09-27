import json

from flask import session, request, jsonify, abort

from app import app, db
from app.models import Manager, Checkout


def validate_session():
    if 'manager' not in session or not session['manager']:
        abort(400, description="You do not have permission for this action!")

    if not Manager.query.get(session['manager']):
        abort(400, description="You do not have permission for this action!")


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
def edit_checkout_rates(checkoutid):
    validate_session()

    if type(request.json) == str:
        discount_data = json.loads(request.json)
    else:
        discount_data = request.json

    if 'discount' not in discount_data or 'tax_rate' not in discount_data:
        abort(400, description="Username or password missing!")
    try:
        discount = float(discount_data['discount'])
        tax_rate = float(discount_data['tax_rate'])
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


@app.route('/item/<itemid>', methods=['GET'])
def get_item_info(itemid):
    pass


@app.route('/receipts', methods=['GET'])
def get_receipts():
    pass


@app.route('/customers', methods=['GET'])
def get_customers():
    pass
