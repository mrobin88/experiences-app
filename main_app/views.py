from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Experience, Profile, City, Booking, Review
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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

class ExperienceUpdate(UpdateView):
    model = Experience
    fields = '__all__'
    template_name = 'experiences/form.html'

class ExperienceList(ListView):
    model = Experience
    context_object_name = 'experiences'
    template_name = 'experiences/index.html'

class ExperienceDetail(LoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'experiences/show.html'

class ExperienceDelete(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'experiences/confirm_delete.html'
    success_url = '/experiences/'

class ExperienceReview(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'experiences/review.html'

@login_required
def bookingNew(request, exp_id):
    experience = Experience.objects.get(id=exp_id)
    return render(request, 'bookings/new.html', {
        'experience': experience
    })

@login_required
def bookingShow(request, exp_id, bkng_id):
    experience = Experience.objects.get(id=exp_id)
    booking = Booking.objects.get(id=bkng_id)
    return render(request, 'bookings/show.html', {
        'experience': experience,
        'booking': booking
    })

@login_required
def bookingCreate(request, exp_id):
    experience = Experience.objects.get(id=exp_id)
    booking = Booking.objects.create(user_id=request.user.id, experience_id=exp_id)
    return redirect('bkng_show', exp_id=exp_id, bkng_id=booking.id)

class BookingDelete(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'bookings/confirm_delete.html'
    success_url = '/experiences/'

class BookingList(LoginRequiredMixin, ListView):
    context_object_name = 'bookings'
    template_name = 'bookings/index.html'
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)