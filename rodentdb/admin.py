from django.contrib import admin
from django.conf import settings
from import_export import resources, widgets
from import_export.admin import ExportActionMixin, ImportMixin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from . import models
from .models import Rodent, Category, Species, Background, CoatColor, InducibleCassette, Origin, ReporterGene, Zygosity
from users.models import Group
from django.contrib.auth import get_user_model

class RodentResource(resources.ModelResource):
    background = Field(attribute='background', column_name='background', widget=ForeignKeyWidget(Background, 'name'))
    category = Field(attribute='category', column_name='category', widget=ForeignKeyWidget(Category, 'name'))
    coat_color = Field(attribute='coat_color', column_name='coat_color', widget=ForeignKeyWidget(CoatColor, 'name'))
    inducible_cassette = Field(attribute='inducible_cassette', column_name='inducible_cassette', widget=ForeignKeyWidget(InducibleCassette, 'name'))
    origin = Field(attribute='origin', column_name='origin', widget=ForeignKeyWidget(Origin, 'name'))
    reporter_gene = Field(attribute='reporter_gene', column_name='reporter_gene', widget=ForeignKeyWidget(ReporterGene, 'name'))
    species = Field(attribute='species', column_name='species', widget=ForeignKeyWidget(Species, 'name'))
    zygosity = Field(attribute='zygosity', column_name='zygosity', widget=ManyToManyWidget(Zygosity, field='name'))
    maintainer = Field(attribute='maintainer', column_name='maintainer', widget=ForeignKeyWidget(get_user_model(), 'name'))
    ownership = Field(attribute='ownership', column_name='ownership', widget=ForeignKeyWidget(Group, 'name'))

    class Meta:
        model = Rodent
        skip_unchanged = True
        clean_model_instances = True

@admin.register(models.Rodent)
class RodentAdmin(ImportMixin, ExportActionMixin, admin.ModelAdmin):
    resource_class = RodentResource
    readonly_fields = ["created", "modified"]


admin.site.register(models.Background)
admin.site.register(models.Category)
admin.site.register(models.CoatColor)
admin.site.register(models.InducibleCassette)
admin.site.register(models.Origin)
admin.site.register(models.ReporterGene)
admin.site.register(models.Species)
admin.site.register(models.Zygosity)
