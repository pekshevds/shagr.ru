from django.urls import path
from api_app.views import CategoryView, GoodView

app_name = "api_app"

urlpatterns = [
    path("v1/pin/", PinView.as_view()),
    path("v1/token/", TokenView.as_view()),
    path("v1/catalog/good/", GoodView.as_view()),
    path("v1/catalog/good/<str:slug>/", GoodView.as_view()),
    path("v1/catalog/category/", CategoryView.as_view()),
    path("v1/catalog/category/<str:slug>/", CategoryView.as_view()),
]
