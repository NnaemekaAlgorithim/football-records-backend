from rest_framework import serializers
from ..models.player_model import Player
from .base_serializer import BaseModelSerializer

class PlayerSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Player
        fields = '__all__'
