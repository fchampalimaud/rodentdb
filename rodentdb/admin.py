from django.contrib import admin

from . import models


@admin.register(models.Rodent)
class RodentAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]


admin.site.register(models.Background)
admin.site.register(models.Category)
admin.site.register(models.Genotype)
admin.site.register(models.Species)
