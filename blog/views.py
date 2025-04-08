from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from blog.models import Article, ArticleCategory
from core.utils.breadcrumbs import build_breadcrumbs


class ArticleListView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        current_category = None
        category_slug = self.kwargs.get("category_slug")
        articles = Article.objects.filter(is_active=True)
        if category_slug:
            current_category = get_object_or_404(ArticleCategory, slug=category_slug)
            articles = articles.filter(category=current_category)
        context = super().get_context_data(**kwargs)
        context.update(
            bc_data=build_breadcrumbs([{"name": "Статьи"}] + ([current_category] if current_category else [])),
            categories=ArticleCategory.objects.list_active_categories(),
            current_category=current_category,
            articles=articles,
        )
        self.request.seo_context.update(current_category=current_category)
        return context


class ArticleDetailView(DetailView):
    template_name = "blog/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Article.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            article=self.object,
            bc_data=build_breadcrumbs([{"name": "Статьи", "url": "/blog/"}, self.object.category, self.object]),
            categories=ArticleCategory.objects.list_active_categories(),
            articles=Article.objects.filter(is_active=True).exclude(id=self.object.id)[:5],
            current_category=self.object.category,
        )
        self.request.seo_context.update(article=self.object, current_category=self.object.category)
        self.request.seo_object = self.object
        return context
