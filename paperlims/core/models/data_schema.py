from django.db import models
from core.models.base import StandardModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.contrib.postgres.fields import JSONField

class DataSchema(StandardModel):

  schema = JSONField()
  version = models.TextField()

  #inspired by generics system. We link to the contenttype to allow
  #scoping of a schema entry to the object that we are expecting to
  #"project" the schema on to. It's manyy-to-many so that similar
  #data can be captured and centrally enforced for a set of objects.
  content_type = models.ManyToManyField(
    'self',
    through='DataSchemaToContentType',
    symmetrical=False,
    related_name="data_schemas",
    blank=True
  )

  class Meta:
    app_label = "core"
    db_table = 'data_schema'
    verbose_name_plural = 'data schema'

  def __str__(self):
    return self.name


class DataSchemaToContentType(models.Model):
  data_schema = models.ForeignKey(DataSchema, related_name='data_schema')
  content_type = models.ForeignKey(ContentType, related_name='content_type')

  class Meta:
    app_label = "core"
    db_table = 'data_schema_to_content_type'
    verbose_name_plural = 'data schema to content types'
    unique_together = ('data_schema','content_type')
