from django.contrib import admin

from core.models import Project
from core.models import Sample
from core.models import Plate
from core.models import Well


class WellInline(admin.TabularInline):
    model = Well
    extra = 0

class PlateAdmin(admin.ModelAdmin):
    inlines = [
        WellInline
    ]


admin.site.register(Project)
admin.site.register(Sample)
admin.site.register(Plate,PlateAdmin)

