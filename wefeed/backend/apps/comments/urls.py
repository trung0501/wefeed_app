# from rest_framework.routers import DefaultRouter
# from .views import CommentViewSet

# router = DefaultRouter()
# router.register(r'', CommentViewSet, basename='comment')

# urlpatterns = router.urls

from django.urls import path
from .views import (
    CommentCreateView,
    CommentDetailView,
    CommentReplyView,
    CommentMentionView,
    SessionCommentListView
)

urlpatterns = [
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:id>/detail/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:id>/reply/', CommentReplyView.as_view(), name='comment-reply'),   
    path('comments/<int:id>/mention/', CommentMentionView.as_view(), name='comment-mention'),
    path('sessions/<int:id>/comments/', SessionCommentListView.as_view(), name='session-comments'),
]
