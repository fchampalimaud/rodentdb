from django.apps import AppConfig


class RodentDBConfig(AppConfig):
    name = "rodentdb"
    verbose_name = "Rodent DB"

    def ready(self):
        from .rodent import RodentApp

        global RodentApp
