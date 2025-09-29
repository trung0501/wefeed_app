from django.db import models
from apps.users.models import User 

# Create your models here.
class Workspace(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    subscription_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    created_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workspaces'

    def __str__(self):
        return self.name