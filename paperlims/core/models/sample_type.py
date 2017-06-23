from django.db import models
from core.models.base import StandardModel

class SampleType(StandardModel):
  source_type = models.ForeignKey('self',null=True,blank=True)

  class Meta:
    app_label = "core"
    db_table = 'sample_type'
    verbose_name_plural = 'sample types'

  def __str__(self):
    return self.name

