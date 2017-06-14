from django.db import models
from core.models.base import Base
from core.models import Sample
from core.models import Note
from core.models import Project



from django.contrib.contenttypes import fields

import json

class SampleUse(Base):
  sample = models.ForeignKey(Sample)
  project = models.ForeignKey(Project,null=True,blank=True)
  action = models.TextField()
  notes = fields.GenericRelation(Note)

  def _get_full_name(self):
      "Returns the person's full name."
      return "red"

  full_name = property(_get_full_name)

  class Meta:
    app_label = "core"
    db_table = 'sample_use'
    verbose_name_plural = 'sample use'

  def __self__(self):
    return self.action

  def get_json(self):
    project = None
    if self.project:
      project = json.JSONDecoder().decode(serializers.serialize('json',[self.project],indent=4,relations='created_by,project'))[0]

    notes = [n.get_json() for n in self.notes.all()]

    me = json.JSONDecoder().decode(serializers.serialize('json',[self],indent=4,relations='created_by'))[0]
    me_obj = json.loads(json.dumps(me))
    me_obj['fields']['notes'] = notes

    return json.JSONDecoder().decode(json.dumps(me_obj))

