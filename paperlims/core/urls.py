from django.conf.urls import url, include
from core.views import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(
		r'^projects/',
		include('core.urlincludes.projects')
	),
	url(
		r'^experiments/',
		include('core.urlincludes.experiments')
	),
	url(
		r'^samples/',
		include('core.urlincludes.samples')
	),
	url(
		r'^datafiles/',
		include('core.urlincludes.data_files')
	),

]
