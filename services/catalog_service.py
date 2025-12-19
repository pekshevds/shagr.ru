from django.core.paginator import Paginator
from django.conf import settings
from catalog_app.models import Good
from catalog_app.schemas import (
    CategorySchemaOutgoing,
    CategoryListSchemaOutgoing,
    GoodListSchemaIncoming,
    GoodSchemaOutgoing,
    GoodListSchemaOutgoing,
)
from converters import catalog_converter
from repositories import catalog_repository


def _fetch_goods(all_goods: list[Good]) -> list[GoodSchemaOutgoing]:
    goods = []
    for good in all_goods:
        good_schema = catalog_converter.good_to_outgoing_schema(good)
        good_schema.price = good.price
        good_schema.balance = good.balance
        goods.append(good_schema)
    return goods


def search_goods(search: str, page_number: int = 0) -> GoodListSchemaOutgoing:
    queryset = _fetch_goods(catalog_repository.search_goods(search))
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_all_categories() -> CategoryListSchemaOutgoing:
    categories = catalog_repository.fetch_all_active_categories()
    return CategoryListSchemaOutgoing(
        categories=[
            catalog_converter.category_to_outgoing_schema(cat) for cat in categories
        ],
        count=len(categories),
    )


def fetch_subcategories_by_slug(
    category_slug: str,
) -> CategoryListSchemaOutgoing | None:
    category = catalog_repository.fetch_category_by_slug(category_slug)
    if not category:
        return None
    categories = catalog_repository.fetch_active_subcategories(category)
    return CategoryListSchemaOutgoing(
        categories=[
            catalog_converter.category_to_outgoing_schema(cat) for cat in categories
        ],
        count=len(categories),
    )


def fetch_all_goods(page_number: int = 0) -> GoodListSchemaOutgoing:
    queryset = _fetch_goods(catalog_repository.fetch_all_active_goods())
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_category_by_slug(slug: str) -> CategorySchemaOutgoing | None:
    category = catalog_repository.fetch_category_by_slug(slug)
    if category:
        return catalog_converter.category_to_outgoing_schema(category)
    return None


def fetch_goods_by_category_slug(
    category_slug: str, page_number: int = 0
) -> GoodListSchemaOutgoing | None:
    category = catalog_repository.fetch_category_by_slug(category_slug)
    if not category:
        return None
    categories = [_ for _ in category.childs.all()]
    categories.append(category)
    goods = catalog_repository.fetch_goods_by_categories(categories)
    queryset = _fetch_goods(goods)
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_good_by_slug(slug: str) -> GoodSchemaOutgoing | None:
    good = catalog_repository.fetch_good_by_slug(slug)
    if not good:
        return None
    result = catalog_converter.good_to_outgoing_schema(good)

    result.price = good.price
    result.balance = good.balance
    return result


def create_or_update_goods(goods_list: GoodListSchemaIncoming) -> None:
    ids = [
        str(_.id)
        for _ in catalog_repository.fetch_goods_by_ids(
            [str(item.id) for item in goods_list.goods]
        )
    ]
    to_create = []
    to_update = []
    for _ in goods_list.goods:
        item = Good(**_.model_dump())
        if item.id in ids:
            to_update.append(item)
        else:
            to_create.append(item)
    catalog_repository.create_or_update_goods(to_create, to_update)
