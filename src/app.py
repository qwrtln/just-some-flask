from datetime import timedelta
from typing import Any

from flask import Flask, jsonify
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from security import authenitcate, identity
from resources.user import UserRegister
from models.user import UserModel

app = Flask(__name__)
app.secret_key = "snake jazz"
api = Api(app)

app.config["JWT_AUTH_URL_RULE"] = "/login"
# configure JWT to expire within half an hour
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=60 * 30)
# configure auth username to be an e-mail
app.config["JWT_AUTH_USERNAME_KEY"] = "email"

jwt = JWT(app, authenitcate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token: bytes, identity_: UserModel) -> Any:
    return jsonify(
        {"access_token": access_token.decode("utf-8"), "user_id": identity_.id}
    )


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
