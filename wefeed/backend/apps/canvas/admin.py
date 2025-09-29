from django.contrib import admin
from .models import Canvas

# Register your models here.
@admin.register(Canvas)
class CanvasAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'iframe_url', 'created_day', 'updated_day')
    list_filter = ('created_day', 'updated_day',)
    search_fields = ('project__id', 'iframe_url')
    ordering = ('-updated_day',)

    def project_id(self, obj):
        return obj.project.id
    project_id.short_description = 'Project ID'