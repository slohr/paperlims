from django.db import models
from polymorphic.models import PolymorphicModel
from core.models.base import StandardModel
from core.models import Plate


class Well(PolymorphicModel,StandardModel):
  plate = models.ForeignKey(Plate)
  index = models.IntegerField()

  well_links = models.ManyToManyField(
    'self',
    through='WellToWell',
    symmetrical=False,
    related_name="linked_to",
    blank=True
  )

  class Meta:
    app_label = "core"
    db_table = 'well'
    ordering = ['-date_created']
    unique_together = ("name","plate")

  def __str__(self):
    return "{0}_{1}".format(self.plate,self.name)


class WellLink(StandardModel):

  class Meta:
    app_label = "core"
    db_table = 'well_link'
    verbose_name_plural = 'well links'

  def __str__(self):
    return self.name


class WellToWell(models.Model):
  source_sample = models.ForeignKey(Well, related_name='source_wells')
  target_sample = models.ForeignKey(Well, related_name='target_wells')
  type = models.ForeignKey(WellLink)

  class Meta:
    app_label = "core"
    db_table = 'well_to_well'
    verbose_name_plural = 'wells to wells'
