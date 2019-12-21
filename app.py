from typing import Any, Dict, List, Tuple

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items: List[Dict[str, Any]] = []


class Item(Resource):
    def get(self, name: str) -> Tuple[Dict[str, Any], int]:
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name: str) -> Tuple[Dict[str, Any], int]:
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with a name '{name}' already exists."}, 400
        request_data = request.get_json()
        print(request_data)
        item = {"name": name, "price": request_data["price"]}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
