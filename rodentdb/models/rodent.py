from django.core.exceptions import ValidationError
from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel

from .rodent_queryset import RodentQuerySet
from .rodent_permission import RodentPermission

class Rodent(TimeStampedModel):

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

    species = models.CharField(max_length=5, choices=SPECIES)

    strain_name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)

    background = models.CharField(max_length=5, choices=BACKGROUNDS)
    background_other = models.CharField(max_length=20, verbose_name="", blank=True)

    genotype = models.CharField(max_length=5, choices=GENOTYPES)
    genotype_other = models.CharField(max_length=20, verbose_name="", blank=True)

    model_type = models.CharField(max_length=5, choices=MODEL_TYPES)
    model_type_other = models.CharField(max_length=20, verbose_name="", blank=True)

    origin = models.CharField(max_length=20)

    # Fields shared with other congento animal models

    AVAILABILITIES = Choices(
        ("live", "Live"),
        ("cryo", "Cryopreserved"),
        ("both", "Live & Cryopreserved"),
        ("none", "Unavailable"),
    )

    availability = models.CharField(max_length=4, choices=AVAILABILITIES)
    comments = models.TextField(blank=True)
    link = models.URLField(blank=True)
    mta = models.BooleanField(verbose_name="MTA", default=False)

    lab = models.ForeignKey('auth.Group', verbose_name='Ownership', on_delete=models.CASCADE)

    # location =
    # contact =
    # pi =

    objects = RodentQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "rodent"

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


    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        RodentPermission.objects.get_or_create(
            rodent=self, group=self.lab, viewonly=False
        )
