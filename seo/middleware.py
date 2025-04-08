from urllib.parse import quote

from django.http import HttpResponse, HttpResponseRedirect

from core.middleware import BaseMiddleware

from .models import Redirect, SeoParameter


def remove_page(value):
    try:
        return "/".join([i for i in value.split("/") if i.find("page__") < 0])
    except Exception:
        pass


def get_request_canonical_path(request) -> str:
    canonical = request.path
    if request.path.find("page__") > 0:
        canonical = remove_page(request.path)
    return canonical


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 308


class SEOMiddleware(BaseMiddleware):
    default_refer = "Прямой переход"

    def __call__(self, request, *args, **kwargs):
        existing_redirect = Redirect.objects.filter(old_path=request.path).first()
        if existing_redirect is not None:
            return HttpResponseSeeOther(existing_redirect.new_path)

        request.canonical_path = get_request_canonical_path(request)
        request.canonical = f"https://{request.get_host()}{request.canonical_path}"
        request.seo_parameter = SeoParameter.objects.get_by_path(request.path)
        request.seo_context = {
            "email": request.email.email if getattr(request, "email", None) else "",
            "main_phone": request.main_phone.phone if getattr(request, "main_phone", None) else "",
            "common_phone": request.common_phone.phone if getattr(request, "common_phone", None) else "",
        }
        request.ignore_html = request.GET.get("ignore_html", "0") == "1"

        request.noindex = request.seo_parameter.noindex if request.seo_parameter else False

        refer = self.default_refer
        old_cookie_refer = request.COOKIES.get("refer")
        meta_http_refer = request.META.get("HTTP_REFERER")
        if isinstance(meta_http_refer, str):
            if "yandex" in meta_http_refer:
                if request.GET.get("yclid") or request.GET.get("utm_source") == "yandex":
                    refer = "Yandex Direct"
                else:
                    refer = "Yandex Search"
            if "google" in meta_http_refer:
                if request.GET.get("gclid") or request.GET.get("utm_source") == "google":
                    refer = "Google-Adwords"
                else:
                    refer = "Google Search"
        request.refer = old_cookie_refer if refer == self.default_refer else self.default_refer
        response: HttpResponse = super().__call__(request, *args, **kwargs)
        if refer not in (old_cookie_refer, self.default_refer):
            response.set_cookie("refer", quote(refer), max_age=3600)
        if request.GET.get("utm_source"):
            response.set_cookie("_utm_source", quote(request.GET.get("utm_source")))
        if request.GET.get("utm_medium"):
            response.set_cookie("_utm_medium", quote(request.GET.get("utm_medium")))
        if request.GET.get("utm_campaign"):
            response.set_cookie("_utm_campaign", quote(request.GET.get("utm_campaign")))
        if request.GET.get("utm_content"):
            response.set_cookie("_utm_content", quote(request.GET.get("utm_content")))
        if request.GET.get("utm_term"):
            response.set_cookie("_utm_term", quote(request.GET.get("utm_term")))
        return response
