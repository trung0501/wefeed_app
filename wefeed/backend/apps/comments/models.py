from django.db import models
from apps.feedbacksessions.models import FeedbackSession
from apps.users.models import User

# Create your models here.
class Comment(models.Model):
    session = models.ForeignKey(FeedbackSession, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    tag_user = models.IntegerField(null=True, blank=True)  # Nếu chỉ tag 1 người, dùng IntegerField
    mention_user = models.JSONField(null=True, blank=True)  # Nếu tag nhiều người, dùng JSON
    attachment_url = models.TextField(null=True, blank=True)
    created_day = models.DateTimeField(auto_now_add=True)
    updated_day = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f"{self.user.email} commented on session {self.session.id}"