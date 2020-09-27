import json

import pytest
from flask import session
from app.models import Customer, Receipt, Manager, Item, Checkout

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
    m = Manager(id=1, username=username)
    m.set_password(password)
    db_.session.add(m)
    db_.session.commit()
    res = login(client, username, password)

    assert 'manager' in session
    assert res.json['manager']
    assert res.json['manager']['id'] == m.id
    assert res.json['manager']['username'] == m.username


def test_logout(client, db_):
    username = "test"
    password = "testPassword=123"
    m = Manager(id=1, username=username)
    m.set_password(password)
    db_.session.add(m)
    db_.session.commit()
    res = logout(client)

    assert 'manager' not in session
    assert res.json['success']

