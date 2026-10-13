from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field
from app.domain.models import OrderItem, OrderStatus
from app.services.order_service import order_service

router = APIRouter(prefix="/orders", tags=["Order Management"])


class OrderItemRequest(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(gt=0, description="Quantity must be greater than zero")
    unit_price: float = Field(ge=0.0, description="Unit price cannot be negative")


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemRequest]


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    subtotal: float
    tax_amount: float
    total_amount: float
    created_at: str
    updated_at: str
    idempotency_key: Optional[str] = None


def _serialize_order(order) -> dict:
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "status": order.status.value,
        "subtotal": order.subtotal,
        "tax_amount": order.tax_amount,
        "total_amount": order.total_amount,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
        "idempotency_key": order.idempotency_key,
    }


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create new order with idempotency")
async def create_order(
    payload: CreateOrderRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
):
    try:
        items = [
            OrderItem(
                product_id=i.product_id,
                product_name=i.product_name,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in payload.items
        ]
        order = order_service.create_order(
            customer_id=payload.customer_id,
            items=items,
            idempotency_key=idempotency_key,
        )
        return _serialize_order(order)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}", summary="Get order by ID")
async def get_order(order_id: str):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return _serialize_order(order)


@router.patch("/{order_id}/status", summary="Transition order status")
async def transition_status(order_id: str, new_status: OrderStatus):
    try:
        order = order_service.transition_order(order_id, new_status)
        return _serialize_order(order)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/{order_id}/cancel", summary="Cancel order")
async def cancel_order(order_id: str):
    try:
        order = order_service.cancel_order(order_id)
        return _serialize_order(order)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("", summary="List orders")
async def list_orders(customer_id: Optional[str] = None):
    orders = order_service.list_orders(customer_id=customer_id)
    return [_serialize_order(o) for o in orders]
