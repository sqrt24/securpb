from django.db import models
from django.template import Context, Template
from django.utils.safestring import mark_safe

from core.mixins import NameModelMixin


class Form(NameModelMixin, models.Model):
    slug = models.SlugField("Слаг", max_length=255, unique=True)
    message_thread_id = models.IntegerField("ID топика")
    message_template = models.TextField("Шаблон сообщения")

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"


class Message(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name="Форма", related_name="messages")
    data = models.JSONField("Данные")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_sent = models.BooleanField("Отправлено", default=False)
    text = models.TextField("Текст", default="", blank=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.text:
            self.generate_text()

    @property
    def phone(self) -> str:
        return self.data.get("phone")

    @property
    def email(self) -> str:
        return self.data.get("email")

    @property
    def ym_uid(self) -> str:
        return self.data.get("ym_uid")

    @property
    def utm_source(self) -> str:
        return self.data.get("utm_source")

    @property
    def utm_medium(self) -> str:
        return self.data.get("utm_medium")

    @property
    def utm_campaign(self) -> str:
        return self.data.get("utm_campaign")

    @property
    def utm_content(self) -> str:
        return self.data.get("utm_content")

    @property
    def utm_term(self) -> str:
        return self.data.get("utm_term")

    def generate_text(self) -> None:
        self.text = mark_safe(Template(self.form.message_template).render(Context(self.data)))
        self.save(update_fields=["text"])

    def mark_sent(self) -> None:
        self.is_sent = True
        self.save(update_fields=["is_sent"])
