from django import template
from kitchen_service.models import Cook

register = template.Library()


@register.simple_tag
def total_cooks_count():
    return Cook.objects.filter(is_superuser=False).count()


@register.simple_tag
def all_cooks():
    cooks = Cook.objects.filter(is_superuser=False)
    return cooks
