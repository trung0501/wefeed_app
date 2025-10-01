# from rest_framework.routers import DefaultRouter
# from .views import CanvasViewSet

# router = DefaultRouter()
# router.register(r'', CanvasViewSet, basename='canvas')

# urlpatterns = router.urls

from django.urls import path
from .views import (
    
    CanvasCreateView, 
    CanvasDetailView
    
)

urlpatterns = [
    path('canvas/', CanvasCreateView.as_view(), name='canvas-create'),
    path('canvas/<int:id>', CanvasDetailView.as_view(), name='canvas-detail'),
]
