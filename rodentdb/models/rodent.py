from django.core.exceptions import ValidationError
from django.db import models
from model_utils import Choices

from .rodent_queryset import RodentQuerySet
from .rodent_permission import RodentPermission


class AbstractRodent(models.Model):
    """
    Must be compatible with Congento model scheme!
    """

    SPECIES = Choices(("rat", "Rat"), ("mouse", "Mouse"))

    GENOTYPES = Choices(
        ("wt", "WT"),
        ("homo", "Homo"),
        ("het", "Het"),
        ("hemi", "Hemi"),
        ("both", "Homo/Het"),
        ("other", "Other"),
    )

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
    species = models.CharField(max_length=5, choices=SPECIES)
    strain_name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)
    origin = models.CharField(max_length=20)
    category = models.ForeignKey(to='rodentdb.Category', on_delete=models.PROTECT, related_name='rodents')
    background = models.ForeignKey(to='rodentdb.Background', on_delete=models.PROTECT, related_name='rodents')

    # genotype
    genotype = models.CharField(max_length=5, choices=GENOTYPES)
    genotype_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    class Meta:
        verbose_name_plural = "rodents"
        abstract = True

    def __str__(self):
        return self.strain_name

    def clean(self):
        if self.genotype == self.GENOTYPES.other:
            if not self.genotype_other:
                raise ValidationError({"genotype_other": "This field is required."})
        else:
            self.genotype_other = ""


class Rodent(AbstractRodent):
    public = models.BooleanField("Public", default=False)

    comments = models.TextField(blank=True)

    lab = models.ForeignKey(
        "auth.Group", verbose_name="Ownership", on_delete=models.CASCADE
    )

    objects = RodentQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.lab is not None:
            RodentPermission.objects.get_or_create(
                rodent=self, group=self.lab, viewonly=False
            )
