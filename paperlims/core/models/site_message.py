from django.db import models
from core.models.base import Base

class SiteMessage(Base):
  message = models.TextField()

  class Meta:
    app_label = "core"
    db_table = 'site_message'

  def __str__(self):
    return self.message


