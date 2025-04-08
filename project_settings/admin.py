from django.contrib import admin

from . import models


@admin.register(models.ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    list_display = list_display_links = ["id", "site"]


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = list_display_links = ["id", "question"]


class ContractImageInline(admin.TabularInline):
    model = models.ContractImage
    extra = 0


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "order"]
    list_display_links = ["id", "name"]
    inlines = [ContractImageInline]
