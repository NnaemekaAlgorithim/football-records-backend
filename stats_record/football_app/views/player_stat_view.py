from .permissions import IsSuperAdminOrDenyDelete
from ..models import PlayerStats
from ..serializers import PlayerStatsSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class PlayerStatsListCreateView(BaseListCreateView):
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]

class PlayerStatsDetailView(BaseRetrieveUpdateDestroyView):
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]
