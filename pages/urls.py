from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("contracts/", views.ContractsView.as_view(), name="contracts"),
    path("careers/", views.CareersView.as_view(), name="careers"),
]
