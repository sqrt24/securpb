from django.contrib import admin

from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "order"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
