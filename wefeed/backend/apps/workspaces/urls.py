from rest_framework.routers import DefaultRouter
from .views import WorkspaceCreateView
from django.urls import path
from .views import (
    WorkspaceCreateView,
    WorkspaceDetailView,
    WorkspaceUpgradeView
)

# from .views import WorkspaceViewSet

# router = DefaultRouter()
# router.register(r'', WorkspaceViewSet, basename='workspace')

# urlpatterns = router.urls

urlpatterns = [
    path('workspaces/', WorkspaceCreateView.as_view(), name='workspace-create'),
    path("workspaces/<int:id>/", WorkspaceDetailView.as_view(), name="workspace-detail"),
    path('workspaces/<int:id>/upgrade', WorkspaceUpgradeView.as_view(), name='workspace-upgrade'),
]