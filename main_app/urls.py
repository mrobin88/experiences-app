from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='registration/logout.html'), name='logout'),

    path('experiences/', views.ExperienceList.as_view(), name='experiences-list'),
    path('experiences/create/', views.ExperienceCreate.as_view(), name='exp_create'),
    path('experiences/<int:pk>/', views.ExperienceDetail.as_view(), name='exp_detail'),
    path('experiences/<int:pk>/update/', views.ExperienceUpdate.as_view(), name='exp_update'),
    path('experiences/<int:pk>/delete/', views.ExperienceDelete.as_view(), name='exp_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)