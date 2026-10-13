from dataclasses import dataclass, field
from datetime import datetime, timezone
import enum
from typing import Dict, List, Optional
import uuid


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# Allowed state transitions
VALID_TRANSITIONS: Dict[OrderStatus, List[OrderStatus]] = {
    OrderStatus.PENDING: [OrderStatus.VALIDATED, OrderStatus.CANCELLED],
    OrderStatus.VALIDATED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
    OrderStatus.PROCESSING: [OrderStatus.COMPLETED, OrderStatus.CANCELLED],
    OrderStatus.COMPLETED: [],
    OrderStatus.CANCELLED: [],
}


@dataclass
class OrderItem:
    product_id: str
    product_name: str
    quantity: int
    unit_price: float

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError(f"Quantity for product {self.product_id} must be > 0.")
        if self.unit_price < 0:
            raise ValueError(f"Unit price for product {self.product_id} cannot be negative.")

    @property
    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    customer_id: str
    items: List[OrderItem]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: OrderStatus = OrderStatus.PENDING
    tax_rate: float = 0.08
    idempotency_key: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not self.customer_id:
            raise ValueError("Customer ID cannot be empty.")
        if not self.items:
            raise ValueError("Order must contain at least one item.")

    @property
    def subtotal(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    @property
    def tax_amount(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total_amount(self) -> float:
        return round(self.subtotal + self.tax_amount, 2)

    def transition_to(self, new_status: OrderStatus) -> None:
        """Enforce domain state machine invariants."""
        if new_status not in VALID_TRANSITIONS.get(self.status, []):
            raise ValueError(
                f"Invalid transition from {self.status.value} to {new_status.value}."
            )
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)
