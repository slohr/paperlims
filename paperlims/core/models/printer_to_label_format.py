from django.db import models

from core.models import Printer
from core.models import LabelFormat

class PrinterToLabelFormat(models.Model):
  printer = models.ForeignKey(Printer)
  label_format = models.ForeignKey(LabelFormat)

  class Meta:
    app_label = "core"
    db_table = 'printer_to_labelformat'
    verbose_name_plural = 'printer to label formats'