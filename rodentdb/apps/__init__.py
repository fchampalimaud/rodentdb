from django.apps import AppConfig


class RodentDBConfig(AppConfig):
    name = "rodentdb"
    verbose_name = "Rodent DB"

    def ready(self):
        from .rodent import RodentApp
        from .categories import RodentCategoryApp
        from .coat_colors import RodentCoatColorApp
        from .backgrounds import RodentBackgroundApp
        from .inducible_cassettes import RodentInducibleCassetteApp
        from .reporter_genes import RodentReporterGeneApp
        from .species import RodentSpeciesApp
        from .zygosities import RodentZygosityApp

        global RodentApp
        global RodentCategoryApp
        global RodentCoatColorApp
        global RodentBackgroundApp
        global RodentInducibleCassetteApp
        global RodentReporterGeneApp
        global RodentSpeciesApp
        global RodentZygosityApp
