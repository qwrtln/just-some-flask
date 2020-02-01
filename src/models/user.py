from __future__ import annotations

import sqlite3
from typing import Optional


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
