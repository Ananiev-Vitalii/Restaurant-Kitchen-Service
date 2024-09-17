from django.urls import path
from .views import DishListView

urlpatterns = [
    path("", DishListView.as_view(), name="home")
]

app_name = "kitchen_service"
