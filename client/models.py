from django.db import models
from django.contrib.auth.models import User,Group
# Create your models here.
class UserSession(models.Model):
    user = models.ForeignKey(User,related_name='user_session',blank=True,null=True,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255,null=True,blank=True)
    allow_cookie = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.session_key