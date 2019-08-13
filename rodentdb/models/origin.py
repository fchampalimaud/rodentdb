from django.db import models


class Origin(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = "origin"
        verbose_name_plural = "origins"
        ordering = ["name"]

    def __str__(self):
        return self.name
