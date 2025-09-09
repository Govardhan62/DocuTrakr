from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    converted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ FIXED
    
    def __str__(self):
        return self.file.name
