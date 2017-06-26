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
from rest_framework.renderers import JSONRenderer

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


def samples(request):
    return render(request, 'core/samples/list.html')


class SampleCreateView(CreateView):
    model = Sample
    fields = [
        'name',
        'owner',
        'sample_type',
        'status'
        'lot',
        'project',
        'source',
        'description',
        'material',
        'volume',
        'concentration',
        'concentration_units',
        'unit_count',
        'storage'
    ]

    def get_initial(self):
        return {
            'name' : Sample.name_generator(),
            'owner': self.request.user,

        }

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(SampleCreateView, self).form_valid(form)


class SampleDetailView(DetailView):
    model = Sample

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SampleUpdateView(UpdateView):
    model = Sample
    fields = [
        'name',
        'owner',
        'sample_type',
        'status',
        'lot',
        'project',
        'source',
        'description',
        'material',
        'volume',
        'concentration',
        'concentration_units',
        'unit_count',
        'storage'
    ]


class SampleListView(ListView):
    model = Sample

    def get_context_data(self, **kwargs):
        context = super(SampleListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def sample_delete(request, pk):
    if request.method == 'DELETE':
        if not request.user.has_perm('core.delete_sample'):
            message = "{0} does not have permission to delete samples.".format(request.user)
            return HttpResponse(content=message, status=401)

        sample = Sample.objects.get(pk=pk)
        logger.debug("Delete sample ID: {0}".format(str(pk)))
        try:
            sample.delete()
        except Exception as e:
            message = "Failed to delete the sample: {0}".format(e.message)
            logger.error(message)
            return HttpResponse(content=message, status=500)

        return HttpResponse(content="Success", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)


def sample_detail_as_json(request, pk):
    sample = Sample.objects.get(pk=pk)
    response = JSONRenderer().render(
        SampleSerializer(sample).data
    )
    return HttpResponse(response, content_type='application/json')


def list_samples_as_json(request):
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

        logger.debug(Sample.objects.filter(query).query)
        objects = Sample.objects.filter(query).distinct().order_by('date_created')
    else:
        objects = Sample.objects.all().order_by('date_created')

    if objects.count() > length:
        chosen_page = int(math.ceil(float(start) / length))
        page = chosen_page
    else:
        page = 1

    logger.debug("start {0} length {1} page {2}".format(start, length, page))
    paginator = Paginator(objects, length)

    serialzed_objects = SampleSerializer(Sample.objects.all(), many=True)

    data = {
        'recordsTotal': Sample.objects.all().count(),
        'recordsFiltered': Sample.objects.all().count(),
        'start': start,
        'length': length,
        'data': serialzed_objects.data
    }
    response = JSONRenderer().render(data)
    return HttpResponse(response, content_type='application/json')


def unlock_sample(request, pk):
    if request.method == 'POST':
        project = Sample.objects.get(pk=pk)
        try:
            if project.owner == request.user:
                project.status = constants.STATUS_ACTIVE
                project.save()
            else:
                raise Exception("Only the owner can unlock a record")
        except Exception as e:
            message = e
            return HttpResponse(content="Error: {0}".format(message), status=500)
        return HttpResponse(content="Success: Sample Locked", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)


def lock_sample(request, pk):
    if request.method == 'POST':
        sample = Sample.objects.get(pk=pk)
        try:
            sample.status = constants.STATUS_LOCKED
            sample.save()
        except Exception as e:
            message = e
            return HttpResponse(content="Error: {0}".format(message), status=500)
        return HttpResponse(content="Success: Sample Locked", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)