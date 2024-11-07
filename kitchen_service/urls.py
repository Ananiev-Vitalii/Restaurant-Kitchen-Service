from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import (
    CustomSetPasswordForm,
    CookAuthenticationForm,
    CustomPasswordResetForm
)
from .views import (
    DishListView,
    AboutTemplateView,
    MenuListView,
    OrderCreateView,
    OrderListView,
    CookRegistrationView,
    CookUpdateView,
    CookOrderListView,
    OrderActionView
)

app_name = "kitchen_service"

urlpatterns = [

    # Main Views
    path("", DishListView.as_view(), name="index"),
    path("about/", AboutTemplateView.as_view(), name="about-template"),
    path("menu/", MenuListView.as_view(), name="menu-list"),
    path(
        "order/<int:pk>/create/",
        OrderCreateView.as_view(),
        name="order-create"
    ),
    path("account/update/", CookUpdateView.as_view(), name="account-update"),
    path("cook/orders/", CookOrderListView.as_view(), name="cook-orders-list"),
    path(
        "cook/orders/action/api/",
        OrderActionView.as_view(),
        name="order-action"
    ),
    path("orders/", OrderListView.as_view(), name="orders-list"),

    # Registration & Authentication Views
    path("accounts/login/", auth_views.LoginView.as_view(
        form_class=CookAuthenticationForm
    ), name="login"),

    path(
        "accounts/register/", CookRegistrationView.as_view(), name="register"
    ),

    path("accounts/logout/", auth_views.LogoutView.as_view(
        next_page="kitchen_service:index"
    ), name="logout"),

    path("accounts/password_reset/",
         auth_views.PasswordResetView.as_view(
             form_class=CustomPasswordResetForm,
             success_url=reverse_lazy("kitchen_service:password-reset-done")
         ),
         name="password-reset"),

    path("accounts/password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(),
         name="password-reset-done"),

    path("accounts/reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             form_class=CustomSetPasswordForm,
             success_url=reverse_lazy(
                 "kitchen_service:password-reset-complete"
             ),
         ),
         name="password-reset-confirm"),

    path("accounts/reset/done/",
         auth_views.PasswordResetCompleteView.as_view(),
         name="password-reset-complete"),
]
