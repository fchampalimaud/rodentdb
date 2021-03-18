from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from model_utils import Choices

from rodentdb.querysets import RodentQuerySet


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

    # Specific fields for this animal model
    species = models.ForeignKey(
        to="rodentdb.Species", on_delete=models.PROTECT, related_name="rodents"
    )
    strain_name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)
    origin = models.ForeignKey(
        to="rodentdb.Origin", on_delete=models.PROTECT, related_name="rodents"
    )
    origin_other = models.CharField(verbose_name="origin", max_length=40, blank=True)
    category = models.ForeignKey(
        to="rodentdb.Category", on_delete=models.PROTECT, related_name="rodents"
    )
    background = models.ForeignKey(
        to="rodentdb.Background",
        on_delete=models.PROTECT,
        related_name="rodents",
        null=True,
        blank=True,
    )
    zygosity = models.ManyToManyField(
        to="rodentdb.Zygosity", related_name="rodents", blank=True
    )
    line_description = models.TextField(blank=True)
    coat_color = models.ForeignKey(
        to="rodentdb.CoatColor", on_delete=models.CASCADE, null=True, blank=True
    )
    reporter_gene = models.ForeignKey(
        to="rodentdb.ReporterGene", on_delete=models.CASCADE, null=True, blank=True
    )
    inducible_cassette = models.ForeignKey(
        to="rodentdb.InducibleCassette", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "rodents"
        abstract = True

    def __str__(self):
        return self.strain_name

    def clean(self):
        if hasattr(self, "origin") and self.origin.name.lower() == "other":
            if not self.origin_other:
                raise ValidationError({"origin_other": "This field is required."})
        else:
            self.origin_other = ""


class Rodent(AbstractRodent):
    public = models.BooleanField(verbose_name="Public through Congento", default=False)
    mta = models.BooleanField(verbose_name="MTA", default=False)

    comments = models.TextField(blank=True)

    maintainer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True
    )
    ownership = models.ForeignKey(
        to="users.Group", on_delete=models.PROTECT, null=True, blank=True
    )

    objects = RodentQuerySet.as_manager()

    class Meta:
        permissions = [("can_import", "Can import from XLSX")]
