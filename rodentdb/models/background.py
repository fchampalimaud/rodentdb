from django.db import models


class Background(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "background"
        verbose_name_plural = "backgrounds"
        ordering = ["name"]

    def __str__(self):
        return self.name
