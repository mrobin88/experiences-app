from django.contrib import admin
from .models import Profile
=======
from .models import City, Experience, Booking, Review

# Register your models here.
admin.site.register(City)
admin.site.register(Experience)
admin.site.register(Booking)
admin.site.register(Review)

# Register your models here.
admin.site.register(Profile)
