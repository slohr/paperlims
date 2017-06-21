from django.db import models
from core.models.base import StandardModel
from core import utils
from core import constants
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Project(StandardModel):
    TYPES = utils.self_zip(constants.PROJECT_TYPES)
    STATUSES = utils.self_zip(constants.PROJECT_STATUSES)
    owner = models.ForeignKey(User, related_name='project_owner')
    type = models.CharField(max_length=255, choices=TYPES)
    status = models.CharField(max_length=255, choices=STATUSES, default=constants.STATUS_ACTIVE)

    class Meta:
        app_label = "core"
        db_table = 'project'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects-detail', kwargs={'pk': self.pk})
