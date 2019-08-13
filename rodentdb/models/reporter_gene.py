from django.db import models


class ReporterGene(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = "reporter gene"
        verbose_name_plural = "reporter genes"
        ordering = ["name"]

    def __str__(self):
        return self.name
