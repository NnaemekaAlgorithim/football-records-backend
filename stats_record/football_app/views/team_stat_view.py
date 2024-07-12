from ..models import TeamStats
from ..serializers import TeamStatsSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class TeamStatsListCreateView(BaseListCreateView):
    queryset = TeamStats.objects.all()
    serializer_class = TeamStatsSerializer

class TeamStatsDetailView(BaseRetrieveUpdateDestroyView):
    queryset = TeamStats.objects.all()
    serializer_class = TeamStatsSerializer