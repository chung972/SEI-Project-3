from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events_detail', kwargs={'event_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"