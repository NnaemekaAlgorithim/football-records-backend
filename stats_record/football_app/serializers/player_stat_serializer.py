from rest_framework import serializers
from ..models import PlayerStats
from .base_serializer import BaseModelSerializer

class PlayerStatsSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = PlayerStats
        fields = '__all__'
