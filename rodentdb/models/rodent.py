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

    BACKGROUNDS = Choices(
        ("c57bl", "C57BL/6"),
        ("balb", "Balb/c"),
        ("sv", "129sv"),
        ("fvb", "FVB"),
        ("mixed", "Mixed"),
        ("other", "Other"),
    )

    GENOTYPES = Choices(
        ("wt", "WT"),
        ("homo", "Homo"),
        ("het", "Het"),
        ("hemi", "Hemi"),
        ("both", "Homo/Het"),
        ("other", "Other"),
    )

    MODEL_TYPES = Choices(
        ("wt", "WT"),
        ("tg", "Transgenic"),
        ("ko", "KO"),
        ("cre", "Cre/flox"),
        ("other", "Other"),
    )

    # Fields shared with other congento animal models
    AVAILABILITIES = Choices(
        ("live", "Live"),
        ("cryo", "Cryopreserved"),
        ("both", "Live & Cryopreserved"),
        ("none", "Unavailable"),
    )

    public = models.BooleanField("Public", default=False)

    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Updated", auto_now=True)
    species = models.CharField(max_length=5, choices=SPECIES)
    strain_name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)
    origin = models.CharField(max_length=20)
    availability = models.CharField(max_length=4, choices=AVAILABILITIES)
    comments = models.TextField(blank=True)
    link = models.URLField(blank=True)
    mta = models.BooleanField(verbose_name="MTA", default=False)

    # background
    background = models.CharField(max_length=5, choices=BACKGROUNDS)
    background_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    # genotype
    genotype = models.CharField(max_length=5, choices=GENOTYPES)
    genotype_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    # model type
    model_type = models.CharField(max_length=5, choices=MODEL_TYPES)
    model_type_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    class Meta:
        verbose_name_plural = "rodents"
        abstract = True

    def __str__(self):
        return self.strain_name

    def clean(self):
        if self.background == self.BACKGROUNDS.other:
            if not self.background_other:
                raise ValidationError({"background_other": "This field is required."})
        else:
            self.background_other = ""

        if self.genotype == self.GENOTYPES.other:
            if not self.genotype_other:
                raise ValidationError({"genotype_other": "This field is required."})
        else:
            self.genotype_other = ""

        if self.model_type == self.MODEL_TYPES.other:
            if not self.model_type_other:
                raise ValidationError({"model_type_other": "This field is required."})
        else:
            self.model_type_other = ""


class Rodent(AbstractRodent):

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
