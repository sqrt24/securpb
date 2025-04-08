from django.db import models
from django.shortcuts import reverse
from django.utils import dateformat
from tinymce.models import HTMLField

from core.mixins import ImageModelMixin, NameModelMixin, TimestampModelMixin
from seo.mixins import SEOMixin


class ArticleCategoryManager(models.Manager):

    def list_active_categories(self):
        return self.filter(
            models.Exists(Article.objects.filter(category_id=models.OuterRef("id"), is_active=True))
        ).annotate(articles_count=models.Count("articles", filter=models.Q(articles__is_active=True)))


class ArticleCategory(NameModelMixin, TimestampModelMixin, models.Model):
    slug = models.SlugField("Слаг", max_length=255, unique=True)

    objects = ArticleCategoryManager()

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория статей"
        verbose_name_plural = "Категории статей"

    def get_absolute_url(self) -> str:
        return reverse("blog", kwargs={"category_slug": self.slug})


class ArticleManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("category")


class Article(NameModelMixin, SEOMixin, ImageModelMixin, TimestampModelMixin, models.Model):
    is_active = models.BooleanField("Активен", blank=True, default=True)
    category = models.ForeignKey("ArticleCategory", models.CASCADE, verbose_name="Категория", related_name="articles")
    image = models.ImageField("Изображение", upload_to="articles")
    slug = models.SlugField("Слаг", max_length=255, unique=True)
    date = models.DateField("Дата")
    text = HTMLField("Текст", blank=True, default="")

    objects = ArticleManager()

    class Meta:
        ordering = ["-date"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def get_absolute_url(self) -> str:
        return reverse("article", kwargs={"slug": self.slug})

    def get_date(self) -> str:
        return dateformat.format(self.date, "d E Y")
