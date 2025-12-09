from django.contrib import admin
from server.admin import make_active
from client_app.models import Client, Pin, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "is_active", "created_at", "updated_at", "id")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "email",
                    ),
                    "organization",
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = (
        "name",
        "email",
        "organization",
        "is_active",
        "created_at",
        "updated_at",
        "id",
    )
    search_fields = ("name",)
    list_filter = ("organization",)
    actions = [make_active]


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("client", "code")},
        ),
    )
    list_display = ("code", "client", "created_at", "id")
    list_filter = ("client",)
