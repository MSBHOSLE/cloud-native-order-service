from typing import Dict, List, Optional
from app.domain.models import Order, OrderItem, OrderStatus


class OrderService:
    def __init__(self):
        # In-memory storage & Idempotency registry for repository pattern
        self._orders: Dict[str, Order] = {}
        self._idempotency_map: Dict[str, str] = {}  # idempotency_key -> order_id

    def create_order(
        self,
        customer_id: str,
        items: List[OrderItem],
        idempotency_key: Optional[str] = None,
        tax_rate: float = 0.08,
    ) -> Order:
        """Create new order with guaranteed idempotency."""
        # 1. Idempotency Check
        if idempotency_key:
            existing_order_id = self._idempotency_map.get(idempotency_key)
            if existing_order_id and existing_order_id in self._orders:
                return self._orders[existing_order_id]

        # 2. Domain Model Construction & Invariant Validation
        order = Order(
            customer_id=customer_id,
            items=items,
            tax_rate=tax_rate,
            idempotency_key=idempotency_key,
        )

        self._orders[order.id] = order
        if idempotency_key:
            self._idempotency_map[idempotency_key] = order.id

        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def list_orders(self, customer_id: Optional[str] = None) -> List[Order]:
        orders = list(self._orders.values())
        if customer_id:
            return [o for o in orders if o.customer_id == customer_id]
        return orders

    def transition_order(self, order_id: str, new_status: OrderStatus) -> Order:
        order = self.get_order(order_id)
        if not order:
            raise KeyError(f"Order with ID {order_id} not found.")
        order.transition_to(new_status)
        return order

    def cancel_order(self, order_id: str) -> Order:
        return self.transition_order(order_id, OrderStatus.CANCELLED)


order_service = OrderService()
