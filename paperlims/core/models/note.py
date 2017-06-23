from django.db import models
from core.models.base import Base
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from core import constants
from core import utils

import json

class Note(Base):
  TYPES = utils.self_zip(constants.NOTE_TYPES)
  note = models.TextField()
  parent_note = models.ForeignKey('self',null=True,blank=True,related_name="parent")
  note_type = models.CharField(max_length=255,choices=TYPES)

  class Meta:
    app_label = "core"
    db_table = 'note'

  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = fields.GenericForeignKey('content_type', 'object_id')

  def __str__(self):
    return self.note

  def get_json(self):
    return json.JSONDecoder().decode(serializers.serialize('json',[self],relations=('created_by')))[0]

