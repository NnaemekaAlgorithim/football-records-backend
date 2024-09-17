from requests import Response
from .permissions import IsSuperAdminOrDenyDelete
from ..models.player_model import Player
from ..serializers.player_serializer import PlayerSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView
from rest_framework import status


class PlayerListCreateView(BaseListCreateView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]


class PlayerDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        # Restrict toggling of `is_subscribed` to superadmins only
        if 'is_subscribed' in data and not request.user.is_superuser:
            return Response(
                {"error": "Only superadmins can toggle the subscription status."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Superadmin can toggle `is_subscribed`
        if request.user.is_superuser and 'is_subscribed' in data:
            instance.is_subscribed = data.get('is_subscribed', instance.is_subscribed)
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
