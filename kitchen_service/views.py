from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from kitchen_service.forms import OrderForm
from kitchen_service.models import Dish, DishType


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


class OrderCreateView(generic.CreateView):
    form_class = OrderForm
    template_name = "kitchen_service/order_form.html"
    success_url = reverse_lazy("kitchen_service:home")

    def form_valid(self, form):
        dish = get_object_or_404(Dish, pk=self.kwargs.get("pk"))
        form.instance.dishes = dish
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = get_object_or_404(Dish, pk=self.kwargs.get("pk"))
        return context
