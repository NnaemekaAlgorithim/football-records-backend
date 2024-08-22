from rest_framework import serializers
from ..models.season_model import Season
from .base_serializer import BaseModelSerializer

class SeasonSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Season
        fields = '__all__'
