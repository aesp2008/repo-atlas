# Patch utils to create circular dependency: utils -> models, orders -> utils
# orders imports utils, utils used by orders indirectly via models re-export

from shared.models import User
from shared.orders import Order

__all__ = ["User", "Order"]
