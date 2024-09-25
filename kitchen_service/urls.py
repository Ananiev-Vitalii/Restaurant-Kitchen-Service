from django.urls import path
from .views import DishListView, AboutTemplateView

urlpatterns = [
    path("", DishListView.as_view(), name="home"),
    path("about/", AboutTemplateView.as_view(), name="about")
]

app_name = "kitchen_service"
