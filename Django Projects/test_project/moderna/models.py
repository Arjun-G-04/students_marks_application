from django.db import models

# Create your models here.

class Card(models.Model):
    title = models.CharField(max_length=30)
    desc = models.TextField()
    img = models.ImageField(upload_to='pics')