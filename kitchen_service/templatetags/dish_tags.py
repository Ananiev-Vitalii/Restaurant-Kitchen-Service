from django import template
from kitchen_service.models import Dish

register = template.Library()


@register.simple_tag
def popular_breakfasts():
    breakfasts = Dish.objects.filter(
        is_popular=True, meal_time="BF"
    ).prefetch_related("cooks", "ingredients")
    return breakfasts


@register.simple_tag
def popular_lunches():
    lunch = Dish.objects.filter(
        is_popular=True, meal_time="LN"
    ).prefetch_related("cooks", "ingredients")
    return lunch


@register.simple_tag
def popular_dinners():
    dinners = Dish.objects.filter(is_popular=True, meal_time="DN")
    return dinners
