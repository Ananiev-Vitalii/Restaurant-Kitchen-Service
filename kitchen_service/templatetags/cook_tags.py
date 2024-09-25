from django import template
from kitchen_service.models import Cook

register = template.Library()


@register.simple_tag
def total_cooks_count():
    return Cook.objects.filter(is_superuser=False).count()


@register.simple_tag(takes_context=True)
def all_cooks(context, limit=None):
    request = context["request"]
    show_all = request.GET.get("show_all_cooks")
    cooks = Cook.objects.filter(
        is_superuser=False
    ).prefetch_related("cooked_dishes")
    if show_all:
        return cooks
    if limit is not None:
        return cooks[:limit]
    return cooks
