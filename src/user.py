from __future__ import annotations

import re
import sqlite3
from typing import Dict, Optional, Tuple

from flask_restful import Resource, reqparse  # type: ignore


class User:
    def __init__(self, _id: int, email: str, password: str) -> None:
        self.id = _id
        self.email = email
        self.password = password

    @classmethod
    def find_by_email(cls, email: str) -> Optional[User]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email=?"
        result = cursor.execute(query, (email,))
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
    email_regex = re.compile("[^@]+@[^@]+\.[^@]+")
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank.",
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank.",
    )

    def post(self) -> Tuple[Dict[str, str], int]:
        data = UserRegister.parser.parse_args()

        email = data["email"]
        if not self.email_regex.match(email):
            return {"message": "User name must be an e-mail address."}, 400
        if User.find_by_email(email):
            return {"message": "A user with that e-mail address already exists."}, 409

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (email, data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
