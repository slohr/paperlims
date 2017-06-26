

from django.conf.urls import url, include

from core.views import views

from core.views import data_file

urlpatterns = [

    url(
        r'^$',
        data_file.datafiles,
        name='datafiles-list'
    ),

    url(
        r'^json$',
        data_file.list_data_files_as_json,
        name='datafiles-json'
    ),

    url(
        r'^upload',
        data_file.upload_data_file,
        name='datafiles-upload'
    ),

    url(
        r'^(?P<id>[-_\w]+)/delete$',
        data_file.data_file_delete,
        name='datafiles-delete'
    ),

    url(
        r'^(?P<pk>[-_\w]+)/json$',
        data_file.data_file_detail_as_json,
        name='datafiles-detail-json'
    ),

    url(
        r'^(?P<pk>[-_\w]+)$',
        data_file.DataFileDetailView.as_view(template_name="core/datafiles/detail.html"),
        name='datafiles-detail'
    ),

]
