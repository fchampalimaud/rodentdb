from django.conf import settings
from django.db import models
from model_utils import Choices

from .rodent_queryset import RodentQuerySet
from .rodent_permission import RodentPermission


class AbstractRodent(models.Model):
    """
    Must be compatible with Congento model scheme!
    """

    AVAILABILITIES = Choices(
        ("live", "Live"),
        ("cryo", "Cryopreserved"),
        ("both", "Live & Cryopreserved"),
        ("none", "Unavailable"),
    )

    # Fields shared with other congento animal models
    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Updated", auto_now=True)
    availability = models.CharField(max_length=4, choices=AVAILABILITIES)
    link = models.URLField(blank=True)
    mta = models.BooleanField(verbose_name="MTA", default=False)

    # Specific fields for this animal model
    species = models.ForeignKey(to='rodentdb.Species', on_delete=models.PROTECT, related_name='rodents')
    strain_name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)
    origin = models.CharField(max_length=20)
    category = models.ForeignKey(to='rodentdb.Category', on_delete=models.PROTECT, related_name='rodents')
    background = models.ForeignKey(to='rodentdb.Background', on_delete=models.PROTECT, related_name='rodents', null=True, blank=True)
    genotype = models.ForeignKey(to='rodentdb.Genotype', on_delete=models.PROTECT, related_name='rodents')
    line_description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "rodents"
        abstract = True

    def __str__(self):
        return self.strain_name


class Rodent(AbstractRodent):
    public = models.BooleanField("Public", default=False)

    comments = models.TextField(blank=True)

    maintainer = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    ownership = models.ForeignKey(to="auth.Group", on_delete=models.PROTECT, null=True, blank=True)
    # lab = models.ForeignKey(
    #     "auth.Group", verbose_name="Ownership", on_delete=models.CASCADE
    # )

    # objects = RodentQuerySet.as_manager()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if self.lab is not None:
    #         RodentPermission.objects.get_or_create(
    #             rodent=self, group=self.lab, viewonly=False
    #         )
