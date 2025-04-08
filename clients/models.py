from django.db import models

from core.mixins import ImageModelMixin, NameModelMixin, OrderModelMixin


class Client(ImageModelMixin, NameModelMixin, OrderModelMixin, models.Model):
    image = models.ImageField("Изображение", upload_to="clients")

    class Meta:
        ordering = ["order"]
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
