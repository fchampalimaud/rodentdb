from django.contrib import admin

from .models import Rodent


@admin.register(Rodent)
class RodentAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
