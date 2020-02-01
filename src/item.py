import sqlite3
from typing import Any, Dict, Tuple, Optional

from flask_jwt import jwt_required  # type: ignore
from flask_restful import Resource, reqparse  # type: ignore


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank.",
    )

    @classmethod
    def find_item_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        if row := result.fetchone():
            connection.close()
            return {"name": row[0], "price": row[1]}
        return None

    @classmethod
    def insert_item(cls, item: dict) -> None:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item: dict) -> None:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name: str) -> Tuple[Dict[str, Any], int]:
        if item := self.find_item_by_name(name):
            return item, 200  # type: ignore
        return {"message": "Item not found."}, 404

    def post(self, name: str) -> Tuple[Dict[str, Any], int]:
        if self.find_item_by_name(name):
            return (
                {"message": f"An item with a name '{name}' already exists."},
                400,
            )

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        try:
            self.insert_item(item)
        except sqlite3.OperationalError as error:
            return {"message": f"Couldnt create item: {error}"}, 500

        return item, 201

    def delete(self, name: str) -> Tuple[Dict[str, str], int]:
        if self.find_item_by_name(name):
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {"message": "Item deleted."}, 200
        return {"message": "Item not found."}, 404

    def put(self, name: str) -> Tuple[Dict[str, Any], int]:
        data = Item.parser.parse_args()
        item = self.find_item_by_name(name)
        if item is None:
            item = {"name": name, "price": data["price"]}
            try:
                self.insert_item(item)
            except sqlite3.OperationalError:
                return {"message": "An error has occurred."}, 500
            return item, 201

        updated_item = {"name": name, "price": data["price"]}
        try:
            self.update_item(updated_item)
        except sqlite3.OperationalError:
            return {"message": "An error has occurred."}, 500
        return updated_item, 200


class ItemList(Resource):
    def get(self) -> Tuple[Dict[str, Any], int]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = [{"name": item[0], "price": item[1]} for item in result.fetchall()]

        connection.close()

        return {"items": items}, 200
