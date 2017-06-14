from core.models.base import StandardModel

class Source(StandardModel):

  class Meta:
    app_label = "core"
    db_table = 'source'
    verbose_name_plural = 'sources'
    ordering = ['name']

  def __self__(self):
    return self.name


