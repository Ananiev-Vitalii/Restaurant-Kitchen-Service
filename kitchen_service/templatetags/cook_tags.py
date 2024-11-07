from typing import Any, Dict, Optional
from django.db.models import QuerySet
from django import template
from django.contrib.auth import get_user_model
from kitchen_service.models import Cook

User = get_user_model()
register = template.Library()


@register.simple_tag
def total_cooks_count() -> int:
    return get_user_model().objects.filter(is_cook=True).count()


@register.simple_tag(takes_context=True)
def all_cooks(
        context: Dict[str, Any], limit: Optional[int] = None
) -> QuerySet[Cook]:
    request = context["request"]
    show_all = request.GET.get("show_all_cooks")
    cooks = get_user_model().objects.filter(
        is_cook=True
    ).prefetch_related("cooked_dishes")
    if show_all:
        return cooks
    if limit is not None:
        return cooks[:limit]
    return cooks
