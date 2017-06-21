from django.conf.urls import url, include
from core.views import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^datafiles/$', views.datafiles, name='datafiles-list'),

	url(r'^datafiles/upload', views.upload_data_file, name='datafiles-upload'),
	url(
		r'^projects/',
		include('core.urlincludes.projects')
	),
	url(
		r'^experiments/',
		include('core.urlincludes.experiments')
	),

]
