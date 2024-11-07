"""
ASGI config for stats_record project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

DEBUG = os.environ.get("DEBUG", None)

if DEBUG == "True":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stats_record.settings.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stats_record.settings.production")

application = get_asgi_application()
