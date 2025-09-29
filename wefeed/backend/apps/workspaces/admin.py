from django.contrib import admin
from .models import Workspace

# Register your models here.
@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner_id', 'subscription_plan', 'created_day')
    list_filter = ('subscription_plan', 'created_day')
    search_fields = ('name', 'description', 'owner__id')
    ordering = ('-created_day',)

    def owner_id(self, obj):
        return obj.owner.id
    owner_id.short_description = 'Owner Id'