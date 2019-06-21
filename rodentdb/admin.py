from django.contrib import admin

from . import models


@admin.register(models.Rodent)
class RodentAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]


admin.site.register(models.Background)
admin.site.register(models.Category)
admin.site.register(models.CoatColor)
admin.site.register(models.InducibleCassette)
admin.site.register(models.ReporterGene)
admin.site.register(models.Species)
admin.site.register(models.Zygosity)
