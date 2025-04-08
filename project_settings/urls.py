from django.urls import path

from . import views

urlpatterns = [path("clear-cache/", views.clear_cache_view)]
