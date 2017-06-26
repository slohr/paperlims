import os
import re
from datetime import datetime

from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
from django.db.models import Q

from django.conf import settings
from django import forms
from django.core.files import File

from django.utils.decorators import method_decorator
# from privateviews.decorators import login_not_required
from django.utils import timezone

# from custom import serializers
from django.core import serializers

from core.serializers import SampleSerializer
from core.serializers import DataFileSerializer
from rest_framework.renderers import JSONRenderer

from core.services import data_file_service

from core.models import Project
from core.models import DataFile

from core.models import Sample

from core import constants
from core import utils

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

import json
import logging
import uuid
import zipfile

logger = logging.getLogger(__name__)

def datafiles(request):
    context = {
      'projects': Project.objects.all()
    }
    return render(request, 'core/datafiles/list.html',context=context)


class DataFileDetailView(DetailView):
    model = DataFile

    def get_context_data(self, **kwargs):
        context = super(DataFileDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def data_file_detail_as_json(request, pk):
    sample = DataFile.objects.get(pk=pk)
    response = JSONRenderer().render(
        DataFileSerializer(sample).data
    )
    return HttpResponse(response, content_type='application/json')


def list_data_files_as_json(request):
    logger.debug(request)
    start = int(request.GET.get('start', 0)) + 1
    length = int(request.GET.get('length', 10))

    search_value = None

    if search_value:
        query = Q(name__icontains=search_value) | \
                Q(created_by__last_name__icontains=search_value) | \
                Q(created_by__first_name__icontains=search_value) | \
                Q(created_by__username__icontains=search_value) | \
                Q(status__icontains=search_value)

        logger.debug(DataFile.objects.filter(query).query)
        objects = DataFile.objects.filter(query).distinct().order_by('date_created')
    else:
        objects = DataFile.objects.all().order_by('date_created')

    if objects.count() > length:
        chosen_page = int(math.ceil(float(start) / length))
        page = chosen_page
    else:
        page = 1

    logger.debug("start {0} length {1} page {2}".format(start, length, page))
    paginator = Paginator(objects, length)

    serialzed_objects = DataFileSerializer(DataFile.objects.all(), many=True)

    data = {
        'recordsTotal': DataFile.objects.all().count(),
        'recordsFiltered': DataFile.objects.all().count(),
        'start': start,
        'length': length,
        'data': serialzed_objects.data
    }
    response = JSONRenderer().render(data)
    return HttpResponse(response, content_type='application/json')



def data_file_delete(request, pk):
    if request.method == 'DELETE':
        if not request.user.has_perm('core.delete_datafile'):
            message = "{0} does not have permission to delete data files.".format(request.user)
            return HttpResponse(content=message, status=401)

        data_file = DataFile.objects.get(pk=pk)
        logger.debug("Delete data_file ID: {0}".format(str(pk)))
        try:
            data_file.delete()
        except Exception as e:
            message = "Failed to delete the data file: {0}".format(e.message)
            logger.error(message)
            return HttpResponse(content=message, status=500)

        return HttpResponse(content="Success", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)


def upload_data_file(request):
  logger.debug('Inside data file upload')
  logger.debug(request)

  uploaded_file = request.FILES['file']

  if request.method == 'POST':
    logger.debug("Received file: {0}".format(uploaded_file.name))
    groups = re.split("\.", format(uploaded_file.name))
    uploaded_file_extension = groups[len(groups)-1]

    project_id = request.POST.get("project_id")

    logger.debug("Parsing primer pair file")

    project = Project.objects.get(pk=project_id)
    data_file = DataFile(
      name=os.path.basename(uploaded_file.name),
      project=project,
      file=uploaded_file,
      created_by=request.user
    )
    data_file.save()
    data_file_service.process_data_file(request.user, data_file)

  return HttpResponse(content="Success",status=200)
