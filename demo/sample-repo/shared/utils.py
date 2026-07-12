"""Shared utilities for the demo repository."""

from shared.models import User
from shared.orders import Order  # circular: orders imports utils


def format_user_display(user: User) -> str:
    return f"{user.name} <{user.email}>"


def order_label(order: Order) -> str:
    return order.summary()
