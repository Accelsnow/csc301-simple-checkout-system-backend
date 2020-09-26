from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from serializable import Serializable

SERIALIZE_RECUR_LIMIT = 3
DEFAULT_TAX_RATE = 0.13


class Customer(db.Model, Serializable):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)

    past_purchases = db.relationship("Receipt", back_populates="customer", cascade="all, delete")

    def serialize(self, **kwargs):
        serialized = {}
        return serialized

    def __repr__(self):
        return '<Customer {}>'.format(self.name)


class Receipt(db.Model, Serializable):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(64), index=True, nullable=False)
    net_total = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.CheckConstraint(0 <= discount <= 1, name="receipt_discount_range_check"),
                      (db.CheckConstraint(net_total >= 0 and total >= 0 and tax_rate >= 0,
                                          name="receipt_positive_check")))

    customer = db.relationship("Customer", back_populates="past_purchases", foreign_keys=[customer_id])
    manager = db.relationship("Manager", back_populates="sale_history", foreign_keys=[manager_id])

    def serialize(self, **kwargs):
        return {}

    def __repr__(self):
        return '<Receipt {}: ${} - ${}>'.format(self.id, self.net_total, self.total)


class Manager(db.Model, Serializable):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=True, unique=True)
    password_hash = db.Column(db.String(128))

    sale_history = db.relationship("Receipt", back_populates="manager", cascade="all, delete")
    checkouts = db.relationship("Checkout", back_populates="manager", cascade="all, delete")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if len(password) == 0:
            return False
        return check_password_hash(self.password_hash, password)

    def serialize(self, **kwargs):
        return {}

    def __repr__(self):
        return '<Manager {}>'.format(self.username)


class Item(db.Model, Serializable):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    discount = db.Column(db.Float, default=0.0)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    __table_args__ = (db.CheckConstraint(0 <= discount <= 1, name="item_discount_range_check"),
                      (db.CheckConstraint(price >= 0, name="item_positive_check")))

    def serialize(self, **kwargs):
        return {}

    def __repr__(self):
        return '<Item {}: ${}>'.format(self.name, self.price)


class Checkout(db.Model, Serializable):
    __tablename__ = 'checkout'
    id = db.Column(db.Integer, primary_key=True)
    tax_rate = db.Column(db.Float, default=DEFAULT_TAX_RATE)
    discount = db.Column(db.Float, default=0.0)

    __table_args__ = (db.CheckConstraint(0 <= discount <= 1, name="checkout_discount_range_check"),
                      (db.CheckConstraint(tax_rate >= 0, name="checkout_positive_check")))

    def serialize(self, **kwargs):
        return {}

    def __repr__(self):
        return '<Checkout {}>'.format(self.id)
