from django.contrib import admin

from . import models


@admin.register(models.ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = list_display_links = ["id", "name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["slug", "name"]


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = list_display_links = ["id", "name", "slug", "date", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["slug", "name"]
    list_filter = ["is_active", "date"]
