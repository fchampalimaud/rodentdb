from django.db import models


    name = models.CharField(max_length=80)
class Zygosity(models.Model):

    class Meta:
        verbose_name = 'zygosity'
        verbose_name_plural = 'zygosities'
        ordering = ['name']

    def __str__(self):
        return self.name
