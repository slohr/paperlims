import os.path
from django.db import models
from polymorphic.models import PolymorphicModel
from core.models.base import Base
from core.models.base import UniqueFileSystemStorage

from core import constants
from core.models import Experiment

class ExperimentDataFile(PolymorphicModel,Base):
  experiment = models.ForeignKey(Experiment)


  class Meta:
    app_label = "core"
    db_table = 'experiment_data_file'
    ordering = ['-date_created']

  def filename(self):
        return os.path.basename(self.file.name)

  def get_upload_path(instance, filename):
    return os.path.join(
      "{0}/{1}/{2}".format(constants.EXPERIMENT_DATA_FILES,instance.experiment.id,filename)
    )

  file = models.FileField(upload_to=get_upload_path,storage=UniqueFileSystemStorage())

  def __unicode__(self):
        return self.filename()


