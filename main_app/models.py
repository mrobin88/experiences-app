from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from languages.fields import LanguageField


class Experience(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    location = models.CharField(max_length=100)
    hours = models.IntegerField(validators=[MaxValueValidator(24)])
    minutes = models.IntegerField(validators=[MaxValueValidator(60)])
    language = LanguageField()
    # user in this case is equal to the experience host
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # add the city property (foreign key) once the city model is set up
    
    def __str__(self):
        return self.title
