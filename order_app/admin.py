from django.contrib import admin
from order_app.models import Order, OrderItem, CartItem, WishItem, StatusOrder
from client_app.models import Organization


@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    (
                        "is_active",
                        "is_closed",
                    ),
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "is_active", "is_closed", "created_at", "updated_at", "id")
    search_fields = ("name",)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "number",
                        "date",
                    ),
                    "client",
                    "is_active",
                    (
                        "status",
                        "comment",
                    ),
                )
            },
        ),
    )
    list_display = (
        "__str__",
        "is_active",
        "client",
        "organization",
        "status",
        "updated_at",
        "id",
    )
    list_filter = (
        "client",
        "status",
        "client__organization",
    )
    readonly_fields = (
        "number",
        "date",
    )

    def organization(self, obj: Order) -> Organization | None:
        if obj.client:
            return obj.client.organization
        return None

    setattr(organization, "organization", "Организация")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "good",
                    "quantity",
                )
            },
        ),
    )
    list_display = ("client", "good", "quantity", "id")
    list_filter = ("client",)


@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "good",
                )
            },
        ),
    )
    list_display = ("client", "good", "id")
    list_filter = ("client",)
