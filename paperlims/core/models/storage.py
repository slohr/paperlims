from django.db import models
from core.models.base import StandardModel
from core.models import StorageType

from core import constants
from core import utils

import logging

logger = logging.getLogger(__name__)

class Storage(StandardModel):
  STATUSES = utils.self_zip(constants.STANDARD_STATUSES)
  status = models.CharField(max_length=255,choices=STATUSES)
  location = models.CharField(max_length=255,null=True,blank=True)
  parent = models.ForeignKey("self",null=True,blank=True)
  type = models.ForeignKey(StorageType,null=True,blank=True,)
  holds_containers = models.BooleanField()
  holds_samples = models.BooleanField()

  class Meta:
    app_label = "core"
    db_table = 'storage'
    verbose_name_plural = 'storage'
    unique_together = ('name',)

  def __str__(self):
    if self.type:
      return "{0} {1}".format(self.type.name,self.name)
    else:
      return "N/A {0}".format(self.name)



  def get_ancestors(self):
    logger.debug("getting ancestors")
    if self.parent is None:
      return []
    return [self.parent] + self.parent.get_ancestors()

  def get_descendants(self):
    tree = []
    tree = tree + list(self.storage_set.all())
    for s in self.storage_set.all():
        tree = tree + s.get_descendants()
    return tree

  def get_samples(self):
    tree = []
    tree = tree + list(self.sample_set.all())
    for s in self.storage_set.all():
        tree = tree + s.get_samples()
    return tree