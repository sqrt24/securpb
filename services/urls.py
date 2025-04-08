from django.urls import path

from . import views

urlpatterns = [
    path("services/", views.ServiceListView.as_view(), name="services"),
    path("services/<slug:category_slug>/", views.ServiceListView.as_view(), name="services"),
    path("service/<slug:slug>/", views.ServiceDetailView.as_view(), name="service"),
    path("price-list/", views.PriceListView.as_view(), name="price-list"),
]
