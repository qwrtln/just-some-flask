from typing import Any, Dict, Tuple, List

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel

ResponseType = Tuple[Dict[str, Any], int]


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank.",
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Every item needs a store_id.",
    )

    @staticmethod
    @jwt_required()
    def get(name: str) -> ResponseType:
        if item := ItemModel.find_by_name(name):
            return item.json(), 200
        return {"message": "Item not found."}, 404

    @staticmethod
    def post(name: str) -> ResponseType:
        if ItemModel.find_by_name(name):
            return (
                {"message": f"An item with a name '{name}' already exists."},
                400,
            )

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201

    @staticmethod
    def delete(name: str) -> ResponseType:
        if item := ItemModel.find_by_name(name):
            item.delete_from_db()
            return {"message": "Item deleted."}, 200
        return {"message": "Item not found."}, 404

    @staticmethod
    def put(name: str) -> ResponseType:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @staticmethod
    def get() -> Tuple[Dict[str, List[Dict[str, Any]]], int]:
        return {"items": [item.json() for item in ItemModel.query.all()]}, 200
