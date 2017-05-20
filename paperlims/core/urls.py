from django.conf.urls import url

from core.views import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^projects/$', views.projects, name='projects-list'),
	url(r'^datafiles/$', views.datafiles, name='datafiles-list'),

	url(r'^datafiles/upload', views.upload_data_file, name='datafiles-upload'),
]
