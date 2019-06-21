from django.db import models


class Zygosity(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'zygosity'
        verbose_name_plural = 'zygosities'
        ordering = ['name']

    def __str__(self):
        return self.name
