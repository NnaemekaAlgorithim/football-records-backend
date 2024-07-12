from ..models import Team
from ..serializers import TeamSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class TeamListCreateView(BaseListCreateView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer