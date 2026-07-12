"""Order models - circular dependency with shared.utils."""

from shared.utils import format_user_display


class Order:
    def __init__(self, order_id: int, user_name: str):
        self.order_id = order_id
        self.user_name = user_name

    def summary(self) -> str:
        return f"Order #{self.order_id} for {self.user_name}"
