import re
from typing import Dict, Tuple

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
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
        if UserModel.find_by_email(email):
            return {"message": "A user with that e-mail address already exists."}, 409

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
