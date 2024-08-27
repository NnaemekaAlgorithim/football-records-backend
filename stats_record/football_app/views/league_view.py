from .permissions import IsSuperAdminOrReadOnly
from ..models.league_model import League
from ..serializers.league_serializer import LeagueSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView


class LeagueListCreateView(BaseListCreateView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [IsSuperAdminOrReadOnly]


class LeagueDetailView(BaseRetrieveUpdateDestroyView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [IsSuperAdminOrReadOnly]
