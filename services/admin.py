from django.contrib import admin

from project_settings.models import FAQ

from . import models


class PriceListItemInline(admin.TabularInline):
    model = models.PriceListItem
    extra = 0


@admin.register(models.PriceListCategory)
class PriceListCategoryAdmin(admin.ModelAdmin):
    inlines = [PriceListItemInline]
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


@admin.register(models.ServiceStepBlock)
class ServiceStepBlockAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


@admin.register(models.ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["id", "name", "slug", "order"]
    list_display_links = ["id", "name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(models.ServiceReasonBlock)
class ServiceReasonBlockAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


class ServiceReasonBlockInline(admin.TabularInline):
    model = models.ServiceReasonBlock
    extra = 0


class ServiceStepBlockInline(admin.TabularInline):
    model = models.ServiceStepBlock
    extra = 0


class ServiceFAQInline(admin.TabularInline):
    model = FAQ
    extra = 0


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["id", "name", "slug", "order", "is_active", "min_price"]
    list_display_links = ["id", "name", "slug"]
    search_fields = ["name", "slug"]
    list_filter = ["is_active", "category"]
    autocomplete_fields = ["category", "price_list_categories", "related_services"]
    inlines = [ServiceReasonBlockInline, ServiceStepBlockInline, ServiceFAQInline]
