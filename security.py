from typing import Any, Dict, Optional

from werkzeug.security import safe_str_cmp

from user import User


users = [User(1, "bob", "admin123")]
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenitcate(username: str, password: str) -> Optional[User]:
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload: dict) -> Optional[User]:
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)
