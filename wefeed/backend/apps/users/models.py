from django.db import models

# Create your models here.
class User(models.Model):
    AUTH_CHOICES = [
        ('default', 'Default'),
        ('google', 'Google'),
        ('sso', 'SSO'),
    ]

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)  # Cho phép null nếu dùng OAuth2
    email = models.EmailField(unique=True)
    # avatar_url = models.TextField(null=True, blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', blank=True, null=True)
    auth_type = models.CharField(max_length=20, choices=AUTH_CHOICES, default='default')
    two_stept_auth = models.BooleanField(default=False)
    created_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name