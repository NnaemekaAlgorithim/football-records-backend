from django.apps import AppConfig


class FootballAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'football_app'

    def ready(self):
        import football_app.signals
