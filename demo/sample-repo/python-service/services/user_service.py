"""User service with business logic."""

from shared.models import User
from shared.utils import format_user_display


def get_user(user_id: int) -> User:
    return User(id=user_id, name=f"User {user_id}", email=f"user{user_id}@demo.local")


def list_users(limit: int = 10) -> list[User]:
    return [get_user(i) for i in range(1, limit + 1)]


def user_display(user_id: int) -> str:
    user = get_user(user_id)
    return format_user_display(user)
