import os
from django.db import models
from core.models.base import Base
from core.models import Project

from core.models.base import FileSystemStorage

from core import constants

def get_datafile_upload_path(instance, filename):
    return os.path.join(
        "{0}/{1}/{2}".format(constants.DATA_FILE_FOLDER,instance.project.id,filename)
    )

class DataFile(Base):

  project = models.ForeignKey(Project)
  class Meta:
    app_label = "core"
    db_table = 'data_file'
    ordering = ['-date_created']

  def filename(self):
        return os.path.basename(self.file.name)


  file = models.FileField(upload_to=get_datafile_upload_path,storage=FileSystemStorage())

  def __self__(self):
        return self.filename()
