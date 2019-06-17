from django.db import models


class InducibleCassette(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'inducible cassette'
        verbose_name_plural = 'inducible cassettes'
        ordering = ['name']

    def __str__(self):
        return self.name
