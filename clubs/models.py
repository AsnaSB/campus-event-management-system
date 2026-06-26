from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Club(models.Model):
    user=models.OneToOneField(User,on_delete=models.PROTECT,related_name="club_account")
    name=models.CharField(max_length=100)
    short_name=models.CharField(max_length=30,unique=True)
    description=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =["name"]
    
    def __str__(self):
        return self.short_name

