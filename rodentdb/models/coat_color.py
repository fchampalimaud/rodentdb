from django.db import models


class CoatColor(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = "coat color"
        verbose_name_plural = "coat colors"
        ordering = ["name"]

    def __str__(self):
        return self.name
