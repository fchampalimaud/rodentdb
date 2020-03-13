from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
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

    def before_import_row(self, row, **kwargs):
        for field, value in row.items():
            if field in self._date_fields:
                # check if the value is a float and convert to datetime here
                if isinstance(value, float):
                    import xlrd
                    row[field] = datetime(*xlrd.xldate_as_tuple(value, 0), tzinfo=timezone.get_current_timezone())
                elif isinstance(value, datetime):
                    # we need to add the timezone to the datetime
                    row[field] = value.replace(tzinfo=timezone.get_current_timezone()).astimezone(tz=timezone.get_current_timezone())
            if value is None:
                # check default value for this field within the model and set it in the row value before proceeding
                try:
                    f = self._meta.model._meta.get_field(field)
                except FieldDoesNotExist:
                    continue
                if f.blank is True and f.null is False:
                    row[field] = ''
                pass 
        return super().before_import_row(row, **kwargs)

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
