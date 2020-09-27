import json

from flask import session

from app.models import Manager, Checkout

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


