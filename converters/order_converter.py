from order_app.models import Order, OrderItem, CartItem
from order_app.schemas import (
    OrderSchemaOutgoing,
    OrderItemSchemaOutgoing,
    StatusSchemaOutgoing,
    CartItemSchemaOutgoing,
)
from converters.catalog_converter import good_to_outgoing_schema
from converters.client_converter import client_to_outgoing_schema


def _calculate_vat(value: float, vat: float) -> float:
    result = value - (value * vat / (100 + vat))
    return result


def cart_item_to_outgoing_schema(cart_item: CartItem) -> CartItemSchemaOutgoing:
    vat = float(cart_item.vat.value) if cart_item.vat else 0.0
    model = CartItemSchemaOutgoing(
        good=good_to_outgoing_schema(cart_item.good),
        okei=cart_item.good.okei,
        quantity=cart_item.quantity,
        price=cart_item.price,
        amount=cart_item.amount,
        vat=vat,
        price_without_vat=round(_calculate_vat(float(cart_item.price), vat), 2),
        amount_without_vat=round(_calculate_vat(float(cart_item.amount), vat), 2),
    )
    return model


def order_item_to_outgoing_schema(order_item: OrderItem) -> OrderItemSchemaOutgoing:
    vat = float(order_item.vat.value) if order_item.vat else 0.0
    model = OrderItemSchemaOutgoing(
        id=str(order_item.id),
        good=good_to_outgoing_schema(order_item.good),
        okei=order_item.good.okei,
        quantity=order_item.quantity,
        price=order_item.price,
        amount=order_item.amount,
        vat=vat,
        price_without_vat=round(_calculate_vat(float(order_item.price), vat), 2),
        amount_without_vat=round(_calculate_vat(float(order_item.amount), vat), 2),
    )
    return model


def order_to_outgoing_schema(order: Order) -> OrderSchemaOutgoing:
    model = OrderSchemaOutgoing(
        id=str(order.id),
        number=order.number,
        date=order.date,
        comment=order.comment,
        client=client_to_outgoing_schema(order.client),
        status=StatusSchemaOutgoing(
            id=str(order.status.id),
            name=order.status.name,
            is_closed=order.status.is_closed,
        ),
        items=[
            order_item_to_outgoing_schema(order_item)
            for order_item in order.items.all()
        ],
    )
    return model
