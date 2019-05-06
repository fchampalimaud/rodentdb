from django.db import models


class RodentPermission(models.Model):

    viewonly  = models.BooleanField('Read only access')
    rodent    = models.ForeignKey('Rodent',  on_delete=models.CASCADE)
    group     = models.ForeignKey('auth.Group', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {}".format(
            str(self.rodent),
            str(self.group),
            str(self.viewonly)
        )

    class Meta:
        verbose_name = "Rodent permission"
        verbose_name_plural = "Rodents permissions"

        unique_together = (
            ('rodent', 'group'),
        )