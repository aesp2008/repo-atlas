"""Order processing service."""

from shared.models import User
from shared.orders import Order
from .user_service import get_user


def create_order(user_id: int) -> Order:
    user = get_user(user_id)
    return Order(order_id=user_id * 100, user_name=user.name)


def process_orders(user_ids: list[int]) -> list[str]:
    return [create_order(uid).summary() for uid in user_ids]
