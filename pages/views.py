from django.views.generic import TemplateView

from blog.models import Article
from clients.models import Client
from core.utils.breadcrumbs import build_breadcrumbs
from project_settings.models import FAQ, Contract


class IndexView(TemplateView):
    template_name = "pages/index.html"
    extra_context = {
        "clients": Client.objects.all(),
        "faq": FAQ.objects.all(),
        "articles": Article.objects.filter(is_active=True)[:5],
    }


class AboutView(TemplateView):
    template_name = "pages/about.html"
    extra_context = {
        "clients": Client.objects.all(),
        "faq": FAQ.objects.all(),
        "bc_data": build_breadcrumbs([{"name": "О компании"}]),
    }


class ContactsView(TemplateView):
    template_name = "pages/contacts.html"
    extra_context = {
        "bc_data": build_breadcrumbs([{"name": "Контакты"}]),
    }


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"
    extra_context = {
        "bc_data": build_breadcrumbs([{"name": "Политика обработки персональных данных"}]),
    }


class ContractsView(TemplateView):
    template_name = "pages/contracts.html"
    extra_context = {
        "bc_data": build_breadcrumbs([{"name": "Типовой договор"}]),
        "contracts": Contract.objects.all().prefetch_related("images"),
    }


class CareersView(TemplateView):
    template_name = "pages/careers.html"
    extra_context = {
        "bc_data": build_breadcrumbs([{"name": " Сотрудничество"}]),
    }
