from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

class Review(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    rating = models.IntegerField(min=1, max=5)
    comment = models.TextField(max_length=250)

class City:
    location = models.CharField(max_length=60)


    



