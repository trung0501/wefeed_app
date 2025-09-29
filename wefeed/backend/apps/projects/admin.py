from django.contrib import admin
from .models import Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'workspace_id', 'type', 'domain_url', 'created_day')
    list_filter = ('type', 'created_day',)
    search_fields = ('name', 'workspace__id', 'domain_url')
    ordering = ('-created_day',)

    def workspace_id(self, obj):
        return obj.workspace.id
    workspace_id.short_description = 'Workspace ID'