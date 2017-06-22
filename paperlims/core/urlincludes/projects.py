from django.conf.urls import url, include

from core.views import views

from core.views import project

urlpatterns = [

    url(
        r'^$',
        project.projects,
        name='projects-list'
    ),
    url(
        r'^json$',
        project.list_projects_as_json,
        name='projects-json'
    ),

    url(
        r'^create',
        project.ProjectCreateView.as_view(template_name="core/projects/create.html"),
        name='projects-create'
    ),

    url(
        r'^(?P<id>[-_\w]+)/delete$',
        project.project_delete,
        name='projects-delete'
    ),
    url(
        r'^(?P<pk>[-_\w]+)/edit$',
        project.ProjectUpdateView.as_view(template_name="core/projects/edit.html"),
        name='projects-edit'
    ),
    url(
        r'^(?P<id>[-_\w]+)/lock$',
        project.lock_project,
        name='projects-lock'
    ),
    url(
        r'^(?P<id>[-_\w]+)/unlock$',
        project.unlock_project,
        name='project-unlock'
    ),
    url(
        r'^(?P<pk>[-_\w]+)/json$',
        project.project_detail_as_json,
        name='projects-detail-json'
    ),

    url(
        r'^(?P<pk>[-_\w]+)$',
        project.ProjectDetailView.as_view(template_name="core/projects/detail.html"),
        name='projects-detail'
    ),

]
