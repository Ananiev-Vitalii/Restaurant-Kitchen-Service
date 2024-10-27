from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from kitchen_service.forms import OrderForm, CookRegistrationForm
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


class OrderCreateView(generic.CreateView):
    form_class = OrderForm
    template_name = "kitchen_service/order_form.html"
    success_url = reverse_lazy("kitchen_service:menu-list")

    def get_dish(self) -> Dish:
        return get_object_or_404(Dish, pk=self.kwargs.get("pk"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs["customer"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = self.get_dish()
        return context

    def form_valid(self, form):
        form.instance.dishes = self.get_dish()
        return super().form_valid(form)


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.all().select_related(
        "cook", "dishes__dish_type"
    ).prefetch_related(
        "dishes__ingredients", "dishes__cooks"
    )


class CookRegistrationView(generic.CreateView):
    form_class = CookRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("kitchen_service:login")
