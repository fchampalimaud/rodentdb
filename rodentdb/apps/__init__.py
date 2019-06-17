from django.apps import AppConfig


class RodentDBConfig(AppConfig):
    name = "rodentdb"
    verbose_name = "Rodent DB"

    def ready(self):
        from .rodent import RodentApp
        from .categories import RodentCategoryApp
        from .coat_colors import RodentCoatColorApp
        from .backgrounds import RodentBackgroundApp
        from .genotypes import RodentGenotypeApp
        from .inducible_cassettes import RodentInducibleCassetteApp
        from .reporter_genes import RodentReporterGeneApp
        from .species import RodentSpeciesApp

        global RodentApp
        global RodentCategoryApp
        global RodentCoatColorApp
        global RodentBackgroundApp
        global RodentGenotypeApp
        global RodentInducibleCassetteApp
        global RodentReporterGeneApp
        global RodentSpeciesApp
