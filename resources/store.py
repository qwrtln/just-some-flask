import sqlite3
from typing import Any, Dict, Tuple

from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


StoreResponseType = Tuple[Dict[str, Any], int]


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str) -> StoreResponseType:
        if store := StoreModel.find_by_name(name):
            return store.json(), 200
        return {"message": "Store not found."}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str) -> StoreResponseType:
        if StoreModel.find_by_name(name):
            return {"message": f"Store '{name}' already exists."}, 409
        store = StoreModel(name)
        try:
            store.save_to_db()
        except sqlite3.OperationalError:
            return {"message": "Error while creating store."}, 500
        return store.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str) -> StoreResponseType:
        if store := StoreModel.find_by_name(name):
            store.delete_from_db()
        return {"message": "Store deleted."}, 200


class StoreList(Resource):
    @classmethod
    @jwt_required()
    def get(cls) -> StoreResponseType:
        return {"stores": [store.json() for store in StoreModel.query.all()]}, 200
