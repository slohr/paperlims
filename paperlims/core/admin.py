from django.contrib import admin

from core.models import Project
from core.models import Experiment
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

class ExperimentInline(admin.TabularInline):
    model = Experiment
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ExperimentInline
    ]


admin.site.register(Project,ProjectAdmin)
admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(Plate,PlateAdmin)
admin.site.register(Well)

