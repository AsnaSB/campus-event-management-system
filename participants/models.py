from django.db import models

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=10,unique=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"