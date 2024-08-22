from ..models.match_model import Match
from ..serializers.match_serializer import MatchSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class MatchListCreateView(BaseListCreateView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class MatchDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer