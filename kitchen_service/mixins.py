from django.http import Http404, HttpResponse, HttpRequest


class CookRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not getattr(request.user, "is_cook", False):  # noqa
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)
