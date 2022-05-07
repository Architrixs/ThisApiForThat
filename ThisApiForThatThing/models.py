from django.db import models


# Create your models here.
class ApiModel(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    description = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    tryMe = models.CharField(max_length=500)
    auth = models.CharField(max_length=10)
    working = models.BooleanField(default=True)
    _id = models.IntegerField(primary_key=True)
