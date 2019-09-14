from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('experiences/', views.ExperienceList.as_view(), name='experiences-list'),
    path('experiences/create/', views.ExperienceCreate.as_view(), name='exp_create'),
    path('experiences/<int:pk>/update/', views.ExperienceUpdate.as_view(), name='exp_update'),
    path('experiences/<int:pk>/', views.ExperienceDetail.as_view(), name='exp_detail'),
    path('experiences/<int:pk>/delete/', views.ExperienceDelete.as_view(), name='exp_delete'),
    path('experiences/<int:pk>/review/', views.ExperienceReview.as_view(), name='exp_review'),
    path('experiences/<int:exp_id>/bookings/new/', views.bookingNew, name='bkng_new'),
    path('experiences/<int:exp_id>/bookings/create/', views.bookingCreate, name='bkng_create'),
    path('bookings/', views.BookingList.as_view(), name='bkng_list'),
    path('experiences/<int:exp_id>/bookings/<int:bkng_id>/', views.bookingShow, name='bkng_show'),
    path('bookings/<int:pk>/delete/', views.BookingDelete.as_view(), name='bkng_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)