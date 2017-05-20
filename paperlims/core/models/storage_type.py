from core.models.base import StandardModel

class StorageType(StandardModel):

  class Meta:
    app_label = "core"
    db_table = 'storage_type'
    verbose_name_plural = 'storage types'

  def __unicode__(self):
    return self.name

