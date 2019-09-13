from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('experiences/create/', views.ExperienceCreate.as_view(), name='exp_create'),
<<<<<<< HEAD
    path('experiences/<int:pk>/update/', views.ExperienceUpdate.as_view(), name='exp_update'),
||||||| merged common ancestors
=======
    path('experiences/<int:pk>/', views.ExperienceDetail.as_view(), name='exp_detail'),
    path('experiences/<int:pk>/delete/', views.ExperienceDelete.as_view(), name='exp_delete'),
>>>>>>> d96c9fa69212628351b132e664142d90e090b058
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)