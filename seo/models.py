from django.db import models

from core.jinja2 import render_jinja_string


class SeoParameterManager(models.Manager):

    def get_by_path(self, path: str):
        obj = None
        if path != "/":
            obj = (
                self.filter(
                    models.Q(path__in=path.split("/")[1:-1]) | (models.Q(use_full_path=True) & models.Q(path=path))
                )
                .order_by("-use_full_path")
                .first()
            )
        if obj is None:
            obj = self.filter(path="").first() or SeoParameter(
                title="ПБ Системы",
                description="ПБ Системы",
                fix_header=True,
            )
        return obj


class SeoParameter(models.Model):
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    path = models.CharField(
        "URL", max_length=255, unique=True, help_text="/catalog/, /about/", db_index=True, blank=True, default=""
    )
    use_full_path = models.BooleanField("Использовать полный путь", default=False)
    title = models.TextField("Title", null=True, blank=True)
    description = models.TextField("Description", null=True, blank=True)
    h1 = models.TextField("H1", null=True, blank=True)
    background_image = models.ImageField("Фон шапки", upload_to="seo/background_image", null=True, blank=True)
    fix_header = models.BooleanField("Фиксировать шапку", default=True)
    noindex = models.BooleanField("Noindex", default=False)
    og_image = models.ImageField("og:image", upload_to="seo/image", null=True, blank=True)

    objects = SeoParameterManager()

    class Meta:
        verbose_name = "Параметр SEO"
        verbose_name_plural = "Параметры SEO"

    def __str__(self):
        return self.name or self.path

    def render_title(self, request, **params) -> str:
        return render_jinja_string(self.title, request=request, **params, **request.seo_context)

    def render_description(self, request, **params) -> str:
        return render_jinja_string(self.description, request=request, **params, **request.seo_context)

    def render_h1(self, request, **params) -> str:
        return render_jinja_string(self.h1, request=request, **params, **request.seo_context)


class RobotsTextManager(models.Manager):

    def get_city_robots(self, city):
        return self.filter(cities=city).first()


class Redirect(models.Model):
    old_path = models.CharField("Старый путь", max_length=255, unique=True, db_index=True)
    new_path = models.CharField("Новый путь", max_length=255)

    class Meta:
        verbose_name = "Редирект"
        verbose_name_plural = "Редиректы"

    def __str__(self):
        return f"{self.old_path} -> {self.new_path}"
