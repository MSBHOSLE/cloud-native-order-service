import unittest
from app.domain.models import Order, OrderItem, OrderStatus


class TestOrderDomain(unittest.TestCase):
    def test_order_item_subtotal_and_validation(self):
        item = OrderItem(product_id="PROD-1", product_name="Keyboard", quantity=2, unit_price=50.0)
        self.assertEqual(item.subtotal, 100.0)

        with self.assertRaises(ValueError):
            OrderItem(product_id="PROD-2", product_name="Mouse", quantity=0, unit_price=25.0)

        with self.assertRaises(ValueError):
            OrderItem(product_id="PROD-3", product_name="Monitor", quantity=1, unit_price=-10.0)

    def test_order_totals_and_tax(self):
        items = [
            OrderItem(product_id="P1", product_name="Item 1", quantity=2, unit_price=50.0),  # 100
            OrderItem(product_id="P2", product_name="Item 2", quantity=1, unit_price=200.0), # 200
        ]
        order = Order(customer_id="CUST-100", items=items, tax_rate=0.10)
        self.assertEqual(order.subtotal, 300.0)
        self.assertEqual(order.tax_amount, 30.0)
        self.assertEqual(order.total_amount, 330.0)
        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_order_empty_items_validation(self):
        with self.assertRaises(ValueError):
            Order(customer_id="CUST-100", items=[])

    def test_order_state_transitions(self):
        item = OrderItem(product_id="P1", product_name="Book", quantity=1, unit_price=20.0)
        order = Order(customer_id="CUST-1", items=[item])

        # Valid transitions
        order.transition_to(OrderStatus.VALIDATED)
        self.assertEqual(order.status, OrderStatus.VALIDATED)

        order.transition_to(OrderStatus.PROCESSING)
        self.assertEqual(order.status, OrderStatus.PROCESSING)

        order.transition_to(OrderStatus.COMPLETED)
        self.assertEqual(order.status, OrderStatus.COMPLETED)

        # Terminal state cannot transition
        with self.assertRaises(ValueError):
            order.transition_to(OrderStatus.PENDING)

    def test_invalid_transition_raises(self):
        item = OrderItem(product_id="P1", product_name="Book", quantity=1, unit_price=20.0)
        order = Order(customer_id="CUST-1", items=[item])

        # Directly from PENDING to COMPLETED is prohibited
        with self.assertRaises(ValueError):
            order.transition_to(OrderStatus.COMPLETED)


if __name__ == "__main__":
    unittest.main()
