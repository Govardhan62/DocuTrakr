from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    file = models.FileField(upload_to='documents/')
    converted_text = models.TextField(blank=True, null=True)
    created_at =models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return self.file.name