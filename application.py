from app import app, db
from app.models import Customer, Manager, Item, Receipt, Checkout

application = app

if __name__ == '__main__':
    if not Manager.query.first() and not Checkout.query.first() and not Item.query.first():
        print("create")
        customer1 = Customer(id=1, name="John Customer Doe")
        customer2 = Customer(id=2, name="Jane Customer Doe")
        manager = Manager(id=1, username="manager")
        manager.set_password("Passw0rd123")

        receipt1 = Receipt(id=1, timestamp="2020-09-27", net_total=149.1, discount=0.2, tax_rate=0.13, total=134.79,
                           customer_id=1)
        receipt2 = Receipt(id=2, timestamp="2020-09-25", net_total=12.4, discount=0, tax_rate=0.13, total=14.01,
                           customer_id=2)
        checkout = Checkout(id=1, tax_rate=0.13, discount=0.1)
        item1 = Item(id=1, name="coke", discount=0.0, price=1.5, stock=50)
        item2 = Item(id=2, name="sprite", discount=0.0, price=1.5, stock=40)
        item3 = Item(id=3, name="candy", discount=0.1, price=3, stock=29)
        item4 = Item(id=4, name="frozen chicken", discount=0.4, price=20.0, stock=5)
        item5 = Item(id=5, name="chopsticks", discount=0.0, price=5.0, stock=4)
        item6 = Item(id=6, name="orange juice", discount=0.25, price=8.0, stock=9)
        item7 = Item(id=7, name="bag of apple", discount=0.1, price=12.0, stock=7)
        item8 = Item(id=8, name="lobster", discount=0.0, price=35.0, stock=4)
        item9 = Item(id=9, name="shrimp cocktail", discount=0.05, price=32.7, stock=6)
        item10 = Item(id=10, name="garlic bread", discount=0.1, price=9.0, stock=15)
        db.session.add(customer1)
        db.session.add(customer2)
        db.session.add(manager)
        db.session.add(receipt1)
        db.session.add(receipt2)
        db.session.add(checkout)
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.add(item5)
        db.session.add(item6)
        db.session.add(item7)
        db.session.add(item8)
        db.session.add(item9)
        db.session.add(item10)
        db.session.commit()

    application.run(host='127.0.0.1', port=8000, debug=True)
