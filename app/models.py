from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from serializable import Serializable

SERIALIZE_RECUR_LIMIT = 3
DEFAULT_TAX_RATE = 0.13

# Customer Model
class Customer(db.Model, Serializable):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)

    past_purchases = db.relationship("Receipt", back_populates="customer", cascade="all, delete")

    def serialize(self, **kwargs):
        serialized = {'id': self.id, 'name': self.name}
        if 'recur' in kwargs and kwargs['recur'] < SERIALIZE_RECUR_LIMIT:
            next_recur = kwargs['recur'] + 1
            serialized['past_purchases'] = [rec.serialize(recur=next_recur) for rec in self.past_purchases]
        return serialized

    def __repr__(self):
        return '<Customer {}>'.format(self.name)

# Receipt Model
class Receipt(db.Model, Serializable):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(64), index=True, nullable=False)
    net_total = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.CheckConstraint('discount <= 1 and discount >= 0', name="receipt_discount_range_check"),
                      db.CheckConstraint('net_total >= 0 and tax_rate >= 0 and total >= 0',
                                         name="receipt_positive_check"),)

    customer = db.relationship("Customer", back_populates="past_purchases", foreign_keys=[customer_id])

    def serialize(self, **kwargs):
        serialized = {'timestamp': self.timestamp, 'net_total': float(self.net_total), 'discount': float(self.discount),
                      'tax_rate': float(self.tax_rate), 'total': float(self.total),
                      'customer_id': int(self.customer_id)}
        if 'recur' in kwargs and kwargs['recur'] < SERIALIZE_RECUR_LIMIT:
            next_recur = kwargs['recur'] + 1
            serialized['customer'] = self.customer.serialize(recur=next_recur)
        return serialized

    def __repr__(self):
        return '<Receipt {}: ${} - ${}>'.format(self.id, self.net_total, self.total)

# Manager Model
class Manager(db.Model, Serializable):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if len(password) == 0:
            return False
        return check_password_hash(self.password_hash, password)

    def serialize(self, **kwargs):
        serialized = {"id": self.id, "username": self.username}
        return serialized

    def __repr__(self):
        return '<Manager {}>'.format(self.username)

# Item Model
class Item(db.Model, Serializable):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    discount = db.Column(db.Float, default=0.0)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    __table_args__ = (db.CheckConstraint('discount <= 1 and discount >= 0', name="item_discount_range_check"),
                      (db.CheckConstraint('price >= 0', name="item_positive_check")))

    def serialize(self, **kwargs):
        serialized = {'id': self.id, 'name': self.name, 'discount': float(self.discount), 'price': float(self.price),
                      'stock': int(self.stock)}
        return serialized

    def __repr__(self):
        return '<Item {}: ${}>'.format(self.name, self.price)

# Checkout Model
class Checkout(db.Model, Serializable):
    __tablename__ = 'checkout'
    id = db.Column(db.Integer, primary_key=True)
    tax_rate = db.Column(db.Float, default=DEFAULT_TAX_RATE)
    discount = db.Column(db.Float, default=0.0)

    __table_args__ = (db.CheckConstraint('discount <= 1 and discount >= 0', name="checkout_discount_range_check"),
                      (db.CheckConstraint('tax_rate >= 0', name="checkout_positive_check")))

    def serialize(self, **kwargs):
        serialized = {'id': self.id, 'tax_rate': float(self.tax_rate), 'discount': float(self.discount)}
        return serialized

    def __repr__(self):
        return '<Checkout {}>'.format(self.id)
