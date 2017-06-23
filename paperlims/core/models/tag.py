from core.models.base import CaseInsensitiveNamedModel

class Tag(CaseInsensitiveNamedModel):

  class Meta:
    app_label = "core"
    db_table = 'tag'
    unique_together = ('name',)
    ordering = ['-date_created']

  def __str__(self):
    return self.name

