import unittest
from app.domain.models import OrderItem, OrderStatus
from app.services.order_service import OrderService


class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.service = OrderService()
        self.sample_items = [
            OrderItem(product_id="P1", product_name="Laptop", quantity=1, unit_price=1200.0)
        ]

    def test_create_order(self):
        order = self.service.create_order("CUST-1", self.sample_items)
        self.assertIsNotNone(order.id)
        self.assertEqual(order.customer_id, "CUST-1")
        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_idempotency_prevents_duplicate_orders(self):
        idempotency_key = "req-uuid-12345"
        # First request
        order1 = self.service.create_order("CUST-1", self.sample_items, idempotency_key=idempotency_key)
        # Duplicate network request with identical key
        order2 = self.service.create_order("CUST-1", self.sample_items, idempotency_key=idempotency_key)

        self.assertEqual(order1.id, order2.id)
        self.assertEqual(len(self.service.list_orders()), 1)

    def test_cancel_order(self):
        order = self.service.create_order("CUST-2", self.sample_items)
        cancelled = self.service.cancel_order(order.id)
        self.assertEqual(cancelled.status, OrderStatus.CANCELLED)


if __name__ == "__main__":
    unittest.main()
