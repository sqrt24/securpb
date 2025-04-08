from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from core.utils.breadcrumbs import build_breadcrumbs
from services.models import PriceListCategory, Service, ServiceCategory


class ServiceListView(TemplateView):
    template_name = "services/services.html"

    def get_context_data(self, **kwargs):
        current_category = None
        category_slug = self.kwargs.get("category_slug")
        services = Service.objects.filter(is_active=True)
        if category_slug:
            current_category = get_object_or_404(ServiceCategory, slug=category_slug)
            services = services.filter(category=current_category)
        context = super().get_context_data(**kwargs)
        context.update(
            bc_data=build_breadcrumbs([{"name": "Услуги"}] + ([current_category] if current_category else [])),
            categories=ServiceCategory.objects.all(),
            current_category=current_category,
            services=services,
        )
        self.request.seo_context.update(
            current_category=current_category,
        )
        return context


class ServiceDetailView(DetailView):
    slug_url_kwarg = "slug"
    slug_field = "slug"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            service=self.object,
            bc_data=build_breadcrumbs([{"name": "Услуги", "url": "/services/"}, self.object.category, self.object]),
            related_services=self.object.related_services.all(),
        )
        self.request.seo_object = self.object
        self.request.seo_context.update(
            service=self.object,
        )
        return context


class PriceListView(TemplateView):
    template_name = "services/price-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            bc_data=build_breadcrumbs([{"name": "Прайс-лист"}]),
            categories=PriceListCategory.objects.all().prefetch_related("items"),
        )
        return context
