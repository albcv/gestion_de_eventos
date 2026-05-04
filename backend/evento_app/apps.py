from django.apps import AppConfig


class EventoAppConfig(AppConfig):
    name = 'evento_app'

    def ready(self):
        import evento_app.signals