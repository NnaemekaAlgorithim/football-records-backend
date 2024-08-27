from .permissions import IsSuperAdminOrDenyDelete
from ..models import CustomUser
from ..serializers import UserSerializer
from .base_view import BaseListCreateView, BaseRetrieveUpdateDestroyView

class UserListCreateView(BaseListCreateView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]

class UserDetailView(BaseRetrieveUpdateDestroyView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdminOrDenyDelete]
