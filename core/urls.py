from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from filebrowser.sites import site

from core import settings
from core.views import page_not_found

admin.site.site_header = "SECURPB admin"
admin.site.site_title = "SECURPB admin portal"
admin.site.index_title = "SECURPB Admin Dashboard"

urlpatterns = [
    path("admin/filebrowser/", site.urls),
    path("admin/tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("informer/", include("informer.urls")),
    path("", include("blog.urls")),
    path("", include("seo.urls")),
    path("", include("services.urls")),
    path(
        "404/",
        page_not_found,
    ),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    ] + debug_toolbar_urls()


handler404 = "core.views.page_not_found"
