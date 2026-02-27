from order_app.models import Order, OrderItem, CartItem, WishItem, StatusOrder
from order_app.schemas import (
    OrderSchemaOutgoing,
    OrderItemSchemaOutgoing,
    StatusSchemaOutgoing,
    CartItemSchemaOutgoing,
    WishItemSchemaOutgoing,
    AvailableStatusSchemaOutgoing,
)
from converters.catalog_converter import good_to_outgoing_schema
from converters.client_converter import client_to_outgoing_schema
from repositories.const_repository import fetch_last_vat


def _calculate_vat(value: float, vat: float) -> float:
    result = value - (value * vat / (100 + vat))
    return result


def cart_item_to_outgoing_schema(cart_item: CartItem) -> CartItemSchemaOutgoing:
    _ = fetch_last_vat()
    vat = float(_.value) if _ else 0.0
    price = float(cart_item.good.price)
    amount = price * float(cart_item.quantity)
    okei = cart_item.good.okei
    model = CartItemSchemaOutgoing(
        good=good_to_outgoing_schema(cart_item.good),
        okei=okei,
        quantity=cart_item.quantity,
        price=price,
        amount=amount,
        vat=vat,
        price_without_vat=round(_calculate_vat(price, vat), 2),
        amount_without_vat=round(_calculate_vat(amount, vat), 2),
        required_date=cart_item.required_date,
        possible_date=cart_item.possible_date,
    )
    return model


def wish_item_to_outgoing_schema(wish_item: WishItem) -> WishItemSchemaOutgoing:
    _ = fetch_last_vat()
    vat = float(_.value) if _ else 0.0
    price = float(wish_item.good.price)
    amount = price * 1
    okei = wish_item.good.okei
    model = WishItemSchemaOutgoing(
        good=good_to_outgoing_schema(wish_item.good),
        okei=okei,
        quantity=1,
        price=price,
        amount=amount,
        vat=vat,
        price_without_vat=round(_calculate_vat(price, vat), 2),
        amount_without_vat=round(_calculate_vat(amount, vat), 2),
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
        required_date=order_item.required_date,
        possible_date=order_item.possible_date,
    )
    return model


def order_to_outgoing_schema(order: Order) -> OrderSchemaOutgoing:
    model = OrderSchemaOutgoing(
        id=str(order.id),
        number=order.number,
        date=order.date,
        comment=order.comment,
        client=client_to_outgoing_schema(order.client),
        sap_number=order.sap_number,
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


def available_status_to_outgoing_schema(
    status: StatusOrder,
) -> AvailableStatusSchemaOutgoing:
    return AvailableStatusSchemaOutgoing(
        id=str(status.id),
        name=status.name,
    )
