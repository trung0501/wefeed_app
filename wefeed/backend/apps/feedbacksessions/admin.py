from django.contrib import admin
from .models import FeedbackSession

# Register your models here.
@admin.register(FeedbackSession)
class FeedbackSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'canvas_id', 'session_type', 'created_day', 'updated_day')
    list_filter = ('session_type', 'created_day', 'updated_day')
    search_fields = ('canvas__id',)
    ordering = ('-updated_day',)

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

    def canvas_id(self, obj):
        return obj.canvas.id
    canvas_id.short_description = 'Canvas ID'