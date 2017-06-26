from django.conf.urls import url, include

from core.views import views

from core.views import sample

urlpatterns = [

    url(
        r'^$',
        sample.samples,
        name='samples-list'
    ),
    url(
        r'^json$',
        sample.list_samples_as_json,
        name='samples-json'
    ),

    url(
        r'^create',
        sample.SampleCreateView.as_view(template_name="core/samples/create.html"),
        name='samples-create'
    ),

    url(
        r'^(?P<id>[-_\w]+)/delete$',
        sample.sample_delete,
        name='samples-delete'
    ),
    url(
        r'^(?P<pk>[-_\w]+)/edit$',
        sample.SampleUpdateView.as_view(template_name="core/samples/edit.html"),
        name='samples-edit'
    ),
    url(
        r'^(?P<id>[-_\w]+)/lock$',
        sample.lock_sample,
        name='samples-lock'
    ),
    url(
        r'^(?P<id>[-_\w]+)/unlock$',
        sample.unlock_sample,
        name='sample-unlock'
    ),
    url(
        r'^(?P<pk>[-_\w]+)/json$',
        sample.sample_detail_as_json,
        name='samples-detail-json'
    ),

    url(
        r'^(?P<pk>[-_\w]+)$',
        sample.SampleDetailView.as_view(template_name="core/samples/detail.html"),
        name='samples-detail'
    ),

]
