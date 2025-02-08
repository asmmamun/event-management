from django.shortcuts import render, redirect
from events.models import Category, Event, Participant
from events.forms import CategoryForm, EventForm, ParticipantForm
from django.contrib import messages
from django.db.models import Count, Sum
from datetime import date
from django.urls import reverse


def org_dashboard(request):
    today = date.today()
    
    events = Event.objects.select_related("category").prefetch_related("participants").all()
    total_events = events.count()
    upcoming_events = events.filter(date__gte=today).count()
    past_events = events.filter(date__lt=today).count()
    today_events_count = events.filter(date=today).count()
    events_today = events.filter(date=today)
    
    total_unique_participants = Participant.objects.count()
    total_participants = Participant.objects.aggregate(total=Count('events'))
    categories = Category.objects.all()
    
    # Total participant count in events
    total_participants_filter = events.annotate(participant_count=Count('participants')).aggregate(total=Sum('participant_count'))['total'] or 0

    # Filters
    category_filter = request.GET.get("category")   
    if category_filter:
        events = events.filter(category__id=category_filter)

    event_filter = request.GET.get('filter')
    if event_filter == "upcoming":
        events = events.filter(date__gte=today)
    elif event_filter == "past":
        events = events.filter(date__lt=today)

    # Date range filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    # Prepare the participant names for each event
    # event_participants_names = {
    #     event.id: [participant.name for participant in event.participants.all()]
    #     for event in events_today
    # }

    context = {
        "today":today,
        "total_participants": total_participants,
        "total_unique_participants": total_unique_participants,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "today_events_count": today_events_count,
        "events": events,
        "events_today": events_today,
        "categories": categories,
        "total_participants_filter": total_participants_filter,

    }
    return render(request, "dashboard/org_dashboard.html", context)



def user_dashboard(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'dashboard/user_dashboard.html', context)


# Event CRUD Operations
def event_create(request):
    today = date.today()
    
    # Fetch categories for filtering
    categories = Category.objects.all()

    # Filter events based on category
    category_filter = request.GET.get("category")
    if category_filter:
        events = Event.objects.filter(category__id=category_filter).select_related("category").prefetch_related("participants")
    else:
        events = Event.objects.all().select_related("category").prefetch_related("participants")

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    # Fetch today's events
    events_today = Event.objects.filter(date=today).select_related("category").prefetch_related("participants")
    total_participants = Event.objects.aggregate(total=Count('participants'))['total'] or 0

    # Handle the form creation
    event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully.")
            return redirect('event_list')  # Redirect to event list after successful creation

    context = {
        'event_form': event_form,
        'events': events,
        'events_today': events_today,
        'total_participants': total_participants,
        'categories': categories,
        'category_filter': category_filter,
    }
    return render(request, 'event_form.html', context)



def event_list(request):
    today = date.today()
    
    # Fetch today's events
    events_today = Event.objects.filter(date=today).select_related("category").prefetch_related("participants")
    events = Event.objects.select_related("category").prefetch_related("participants").all()
    total_participants = Participant.objects.aggregate(total=Count('events'))
    categories = Category.objects.all()
    
    category_filter = request.GET.get("category")    
    if category_filter:
        events = events.filter(category__id=category_filter)

    # Filter by predefined event type
    event_filter = request.GET.get('filter')
    if event_filter == "upcoming":
        events = events.filter(date__gte=today)
    elif event_filter == "past":
        events = events.filter(date__lt=today)

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    context = {"events": events, "events_today": events_today, "total_participants": total_participants, "categories": categories}
    return render(request, "event_list.html", context)


def event_update(request, id):
    event = Event.objects.get(id=id)
    event_form = EventForm(instance=event)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully.")
            return redirect(reverse('event_update', args=[id])) 
    
    context = {'event_form': event_form}
    return render(request, 'event_form.html', context)


def event_delete(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('org_dashboard')
    else:
        messages.error(request, 'Something went wrong')
    return redirect('org_dashboard')



def view_event(request):
    events = Event.objects.annotate(
        num_participant=Count('participants')).order_by('name')
    return render(request, "event_form.html", {"events": events})




# Participant CRUD operations
def participant_create(request):
    participants = Participant.objects.all()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant Created Successfully.") 
            return redirect('participant_create') 
    else:
        form = ParticipantForm()
    context = {'participants': participants, 'form': form}
    return render(request, 'participant_form.html', context)


# Update Participant
def participant_update(request, id):
    participant = Participant.objects.get(id=id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant Updated Successfully.")  
            return redirect('participant_create')
    else:
        form = ParticipantForm(instance=participant)

    context = {'form': form, 'participant': participant}
    return render(request, 'participant_form.html', context)

# Delete Participant
def participant_delete(request, id):
    participant = Participant.objects.get(id=id)
    participant.delete()
    messages.success(request, "Participant Deleted Successfully.")  
    return redirect('participant_create')

def view_participant(request):
    events = Participant.objects.annotate(
        num_event=Count('events')).order_by('num_event')
    return render(request, "participant_create.html", {"events": events})


# Category CRUD operations
def category_create(request):
    categories=Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully.")   
            return redirect('category_create')
    else:
        form = CategoryForm()
    context = {'categories': categories, 'form': form}
    return render(request, 'category_form.html', context)


def category_update(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully.")
            return redirect('category_create')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})


def category_delete(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, "Category Deleted Successfully.")  
    return redirect('category_create')
