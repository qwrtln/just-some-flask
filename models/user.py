from __future__ import annotations

import base64
from typing import Optional

import bcrypt

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    hashed_password_b64 = db.Column(db.LargeBinary(80))

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.hashed_password_b64 = base64.b64encode(
            bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email: str) -> Optional[UserModel]:
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: str) -> Optional[UserModel]:
        return cls.query.filter_by(id=_id).first()
