from django.contrib import admin
from .models import WorkspaceMember

# Register your models here.
@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'workspace_id', 'role', 'joined_day')
    list_filter = ('role', 'joined_day',)
    search_fields = ('user__id', 'workspace__id')
    ordering = ('-joined_day',)

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

    def workspace_id(self, obj):
        return obj.workspace.id
    workspace_id.short_description = 'Workspace ID'