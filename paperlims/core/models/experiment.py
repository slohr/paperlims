import os.path
from django.db import models
from core.models.base import StandardModel
from core import utils
from core import constants
from core.models import Project
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from django.db import connection


from polymorphic.models import PolymorphicModel

import logging

logger = logging.getLogger(__name__)


class Experiment(PolymorphicModel,StandardModel):
  TYPES = utils.self_zip(constants.EXPERIMENT_TYPES)
  STATUSES = utils.self_zip(constants.EXPERIMENT_STATUSES)
  project = models.ForeignKey(Project)
  owner = models.ForeignKey(User,related_name='experiment_owner')
  type = models.CharField(max_length=255,choices=TYPES)
  status = models.CharField(max_length=255,choices=STATUSES,default=constants.STATUS_ACTIVE)

  class Meta:
    app_label = "core"
    db_table = 'experiment'
    unique_together = ('name','project')
    ordering = ['-date_created']

  def get_experiment_dir(self):
    utils.create_directory(
      os.path.join(settings.DATA_ROOT,constants.EXPERIMENT_DATA_FILES,str(self.id))
    )
    return os.path.join(settings.DATA_ROOT,constants.EXPERIMENT_DATA_FILES,str(self.id))

  def __str__(self):
        return self.name

  def get_absolute_url(self):
        return reverse('experiments-detail', kwargs={'pk': self.pk})


  # get the next value in the sequence based on the record name
  # record_1 would generate 2
  # record_10 would generate 11
  @staticmethod
  def get_operational_index(value):
    replacement_value = "{0}_".format(value)
    predicate_value = "{0}_[0-9]+$".format(value)
    sql_string = """
      select max(
        to_number(
          substring(name from char_length(%(replacement_value)s) + position(%(replacement_value)s in name)),
          '999'
        ) + 1
      ) from experiment
      where name ~ (%(predicate_value)s);
    """
    index = 1
    try:
      logger.debug(sql_string)
      cursor = connection.cursor()
      cursor.execute(
        sql_string,
        {
          'replacement_value': replacement_value,
          'predicate_value':predicate_value
        }
      )
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



