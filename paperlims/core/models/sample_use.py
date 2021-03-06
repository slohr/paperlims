from django.db import models
from core.models.base import Base
from core.models import Sample
from core.models import Note
from core.models import Project



from django.contrib.contenttypes import fields

import json

class SampleUse(Base):
  sample = models.ForeignKey(Sample)
  project = models.ForeignKey(Project,null=True,blank=True)
  action = models.TextField()
  notes = fields.GenericRelation(Note)

  class Meta:
    app_label = "core"
    db_table = 'sample_use'
    verbose_name_plural = 'sample use'

  def __str__(self):
    return self.action

