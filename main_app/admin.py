from django.contrib import admin
from .models import Profile, Experience, Booking, Review

# Register your models here.
admin.site.register(Experience)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Profile)
