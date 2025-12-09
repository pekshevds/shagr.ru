from typing import Callable, Any
import logging
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from services import catalog_service, client_service
from client_app.schemas import (
    ClientSchemaIncoming,
    ClientCredentialSchema,
    TokenSchema,
    SendEmailSchemaOutgoing,
)

logger = logging.getLogger(__name__)


def auth(only: bool = True) -> Callable:
    def out_wrapper(view_function: Callable) -> Callable:
        def in_wrapper(
            obj: Any, request: HttpRequest, **kwargs: dict[str, Any]
        ) -> JsonResponse:
            token = client_service.extract_token(request)
            client = client_service.client_by_token(token)
            if only and client is None:
                raise PermissionDenied("bad Auth token")
            return view_function(obj, request, client, **kwargs)

        return in_wrapper

    return out_wrapper


@method_decorator(csrf_exempt, name="dispatch")
class PinView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        client_schema = ClientSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        pin = client_service.fetch_pin_by_client(client_schema)
        if pin:
            pin_schema = SendEmailSchemaOutgoing(
                client_name=client_schema.name, email=client_schema.name, pin=pin
            )
            client_service.send_pin_by_email(pin_schema)
            return JsonResponse({}, status=200)
        return JsonResponse({}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        credential = ClientCredentialSchema.model_validate_json(
            request.body.decode("utf-8")
        )
        token = client_service.fetch_token_by_credentials(credential)
        if not token:
            raise PermissionDenied("bad name or pin")
        response = JsonResponse(TokenSchema(token=token).model_dump(), status=200)
        response.set_cookie("Authorization", token)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request: HttpRequest, slug: str = "") -> JsonResponse:
        if slug:
            category = catalog_service.fetch_category_by_slug(slug)
            if category:
                return JsonResponse(category.model_dump(), status=200)
            return JsonResponse({}, status=200)
        categories = catalog_service.fetch_all_categories()
        return JsonResponse(categories.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
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
        goods = catalog_service.fetch_all_goods(page_number)
        return JsonResponse(goods.model_dump(), status=200)
