import sqlite3
from typing import Any, Dict, Tuple, List

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank.",
    )

    @staticmethod
    @jwt_required()
    def get(name: str) -> Tuple[Dict[str, Any], int]:
        if item := ItemModel.find_by_name(name):
            return item.json(), 200  # type: ignore
        return {"message": "Item not found."}, 404

    @staticmethod
    def post(name: str) -> Tuple[Dict[str, Any], int]:
        if ItemModel.find_by_name(name):
            return (
                {"message": f"An item with a name '{name}' already exists."},
                400,
            )

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])

        try:
            item.insert()
        except sqlite3.OperationalError as error:
            return {"message": f"Couldn't create item: {error}"}, 500

        return item.json(), 201

    @staticmethod
    def delete(name: str) -> Tuple[Dict[str, str], int]:
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {"message": "Item deleted."}, 200
        return {"message": "Item not found."}, 404

    @staticmethod
    def put(name: str) -> Tuple[Dict[str, Any], int]:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data["price"])
            try:
                item.insert()
            except sqlite3.OperationalError:
                return {"message": "An error has occurred."}, 500
            return item.json(), 201

        updated_item = ItemModel(name, data["price"])
        try:
            updated_item.update()
        except sqlite3.OperationalError:
            return {"message": "An error has occurred."}, 500
        return updated_item.json(), 200


class ItemList(Resource):
    @staticmethod
    def get() -> Tuple[Dict[str, List[Dict[str, Any]]], int]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = [ItemModel(*item).json() for item in result.fetchall()]

        connection.close()

        return {"items": items}, 200
