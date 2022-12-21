from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.contrib import messages

# from django.core.paginator import Paginator





# Create My Events Page
def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		events = Event.objects.filter(attendees=me)
		return render(request, 
			'event/my_events.html', {
				"events":events
			})

	else:
		messages.success(request, ("You Aren't Authorized To View This Page"))
		return redirect('home')


# generate csv file venue list
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv' 

    writer = csv.writer(response)

    # designate the model
    venues = Venue.objects.all()


    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.website, venue.email])

    return response

# generate text file venue list
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt' 
    # designate the model
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.website}\n{venue.email}\n\n\n')

    # lines = ["This is line 1\n",
    # "This is line 2\n",
    # "This is line 3\n"]

    #write to text field
    response.writelines(lines)
    return response


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!!"))
        return redirect('list_events')      
    else:
            messages.success(request, ("You Aren't Authorized To Delete This Event!"))
    return redirect('list_events')





def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list_events')
        
    return render(request, 'event/update_event.html',
    {'event':event, 'form':form})

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                    form.save()
                    return  HttpResponseRedirect('/add_event?submitted=True')   
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                #form.save()
                event = form.save(commit=False)
                event.manager = request.user # logged in user
                event.save()
                return  HttpResponseRedirect('/add_event?submitted=True')   
    else:
        # Just Going To The Page, Not Submitting 
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'event/add_event.html', {'form':form, 'submitted':submitted})




def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
        
    return render(request, 'event/update_venue.html',
    {'venue':venue, 'form':form})


def search_venues(request):
    if request.method == "POST":
         searched = request.POST.get('searched')
         venues = Venue.objects.filter(name__contains=searched)

         return render(request, 'event/search_venues.html', {'searched':searched,
		'venues':venues})
    else:
         return render(request, 'event/search_venues.html', {})


def search_events(request):
    if request.method == "POST":
         searched = request.POST.get('searched')
         events = Event.objects.filter(name__contains=searched)

         return render(request, 'event/search_events.html', {'searched':searched,
		'events':events})
    else:
         return render(request, 'event/search_events.html', {})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'event/show_venue.html',
    {'venue':venue, 'venue_owner': venue_owner})


def list_venues(request):
    # Venue_list = Venue.objects.all().ordered_by
    Venue_list = Venue.objects.all()

    #  set up pagination
    # p = Paginator(Venue.objects.all(), 2)
    # page = request.GET.get('page')
    # venues  = p.get_page(page)
    
    return render(request, 'event/venue.html',
    {'Venue_list':Venue_list}) # , 'venues':venues
 


def add_Venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user
            venue.save()
            #form.save()
            return HttpResponseRedirect('/add_Venue?submitted=True')
    else:
      form = VenueForm
      if 'sumbitted' in request.GET:
        submitted = True
    return render(request, 'event/add_Venue.html', {'form':form, 'submitted':submitted})



def all_events(request):
    event_list = Event.objects.all().order_by('-name')
    return render(request, 'event/event_list.html',
    {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "yahya"
    month = month.capitalize()
    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number)

    # current date

    now = datetime.now()
    current_year = now.year

    event_list = Event.objects.filter(
        date__year = year,
        date__month = month_number
        )

    # get current time
    time = now.strftime('%H:%M')

    return render(request, 'event/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        "event_list": event_list,


    })
