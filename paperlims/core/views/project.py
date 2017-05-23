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
#from privateviews.decorators import login_not_required
from django.utils import timezone

#from custom import serializers
from django.core import serializers

from core.serializers import ExperimentSerializer
from core.serializers import ProjectSerializer
from rest_framework.renderers import JSONRenderer

from core.models import Project


from core import constants
from core import utils

import json
import logging
import uuid
import zipfile

try:
    import io as StringIO
except ImportError:
    import io

logger = logging.getLogger(__name__)

class ProjectCreateView(CreateView):
  model = Project
  fields = ['name','type','owner','description']
  template_name_suffix = '_create_form'

  def get_initial(self):
    logger.debug('In get initial {0}'.format(str(self.request.user.id)))
    return {'owner' : self.request.user}

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
  fields = ['name','type','owner','description']
  template_name_suffix = '_update_form'


class ProjectListView(ListView):

  model = Project

  def get_context_data(self, **kwargs):
    context = super(ProjectListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

def project_delete(request,id):
  if request.method == 'DELETE':
    if not request.user.has_perm('molecular.delete_project'):
      message="{0} does not have permission to delete projects.".format(request.user)
      return HttpResponse(content=message,status=401)

    project = Project.objects.get(pk=id)
    logger.debug("Delete project ID: {0}".format(str(id)))
    try:
      project.delete()
    except Exception as e:
      message="Failed to delete the project: {0}".format(e.message)
      logger.error(message)
      return HttpResponse(content=message,status=500)

    return HttpResponse(content="Success",status=200)
  else:
    return HttpResponse(content="Not Supported",status=500)

def list_projects(request):

  start = int(request.GET.get('start',0)) + 1
  length = int(request.GET.get('length',10))

  search_value = None

  if search_value:
    query = Q(name__icontains=search_value) | \
            Q(created_by__last_name__icontains=search_value) | \
            Q(created_by__first_name__icontains=search_value) | \
            Q(created_by__username__icontains=search_value) | \
            Q(status__icontains=search_value)

    logger.debug(Project.objects.filter(query).query)
    objects = Project.objects.filter(query).distinct().order_by(sort_column)
  else:
    #virus_samples = VirusRequest.objects.all()
    #virus_samples = VirusRequest.objects.all().order_by('virus_sample__material__name')
    virus_samples = VirusRequest.objects.all().order_by(sort_column)

  if virus_samples.count() > length:
    chosen_page = int(math.ceil(float(start)/length))
    page = chosen_page
  else:
    page = 1

  logger.debug("start {0} length {1} page {2}".format(start,length,page))
  paginator = Paginator(virus_samples, length)

  serialzed_objects = ProjectSerializer(Project.objects.all(),many=True)

  data = {
    'recordsTotal':Project.objects.all().count(),
    'recordsFiltered':Project.objects.all().count(),
    'data':serialzed_objects.data
  }
  response = JSONRenderer().render(data)
  return HttpResponse(response, content_type='application/json')

def unlock_project(request,id):
  if request.method == 'POST':
    project = Project.objects.get(pk=id)
    try:
      if project.owner == request.user:
        project.status = constants.STATUS_ACTIVE
        project.save()
      else:
        raise Exception("Only the owner can unlock a record")
    except Exception as e:
      message = e
      return HttpResponse(content="Error: {0}".format(message),status=500)
    return HttpResponse(content="Success: Project Locked",status=200)
  else:
    return HttpResponse(content="Not Supported",status=500)

def lock_project(request,id):
  if request.method == 'POST':
    project = Project.objects.get(pk=id)
    try:
      project.status = constants.STATUS_LOCKED
      project.save()
    except Exception as e:
      message = e
      return HttpResponse(content="Error: {0}".format(message),status=500)
    return HttpResponse(content="Success: Project Locked",status=200)
  else:
    return HttpResponse(content="Not Supported",status=500)

def list_project_experiments(request,pk):
  project = Project.objects.get(pk=pk)

  experiments = ExperimentSerializer(project.experiment_set.all(),many=True)

  data = {
    'recordsTotal': project.experiment_set.count(),
    'recordsFiltered': project.experiment_set.count(),
    'data':experiments.data
  }
  response = JSONRenderer().render(data)
  return HttpResponse(response, content_type='application/json')

def experiment_data_files(request,pk):
  project = Project.objects.get(pk=pk)
  #data_files = serializers.serialize("custom_json", experiment.experimentdatafile_set.select_subclasses(),indent=4)
  data_files = serializers.serialize(
    "json",
    ExperimentDataFile.objects.filter(experiment__project=project).all(),
    excludes=('sequence'),
    indent=4,
    subclass=True,
    relations="created_by,plate",
    extras=('master_count','length','alias_list')
  )


  logger.debug(data_files)
  data = {
    'recordsTotal':ExperimentDataFile.objects.filter(experiment__project=project).count(),
    'recordsFiltered':ExperimentDataFile.objects.filter(experiment__project=project).count(),
    'data':json.JSONDecoder().decode(data_files)
  }
  return HttpResponse(json.dumps(data), content_type='application/json')

def create_project_analysis_criteria(request):
    analysis_criteria_id = request.POST['analysis-criteria-id']
    name = request.POST['analysis-criteria-name']
    criteria = request.POST['analysis-criteria-criteria']
    owner = request.POST['analysis-criteria-owner']
    type = request.POST['analysis-criteria-type']
    logger.debug(name)
    project_analysis_criteria = ProjectAnalysisCriteria(
        analysis_criteria = AnalysisCriteria.objects.get(pk=analysis_criteria_id),
        name = name,
        type = type,
        created_by_id = owner,
        criteria = criteria
    )
    try:
        project_analysis_criteria.save()
    except Exception as e:
      logger.error(e)
      message = e
      return HttpResponse(content="Error: {0}".format(message),status=500)

    object_in_array = json.loads(serializers.serialize("custom_json", [project_analysis_criteria,]))
    single_object = json.JSONDecoder().decode(json.dumps(object_in_array[0]))

    data = {
            'status':'OK',
            'object':single_object
    }
    return HttpResponse(json.dumps(data),content_type='application/json')

def project_analyses(request,id):
  project = Project.objects.get(pk=id)
  #analyses = serializers.serialize("custom_json", project.projectanalysis_set.select_subclasses(),indent=4)

  analyses = serializers.serialize(
    "json",
    project.projectanalysis_set.select_subclasses(),
    indent=4,
    subclass=True,
    relations="created_by,project",
  )

  #logger.debug(analyses)
  data = {
    'recordsTotal':project.projectanalysis_set.count(),
    'recordsFiltered':project.projectanalysis_set.count(),
    'data':json.JSONDecoder().decode(analyses)
  }
  return HttpResponse(json.dumps(data), content_type='application/json')

def project_analysis_data_files(request,id):
  project_analysis = ProjectAnalysis.objects.get(pk=id)
  data_files = serializers.serialize("custom_json", project_analysis.datafiles.all().select_subclasses(),indent=4)

  logger.debug(data_files)
  data = {
    'recordsTotal':project_analysis.datafiles.count(),
    'recordsFiltered':project_analysis.datafiles.count(),
    'data':json.JSONDecoder().decode(data_files)
  }
  return HttpResponse(json.dumps(data), content_type='application/json')

def project_analysis_data_file_delete(request,analysis_id,data_file_id):
    project_analysis = ProjectAnalysis.objects.get(pk=analysis_id)
    data_file = ExperimentDataFile.objects.get(pk=data_file_id)
    logger.debug("Delete analysis data_file ID: {0}".format(str(data_file_id)))
    try:
      project_analysis.datafiles.remove(data_file)
      return HttpResponse(content="Success",status=200)
    except Exception as e:
      return HttpResponse(content="Failed to delete the file: {0}".format(e.message),status=500)

def project_analysis_data_file_add(request,analysis_id):
  logger.debug('Inside project analysis data_file add')
  project_analysis = ProjectAnalysis.objects.get(pk=analysis_id)
  if request.method == 'POST':
    data_files = request.POST.getlist('experiment_datafile')
    for file_id in data_files:
      logger.debug("Received files: {0}".format(file_id))
      data_file = ExperimentDataFile.objects.get(pk=file_id)
      project_analysis.datafiles.add(data_file)

    try:
      project_analysis.save()
    except Exception as e:
      logger.error(e)
      message = e
      return HttpResponse(content="Error: {0}".format(message),status=500)

  return HttpResponse(content="Success",status=200)

def fill_project_analysis_script(id):
  logger.debug("Filling project analysis script")
  project_analysis = ProjectAnalysis.objects.get(pk=id)
  project_criteria = project_analysis.project_analysis_criteria
  analysis_script = project_analysis.analysis_script

  script_template = Template(analysis_script.file.read())
  criteria_container = json.loads(project_criteria.criteria)
  criteria_object = criteria_container['criteria']

  #add the canonical values that are always available
  criteria_object['analysis_dir'] = os.path.join(constants.PROJECT_ANALYSES,str(project_analysis.id))
  criteria_object['project_analysis_id'] = id
  criteria_object['project_id'] = project_analysis.project.id

  if('odbc_name' not in criteria_object):
    criteria_object['odbc_name'] = settings.DEFAULT_ODBC_NAME

  filled_script = script_template.render(Context(criteria_object))
  return filled_script

def filled_project_analysis_script(request,id):
  filled_script = fill_project_analysis_script(id)
  response = HttpResponse(filled_script, content_type='text/plain')
  response['Content-Disposition'] = 'attachment; filename="project_analysis_filled_script_{0}.R"'.format(id)
  return response

def update_project_analysis_criteria(request,id):
    logger.debug(id)
    criteria_object = ProjectAnalysisCriteria.objects.get(pk=id)

    value = request.POST['criteria-json-value']
    criteria_object.criteria = value
    criteria_object.save()
    return HttpResponse(value)

def unlock_project_analysis(request,id):
  if request.method == 'POST':
    project_analysis = ProjectAnalysis.objects.get(pk=id)
    try:
      if project_analysis.owner == request.user:
        project_analysis.status = constants.STATUS_ACTIVE
        project_analysis.save()
      else:
        raise Exception("Only the owner can unlock a record")
    except Exception as e:
      message = e
      return HttpResponse(content="Error: {0}".format(message),status=500)
    return HttpResponse(content="Success: Analysis Locked",status=200)
  else:
    return HttpResponse(content="Not Supported",status=500)

def lock_project_analysis(request,id):
  if request.method == 'POST':
    project_analysis = ProjectAnalysis.objects.get(pk=id)
    try:
      project_analysis.status = constants.STATUS_LOCKED
      project_analysis.save()
    except Exception as e:
      message = e
      return HttpResponse(content="Error: {0}".format(message),status=500)
    return HttpResponse(content="Success: Analysis Locked",status=200)
  else:
    return HttpResponse(content="Not Supported",status=500)

def run_filled_project_analysis_script(request,id):
  logger.debug("Running filled script")
  project_analysis = ProjectAnalysis.objects.get(pk=id)


  project_analysis.delete_output_files()

  if(project_analysis.status == constants.STATUS_NEW):
    project_analysis.status = constants.STATUS_ACTIVE
  elif(project_analysis.status == constants.STATUS_LOCKED):
    raise Exception("Analysis is locked. Unlock to re-run")

  logger.debug("Switching to analysis dir: {0}".format(project_analysis.get_analysis_dir()))
  robjects.r("setwd(\"{0}\")".format(project_analysis.get_analysis_dir()))

  filled_script = fill_project_analysis_script(id)
  try:
    res = robjects.r(filled_script)
    logger.debug(res)
  except Exception as e:
    message = e
    logger.debug("Switching to app dir: {0}".format(settings.BASE_DIR))
    robjects.r("setwd(\"{0}\")".format(settings.BASE_DIR))
    return HttpResponse(content="Error: {0}".format(message),status=500)


  logger.debug("Switching to app dir: {0}".format(settings.BASE_DIR))
  robjects.r("setwd(\"{0}\")".format(settings.BASE_DIR))
  response = HttpResponse(res, content_type='text/plain')
  return response

def project_analysis_output_files(request,id):
  project_analysis = ProjectAnalysis.objects.get(pk=id)
  absolute_directory_path = os.path.join(settings.BASE_DIR,project_analysis.get_analysis_dir())
  analysis_files = []
  for file in os.listdir(absolute_directory_path):
     name, extension = os.path.splitext(file)
     analysis_files.append(
         {
             'filename':file,
             'extension':extension.lower(),
             'url': project_analysis.get_analysis_dir_url() + "/" + file
         }
     )
  logger.debug(json.dumps(analysis_files))
  data = {
    'recordsTotal':0,
    'recordsFiltered':0,
    'data':json.JSONDecoder().decode(json.dumps(analysis_files))
  }
  return HttpResponse(json.dumps(data), content_type='application/json')

def project_analysis_handler(request,id):
  if request.method == 'DELETE':
    return project_analysis_delete(id)
  else:
    return HttpResponse(content="Unsupported operation",status=500)

@transaction.atomic
def project_analysis_delete(id):
  project_analysis = ProjectAnalysis.objects.get(pk=id)
  logger.debug("Delete project_analysis ID: {0}".format(str(id)))
  try:
    project_analysis.delete()
  except Exception as e:
    message="Failed to delete the project_analysis: {0}".format(e.message)
    logger.error(message)
    return HttpResponse(content=message,status=500)

  return HttpResponse(content="Success",status=200)

def list_project_analyses(request):
  serialized_project_analyses = serializers.serialize(
    'json',
    ProjectAnalysis.objects.all(),
    indent=4,
    relations='created_by,project'
  )

  data = {
    'recordsTotal':ProjectAnalysis.objects.all().count(),
    'recordsFiltered':ProjectAnalysis.objects.all().count(),
    'data':json.JSONDecoder().decode(serialized_project_analyses)
  }
  return HttpResponse(json.dumps(data), content_type='application/json')

def output_file_delete(request,id):
  if request.method == 'POST':
    project_analysis = ProjectAnalysis.objects.get(pk=id)
    file_name = request.POST['file_name']
    logger.debug("Delete output file for: {0}".format(project_analysis))
    file_to_delete =  os.path.join(project_analysis.get_analysis_dir(),file_name)
    logger.debug("Will also remove the following outputfile: {0}".format(file_to_delete))

    try:
      os.remove(file_to_delete)
      return HttpResponse(content="Success",status=200)
    except Exception as e:
      logger.error(e)
      return HttpResponse(content="Failed to delete the file: {0}".format(e),status=500)
  else:
    return HttpResponse(content="Not Supported",status=500)

def zip_project_analysis_output(request,id):


    project_analysis = ProjectAnalysis.objects.get(pk=id)

    analysis_dir = project_analysis.get_analysis_dir()

    zipfile_name_base = "project_analysis_{0}".format(project_analysis.id)
    zipfile_name = "{0}.zip".format(zipfile_name_base)
    string_io = io.StringIO()
    zip_handle = zipfile.ZipFile(string_io, "w")
    utils.zipdir(analysis_dir,zip_handle)

    # Must close zip for all contents to be written
    zip_handle.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(string_io.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zipfile_name

    return resp
