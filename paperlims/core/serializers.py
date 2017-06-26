from rest_framework import serializers

from core.models import Experiment
from core.models import Project
from core.models import SiteMessage
from core.models import Sample
from core.models import DataFile

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


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ('__all__')
        depth = 5


class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ('__all__')
        depth = 5

################################
#
# SUBSET fields model serializers
#
################################
