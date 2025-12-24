from typing import Callable, Any
import logging
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from services import catalog_service, client_service, order_service
from client_app.schemas import (
    ClientSchemaIncoming,
    ClientCredentialSchema,
    TokenSchema,
    SendEmailSchemaOutgoing,
)
from order_app.schemas import (
    AddCartItemSchemaIncoming,
    NewOrderIncoming,
    OrderStatusListUpdateSchemaIncoming,
)
from client_app.models import Client
from catalog_app.schemas import GoodListSchemaIncoming

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
                client_name=client_schema.email, email=client_schema.email, pin=pin
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


@method_decorator(csrf_exempt, name="dispatch")
class UploadCatalogView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        goods_list = GoodListSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        catalog_service.create_or_update_goods(goods_list)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        items = order_service.fetch_cart_items(client)
        return JsonResponse(items.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartSetView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.set_item_to_cart(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartAddView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.add_item_to_cart(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartDeleteView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.drop_item_from_cart(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartClearView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        order_service.clear_cart(client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class WishView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        items = order_service.fetch_wish_items(client)
        return JsonResponse(items.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class WishSetView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.set_item_to_wish(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class WishDeleteView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.drop_item_from_wish(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class WishClearView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        order_service.clear_wish(client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class OrderView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        date_from = request.GET.get("date_from", None)
        date_to = request.GET.get("date_to", None)
        new_orders = order_service.fetch_orders(client, date_from, date_to)
        return JsonResponse(new_orders.model_dump(), status=200)

    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = NewOrderIncoming.model_validate_json(request.body.decode("utf-8"))
        order = order_service.create_order(data)
        if order:
            return JsonResponse(order.model_dump(), status=200)
        return JsonResponse({}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ActiveOrderView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        date_from = request.GET.get("date_from", None)
        date_to = request.GET.get("date_to", None)
        new_orders = order_service.fetch_active_orders(client, date_from, date_to)
        return JsonResponse(new_orders.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class ClosedOrderView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        date_from = request.GET.get("date_from", None)
        date_to = request.GET.get("date_to", None)
        new_orders = order_service.fetch_closed_orders(client, date_from, date_to)
        return JsonResponse(new_orders.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class NewOrderView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        new_orders = order_service.fetch_new_orders()
        return JsonResponse(new_orders.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateOrderStatusView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = OrderStatusListUpdateSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.update_order_statuses(data)
        return JsonResponse({}, status=200)
