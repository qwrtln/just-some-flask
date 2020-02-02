from __future__ import annotations

import sqlite3
from typing import Optional

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id: int, email: str, password: str) -> None:
        self.id = _id
        self.email = email
        self.password = password

    @classmethod
    def find_by_email(cls, email: str) -> Optional[UserModel]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email=?"
        result = cursor.execute(query, (email,))
        row = result.fetchone()
        connection.close()

        return cls(*row) if row else None

    @classmethod
    def find_by_id(cls, _id: str) -> Optional[UserModel]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()

        return cls(*row) if row else None
