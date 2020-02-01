import sqlite3
from typing import Any, Dict, List, Tuple, Optional

from flask_jwt import jwt_required  # type: ignore
from flask_restful import Resource, reqparse  # type: ignore

items: List[Dict[str, Any]] = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank.",
    )

    @jwt_required()
    def get(self, name: str) -> Optional[Tuple[Dict[str, Any], int]]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM ITEMS WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return {"item": row[0], "price": row[1]}, 200
        return {"message": "Item not found."}, 404

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
