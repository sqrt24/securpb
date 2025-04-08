from django.contrib import admin

from . import models


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "message_thread_id"]
    list_display_links = ["id", "slug"]


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "form", "phone", "email", "is_sent", "created_at"]
    list_display_links = ["id", "form"]
    list_filter = ["is_sent", "form", "created_at"]
