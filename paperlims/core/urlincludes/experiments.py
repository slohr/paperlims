from django.conf.urls import url, include

from core.views import views

from core.views import experiment

urlpatterns = [

    url(
        r'^$',
        experiment.experiments,
        name='experiments-list'
    ),
    url(
        r'^json$',
        experiment.list_experiments_as_json,
        name='experiments-json'
    ),

    url(
        r'^(?P<id>[-_\w]+)/delete$',
        experiment.experiment_delete,
        name='experiments-delete'
    ),
    url(
        r'^(?P<pk>[-_\w]+)/edit$',
        experiment.ExperimentUpdateView.as_view(template_name="core/experiments/edit.html"),
        name='experiments-edit'
    ),
    url(
        r'^(?P<id>[-_\w]+)/lock$',
        experiment.lock_experiment,
        name='experiments-lock'
    ),
    url(
        r'^(?P<id>[-_\w]+)/unlock$',
        experiment.unlock_experiment,
        name='experiment-unlock'
    ),
    url(
        r'^(?P<pk>[-_\w]+)/json$',
        experiment.experiment_detail_as_json,
        name='experiments-detail-json'
    ),

    url(
        r'^(?P<pk>[-_\w]+)$',
        experiment.ExperimentDetailView.as_view(template_name="core/experiments/detail.html"),
        name='experiments-detail'
    ),

]
