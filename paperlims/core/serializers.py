from rest_framework import serializers

from core.models import Experiment
from core.models import Project
from core.models import SiteMessage

################################
#
# ALL fields model serializers
#
################################
class SiteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteMessage
        fields = ('__all__')


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('__all__')
        depth = 3

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('__all__')
        depth = 3


################################
#
# SUBSET fields model serializers
#
################################
