from django.views import generic

from kitchen_service.models import Dish, DishType, Order


class DishListView(generic.ListView):
    model = Dish
    template_name = "kitchen_service/index.html"
    context_object_name = "dish_list"
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")


class AboutTemplateView(generic.TemplateView):
    template_name = "kitchen_service/about.html"
    extra_context = {
        "dish_list": Dish.objects.all().prefetch_related(
            "cooks", "ingredients"
        )
    }


class MenuListView(generic.ListView):
    model = DishType
    template_name = "kitchen_service/menu.html"
    context_object_name = "dish_type_list"
    queryset = DishType.objects.all()

# class Order(generic.DetailView):
#     model = Order
#     template_name = "kitchen_service/order.html"
#     context_object_name = "order_detail"
#     queryset = Order.objects.select_related(
#         "dishes", "cook"
#     ).prefetch_related("dishes__cooks", "dishes__ingredients")
