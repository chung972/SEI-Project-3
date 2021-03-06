from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# these two imports below are generic views provided by Django
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# imports to upload images
import uuid
import boto3
# these four imports below are required for all login/out authentication processes
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# import models below
from .models import Profile, Event, Photo, User
# import forms below
from .forms import LoginForm, ExtendedUserCreationForm, ExtendedUserChangeForm, ProfileForm

import random

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'eventcollecting'


def home(request):
    event_ceiling = len(Event.objects.all())
    # we grab the length of ALL the events in the database and set that to be the CEILING VALUE
    event_rand_num = random.randint(0, event_ceiling-1)
    # next, we use random.randint 
    # https://docs.python.org/3/library/random.html
    event = Event.objects.all()[event_rand_num]

    photo = None
    if event.photo_set.all():
        # print(f'{event.photo_set.all()}')
        # eventname = event.name
        # print(f'you in the if; eventname is: {eventname}')
        photo_ceiling = len(event.photo_set.all())
        # print(f'made it past photo_ceiling; photo_ceiling value is: {photo_ceiling}')
        photo_rand_num = random.randint(0, photo_ceiling-1)
        # print(f'photo_rand_num is: {photo_rand_num}')
        photo = event.photo_set.all()[photo_rand_num]
        # print(f'photo: {photo}')


    context = {
        'event': event,
        'photo': photo
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            # This will add the user to the database
            user = form.save()
            # below, we set commit=False so that we don't save profile to the database just yet;
            # we need to attach the user (created above) to it first
            profile = profile_form.save(commit=False)
            # below is where the OneToOneField comes in
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            # This is how we log a user in via code
            login(request, user)
            return redirect('user_detail', user_id=user.id)
        else:
            error_message = 'Invalid sign up - try again'
    else:
        # A bad POST or a GET request, so render signup.html with an empty form
        form = ExtendedUserCreationForm()
        profile_form = ProfileForm()

        context = {
            'form': form,
            'profile_form': profile_form,
            'error_message': error_message
        }
        return render(request, 'registration/signup.html', context)



@login_required
def photo_gal(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'main_app/photo_gallery.html', {'event': event})
    # return render(request, 'photo_gallery', {'event':event})


# full CRUD operations for Profiles (extension of User) below:
@login_required
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, 'auth/user_detail.html', context)


@login_required
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    logout(request)
    return redirect('home')


@login_required
def user_delete_confirm(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, 'auth/user_confirm_delete.html', context)


@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = ExtendedUserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('user_detail', user_id=user.id)
    else:
        form = ExtendedUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'auth/user_form.html/', {'form': form, 'profile_form': profile_form})


# full CRUD operations for Events below:
class EventList(ListView):
    model = Event
# something to note: in the "real" world, an ENTIRE APP is dedicated to
# ONE resource (so, for example, events); that app would handle ALL of the
# crud operations and whatever else that can be possibly be done with Events


class EventDetail(DetailView):
    model = Event


# for EventCreate/Update, they share the same template (event_form.html);
# documentation for further study: https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#listview
# suffice it to say that CBVs are REALLY powerful and convenient
class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'date', 'time', 'location', 'description']
    # success_url = '/events/'
    # TODO: see if you can redirect straight back to the newly created Event


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = '__all__'


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'


@login_required
def add_photo(request, event_id, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, event_id=event_id, user_id=user_id)
            print(f'stored user_id: {user_id}')
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect(f'/events/{event_id}/')


@login_required
def delete_photo(request, event_id):
    logged_in_user_id = request.user.id
    
    if Event.objects.get(id=event_id).photo_set.filter(user_id=logged_in_user_id):
        Event.objects.get(id=event_id).photo_set.filter(user_id=logged_in_user_id).delete()
    return redirect(f'/events/{event_id}/photo_gal')


@login_required
def assoc_user(request, event_id, user_id):
    Event.objects.get(id=event_id).users.add(user_id)
    return redirect(f'/events/{event_id}/')
    # return reverse('events_detail', pk=event_id)
    # pay attention to key that is passed in when redirecting
    # notice we must pass pk and not event_id because of route in urls.py


@login_required
def unassoc_user(request, event_id, user_id):
    logged_in_user_id = request.user.id
    if logged_in_user_id == user_id:
        Event.objects.get(id=event_id).users.remove(user_id)
    return redirect(f'/events/{event_id}/')

    def get_success_url(self):
        return reverse('events_detail', event_id=event_id)


class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/events/'
    # TODO attempt to get success_url to route back to events_detail page
