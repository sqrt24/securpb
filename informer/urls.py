from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.InformerAPIView.as_view(), name="informer"),
]
