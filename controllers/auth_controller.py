import hashlib
from models.user_model import (
    get_user_by_username, create_user, update_last_login
)
from utils.validators import validate_user

# Simple in-memory session (replace with proper session handling if needed)
_current_user = None


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login(username, password):
    """
    Authenticate a user.
    Returns (True, user_dict) or (False, error_message).
    """
    global _current_user

    valid, error = validate_user({'username': username, 'password': password})
    if not valid:
        return False, error

    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password."

    if user['password_hash'] != _hash_password(password):
        return False, "Invalid username or password."

    update_last_login(user['id'])
    _current_user = user
    return True, user


def signup(username, password, full_name=None, email=None):
    """
    Register a new user.
    Returns (True, user_id) or (False, error_message).
    """
    valid, error = validate_user(
        {'username': username, 'password': password, 'email': email},
        is_signup=True
    )
    if not valid:
        return False, error

    existing = get_user_by_username(username)
    if existing:
        return False, "Username already taken."

    user_id = create_user(username, _hash_password(password), full_name, email)
    if not user_id:
        return False, "Could not create user. Please try again."

    return True, user_id


def logout():
    global _current_user
    _current_user = None


def get_current_user():
    return _current_user


def require_login():
    """Returns current user or raises RuntimeError if not logged in."""
    if not _current_user:
        raise RuntimeError("Not logged in.")
    return _current_user
