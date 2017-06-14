from django.db import models
from core.models.base import StandardModel
from core.models import Note
from core.models import Attachment
from django.contrib.contenttypes import fields


from polymorphic.models import PolymorphicModel

class Material(PolymorphicModel, StandardModel):

  notes = fields.GenericRelation(Note)
  attachments = fields.GenericRelation(Attachment)

  material_links = models.ManyToManyField(
    'self',
    through='MaterialToMaterial',
    symmetrical=False,
    related_name="linked_to",
    blank=True
  )


  class Meta:
    app_label = "core"
    db_table = 'material'
    verbose_name_plural = 'materials'
    unique_together = ('name',)

  def __self__(self):
    return self.name

  def add_material_link(self, material, link_type):
    link, created = MaterialToMaterial.objects.get_or_create(
      source_material=self,
      target_material=material,
      type=link_type
    )
    return link

  def remove_material_link(self, material, link_type):
    MaterialToMaterial.objects.filter(
      source_material=self,
      target_material=material,
      type=link_type
    ).delete()
    return

  def get_material_links(self, link_type):
    return self.material_links.filter(
      target_materials__type=link_type,
      target_materials__source_material=self
    )

  def get_related_to(self, link_type):
    return self.linked_to.filter(
      source_materials__type=link_type,
      source_materials__target_material=self
    )


class MaterialLink(StandardModel):

  class Meta:
    app_label = "core"
    db_table = 'material_link'
    verbose_name_plural = 'material links'

  def __self__(self):
    return self.name


class MaterialToMaterial(models.Model):
  source_material = models.ForeignKey(Material, related_name='source_materials')
  target_material = models.ForeignKey(Material, related_name='target_materials')
  type = models.ForeignKey(MaterialLink)

  class Meta:
    app_label = "core"
    db_table = 'material_to_material'
    verbose_name_plural = 'material to materials'
