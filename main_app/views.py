from django.shortcuts import render, redirect
# these two imports below are generic views provided by Django
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# these four imports below are required for all login/out authentication processes 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# import models below
from .models import Profile, Event

# TODO:
#  - we still need to implement login_required and LoginRequiredMixin
#  - also look at steps 3, 8, and 9(10) in the lab
#  - keep in mind WHERE we want to send the user after a successful login/out (change in settings)
#  for specifics, just refer to the lab:
#  https://git.generalassemb.ly/SEI-CC/SEI-CC-2/blob/master/work/w08/d4/02-03-django-authentication/django-authentication.md


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# full CRUD operations for Profiles (extension of User) below:
class ProfileCreate(CreateView):
    model = Profile
    fields = ['email', 'organization']


class ProfileDetail(DetailView):
    model = Profile


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['email', 'organization']


class ProfileDelete(DeleteView):
    model = Profile
    success_url = '/'


# full CRUD operations for Events below:
class EventList(ListView):
    print("you in eventlist")
    model = Event


class EventDetail(DetailView):
    model = Event


# for EventCreate/Update, they share the same template (event_form.html);
# documentation for further study: https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#listview
# suffice it to say that CBVs are REALLY powerful and convenient
class EventCreate(CreateView):
    model = Event
    fields = '__all__'
    success_url = '/events/'
    # TODO: see if you can redirect straight back to the newly created Event


class EventUpdate(UpdateView):
    model = Event
    fields = '__all__'


class EventDelete(DeleteView):
    model = Event
    success_url = '/events/'
