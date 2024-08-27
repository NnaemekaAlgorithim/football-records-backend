from rest_framework import serializers
from ..models.league_model import League
from .base_serializer import BaseModelSerializer

class LeagueSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = League
        fields = '__all__'
