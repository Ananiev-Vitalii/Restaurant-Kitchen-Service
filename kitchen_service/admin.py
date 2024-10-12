from django.contrib import admin
from .models import Cook, Ingredient, DishType, Dish, Order
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    search_fields = ["username", "first_name", "last_name"]
    search_help_text = "Search by username, first_name or description"
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {
            "fields": (
                "photo",
                "years_of_experience",
                "facebook_link",
                "instagram_link",
                "twitter_link"
            )
        }),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = [
        "name", "price", "dish_type", "get_cooks", "get_ingredients"
    ]
    search_fields = ["name"]
    search_help_text = "Search by name"
    list_filter = ["dish_type__name", "is_popular"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related(
            "cooks", "ingredients"
        )

    def get_cooks(self, obj: Dish) -> str:
        return ", ".join([cook.username for cook in obj.cooks.all()])

    get_cooks.short_description = "Cooks"

    def get_ingredients(self, obj: Dish) -> str:
        return ", ".join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    get_ingredients.short_description = "Ingredients"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number", "customer_name", "total_price", "status", "dishes"
    ]
    search_fields = ["order_number", "customer_name"]
    search_help_text = "Search by order_number  or customer_name"
    list_filter = ["status"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related("dishes")
