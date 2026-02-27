from datetime import datetime
from pydantic import BaseModel, Field
from client_app.schemas import ClientSchemaOutgoing
from catalog_app.schemas import GoodSchemaOutgoing


class StatusSchemaIncoming(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)


class StatusSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field()
    is_closed: bool = Field()


class OrderItemSchemaOutgoing(BaseModel):
    id: str = Field()
    good: GoodSchemaOutgoing = Field()
    okei: str = Field()
    quantity: float = Field()
    price: float = Field()
    amount: float = Field()
    vat: float = Field()
    price_without_vat: float = Field()
    amount_without_vat: float = Field()
    required_date: datetime | None = Field(default=None)
    possible_date: datetime | None = Field(default=None)


class OrderSchemaOutgoing(BaseModel):
    id: str = Field()
    number: int = Field()
    date: datetime = Field()
    comment: str = Field(default="")
    client: ClientSchemaOutgoing = Field()
    sap_number: str = Field(default="")
    status: StatusSchemaOutgoing = Field()
    items: list[OrderItemSchemaOutgoing] = Field(default=[])


class AvailableStatusSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field()


class AvailableStatusListSchemaOutgoing(BaseModel):
    statuses: list[AvailableStatusSchemaOutgoing] = Field()


class OrderListSchemaOutgoing(BaseModel):
    orders: list[OrderSchemaOutgoing] = Field()


class NewOrderItemIncoming(BaseModel):
    good_slug: str = Field()
    quantity: float = Field(default=0.0)
    price: float = Field(default=0.0)
    amount: float = Field(default=0.0)


class NewOrderIncoming(BaseModel):
    items: list[NewOrderItemIncoming] = Field()


class CartItemSchemaOutgoing(BaseModel):
    good: GoodSchemaOutgoing = Field()
    okei: str = Field()
    quantity: float = Field(default=0.0)
    price: float = Field(default=0.0)
    amount: float = Field(default=0.0)
    vat: float = Field()
    price_without_vat: float = Field()
    amount_without_vat: float = Field()
    required_date: datetime | None = Field(default=None)
    possible_date: datetime | None = Field(default=None)


class CartItemListSchemaOutgoing(BaseModel):
    items: list[CartItemSchemaOutgoing] = Field()


class AddCartItemSchemaIncoming(BaseModel):
    good_slug: str = Field()
    quantity: float = Field(default=0.0)


class WishItemSchemaOutgoing(BaseModel):
    good: GoodSchemaOutgoing = Field()
    okei: str = Field()
    quantity: float = Field(default=0.0)
    price: float = Field(default=0.0)
    amount: float = Field(default=0.0)
    vat: float = Field()
    price_without_vat: float = Field()
    amount_without_vat: float = Field()


class WishItemListSchemaOutgoing(BaseModel):
    items: list[WishItemSchemaOutgoing] = Field()


class AddWishItemSchemaIncoming(BaseModel):
    good_slug: str = Field()
    quantity: float = Field(default=0.0)


class OrderStatusUpdateSchemaIncoming(BaseModel):
    order_id: str = Field()
    status_id: str = Field()


class OrderStatusListUpdateSchemaIncoming(BaseModel):
    statuses: list[OrderStatusUpdateSchemaIncoming] = Field()
