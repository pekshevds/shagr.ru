from django.conf import settings
from catalog_app.models import Category, Good, Image
from catalog_app.schemas import (
    CategorySchemaOutgoing,
    GoodSchemaOutgoing,
    ImageSchemaOutgoing,
)


def image_to_outgoing_schema(image: Image) -> ImageSchemaOutgoing | None:
    if image:
        return ImageSchemaOutgoing(
            path=f"https://{settings.BACKEND_NAME}{image.image.url}"
        )
    return None


def images_to_outgoing_schema(
    images: list[Image],
) -> list[ImageSchemaOutgoing] | None:
    if images:
        return [image_to_outgoing_schema(image.image) for image in images]
    return None


def category_to_outgoing_schema(category: Category) -> CategorySchemaOutgoing:
    model = CategorySchemaOutgoing(
        id=str(category.id),
        name=category.name,
        slug=category.slug,
        parent_slug=category.parent.slug if category.parent else "",
        preview_image=image_to_outgoing_schema(category.preview_image),
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
        preview_image=image_to_outgoing_schema(good.preview_image),
        images=images_to_outgoing_schema(good.images.all()),
        seo_title=good.seo_title,
        seo_description=good.seo_description,
        seo_keywords=good.seo_keywords,
    )
    return model
