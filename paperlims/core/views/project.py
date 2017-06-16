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

from core.serializers import ExperimentSerializer
from core.serializers import ProjectSerializer
from rest_framework.renderers import JSONRenderer

from core.models import Project

from core import constants
from core import utils

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

import json
import logging
import uuid
import zipfile

logger = logging.getLogger(__name__)


def projects(request):
    return render(request, 'core/projects/list.html')


class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'type', 'owner', 'description']
    template_name_suffix = '_create_form'

    def get_initial(self):
        logger.debug('In get initial {0}'.format(str(self.request.user.id)))
        return {'owner': self.request.user}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ProjectCreateView, self).form_valid(form)


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'type', 'owner', 'description']
    template_name_suffix = '_update_form'


class ProjectListView(ListView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def project_delete(request, pk):
    if request.method == 'DELETE':
        if not request.user.has_perm('molecular.delete_project'):
            message = "{0} does not have permission to delete projects.".format(request.user)
            return HttpResponse(content=message, status=401)

        project = Project.objects.get(pk=pk)
        logger.debug("Delete project ID: {0}".format(str(pk)))
        try:
            project.delete()
        except Exception as e:
            message = "Failed to delete the project: {0}".format(e.message)
            logger.error(message)
            return HttpResponse(content=message, status=500)

        return HttpResponse(content="Success", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)


def project_detail_as_json(request, pk):
    project = Project.objects.get(pk=pk)
    response = JSONRenderer().render(
        ProjectSerializer(project).data
    )
    return HttpResponse(response, content_type='application/json')


def list_projects_as_json(request):
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

        logger.debug(Project.objects.filter(query).query)
        objects = Project.objects.filter(query).distinct().order_by('date_created')
    else:
        objects = Project.objects.all().order_by('date_created')

    if objects.count() > length:
        chosen_page = int(math.ceil(float(start) / length))
        page = chosen_page
    else:
        page = 1

    logger.debug("start {0} length {1} page {2}".format(start, length, page))
    paginator = Paginator(objects, length)

    serialzed_objects = ProjectSerializer(Project.objects.all(), many=True)

    data = {
        'recordsTotal': Project.objects.all().count(),
        'recordsFiltered': Project.objects.all().count(),
        'start': start,
        'length': length,
        'data': serialzed_objects.data
    }
    response = JSONRenderer().render(data)
    return HttpResponse(response, content_type='application/json')


def unlock_project(request, pk):
    if request.method == 'POST':
        project = Project.objects.get(pk=pk)
        try:
            if project.owner == request.user:
                project.status = constants.STATUS_ACTIVE
                project.save()
            else:
                raise Exception("Only the owner can unlock a record")
        except Exception as e:
            message = e
            return HttpResponse(content="Error: {0}".format(message), status=500)
        return HttpResponse(content="Success: Project Locked", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)


def lock_project(request, pk):
    if request.method == 'POST':
        project = Project.objects.get(pk=pk)
        try:
            project.status = constants.STATUS_LOCKED
            project.save()
        except Exception as e:
            message = e
            return HttpResponse(content="Error: {0}".format(message), status=500)
        return HttpResponse(content="Success: Project Locked", status=200)
    else:
        return HttpResponse(content="Not Supported", status=500)


def list_project_experiments(request, pk):
    project = Project.objects.get(pk=pk)

    experiments = ExperimentSerializer(project.experiment_set.all(), many=True)

    data = {
        'recordsTotal': project.experiment_set.count(),
        'recordsFiltered': project.experiment_set.count(),
        'data': experiments.data
    }
    response = JSONRenderer().render(data)
    return HttpResponse(response, content_type='application/json')
