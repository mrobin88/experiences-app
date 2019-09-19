from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, reverse, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import uuid
import boto3
from .models import Experience, Profile, Booking, Review, Photo
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, BookingForm
import os
from unsplash_search import UnsplashSearch

UNSPLASH_ACCESS_KEY = os.environ['UNSPLASH_ACCESS_KEY']
unsplash = UnsplashSearch(UNSPLASH_ACCESS_KEY)


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-gam'

def home(request):
    return redirect('experiences-list')

#------ SIGNUP ------
def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('experiences-list')
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
            messages.success(request, f'Your account has been created')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    experiences = Experience.objects.filter(user_id=request.user.id)
    for experience in experiences:
        category = experience.category
        try:
            src_data = unsplash.search_photo(category)
            src_url = src_data['img']
            src_auth = src_data['credits']
        except:
            src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
            src_auth = None
        if src_auth == None:
            src_auth = '?'
        experience.src_url = src_url
        experience.src_auth = src_auth

    bookings = Booking.objects.filter(user_id=request.user.id)
    for booking in bookings:
        category = booking.experience.category
        try:
            src_data = unsplash.search_photo(category)
            src_url = src_data['img']
            src_auth = src_data['credits']
        except:
            src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
            src_auth = None
        if src_auth == None:
            src_auth = '?'
        booking.experience.src_url = src_url
        booking.experience.src_auth = src_auth

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'bookings': bookings,
        'experiences': experiences,
    }
    return render(request, 'registration/profile.html', context)

#----- EXPERIENCE ---------
class ExperienceCreate(LoginRequiredMixin, CreateView):
    model = Experience
    fields = ['title', 'category', 'description', 'price', 'hours', 'minutes', 'language', 'city', 'address', 'zipcode',]
    template_name = 'experiences/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExperienceUpdate(LoginRequiredMixin, UpdateView):
    model = Experience
    fields = ['title', 'category', 'description', 'price', 'hours', 'minutes', 'language', 'city', 'address', 'zipcode']
    template_name = 'experiences/form.html'

class ExperienceList(ListView):
    template_name = 'experiences/index.html'
    
    def get_queryset(self):
        experiences = list(Experience.objects.all())
        object_list = []
        for experience in experiences:
            category = experience.category
            try:
                src_data = unsplash.search_photo(category)
                src_url = src_data['img']
                src_auth = src_data['credits']
            except:
                src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
                src_auth = None
            if src_auth == None:
                src_auth = '?'
            experience.src_url = src_url
            experience.src_auth = src_auth
            object_list.append(experience)
        return object_list

class ExperienceDetail(DetailView):
    model = Experience
    template_name = 'experiences/show.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = Booking.objects.filter(experience_id=self.kwargs['pk']).filter(user_id=self.request.user)
        bookings = context["bookings"]
        return context 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = Booking.objects.filter(experience_id=self.kwargs['pk']).filter(user_id=self.request.user)
        experience = Experience.objects.get(id=self.kwargs['pk'])
        category = experience.category
        try:
            src_data = unsplash.search_photo(category)
            src_url = src_data['img']
            src_auth = src_data['credits']
        except:
            src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
            src_auth = None
        if src_auth == None:
            src_auth = '?'
        experience.src_url = src_url
        experience.src_auth = src_auth
        context["experience"] = experience
        return context

class ExperienceDelete(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'experiences/confirm_delete.html'
    success_url = '/experiences/'

#----- BOOKING ---------
@login_required
def bookingNew(request, exp_id):
    experience = Experience.objects.get(id=exp_id)
    booking_form = BookingForm
    return render(request, 'bookings/new.html', {
        'experience': experience,
        'booking_form': booking_form
    })

@login_required
def bookingShow(request, exp_id, bkng_id):
    experience = Experience.objects.get(id=exp_id)
    booking = Booking.objects.get(id=bkng_id)
    category = booking.experience.category
    try:
        src_data = unsplash.search_photo(category)
        src_url = src_data['img']
        src_auth = src_data['credits']
    except:
        src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
        src_auth = None
    if src_auth == None:
        src_auth = '?'
    booking.experience.src_url = src_url
    booking.experience.src_auth = src_auth
    return render(request, 'bookings/show.html', {
        'experience': experience,
        'booking': booking
    })

@login_required
def bookingCreate(request, exp_id):
    form = BookingForm(request.POST)
    if form.is_valid():
        new_booking = form.save(commit=False)
        new_booking.experience_id = exp_id
        new_booking.user_id = request.user.id
        new_booking.save()
    return redirect('bkng_list')

@login_required
def bookingList(request):
    bookings = Booking.objects.filter(user=request.user)
    for booking in bookings:
        category = booking.experience.category
        try:
            src_data = unsplash.search_photo(category)
            src_url = src_data['img']
            src_auth = src_data['credits']
        except:
            src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
            src_auth = None
        if src_auth == None:
            src_auth = '?'
        booking.experience.src_url = src_url
        booking.experience.src_auth = src_auth

    return render(request, 'bookings/index.html', { 'bookings': bookings })

def search(request):
    query = request.GET.get('searchquery')
    results = list(Experience.objects.filter(city__icontains = query))
    results.extend(list(Experience.objects.filter(category__icontains = query)))
    for experience in results:
        category = experience.category
        try:
            src_data = unsplash.search_photo(category)
            src_url = src_data['img']
            src_auth = src_data['credits']
        except:
            src_url = 'https://mdbootstrap.com/img/Photos/Horizontal/Food/full%20page/2.jpg'
            src_auth = None
        if src_auth == None:
            src_auth = '?'
        experience.src_url = src_url
        experience.src_auth = src_auth
    return render_to_response('experiences/results.html', { "experiences": results })

class BookingDelete(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'bookings/confirm_delete.html'
    success_url = '/bookings/'
    

#----- REVIEW ---------
class ExperienceReviewList(ListView):
    context_object_name = 'reviews'
    template_name = 'experiences/reviews.html'
    def get_queryset(self, *args, **kwargs):
        return Review.objects.filter(experience_id=self.kwargs['pk'])

class ExperienceReview(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'experiences/review.html'
    reverse_lazy(ExperienceDetail)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.experience = Experience.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

#----- PHOTO ---------
def add_photo(request, pk):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, experience_id=pk)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('exp_detail', pk=pk)

 
@login_required   
def delete_photo(request, exp_id, photo_id):
    Photo.objects.filter(id=photo_id).delete()

    return redirect('exp_detail', pk=exp_id)

