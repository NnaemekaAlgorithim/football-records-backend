from .permissions import IsSuperAdminOrDenyDelete
from ..models.season_model import Season
from ..serializers.season_serializer import SeasonSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView


class SeasonListCreateView(BaseListCreateView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]


class SeasonDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]
