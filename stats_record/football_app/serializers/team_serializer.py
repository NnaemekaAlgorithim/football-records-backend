from ..models import Team
from .base_serializer import BaseModelSerializer

class TeamSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Team
        fields = '__all__'
