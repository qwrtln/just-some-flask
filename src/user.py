from __future__ import annotations

import sqlite3
from typing import Dict, Optional, Tuple

from flask_restful import Resource, reqparse  # type: ignore


class User:
    def __init__(self, _id: int, username: str, password: str) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> Optional[User]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        connection.close()

        return cls(*row) if row else None

    @classmethod
    def find_by_id(cls, _id: str) -> Optional[User]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()

        return cls(*row) if row else None


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank.",
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank.",
    )

    def post(self) -> Tuple[Dict[str, str], int]:
        data = UserRegister.parser.parse_args()

        username = data["username"]
        if User.find_by_username(username):
            return {"message": "A user with that name already exists."}, 409

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (username, data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
