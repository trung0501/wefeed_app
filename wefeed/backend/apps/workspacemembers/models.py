from django.db import models
from apps.users.models import User
from apps.workspaces.models import Workspace

# Create your models here.
class WorkspaceMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workspacemembers'

    def __str__(self):
        return f"{self.user.name} in {self.workspace.name} as {self.role}"