from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404, HttpRequest, HttpResponse
from kitchen_service.mixins import CookRequiredMixin
from kitchen_service.forms import OrderForm, CookRegistrationForm, CookUpdateForm
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


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen_service:account-update")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["is_cook"] = self.request.user.is_cook
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)


class CookOrderListView(LoginRequiredMixin, CookRequiredMixin, generic.ListView):
    model = Order
    template_name = "kitchen_service/cook_order_list.html"

    def get_queryset(self):
        return Order.objects.filter(cook=self.request.user)


class OrderActionView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        raise Http404("Page not found")

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        action = request.POST.get("action")

        if order_id and action:
            order = get_object_or_404(Order, pk=order_id, cook=self.request.user)
            if action in ["complete", "cancel"]:
                order.delete()

        return HttpResponseRedirect(reverse_lazy("kitchen_service:cook-orders-list"))


class CookRegistrationView(generic.CreateView):
    form_class = CookRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("kitchen_service:login")


def custom_page_not_found_view(
        request: HttpRequest, exception: Http404
) -> HttpResponse:
    return render(request, "404.html", status=404)
