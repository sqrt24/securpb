from django.contrib.sites.models import Site
from django.db import models
from tinymce.models import HTMLField

from core.mixins import NameModelMixin, OrderModelMixin


class ProjectSettings(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="Сайт")
    phone = models.CharField("Телефон", max_length=255, default="")
    phone_href = models.CharField("Телефон для ссылок", max_length=255, default="")
    telegram_link = models.CharField("Telegram (ссылка)", max_length=255, default="")
    telegram_channel_link = models.CharField("Telegram-канал (ссылка)", null=True, max_length=255, default="")
    whatsapp_link = models.CharField("Whatsapp (ссылка)", max_length=255, default="")
    whatsapp_link_number = models.CharField(
        "Whatsapp (телефон)", max_length=255, default="", help_text="Без пробелов, плюса, скобок"
    )
    email = models.CharField("Email", max_length=255, default="")
    address = models.CharField("Адрес", max_length=255, default="")
    schedule = models.CharField("График работы", max_length=255, default="")
    inn = models.CharField("ИНН", max_length=255, default="")
    kpp = models.CharField("КПП", max_length=255, default="")
    ogrn = models.CharField("ОГРН", max_length=255, default="")
    legal_address = models.CharField("Юр.адрес", max_length=255, default="")
    html_head = models.TextField("<head/> HTML", default="", blank=True)
    html_upper = models.TextField("Верхний блок HTML", default="", blank=True)
    html_bottom = models.TextField("Нижний блок HTML", default="", blank=True)
    robots_txt = models.TextField("robots.txt", default="", blank=True)
    privacy_policy = HTMLField("Политика конфиденциальности", default="", blank=True)
    ymaps_widget_url = models.URLField("URL виджета Яндекс.Карт", default="", blank=True)
    ymaps_url = models.URLField("URL Яндекс.Карт", default="", blank=True)
    bitrix_webhook_url = models.URLField("Битрикс24 Webhook URL", default="", blank=True)
    bitrix_user_id = models.CharField("Битрикс24 USER ID", max_length=255, default="", blank=True)
    bitrix_source_id = models.CharField("Битрикс24 SOURCE ID", max_length=255, default="", blank=True)

    class Meta:
        verbose_name = "Настройки проекта"
        verbose_name_plural = "Настройки проекта"

    def __str__(self):
        return str(self.site)


class FAQ(OrderModelMixin, models.Model):
    question = models.CharField("Вопрос", max_length=255, default="")
    answer = models.TextField("Ответ", default="")
    service = models.ForeignKey(
        "services.Service",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="faqs",
        verbose_name="Прикрепить к услуге",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"

    def __str__(self):
        return str(self.question)


class Contract(OrderModelMixin, NameModelMixin, models.Model):
    file = models.FileField("Файл", upload_to="contracts/files")
    text = HTMLField("Текст", blank=True, default="")

    class Meta:
        ordering = ["order"]
        verbose_name = "Типовой договор"
        verbose_name_plural = "Типовые договоры"


class ContractImage(OrderModelMixin, models.Model):
    contract = models.ForeignKey("Contract", models.CASCADE, verbose_name="Договор", related_name="images")
    order = models.IntegerField("Номер страницы", default=0, blank=True)
    image = models.ImageField("Изображение", upload_to="contacts/images")

    class Meta:
        ordering = ["order"]
        verbose_name = "Типовой договор: изображение"
        verbose_name_plural = "Типовые договоры: изображения"
