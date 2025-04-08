import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "1") not in (False, "False", "false", 0, "0")
DEV = os.getenv("DEV", "0") not in (False, "False", "false", 0, "0")
STATIC_VERSION = "?v=" + os.getenv("STATIC_VERSION", "61")

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "filebrowser",
    # django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # additional
    "django.contrib.sites",
    "django.contrib.postgres",
    "django.contrib.sitemaps",
    # third party applications
    "rest_framework",
    "tinymce",
    # django applications
    "pages",
    "services",
    "seo",
    "project_settings",
    "informer",
    "clients",
    "blog",
    "administration",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.BaseContentMiddleware",
    "seo.middleware.SEOMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            BASE_DIR / "core/templates",
            BASE_DIR / "seo/templates",
            BASE_DIR / "pages/templates",
            BASE_DIR / "services/templates",
            BASE_DIR / "blog/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "core.jinja2.environment",
            "auto_reload": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "core.context_processors.base_context",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates_django",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "core.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

CSRF_TRUSTED_ORIGINS = [
    "https://securpb.ru",
    "https://test.securpb.ru",
    "https://*.securpb.ru",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = [BASE_DIR / "core/static"]

MEDIA_ROOT = BASE_DIR / "media/"
if DEV:
    MEDIA_URL = "https://dev.securpb.ru/media/"
else:
    MEDIA_URL = "/media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")

CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_URL = REDIS_URL

if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    DEBUG_TOOLBAR_PANELS = (
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.timer.TimerPanel",
    )

SITE_ID = 1

# TINYMCE_JS_URL = "/static/tinymce/tinymce.min.js"
TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = True

TINYMCE_DEFAULT_CONFIG = {
    "relative_urls": False,
    "remove_script_host": True,
    "convert_urls": True,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    # 'theme': 'silver',
    "height": "800px",
    "menubar": "file edit view insert format tools table help",
    "plugins": """
        textcolor save media codesample contextmenu directionality charmap print hr
        advlist,autolink,lists,link,image,charmap,print,preview,anchor,searchreplace,
        visualblocks,code,fullscreen,insertdatetime,media,table,paste,scode,help,wordcount
    """,
    "toolbar": """
    undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify |
     bullist numlist outdent indent | removeformat | image help
    """,
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }
        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
    "statusbar": True,
    "language": "ru_ru",
}
FILEBROWSER_DIRECTORY = ""
DIRECTORY = ""
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg", ".gif", ".png", ".tif", ".tiff"],
    "Document": [".pdf", ".doc", ".rtf", ".txt", ".xls", ".csv", ".xml"],
    "Video": [".mov", ".wmv", ".mpeg", ".mpg", ".avi", ".rm"],
    "Audio": [".mp3", ".mp4", ".wav", ".aiff", ".midi", ".m4p"],
}

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
