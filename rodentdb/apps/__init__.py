from django.apps import AppConfig


class RodentDBConfig(AppConfig):
    name = "rodentdb"
    verbose_name = "Rodent DB"

    def ready(self):
        from .rodent import RodentApp
        from .categories import RodentCategoryApp
        from .backgrounds import RodentBackgroundApp

        global RodentApp
        global RodentCategoryApp
        global RodentBackgroundApp
