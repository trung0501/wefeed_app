from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'auth_type', 'two_stept_auth', 'created_day')
    list_filter = ('auth_type', 'two_stept_auth', 'created_day')
    search_fields = ('email', 'name')
    ordering = ('-created_day',)