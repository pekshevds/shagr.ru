from django.contrib import admin
from catalog_app.models import (
    Good,
    Category,
)
from server.admin import make_active

admin.site.site_header = "Панель администрирования goodcup"
admin.site.site_title = "Панель администрирования goodcup"
admin.site.index_title = "Добро пожаловать!"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "parent",
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
        "is_active",
        "parent",
        "created_at",
        "updated_at",
        "slug",
        "id",
    )
    actions = [make_active]


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "art",
                        "code",
                        "short_name",
                    ),
                    ("category",),
                    (
                        "balance",
                        "price",
                    ),
                    (
                        "is_active",
                        "sort_ordering",
                    ),
                    "comment",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                    "seo_keywords",
                )
            },
        ),
    )
    list_display = (
        "name",
        "art",
        "code",
        "okei",
        "is_active",
        "category",
        "balance",
        "price",
        "created_at",
        "updated_at",
        "id",
        "slug",
    )
    search_fields = ("name", "art")
    list_filter = ("is_active",)
    actions = [make_active]
