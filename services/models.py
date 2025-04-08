from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

from core.mixins import NameModelMixin, OrderModelMixin, TimestampModelMixin
from seo.mixins import SEOMixin


class PriceListCategory(NameModelMixin, OrderModelMixin, models.Model):
    class Meta:
        ordering = ["order"]
        verbose_name = "Прайс-лист: категория"
        verbose_name_plural = "Прайс-лист: категории"


class PriceListItem(NameModelMixin, OrderModelMixin, models.Model):
    category = models.ForeignKey(PriceListCategory, models.CASCADE, verbose_name="категория", related_name="items")
    price = models.CharField("Цена", max_length=255)

    class Meta:
        ordering = ["order"]
        verbose_name = "Прайс-лист: элемент категории"
        verbose_name_plural = "Прайс-лист: элементы категорий"

    @property
    def integer_price(self) -> str:
        return "".join(char for char in self.price if char.isdigit())


class ServiceCategory(TimestampModelMixin, NameModelMixin, OrderModelMixin, models.Model):
    slug = models.SlugField("Слаг", max_length=255, unique=True)
    icon = models.FileField("Иконка", upload_to="services", blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Услуга: категория"
        verbose_name_plural = "Услуга: категории"

    def get_absolute_url(self) -> str:
        return reverse("services", kwargs={"category_slug": self.slug})

    def get_icon_url(self) -> str:
        if self.icon:
            return self.icon.url
        return ""


class ServiceManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("category")

    def list_footer_services(self):
        return self.filter(show_in_footer=True, is_active=True)

    def list_slider_services(self):
        return self.filter(show_in_slider=True, is_active=True)


class Service(TimestampModelMixin, SEOMixin, NameModelMixin, OrderModelMixin, models.Model):
    is_active = models.BooleanField("Активен", blank=True, default=True)
    category = models.ForeignKey(ServiceCategory, models.CASCADE, verbose_name="Категория", related_name="services")
    slug = models.SlugField("Слаг", max_length=255, unique=True)
    show_in_footer = models.BooleanField("Показывать в подвале", default=False)
    show_in_slider = models.BooleanField("Показывать в слайдере", default=False)
    noindex = models.BooleanField("Закрыть от индексации", default=False)
    min_price = models.CharField("Минимальная цена", max_length=255, blank=True)
    short_description = HTMLField("Текст (краткое описание)", blank=True, default="")
    text = HTMLField("Текст", blank=True, default="")
    price_list_categories = models.ManyToManyField(
        "PriceListCategory", blank=True, related_name="services", verbose_name="Категории прайс-листа"
    )
    related_services = models.ManyToManyField("self", verbose_name="Сопутствующие услуги", blank=True)

    objects = ServiceManager()

    class Meta:
        ordering = ["order"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def get_absolute_url(self) -> str:
        return reverse("service", kwargs={"slug": self.slug})

    def get_icon_url(self) -> str:
        if self.category.icon:
            return self.category.get_icon_url()
        return ""


class ServiceReasonBlock(NameModelMixin, OrderModelMixin, models.Model):
    service = models.ForeignKey(Service, models.CASCADE, verbose_name="Услуга", related_name="reasons")
    description = models.TextField("Описание")

    class Meta:
        ordering = ["order"]
        verbose_name = "Услуга: блок причин"
        verbose_name_plural = "Услуга: блок причин"


class ServiceStepBlock(NameModelMixin, OrderModelMixin, models.Model):
    service = models.ForeignKey(Service, models.CASCADE, verbose_name="Услуга", related_name="steps")
    description = models.TextField("Описание")

    class Meta:
        ordering = ["order"]
        verbose_name = "Услуга: шаг оказания услуги"
        verbose_name_plural = "Услуга: шаги оказания услуги"
