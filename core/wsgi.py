import os

from django.core.wsgi import get_wsgi_application

from core.env import load_env

load_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
