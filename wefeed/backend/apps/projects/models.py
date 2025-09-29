from django.db import models
from apps.workspaces.models import Workspace

# Create your models here.
class Project(models.Model):
    TYPE_CHOICES = [
        ('canvas', 'Canvas'),
        ('shoot', 'Shoot'),
    ]

    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='projects')
    domain_url = models.TextField(null=True, blank=True)
    thumbnail_url = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='canvas')
    created_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.name