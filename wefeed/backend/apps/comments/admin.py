from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'session_id', 'position_x', 'position_y', 'short_content', 
        'tag_user', 'created_day', 'updated_day'
    )
    list_filter = ('created_day', 'updated_day', 'session')
    search_fields = ('user__id', 'session__id', 'content')
    ordering = ('-created_day',)

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

    def session_id(self, obj):
        return obj.session.id
    session_id.short_description = 'Session ID'

    def short_content(self, obj):
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'
