from django.apps import AppConfig


class MunaKalatiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'muna_kalati'
    

    def ready(self):
        import muna_kalati.signals
