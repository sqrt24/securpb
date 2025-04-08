from django.urls import path

from . import views

urlpatterns = [
    path("robots.txt", views.robots_view, name="robots"),
    path("sitemap.xml", views.sitemap_view, name="sitemap"),
    path("feed.xml", views.feed_view, name="feed"),
    path("2gis.xlsx", views.xlsx_2gis_view, name="2gis"),
    path("service-feed.xml", views.service_feed_view, name="service-feed"),
]
