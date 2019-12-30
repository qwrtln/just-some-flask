from typing import Any, Dict, List, Tuple

from flask import Flask, request
from flask_jwt import JWT, jwt_required  # type: ignore
from flask_restful import Api, Resource, reqparse  # type: ignore

from security import authenitcate, identity

app = Flask(__name__)
app.secret_key = "snake jazz"
api = Api(app)

jwt = JWT(app, authenitcate, identity)  # /auth

items: List[Dict[str, Any]] = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank.",
    )

    @jwt_required()
    def get(self, name: str) -> Tuple[Dict[str, Any], int]:
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name: str) -> Tuple[Dict[str, Any], int]:
        data = Item.parser.parse_args()
        if next(filter(lambda x: x["name"] == name, items), None):
            return (
                {"message": f"An item with a name '{name}' already exists."},
                400,
            )
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name: str) -> Dict[str, str]:
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name: str) -> Dict[str, Any]:
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
