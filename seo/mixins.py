from django.db import models

from core.jinja2 import render_jinja_string
from seo.services import SEOProtocol


class SEOMixin(SEOProtocol, models.Model):
    seo_title = models.TextField("SEO Title", default="", blank=True)
    seo_description = models.TextField("SEO Description", blank=True, default="")
    seo_h1 = models.TextField("SEO H1", default="", blank=True)

    class Meta:
        abstract = True

    def render_title(self, request, **params) -> str:
        return render_jinja_string(self.seo_title, request=request, **params, **request.seo_context)

    def render_description(self, request, **params) -> str:
        return render_jinja_string(self.seo_description, request=request, **params, **request.seo_context)

    def render_h1(self, request, **params) -> str:
        return render_jinja_string(self.seo_h1, request=request, **params, **request.seo_context)
