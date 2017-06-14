from django.db import models
from core.models.base import StandardModel
from core.models import Sample
from core.models import Project

from django.contrib.auth.models import User

class SampleBucket(StandardModel):
  samples = models.ManyToManyField(Sample,blank=True)
  projects = models.ManyToManyField(Project,blank=True)
  owner = models.ForeignKey(User)

  class Meta:
    app_label = "core"
    db_table = 'sample_bucket'
    verbose_name_plural = 'sample buckets'

  def __self__(self):
    return self.name

