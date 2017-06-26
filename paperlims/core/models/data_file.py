import os
from django.db import models
from core.models.base import StandardModel
from core.models import Project

from django.conf import settings


from core.models.base import FileSystemStorage

from core import constants

def get_datafile_upload_path(instance, filename):
    #"{0}/{1}/{2}/{3}".format(settings.DATA_ROOT,constants.DATA_FILE_FOLDER,instance.project.id,filename)
    return os.path.join(
        "{0}/{1}/{2}".format(constants.DATA_FILE_FOLDER, instance.project.id, filename)
    )

class DataFile(StandardModel):

  project = models.ForeignKey(Project)
  class Meta:
    app_label = "core"
    db_table = 'data_file'
    ordering = ['-date_created']

  def filename(self):
        return os.path.basename(self.file.name)


  file = models.FileField(upload_to=get_datafile_upload_path,storage=FileSystemStorage(base_url=settings.DATA_ROOT))

  def __str__(self):
        return "{0}".format(self.name)
