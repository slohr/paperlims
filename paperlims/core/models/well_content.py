from django.db import models
from core.models.base import Base
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


from core import constants
from core import utils
from core.models import Well

import json

class WellContent(Base):
  well = models.ForeignKey(Well)
  amount_value = models.CharField(max_length=255,null=True,blank=True)
  amount_unit = models.CharField(max_length=255,null=True,blank=True)

  class Meta:
    app_label = "core"
    db_table = 'well_content'

  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = fields.GenericForeignKey('content_type', 'object_id')

  def __str__(self):
    return self.note

