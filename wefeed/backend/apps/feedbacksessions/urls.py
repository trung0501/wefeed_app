# from rest_framework.routers import DefaultRouter
# from .views import FeedbackSessionViewSet

# router = DefaultRouter()
# router.register(r'', FeedbackSessionViewSet, basename='feedbacksession')

# urlpatterns = router.urls

from django.urls import path
from .views import (
    FeedbackSessionCreateView,
    FeedbackSessionDetailView,
    ProjectFeedbackSessionListView
)

urlpatterns = [
    path('sessions/', FeedbackSessionCreateView.as_view(), name='session-create'),  
    path('sessions/<int:id>', FeedbackSessionDetailView.as_view(), name='session-detail'),
    path('projects/<int:id>/sessions/', ProjectFeedbackSessionListView.as_view(), name='project-sessions'),   
]
