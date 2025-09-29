# from rest_framework.routers import DefaultRouter
# from .views import ProjectViewSet

# router = DefaultRouter()
# router.register(r'', ProjectViewSet, basename='project')

# urlpatterns = router.urls

from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView      
)

urlpatterns = [
    path('projects/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/list/', ProjectListView.as_view(), name='project-list'),
]
