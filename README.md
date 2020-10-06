CSC301 - A1 - CHECKOUT APP - MADE BY Youhai Li & Junan Zhao
# Instructions

Our backend is an API server deployed on AWS Elasticbeanstalk on this [link](http://checkout-env.eba-icztdryu.ca-central-1.elasticbeanstalk.com). You can visit this link to test our backend API functionalities.

We are using Github Actions as our CI/CD tool. Upon a push to the master branch(merged PR), "Build, test and deploy to production server" workflow will execute, building the project and deploying it onto AWS elasticbeanstalk service located at the above link. A success deployment will be indicated by a green check mark beside the commits in the master branch. The "Actions" tab in the repository will also show all workflows executed since the creation of the repository. Since we migrated our repository from the CSC301 Classroom repo to this repository, all the previous workflow logs are not visible in this repository.

Besides, we also created a test server for testing-after-deployment purpose, since the communication between our API and frontend website involves session cookies and CORS requests, localhost testing may not be sufficient enough. Therefore, we created a test server that has exactly same configuration as our production server to mimic server-side behaviours and perform tests on our frontends to make sure the API server works as intended before we deploy to production server. This test deployment is also completed automaticall via Github Action, "Build, test and deploy to test server" workflow, which is triggered upon the creation of the pull request (before it is merged). It is also possible to visit and test our test server via [this link](http://checkouttest-env.eba-efcqkfw6.ca-central-1.elasticbeanstalk.com/).

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

  route: '/item/\<itemid>'
  
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
  
- Get item given id or item name

  route: '/item/\<itemid>'
  
  method: GET
  
  e.g. if itemid == 'coke' return: {
    {"item":{"discount":0.0,"id":1,"name":"coke","price":0.5,"stock":85}}
  }
  
  e.g if itemid == 1 return {
    {"item":{"discount":0.0,"id":1,"name":"coke","price":0.5,"stock":85}}
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

For more specific implementations, check app/routes.py

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
