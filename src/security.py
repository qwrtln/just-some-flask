from typing import Any, Dict, Optional

from werkzeug.security import safe_str_cmp

from user import User


def authenitcate(email: str, password: str) -> Optional[User]:
    user = User.find_by_email(email)
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload: dict) -> Optional[User]:
    user_id = payload["identity"]
    return User.find_by_id(user_id)
