from rest_framework import serializers
from ..models.match_model import Match
from .base_serializer import BaseModelSerializer

class MatchSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Match
        fields = '__all__'
