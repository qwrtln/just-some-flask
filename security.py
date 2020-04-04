import bcrypt
from typing import Optional, Dict, Any

from models.user import UserModel


def authenticate(email: str, password: str) -> Optional[UserModel]:
    user = UserModel.find_by_email(email)
    if user and bcrypt.checkpw(password.encode(), user.hashed_password):
        return user
    return None


def identity(payload: Dict[str, Any]) -> Optional[UserModel]:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
