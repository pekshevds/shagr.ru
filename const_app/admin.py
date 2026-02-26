from django.contrib import admin
from const_app.models import Const, Vat


@admin.register(Vat)
class VatAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "value",
                    (
                        "is_active",
                        "sort_ordering",
                    ),
                    "comment",
                )
            },
        ),
    )
    list_display = (
        "name",
        "value",
        "is_active",
        "created_at",
        "updated_at",
        "id",
    )


@admin.register(Const)
class ConstAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "start",
                    "vat",
                )
            },
        ),
    )
    list_display = (
        "start",
        "vat",
    )
