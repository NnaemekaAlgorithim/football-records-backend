# base_views.py

from rest_framework import generics, permissions
from django.utils import timezone

class ReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access for unauthenticated users.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class BaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user, updated_at=timezone.now())

class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())
