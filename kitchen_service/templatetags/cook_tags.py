from django import template
from kitchen_service.models import Cook

register = template.Library()


@register.simple_tag
def total_cooks_count():
    return Cook.objects.count()
