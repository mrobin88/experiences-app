from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from datetime import date
from languages.fields import LanguageField

#----- PROFILE ------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile",  verbose_name=_("user"), on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class City(models.Model):
    location = models.CharField(max_length=60)

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
    
    def get_absolute_url(self):
        return reverse('exp_detail', kwargs = { 'pk': self.id })

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

class Review(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1) , MaxValueValidator(5)])
    comment = models.TextField(max_length=250)

    
