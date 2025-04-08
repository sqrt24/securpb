from abc import ABC
from datetime import date

from django.conf import settings
from django.contrib.sites.models import Site

from project_settings.models import ProjectSettings


class BaseMiddleware(ABC):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response


def break_middleware(func):
    def _break_middleware_inner(*args, **kwargs):
        return func(*args, **kwargs)

    return _break_middleware_inner


class BaseViewMiddleware(BaseMiddleware):

    def process_view(self, request, view_func, view_args, view_kwargs):
        raise NotImplementedError("Inherits of BaseViewMiddleware class must implement process_view() method!")


class BaseContentMiddleware(BaseMiddleware):

    def __call__(self, request, *args, **kwargs):
        request.site = Site.objects.filter(id=settings.SITE_ID)
        request.project_settings = (
            ProjectSettings.objects.filter(site_id=settings.SITE_ID).first() if request.site else None
        )
        request.avg_rating = 4.3
        request.reviews_count = 125
        request.price_valid_until = date.today().strftime("%Y-%m-%d")
        return super().__call__(request, *args, **kwargs)
