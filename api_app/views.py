import logging
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from services import catalog_service

logger = logging.getLogger(__name__)


class CategoryView(View):
    def get(self, request: HttpRequest, slug: str = "") -> JsonResponse:
        if slug:
            category = catalog_service.fetch_category_by_slug(slug)
            if category:
                return JsonResponse(category.model_dump(), status=200)
            return JsonResponse({}, status=200)
        categories = catalog_service.fetch_all_categories()
        return JsonResponse(categories.model_dump(), status=200)


class GoodView(View):
    def get(self, request: HttpRequest, slug: str = "") -> JsonResponse:
        goods = None
        page_number = request.GET.get("page", 0)
        if slug:
            good = catalog_service.fetch_good_by_slug(slug)
            if good:
                return JsonResponse(good.model_dump(), status=200)
            return JsonResponse({}, status=400)
        search = request.GET.get("search")
        if search:
            goods = catalog_service.search_goods(search, page_number)
            return JsonResponse(goods.model_dump(), status=200)
        category_slug = request.GET.get("category")
        if category_slug:
            goods = catalog_service.fetch_goods_by_category_slug(
                category_slug, page_number
            )
            if goods:
                return JsonResponse(goods.model_dump(), status=200)
            return JsonResponse({}, status=200)
        compilation_slug = request.GET.get("compilation")
        if compilation_slug:
            goods = catalog_service.fetch_goods_by_compilation_slug(
                compilation_slug, page_number
            )
            if goods:
                return JsonResponse(goods.model_dump(), status=200)
            return JsonResponse({}, status=200)
        goods = catalog_service.fetch_all_goods(page_number)
        return JsonResponse(goods.model_dump(), status=200)
