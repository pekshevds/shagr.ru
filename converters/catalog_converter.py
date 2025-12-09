from catalog_app.models import Category, Good
from catalog_app.schemas import (
    CategorySchemaOutgoing,
    GoodSchemaOutgoing,
)


def category_to_outgoing_schema(category: Category) -> CategorySchemaOutgoing:
    model = CategorySchemaOutgoing(
        id=str(category.id),
        name=category.name,
        slug=category.slug,
        parent_slug=category.parent.slug if category.parent else "",
        childs=[
            category_to_outgoing_schema(c)
            for c in category.childs.filter(is_active=True).all()
        ],
    )
    return model


def good_to_outgoing_schema(good: Good) -> GoodSchemaOutgoing:
    price = good.price
    balance = good.balance
    model = GoodSchemaOutgoing(
        id=str(good.id),
        name=good.name,
        short_name=good.short_name,
        art=good.art,
        slug=good.slug,
        code=good.code,
        okei=good.okei,
        price=price,
        description=good.description,
        balance=balance,
        is_active=good.is_active,
        seo_title=good.seo_title,
        seo_description=good.seo_description,
        seo_keywords=good.seo_keywords,
    )
    return model
