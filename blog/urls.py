from django.urls import path

from . import views

urlpatterns = [
    path("blog/", views.ArticleListView.as_view(), name="blog"),
    path("blog/<slug:category_slug>/", views.ArticleListView.as_view(), name="blog"),
    path("article/<slug:slug>/", views.ArticleDetailView.as_view(), name="article"),
]
