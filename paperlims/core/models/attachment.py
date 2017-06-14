import os
from django.db import models
from core.models.base import Base
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from core import constants
from core.models.base import UniqueFileSystemStorage

import json

class Attachment(Base):

  description = models.TextField()

  class Meta:
    app_label = "core"
    db_table = 'attachment'
    ordering = ['-date_created']

  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = fields.GenericForeignKey('content_type', 'object_id')

  def __self__(self):
    return self.filename()


  def filename(self):
        return os.path.basename(self.file.name)

  def get_upload_path(instance, filename):
    return os.path.join(
      "{0}/{1}_{2}/{3}".format(constants.ATTACHMENT_FOLDER,instance.content_type.name,instance.object_id,filename)
    )

  file = models.FileField(upload_to=get_upload_path,storage=UniqueFileSystemStorage())

