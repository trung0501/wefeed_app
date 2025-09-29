from django.db import models
from apps.workspaces.models import Workspace

# Create your models here.
class Webhook(models.Model):
    EVENT_CHOICES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    MODEL_CHOICES = [
        ('project', 'Project'),
        ('comment', 'Comment'),
        ('user', 'User'),
    ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='webhooks')
    endpoint_url = models.TextField()
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    model = models.CharField(max_length=20, choices=MODEL_CHOICES)
    created_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'webhooks'  

    def __str__(self):
        return f"{self.event_type.upper()} webhook for {self.model} in workspace {self.workspace.name}"