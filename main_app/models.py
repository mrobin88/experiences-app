from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from PIL import Image
from datetime import date
from languages.fields import LanguageField

#----- PROFILE ------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile",  verbose_name=_("user"), on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.id})"

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# ---- CITY ------
class City(models.Model):
    location = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.location} ({self.id})'

# ---- EXPERIENCE ------
class Experience(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    location = models.CharField(max_length=100)
    hours = models.IntegerField(validators=[MaxValueValidator(24)])
    minutes = models.IntegerField(choices=(
            (0, '00'),
            (15, '15'),
            (30, '30'),
            (45, '45'),
        ),
        default=0
    )
    language = LanguageField(default='en')
    # user in this case is equal to the experience host
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('exp_detail', kwargs = { 'pk': self.id })

# ---- BOOKING ------
class Booking(models.Model):
    # user in this case is equal to the experience participant
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    date = models.DateField('booking date')

    def __str__(self):
        return f'Booking ({self.id}) by {self.user} ({self.user_id}) for Experience ({self.experience_id})'

    def get_absolute_url(self):
        return reverse('bkng_show', kwargs = { 'exp_id': self.experience_id, 'bkng_id': self.id })
    
    class Meta:
        ordering = ['date']


# ---- REVIEW ------
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1) , MaxValueValidator(5)])
    comment = models.TextField(max_length=250)

    def __str__(self):
        return f'Review by {self.user} ({self.user_id}) for Experience ({self.experience_id})'

