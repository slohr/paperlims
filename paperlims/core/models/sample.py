import uuid
from django.db import models
from core.models.base import StandardModel
from core.models.base import CaseInsensitiveNamedModel
from core.models import Material
from core.models import Source
from core.models import SampleType
from core.models import Storage
from core.models import Project
from core.models import Note

from django.contrib.auth.models import User
from django.contrib.contenttypes import fields
from django.core.urlresolvers import reverse

from django.db import connection

from core import constants
from core import utils

from polymorphic.models import PolymorphicModel

import logging

logger = logging.getLogger(__name__)


class Sample(PolymorphicModel, CaseInsensitiveNamedModel):
  STATUSES = utils.self_zip(constants.STANDARD_STATUSES)
  sample_type = models.ForeignKey(SampleType)
  material = models.ForeignKey(Material)
  status = models.CharField(max_length=255,choices=STATUSES,default=constants.STATUS_ACTIVE)
  owner = models.ForeignKey(User,null=True,blank=True)

  source = models.ForeignKey(Source,null=True,blank=True)
  lot = models.CharField(max_length=255, null=True, blank=True)
  volume = models.CharField(max_length=255, null=True, blank=True)
  concentration = models.CharField(max_length=255, null=True, blank=True)
  concentration_units = models.CharField(max_length=255, null=True, blank=True)
  project = models.ManyToManyField(Project,blank=True)
  storage = models.ForeignKey(Storage,null=True, blank=True)
  unit_count = models.CharField(max_length=255, null=True, blank=True)

  notes = fields.GenericRelation(Note)

  sample_links = models.ManyToManyField(
    'self',
    through='SampleToSample',
    symmetrical=False,
    related_name="linked_to",
    blank=True
  )

  def _has_alert_note(self):
    logger.debug('looking for alert note')
    return self.notes.filter(note_type=constants.TYPE_ALERT).exists()

  has_alert_note = property(_has_alert_note)

  class Meta:
    app_label = "core"
    db_table = 'sample'
    verbose_name_plural = 'samples'
    unique_together = ("name",)
    ordering = ['-date_created']

  def save(self, *args, **kwargs):
    if not self.name:
        self.name = Sample.name_generator()
    super(Sample, self).save(*args, **kwargs)

  def get_absolute_url(self):
        return reverse('samples-detail', kwargs={'pk': self.pk})

  def __str__(self):
    return self.name

  def add_sample_link(self, sample, link_type):
    link, created = SampleToSample.objects.get_or_create(
      source_sample=self,
      target_sample=sample,
      type=link_type
    )
    return link

  def remove_sample_link(self, sample, link_type):
    SampleToSample.objects.filter(
      source_sample=self,
      target_sample=sample,
      type=link_type
    ).delete()
    return

  def get_sample_links(self, link_type):
    return self.sample_links.filter(
      target_samples__type=link_type,
      target_samples__source_sample=self
    )

  def get_related_to(self, link_type):
    return self.linked_to.filter(
      source_samples__type=link_type,
      source_samples__target_sample=self
    )

  def get_children(self):
    logger.debug("in generic get children")
    link_type = SampleLink.objects.get(name=constants.LINK_TYPE_CHILD)
    return self.get_sample_links(link_type)

  def get_parents(self):
    logger.debug("in generic get parents")
    link_type = SampleLink.objects.get(name=constants.LINK_TYPE_PARENT)
    return self.get_related_to(link_type)

  @classmethod
  def name_generator(cls):
    return "S-{0}".format(uuid.uuid4())

  # get the next value in the sequence based on the record name
  # record_1 would generate 2
  # record_10 would generate 11
  @staticmethod
  def get_operational_index(value):
    sql_string = """
      select max(
        to_number(
          substring(name from char_length(%(value)s) + position(%(value)s in name)),
          '999'
        ) + 1
      ) from sample
      where name ~ (%(value)s || '[0-9]+$');
    """
    index = 1
    try:
      cursor = connection.cursor()
      cursor.execute(sql_string, {'value': value})
      row = cursor.fetchone()
      logger.debug(row)
      index = row[0]
      if index is None:
        index = 1
    except Exception as e:
      logger.debug(e)
      logger.debug("exception while looking up values")
      index = 1

    logger.debug("returning the following index {0}".format(index))
    return index


Sample._meta.get_field('name').null = True
Sample._meta.get_field('name').blank = True

class SampleLink(StandardModel):

  class Meta:
    app_label = "core"
    db_table = 'sample_link'
    verbose_name_plural = 'sample links'

  def __str__(self):
    return self.name


class SampleToSample(models.Model):
  source_sample = models.ForeignKey(Sample, related_name='source_samples')
  target_sample = models.ForeignKey(Sample, related_name='target_samples')
  type = models.ForeignKey(SampleLink)

  class Meta:
    app_label = "core"
    db_table = 'sample_to_sample'
    verbose_name_plural = 'sample to samples'


