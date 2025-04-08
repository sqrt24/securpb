from django.contrib.auth.mixins import LoginRequiredMixin as _LoginRequiredMixin
from django.db import models


class LoginRequiredMixin(_LoginRequiredMixin):
    login_url = "/members/login/"


class ImageModelMixin:

    def get_image_url(self) -> str:
        if self.image:
            return self.image.url
        return ""


class NameModelMixin(models.Model):
    name = models.CharField("Название", max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class OrderModelMixin(models.Model):
    order = models.IntegerField("Порядковый номер", default=0, blank=True)

    class Meta:
        ordering = ["order"]
        abstract = True


class CreatedAtModelMixin(models.Model):
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        abstract = True


class TimestampModelMixin(models.Model):
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        abstract = True

    @property
    def lastmod(self):
        return (self.updated_at or self.created_at).date()
