from core.models.base import StandardModel


class Species(StandardModel):
  class Meta:
    app_label = "core"
    db_table = 'species'
    ordering = ['-date_created']

  def __str__(self):
    return self.name

