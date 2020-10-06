CSC301 - A1 - CHECKOUT APP - MADE BY Youhai Li & Junan Zhao
# Instructions

To test our database, please send below api calls to our deployed server: (http://checkout-env.eba-icztdryu.ca-central-1.elasticbeanstalk.com) to test our functionalities

**API docs**

- Login as Manager

  route: '/login'
  
  method: POST
  
  body: {username: manager, password: Passw0rd123}
  
  if correct return: {
    "manager": {
        "id": 1,
        "username": "manager"
    }
  }
  
  
- Log out as Manager

  route: '/logout'
  
  method: GET
  
  if correct return: {
    "success": true
  }
  
  
- Check Manager session

  route: '/session'
  
  method: GET
  
  if manager logged in return: {
    "current_user": {
        "id": 1,
        "username": "manager"
    }
  }
  
 
- Get global tax & discount

  route: '/checkout/checkoutid'
  
  method: GET
  
  e.g. if checkoutid == 1 return: {
    "checkout": {
        "discount": 0.2,
        "id": 1,
        "tax_rate": 0.2
    }
  }
  
  
- Edit global tax & discount

  route: '/checkout/checkoutid'
  
  method: PATCH
  
  e.g. body: {discount: 0.9, tax_rate: 0.1}
  
  e.g. if checkoutid == 1 return: {
    "checkout": {
        "discount": 0.9,
        "id": 1,
        "tax_rate": 0.1
    }
  }
  
  
- Get all items

  route: '/items'
  
  method: GET
  
  if correct return: {
    "items": [
        {
            "discount": 0.0,
            "id": 1,
            "name": "coke",
            "price": 0.5,
            "stock": 85
        },
        {
            "discount": 1.0,
            "id": 2,
            "name": "sprite",
            "price": 3.0,
            "stock": 21
        },
        ...
    ]
  }
  
- Delete item given id

  route: '/item/itemid'
  
  method: DELETE
  
  e.g. if itemid == 33 return: {
    "success": true
  }
  
- Add item given valid info

  route: 'item'
  
  method: POST
  
  e.g. body: {discount: 0.1, stock: 100, price: 1.50, name: "301"}
  
  e.g. return: {
    "item": {
        "discount": 0.1,
        "id": 34,
        "name": "301",
        "price": 1.5,
        "stock": 100
    }
  }
  
- Edit item info given id and valid info

  route: '/item/itemid'
  
  method: PATCH
  
  e.g. body: {discount: 0.9, stock: 1000, price: 3.00}
  
  e.g. if itemid == 34 return: {
    "item": {
        "discount": 0.9,
        "id": 34,
        "name": "301",
        "price": 3.0,
        "stock": 1000
    }
  }
  
- Get item given id

  route: '/item/itemid'
  
  method: GET
  
  e.g. if itemid == 34 return: {
    "item": {
        "discount": 0.9,
        "id": 34,
        "name": "301",
        "price": 3.0,
        "stock": 1000
    }
  }
  
- Purchase item given valid info

  route: '/item/purchase'
  
  method: POST
  
  e.g. body: {id: 34, amount: 50}
  
  e.g. return: {
    "item": {
        "discount": 0.9,
        "id": 34,
        "name": "301",
        "price": 3.0,
        "stock": 950
    }
  }

**Backend Model Design**

- The database models we implement:

Manager: {

username: String, // username

password\_hash: String // passoword

}

Item: {

id: Integer, // unique item id

name: String, // item name

discount: Float, // item discount rate should be in range [0,1]

price: Float, // item price should be in range [0,

stock: Integer // iten stock should be in range [0,

}

Checkout: {

id: Integer, // unique checkout id

tax\_rate: Float, // global tax rate should be in range [0,

discount: Float // global discount should be in range [0,1]

}
