from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Cook, Ingredient, DishType, Dish, Order
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.db.models import ForeignKey, ManyToManyField
from typing import Optional, List, Tuple, Any
from django import forms


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", "is_cook")
    search_fields = ["username", "first_name", "last_name"]
    search_help_text = "Search by username, first_name or last_name"

    additional_info_fields = ("years_of_experience", "is_cook")
    social_links_fields = ("facebook_link", "instagram_link", "twitter_link")
    photo_field = ("photo",)

    list_filter = UserAdmin.list_filter + ("is_cook", "years_of_experience")

    def get_fieldsets(
            self, request: HttpRequest, obj: Optional[Any] = None
    ) -> List[Tuple[str, dict]]:
        fieldsets = list(super().get_fieldsets(request, obj))

        if obj and obj.is_cook:
            fieldsets.append(
                ("Additional info", {
                    "fields": self.photo_field + self.additional_info_fields + self.social_links_fields
                }),
            )
        else:
            fieldsets.append(
                ("Additional info", {
                    "fields": ("is_cook",)
                }),
            )
        return fieldsets


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

    def formfield_for_manytomany(
            self, db_field: ManyToManyField, request: HttpRequest, **kwargs
    ) -> Optional[forms.ModelMultipleChoiceField]:
        if db_field.name == "cooks":
            kwargs["queryset"] = get_user_model().objects.filter(is_cook=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_cooks(self, obj: Dish) -> str:
        return ", ".join([cook.username for cook in obj.cooks.filter(is_cook=True)])

    def get_ingredients(self, obj: Dish) -> str:
        return ", ".join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    get_cooks.short_description = "Cooks"
    get_ingredients.short_description = "Ingredients"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number", "customer_name", "dishes",
        "quantity", "total_price", "cook", "status"
    ]
    search_fields = ["order_number", "customer_name"]
    search_help_text = "Search by order_number or customer_name"
    list_filter = ["status"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related("dishes")

    def formfield_for_foreignkey(
            self, db_field: ForeignKey, request: HttpRequest, **kwargs
    ) -> Optional[forms.ModelChoiceField]:
        if db_field.name == "cook":
            kwargs["queryset"] = get_user_model().objects.filter(is_cook=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
