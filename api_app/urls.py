from django.urls import path
from api_app.views import (
    CategoryView,
    GoodView,
    PinView,
    TokenView,
    CartView,
    CartSetView,
    CartAddView,
    CartDeleteView,
    CartClearView,
    WishView,
    WishSetView,
    WishDeleteView,
    WishClearView,
    OrderView,
    NewOrderView,
    UpdateOrderStatusView,
    UploadCatalogView,
)

app_name = "api_app"

urlpatterns = [
    path("v1/auth/pin/", PinView.as_view()),
    path("v1/auth/token/", TokenView.as_view()),
    path("v1/catalog/good/", GoodView.as_view()),
    path("v1/catalog/good/<str:slug>/", GoodView.as_view()),
    path("v1/catalog/category/", CategoryView.as_view()),
    path("v1/catalog/category/<str:slug>/", CategoryView.as_view()),
    path("v1/cart/", CartView.as_view()),
    path("v1/cart/set/", CartSetView.as_view()),
    path("v1/cart/add/", CartAddView.as_view()),
    path("v1/cart/delete/", CartDeleteView.as_view()),
    path("v1/cart/clear/", CartClearView.as_view()),
    path("v1/wish/", WishView.as_view()),
    path("v1/wish/set/", WishSetView.as_view()),
    path("v1/wish/delete/", WishDeleteView.as_view()),
    path("v1/wish/clear/", WishClearView.as_view()),
    path("v1/orders/", OrderView.as_view()),
    path("v1/orders/get-new/", NewOrderView.as_view()),
    path("v1/orders/update-statuses/", UpdateOrderStatusView.as_view()),
    path("v1/catalog/upload/", UploadCatalogView.as_view()),
]
