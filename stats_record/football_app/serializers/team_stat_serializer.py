from ..models import TeamStats
from .base_serializer import BaseModelSerializer

class TeamStatsSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = TeamStats
        fields = '__all__'
