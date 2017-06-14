from django.db import models
from core.models.base import StandardModel
from core import utils
from core import constants
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Plate(StandardModel):
  STATUSES = utils.self_zip(constants.STANDARD_STATUSES)
  status = models.CharField(max_length=255,choices=STATUSES)
  TYPES = utils.self_zip(constants.PLATE_TYPES)
  type = models.CharField(max_length=255,choices=TYPES)
  replicate = models.CharField(max_length=255)
  owner = models.ForeignKey(User,related_name='plate_owner',null=True,blank=True)
  DIMENSIONS = utils.self_zip(constants.PLATE_DIMENSIONS)
  dimension = models.CharField(max_length=255,choices=DIMENSIONS,null=True,blank=True)

  class Meta:
    app_label = "core"
    db_table = 'plate'
    unique_together = ("name", "replicate")
    ordering = ['-date_created']

  def full_name(self):
    return "{0}_{1}".format(self.name,self.replicate)

  def __self__(self):
    return "{0}_{1}".format(self.name,self.replicate)

  def get_absolute_url(self):
        return reverse('plate-detail', kwargs={'pk': self.pk})


