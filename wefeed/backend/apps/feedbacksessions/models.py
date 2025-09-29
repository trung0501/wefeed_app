from django.db import models
from apps.users.models import User 
from apps.canvas.models import Canvas

# Create your models here.
class FeedbackSession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('canvas', 'Canvas'),
        ('shoot', 'Shoot'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_sessions', null=True, blank=True)
    canvas = models.ForeignKey(Canvas, on_delete=models.CASCADE, related_name='feedback_sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='canvas')
    created_day = models.DateTimeField(auto_now_add=True)
    updated_day = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feedbacksessions'

    def __str__(self):
        return f"{self.session_type.capitalize()} session for canvas {self.canvas.id}"