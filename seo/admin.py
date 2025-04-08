from django.contrib import admin

from . import models


@admin.register(models.SeoParameter)
class SeoParameterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "path"]
    list_display_links = ["id", "name", "path"]
    search_fields = ["name", "path"]


@admin.register(models.Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ["id", "old_path", "new_path"]
    list_display_links = ["id", "old_path", "new_path"]
    search_fields = ["old_path", "new_path"]
