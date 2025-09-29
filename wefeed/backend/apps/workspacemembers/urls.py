from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    WorkspaceMemberListCreateView,
    WorkspaceMemberRoleUpdateView,
    WorkspaceMemberDeleteView
)

# from .views import WorkspaceMemberViewSet

# router = DefaultRouter()
# router.register(r'', WorkspaceMemberViewSet, basename='workspacemember')

# urlpatterns = router.urls

urlpatterns = [
    path('workspaces/<int:id>/members', WorkspaceMemberListCreateView.as_view(), name='workspace-members'),
    path('workspaces/<int:id>/members/<int:userId>/role', WorkspaceMemberRoleUpdateView.as_view(), name='workspace-member-role'),
    path('workspaces/<int:id>/members/<int:userId>', WorkspaceMemberDeleteView.as_view(), name='workspace-member-delete'),
]