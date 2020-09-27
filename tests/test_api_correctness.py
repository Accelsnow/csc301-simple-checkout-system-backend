import json

from flask import session

from app.models import Manager, Checkout, Item

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def login(client, username, password):
    return client.post('/login', json=json.dumps({'username': username, 'password': password}), headers=headers)


def logout(client):
    return client.get('/logout', headers=headers)


def test_login(client, db_):
    username = "test"
    password = "testPassword=123"
    manager_id = 1
    manager = Manager(id=manager_id, username=username)
    manager.set_password(password)
    db_.session.add(manager)
    db_.session.commit()
    res = login(client, username, password)

    assert 'manager' in session
    assert res.json['manager']
    assert res.json['manager']['id'] == manager_id
    assert res.json['manager']['username'] == username


def test_logout(client, db_):
    username = "test"
    password = "testPassword=123"
    manager = Manager(id=1, username=username)
    manager.set_password(password)
    db_.session.add(manager)
    db_.session.commit()
    login(client, username, password)
    res = logout(client)

    assert 'manager' not in session
    assert res.json['success']


def test_get_checkout(client, db_):
    checkout_id = 1
    checkout_tax_rate = 0
    checkout_discount = 0
    checkout = Checkout(id=checkout_id, tax_rate=checkout_tax_rate, discount=checkout_discount)
    db_.session.add(checkout)
    db_.session.commit()
    res = client.get('/checkout/1', headers=headers)
    assert res.json['checkout']
    assert res.json['checkout']['id'] == checkout_id
    assert res.json['checkout']['tax_rate'] == checkout_tax_rate
    assert res.json['checkout']['discount'] == checkout_discount


def test_edit_checkout(client, db_):
    new_tax_rate = 0.25
    new_discount = 0.5
    checkout = Checkout(id=1, tax_rate=0, discount=0)
    username = "test"
    password = "testPassword=123"
    manager = Manager(id=1, username=username)
    manager.set_password(password)
    db_.session.add(manager)
    db_.session.add(checkout)
    db_.session.commit()
    login(client, username, password)
    res = client.patch('/checkout/1', json=json.dumps({'tax_rate': 0.25, 'discount': 0.5}), headers=headers)

    assert res.json['checkout']
    assert res.json['checkout']['id'] == 1
    assert res.json['checkout']['tax_rate'] == new_tax_rate
    assert res.json['checkout']['discount'] == new_discount


def test_edit_checkout_permission(client, db_):
    checkout = Checkout(id=1, tax_rate=0, discount=0)
    db_.session.add(checkout)
    db_.session.commit()
    res = client.patch('/checkout/1', json=json.dumps({'tax_rate': 0.25, 'discount': 0.5}), headers=headers)

    assert res.status_code == 400


def test_get_all_items(client, db_):
    item1 = Item(id=1, name="test1", discount=0.1, price=0.1, stock=1)
    item2 = Item(id=2, name="test2", discount=0.2, price=0.2, stock=2)
    item3 = Item(id=3, name="test3", discount=0.3, price=0.3, stock=3)
    username = "test"
    password = "testPassword=123"
    manager = Manager(id=1, username=username)
    manager.set_password(password)
    db_.session.add(manager)
    db_.session.add(item1)
    db_.session.add(item2)
    db_.session.add(item3)
    db_.session.commit()
    login(client, username, password)
    res = client.get('/items', headers=headers)

    assert res.json['items']
    assert len(res.json['items']) == 3
    assert res.json['items'][0]['name'] == "test1"
    assert res.json['items'][1]['name'] == "test2"
    assert res.json['items'][2]['name'] == "test3"


def test_get_all_items_permission(client, db_):
    item1 = Item(id=1, name="test1", discount=0.1, price=0.1, stock=1)
    item2 = Item(id=2, name="test2", discount=0.2, price=0.2, stock=2)
    item3 = Item(id=3, name="test3", discount=0.3, price=0.3, stock=3)
    db_.session.add(item1)
    db_.session.add(item2)
    db_.session.add(item3)
    db_.session.commit()
    res = client.get('/items', headers=headers)

    assert res.status_code == 400


def test_edit_item(client, db_):
    new_discount = 0.5
    new_price = 50.0
    new_stock = 5
    item = Item(id=1, name="test1", discount=0.1, price=0.1, stock=1)
    username = "test"
    password = "testPassword=123"
    manager = Manager(id=1, username=username)
    manager.set_password(password)
    db_.session.add(manager)
    db_.session.add(item)
    db_.session.commit()
    login(client, username, password)
    res = client.patch('/item/1', json=json.dumps({'stock': new_stock, 'price': new_price, 'discount': new_discount}),
                       headers=headers)

    assert res.json['item']
    assert res.json['item']['id'] == 1
    assert res.json['item']['discount'] == new_discount
    assert res.json['item']['price'] == new_price
    assert res.json['item']['stock'] == new_stock


def test_edit_item_permission(client, db_):
    new_discount = 0.5
    new_price = 50.0
    new_stock = 5
    item = Item(id=1, name="test1", discount=0.1, price=0.1, stock=1)
    db_.session.add(item)
    db_.session.commit()
    res = client.patch('/item/1', json=json.dumps({'stock': new_stock, 'price': new_price, 'discount': new_discount}),
                       headers=headers)

    assert res.status_code == 400


def test_get_item(client, db_):
    item = Item(id=1, name="test1", discount=0.1, price=0.1, stock=1)
    db_.session.add(item)
    db_.session.commit()
    res = client.get('/item/1', headers=headers)

    assert res.json['item']
    assert res.json['item']['id'] == 1
    assert res.json['item']['name'] == 'test1'

    res = client.get('/item/test1', headers=headers)

    assert res.json['item']
    assert res.json['item']['id'] == 1
    assert res.json['item']['name'] == 'test1'
