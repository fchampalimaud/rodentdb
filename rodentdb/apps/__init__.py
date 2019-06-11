from django.apps import AppConfig


class RodentDBConfig(AppConfig):
    name = "rodentdb"
    verbose_name = "Rodent DB"

    def ready(self):
        from .rodent import RodentApp
        from .categories import RodentCategoryApp
        from .backgrounds import RodentBackgroundApp
        from .genotypes import RodentGenotypeApp
        from .species import RodentSpeciesApp

        global RodentApp
        global RodentCategoryApp
        global RodentBackgroundApp
        global RodentGenotypeApp
        global RodentSpeciesApp
