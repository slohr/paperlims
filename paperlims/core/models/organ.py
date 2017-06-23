from core.models.base import StandardModel


class Organ(StandardModel):
  class Meta:
    app_label = "core"
    db_table = 'organ'
    ordering = ['-date_created']

  def __str__(self):
    return self.name

