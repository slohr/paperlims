import os
from django.db import models
from core.models.base import Base
from core import utils
from core import constants
from core.models import Experiment

class ExperimentAttachment(Base):
  TYPES = utils.self_zip(constants.ATTACHMENT_TYPES)
  experiment = models.ForeignKey(Experiment)
  type = models.CharField(max_length=255,choices=TYPES)

  class Meta:
    app_label = "core"
    db_table = 'experiment_attachment'
    ordering = ['-date_created']

  def filename(self):
        return os.path.basename(self.file.name)

  def get_upload_path(instance, filename):
    return os.path.join(
      "{0}/{1}/{2}".format(constants.EXPERIMENT_ATTACHMENTS,instance.experiment.id,filename)
    )

  file = models.FileField(upload_to=get_upload_path)

  def __str__(self):
        return self.file.url


