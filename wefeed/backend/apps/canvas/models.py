from django.db import models
from apps.projects.models import Project

# Create your models here.
class Canvas(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='canvases')
    iframe_url = models.TextField(null=True, blank=True)
    created_day = models.DateTimeField(auto_now_add=True)
    updated_day = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'canvas'

    def __str__(self):
        return f"Canvas for {self.project.name}"