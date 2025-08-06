from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def home(request):
    # events = Event.objects.filter(is_active=True).order_by('-start_time')[:5] 
    return render(request, 'home.html')


# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user)  
        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'auth/register.html')

# User Login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'auth/login.html')

# User Logout
@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


# Event View 
def event_view(request):
    events = Event.objects.filter(is_active=True).order_by('-start_time')
    return render(request, 'events/events.html', {'events': events})

@login_required(login_url='login')
def eventdetail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required(login_url='login')
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if max attendees limit is reached
        if event.max_attendees > 0:  # If there is a limit
            current_ticket_count = Ticket.objects.filter(event=event).count()
            if current_ticket_count + quantity > event.max_attendees:
                messages.error(request, "Sorry, this event has limited capacity and cannot accommodate your request.")
                return redirect('event_detail', event_id=event.id)
        
        # Create a new order
        order = Order.objects.create(
            user=request.user,
            subtotal=event.ticket_price * quantity,
            total=event.ticket_price * quantity,
            billing_name=request.POST.get('billing_name'),
            billing_email=request.POST.get('billing_email'),
            billing_phone=request.POST.get('billing_phone'),
            billing_address=request.POST.get('billing_address'),
            payment_method=request.POST.get('payment_method', 'credit_card')
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            event=event,
            quantity=quantity,
            unit_price=event.ticket_price
        )
        
        # Create tickets
        for _ in range(quantity):
            Ticket.objects.create(
                user=request.user,
                event=event,
                order=order,
                attendee_name=request.POST.get('attendee_name', request.user.get_full_name()),
                attendee_email=request.POST.get('attendee_email', request.user.email),
                attendee_phone=request.POST.get('attendee_phone', '')
            )
        
        # Update order status
        order.status = 'completed'
        order.save()
        
        messages.success(request, "Ticket purchase successful!")
        return redirect('my_tickets')
        
    context = {
        'event': event,
    }
    return render(request, 'ticket/buy_ticket.html', context)

@login_required(login_url='login')
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-purchased_at')
    
    context = {
        'tickets': tickets
    }
    return render(request, 'ticket/my_tickets.html', context)

@login_required(login_url='login')
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    context = {
        'ticket': ticket
    }
    return render(request, 'ticket/ticket_detail.html', context)



@login_required(login_url='login')
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')

        user_profile.contact_number = contact_number
        user_profile.address = address
        user_profile.save()

        return redirect('user_profile')  

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'auth/profile.html', context)


def ContactUs(request):
    return render(request, 'contact.html')