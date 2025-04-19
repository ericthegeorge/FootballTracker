from django.apps import AppConfig


class FootballtrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'footballtracker'
def ready(self):
    import footballtracker.signals