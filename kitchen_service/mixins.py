from django.http import Http404, HttpResponse
from typing import Any


class CookRequiredMixin:
    def dispatch(self, request: Any, *args, **kwargs) -> HttpResponse:
        if not getattr(request.user, "is_cook", False):
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)  # type: ignore
