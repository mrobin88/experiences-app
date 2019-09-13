from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Experience

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

class ExperienceCreate(LoginRequiredMixin, CreateView):
    model = Experience
    fields = ['title', 'description', 'price', 'location', 'hours', 'minutes', 'language']
    template_name = 'experiences/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExperienceDetail(LoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'experiences/show.html'

class ExperienceDelete(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'experiences/confirm_delete.html'
    success_url = '/'