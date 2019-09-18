from django.contrib import admin
from .models import Profile, Experience, Booking, Review, Photo

# Register your models here.
admin.site.register(Experience)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Photo)


