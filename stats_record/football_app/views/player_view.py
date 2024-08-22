from ..models.player_model import Player
from ..serializers.player_serializer import PlayerSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class PlayerListCreateView(BaseListCreateView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
