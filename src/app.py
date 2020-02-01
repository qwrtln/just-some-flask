from flask import Flask
from flask_jwt import JWT  # type: ignore
from flask_restful import Api  # type: ignore

from item import Item, ItemList
from security import authenitcate, identity
from user import UserRegister


app = Flask(__name__)
app.secret_key = "snake jazz"
api = Api(app)

jwt = JWT(app, authenitcate, identity)  # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
