from django.db import models


class Genotype(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = 'genotype'
        verbose_name_plural = 'genotypes'
        ordering = ['name']

    def __str__(self):
        return self.name
