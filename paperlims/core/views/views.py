# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import logging

import os

import re

from core.services import data_file_service

from core.models import Project
from core.models import DataFile

logger = logging.getLogger(__name__)

def index(request):
	return render(request, 'core/index.html')

def datafiles(request):
    return render(request, 'core/datafiles/list.html')


#DATAFILES
def upload_data_file(request):
  logger.debug('Inside data file upload')
  uploaded_file = request.FILES['file']

  if request.method == 'POST':
    logger.debug("Received file: {0}".format(uploaded_file.name))
    groups = re.split("\.", format(uploaded_file.name))
    uploaded_file_extension = groups[len(groups)-1]

    #try:
    logger.debug("Parsing primer pair file")

    project = Project.objects.get(name="first")
    data_file = DataFile(
      project=project,
      file=uploaded_file,
      created_by=request.user
    )
    data_file.save()
    data_file_service.process_data_file(request.user, data_file)

    # except AttributeError, e:
    #   message = e
    #   logger.error(e)
    #   return HttpResponse(content="File processing error: {0}".format(message),status=500)
    # except Exception, e:
    #   logger.error(e)
    #   message = e
    #   return HttpResponse(content="Unknown Error: {0}".format(message),status=500)

  return HttpResponse(content="Success",status=200)
