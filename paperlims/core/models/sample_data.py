from django.db import models
from core.models.base import Base
from core.models import Sample
from core.models import Note
from core.models import Project



from django.contrib.contenttypes import fields
from django.contrib.postgres.fields import JSONField

import json

class SampleData(Base):
  sample = models.ForeignKey(Sample)
  data = JSONField()
  notes = fields.GenericRelation(Note)


  class Meta:
    app_label = "core"
    db_table = 'sample_data'
    verbose_name_plural = 'sample data'

  def __str__(self):
    return self.action

