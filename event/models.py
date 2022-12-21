from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name = models.CharField('name',  max_length=120)
    address = models.CharField('address',  max_length=120)
    phone = models.CharField('phone',  max_length=120, blank=True)  # blank=True means the field is not mandatory.
    website = models.URLField('website',  max_length=120, blank=True)
    email = models.EmailField('email',  max_length=120, blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")


    def __str__(self):
        return self.name

class myuser(models.Model):
    first_name = models.CharField('First name',  max_length=120)
    last_name = models.CharField('Last name',  max_length=120)
    # email = models.EmailField('Email',null=True,  max_length=120)
    def __str__(self):
        return self.first_name + ' ' + self.last_name


# create table columns
class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    date = models.DateTimeField()
    # foreinkey connect two tables
    event = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue = models.CharField( max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(myuser, blank=True)
    approved = models.BooleanField('Aprroved', default=False)


# make the name as a url to press on and take me to the whole event
    def __str__(self):
        return self.name


    @property
    def Days_till(self):
        today = date.today()
        days_till = self.date.date() - today
        days_till_stripped = str(days_till).split(",", 1)[0]
        return days_till_stripped
    