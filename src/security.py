from typing import Optional, Dict, Any

from werkzeug.security import safe_str_cmp

from models.user import UserModel


def authenticate(email: str, password: str) -> Optional[UserModel]:
    user = UserModel.find_by_email(email)
    if user and safe_str_cmp(user.password, password):  # type: ignore
        return user
    return None


def identity(payload: Dict[str, Any]) -> Optional[UserModel]:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
