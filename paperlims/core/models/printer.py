from django.db import models
from core.models.base import StandardModel
from core.models import Location
from core.models import LabelFormat

from core import constants
from core import utils

class Printer(StandardModel):
  TYPES = utils.self_zip(constants.ALL_PRINTER_TYPES)
  type = models.CharField(max_length=255,choices=TYPES)
  address = models.CharField(max_length=255,null=True,blank=True)
  location = models.ForeignKey(Location,null=True,blank=True)
  label_formats = models.ManyToManyField(LabelFormat,blank=True,through='PrinterToLabelFormat')

  class Meta:
    app_label = "core"
    db_table = 'printer'
    verbose_name_plural = 'printers'

  def __unicode__(self):
    return "{0}({1})".format(self.name,self.address)

