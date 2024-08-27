from .permissions import IsSuperAdminOrDenyDelete
from rest_framework import status
from requests import Response
from ..models import Team
from ..serializers import TeamSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class TeamListCreateView(BaseListCreateView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]

    def delete(self, request, *args, **kwargs):
        # Only superadmins can delete
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superadmins can delete a team."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)