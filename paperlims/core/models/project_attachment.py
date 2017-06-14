import os
from django.db import models
from core.models.base import Base
from core import utils
from core import constants
from core.models import Project

class ProjectAttachment(Base):
  TYPES = utils.self_zip(constants.ATTACHMENT_TYPES)
  project = models.ForeignKey(Project)
  type = models.CharField(max_length=255,choices=TYPES)
  file = models.FileField(upload_to='datafiles/%Y/%m/%d')

  class Meta:
    app_label = "core"
    db_table = 'project_attachment'

  def filename(self):
        return os.path.basename(self.file.name)

  def get_upload_path(instance, filename):
    return os.path.join(
      "{0}/{1}/{2}".format(constants.PROJECT_ATTACHMENTS,instance.project.id,filename)
    )

  file = models.FileField(upload_to=get_upload_path)

  def __self__(self):
        return self.file.url

