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
      project.list_projects,
      name='projects-json'
    ),

]
