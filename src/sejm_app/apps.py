from django.apps import AppConfig


class SejmAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sejm_app"

    def ready(self):
        # import sejm_app.signals
        from sejm_app import init_db

        init_db.run()
