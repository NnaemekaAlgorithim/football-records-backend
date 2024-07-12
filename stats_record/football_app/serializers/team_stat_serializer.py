from rest_framework import serializers
from ..models import TeamStats

class TeamStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamStats
        fields = '__all__'
