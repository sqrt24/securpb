from datetime import date
from typing import TYPE_CHECKING

from django.conf import settings

from services.models import Service, ServiceCategory

if TYPE_CHECKING:
    from seo.services import SEOProtocol


def get_seo_title(request):
    seo_title = None
    if hasattr(request, "seo_object") and hasattr(request.seo_object, "render_title"):
        request.seo_object: "SEOProtocol"
        seo_title = request.seo_object.render_title(request)
    if not seo_title:
        seo_title = request.seo_parameter.render_title(request)
    return seo_title


def get_seo_description(request):
    seo_description = None
    if hasattr(request, "seo_object") and hasattr(request.seo_object, "render_description"):
        request.seo_object: "SEOProtocol"
        seo_description = request.seo_object.render_description(request)
    if not seo_description:
        seo_description = request.seo_parameter.render_description(request)
    return seo_description


def get_seo_h1(request):
    seo_h1 = None
    if hasattr(request, "seo_object") and hasattr(request.seo_object, "render_h1"):
        request.seo_object: "SEOProtocol"
        try:
            seo_h1 = request.seo_object.render_h1(request)
        except Exception:
            pass
    if not seo_h1:
        seo_h1 = request.seo_parameter.render_h1(request)
    return seo_h1


def base_context(request):
    seo_title = get_seo_title(request)
    seo_description = get_seo_description(request)
    seo_h1 = get_seo_h1(request)
    return {
        "seo_title": seo_title,
        "seo_description": seo_description,
        "seo_h1": seo_h1,
        "static_version": settings.STATIC_VERSION,
        "header_categories": ServiceCategory.objects.all(),
        "footer_services": Service.objects.list_footer_services(),
        "slider_services": Service.objects.list_slider_services(),
        "news_counter": 1,
        "current_year": date.today().year,
    }
