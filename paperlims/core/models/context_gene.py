from django.db import models
from core.models.base import Base
from core import constants
from core import utils
from core.models import Gene

class ContextGene(Base):
  CONTEXTS = utils.self_zip(constants.GENE_CONTEXTS)
  gene = models.ForeignKey(Gene)
  context = models.CharField(max_length=255, choices=CONTEXTS)


  class Meta:
    app_label = "core"
    db_table = 'context_gene'
    ordering = ['-date_created']
    unique_together = ('gene','context')

  def __str__(self):
    return "{0} {1}".format(self.gene.name,self.context)

