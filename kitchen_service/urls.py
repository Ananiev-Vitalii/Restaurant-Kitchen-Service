from django.urls import path
from .views import (
    DishListView,
    AboutTemplateView,
    MenuListView)

urlpatterns = [
    path("", DishListView.as_view(), name="home"),
    path("about/", AboutTemplateView.as_view(), name="about"),
    path("menu/", MenuListView.as_view(), name="menu")
]

app_name = "kitchen_service"
