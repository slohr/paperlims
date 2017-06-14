from django.db import models
from core.models.base import StandardModel

class Location(StandardModel):
  parent_location = models.ForeignKey('self',null=True,blank=True)

  class Meta:
    app_label = "core"
    db_table = 'location'
    verbose_name_plural = 'locations'

  def __self__(self):
    return self.name

