from django.contrib.auth import login 
<<<<<<< HEAD
from django.views.generic.edit import CreateView, UpdateView
||||||| merged common ancestors
from django.views.generic.edit import CreateView
=======
from django.views.generic import DetailView
from django.shortcuts import render, redirect
>>>>>>> d96c9fa69212628351b132e664142d90e090b058
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
<<<<<<< HEAD
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Experience, Profile, City, Booking, Review
||||||| merged common ancestors
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Experience
=======
from django.views.generic.edit import CreateView, DeleteView

from .models import Experience
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
>>>>>>> d96c9fa69212628351b132e664142d90e090b058

def home(request):
    return render(request, 'home.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserRegisterForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

#------ PROFILE ------
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)

#----- EXPERIENCE ---------

class ExperienceCreate(LoginRequiredMixin, CreateView):
    model = Experience
    fields = ['title', 'description', 'price', 'location', 'hours', 'minutes', 'language']
    template_name = 'experiences/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
<<<<<<< HEAD

class ExperienceUpdate(UpdateView):
    model = Experience
    fields = '__all__'
    template_name = 'experiences/form.html'
||||||| merged common ancestors
=======

class ExperienceDetail(LoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'experiences/show.html'

class ExperienceDelete(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'experiences/confirm_delete.html'
    success_url = '/'
>>>>>>> d96c9fa69212628351b132e664142d90e090b058
