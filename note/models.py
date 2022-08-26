from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notes')
