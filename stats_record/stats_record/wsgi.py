"""
WSGI config for stats_record project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

DEBUG = os.environ.get("DEBUG", None)

if DEBUG == "True":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stats_record.settings.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stats_record.settings.production")

application = get_wsgi_application()
