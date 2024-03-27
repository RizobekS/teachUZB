from django.apps import AppConfig


class TeachuzbAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teachUZB_app'

    # def ready(self):
    #     import teachUZB_app.signals  # noqa
