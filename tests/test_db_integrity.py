import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Customer, Receipt, Manager, Item, Checkout


def test_receipt_positive_constraint(db_):
    c = Customer(id=1, name="test")
    m = Manager(id=1, username="test")
    db_.session.add(c)
    db_.session.add(m)
    invalid_data = [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 1.01, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]

    for invalid in invalid_data:
        r = Receipt(timestamp="1", net_total=invalid[0], discount=invalid[1], tax_rate=invalid[2], total=invalid[3],
                    customer_id=1, manager_id=1)
        db_.session.add(r)
        pytest.raises(IntegrityError, db_.session.commit)
        db_.session.rollback()


def test_item_positive_constraint(db_):
    invalid_data = [[-1, 0], [1.01, 0], [0, -1]]

    for invalid in invalid_data:
        i = Item(name="test", discount=invalid[0], price=invalid[1], stock=0)
        db_.session.add(i)
        pytest.raises(IntegrityError, db_.session.commit)
        db_.session.rollback()


def test_checkout_positive_constraint(db_):
    m = Manager(id=1, username="test")
    db_.session.add(m)
    invalid_data = [[-1, 0], [1.01, 0], [0, -1]]

    for invalid in invalid_data:
        c = Checkout(discount=invalid[0], tax_rate=invalid[1], manager_id=1)
        db_.session.add(c)
        pytest.raises(IntegrityError, db_.session.commit)
        db_.session.rollback()


def test_manager_password_verification():
    m = Manager(id=1, username="test")
    m.set_password("test_password")
    assert m.check_password("test_password")
