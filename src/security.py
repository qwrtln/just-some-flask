from typing import Optional

from werkzeug.security import safe_str_cmp

from models.user import UserModel


def authenitcate(email: str, password: str) -> Optional[UserModel]:
    user = UserModel.find_by_email(email)
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload: dict) -> Optional[UserModel]:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
