from django.db import models
from core.models.base import StandardModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

class LabelFormat(StandardModel):

  format = models.TextField()

  #inspired by generics system. We link to the contenttype to allow
  #scoping of labels to the object that we are expecting to print
  #a label for.
  content_type = models.ForeignKey(ContentType,null=True)

  class Meta:
    app_label = "core"
    db_table = 'label_format'
    verbose_name_plural = 'label formats'

  def __str__(self):
    return self.name


