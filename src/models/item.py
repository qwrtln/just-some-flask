from __future__ import annotations

import sqlite3
from typing import Dict, Any, Optional


class ItemModel:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def json(self) -> Dict[str, Any]:
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name: str) -> Optional[ItemModel]:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return cls(*row) if row else None

    def insert(self) -> None:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self) -> None:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()
