import logging

import os

from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User

from django.db import models

from django.db.models import fields

from django.core.urlresolvers import reverse

from core import constants

from core import exceptions

from core import utils

logger = logging.getLogger(__name__)


####################################
# CUSTOM FIELDS
####################################
class CaseInsensitiveTextField(fields.TextField):
  def db_type(self, connection):
    return "citext"

class CaseInsensitiveCharField(fields.CharField):
  def db_type(self, connection):
    return "citext"

####################################
# CUSTOM STORAGE
####################################


class UniqueFileSystemStorage(FileSystemStorage):
  def get_available_name(self, name,  max_length=None):
    return name

  def _save(self, name, content):
    if self.exists(name):
      raise exceptions.DuplicateFileError('File already exists: %s' % name)

    return super(UniqueFileSystemStorage, self)._save(name, content)

class ModelAttachmentStorage(FileSystemStorage):
  def get_available_name(self, name, max_length=None):
    return name

####################################
# ABSTRACT MODELS
####################################


class Base(models.Model):
  id = models.AutoField(primary_key=True)
  date_created = models.DateTimeField(auto_now_add=True) #only update during creation
  date_modified = models.DateTimeField(auto_now=True) #update everytime it's saved
  created_by = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_creator")

  class Meta:
    abstract = True
    get_latest_by = 'date_created'


class StandardModel(Base):
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)

  class Meta:
    abstract = True


class CaseInsensitiveNamedModel(Base):
  name = CaseInsensitiveCharField(max_length=255,unique=True)
  description = models.TextField(blank=True)

  class Meta:
    abstract = True
