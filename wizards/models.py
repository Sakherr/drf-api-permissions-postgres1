from django.db import models
from django.contrib.auth import get_user_model

class Wizard(models.Model):
  creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  name = models.CharField(max_length=64)
  about = models.TextField()
  source = models.CharField(max_length=64)


  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

