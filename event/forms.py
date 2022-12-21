from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# Create a Superuser event form
class EventFormAdmin(ModelForm):
	class Meta: 
		model = Event
		fields = "__all__"    
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'date'}),
			'event': forms.Select(attrs={'class':'form-control', 'placeholder':'Venue'}),
			'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'manager'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'description'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'attendees'}),
		}


# Create a event form
class EventForm(ModelForm):
	class Meta: 
		model = Event
		fields = ('name', 'date', 'event', 'description', 'attendees')  
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'date'}),
			'event': forms.Select(attrs={'class':'form-control', 'placeholder':'Venue'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'description'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'attendees'}),
		}

# Create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = "__all__"    # ('name', 'address',  'phone', 'website', 'email', 'venue_image')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
			'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
			'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
			'website': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Web Address'}),
			'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
		}

        