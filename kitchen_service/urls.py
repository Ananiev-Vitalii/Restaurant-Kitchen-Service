from django.urls import path
from .views import (
    DishListView,
    AboutTemplateView,
    MenuListView,
    OrderCreateView,
    OrdersListView
)

urlpatterns = [
    path("", DishListView.as_view(), name="home"),
    path("about/", AboutTemplateView.as_view(), name="about"),
    path("menu/", MenuListView.as_view(), name="menu"),
    path("order/<int:pk>/", OrderCreateView.as_view(), name="order"),
    path("orders/", OrdersListView.as_view(), name="orders")
]

app_name = "kitchen_service"
