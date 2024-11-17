from django import template
from django.db.models import QuerySet
from kitchen_service.models import Dish

register = template.Library()


@register.simple_tag
def popular_breakfasts() -> QuerySet[Dish]:
    breakfasts = Dish.objects.filter(
        is_popular=True, meal_time="BF"
    )
    return breakfasts


@register.simple_tag
def popular_lunches() -> QuerySet[Dish]:
    lunch = Dish.objects.filter(
        is_popular=True, meal_time="LN"
    )
    return lunch


@register.simple_tag
def popular_dinners() -> QuerySet[Dish]:
    dinners = Dish.objects.filter(
        is_popular=True, meal_time="DN"
    )
    return dinners
