from django.db import models

from  core.models.base import Base

class RecordNote(Base):
  table_name = models.CharField(max_length=255)
  record_id = models.CharField(max_length=255)
  note = models.TextField()

  class Meta:
    app_label = "core"
    db_table = 'record_note'

  def __self__(self):
    return self.note


