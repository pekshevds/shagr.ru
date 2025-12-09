from django.urls import path
from api_app.views import CategoryView, GoodView, PinView, TokenView

app_name = "api_app"

urlpatterns = [
    path("v1/auth/pin/", PinView.as_view()),
    path("v1/auth/token/", TokenView.as_view()),
    path("v1/catalog/good/", GoodView.as_view()),
    path("v1/catalog/good/<str:slug>/", GoodView.as_view()),
    path("v1/catalog/category/", CategoryView.as_view()),
    path("v1/catalog/category/<str:slug>/", CategoryView.as_view()),
]
