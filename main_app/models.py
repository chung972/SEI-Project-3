from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliations = models.CharField(max_length=100)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            profile = Profile.objects.create(user=kwargs['instance'])

    # TODO: uncomment the below code once you've set up the correct path; will be necessary
    # when trying to update a profile; also, be mindful of PLURALIZATION when creating the routes
    # def get_absolute_url(self):
    #     return reverse('profile_detail', kwargs={'pk': self.id})


# TODO: decide which model you want to hold the ManyToMany attribute;
# first thought is that Event might be better off holding it; that would place the
# focus on EVENTS, which makes sense thematically; however, if we want to be more
# USER-centric, letting the profile hold the M:M field can also work
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(
        blank=True,
        null=True
    )
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # this method is triggered whenever an instance of this model is created;
        # very useful for whenever we create/update an instance
        return reverse('events_detail', kwargs={'pk': self.id})
        # what reverse() does, essentially, redirect 


class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"

