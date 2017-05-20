from django.db import models
from core.models.base import StandardModel

class Gene(StandardModel):
  official_symbol = models.CharField(max_length=255)
  official_full_name = models.CharField(max_length=255)

  class Meta:
    app_label = "core"
    db_table = 'gene'
    ordering = ['-date_created']
    unique_together = ('name',)

  def __unicode__(self):
    return self.name

