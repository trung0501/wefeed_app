from django.contrib import admin
from .models import Webhook

# Register your models here.
@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('id', 'workspace', 'model', 'event_type', 'endpoint_url', 'created_day')
    list_filter = ('workspace', 'model', 'event_type', 'created_day')
    search_fields = ('endpoint_url', 'workspace__name', 'model')
    ordering = ('-created_day',)