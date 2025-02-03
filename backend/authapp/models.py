from django.db import models
from django.contrib.auth.models import User

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.username} - {'Blacklisted' if self.blacklisted else 'Active'}"
