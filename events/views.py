import logging
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Ticket, Booking
from django.contrib import messages
from django.utils import timezone
from users.models import Manager 
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.db import transaction
import threading
import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Create your views here.

def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Check if all required fields are filled
        if not all([title, description, event_type, location, start_date, end_date]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'event_creation.html')

        try:
            # Get the manager associated with the logged-in user
            manager = Manager.objects.get(user=request.user)

            # Create and save the event with manager attached
            event = Event.objects.create(
                manager=manager,
                title=title,
                description=description,
                event_type=event_type,
                location=location,
                image=image,
                start_date=start_date,
                end_date=end_date
            )

            print("Event saved:", event)  # Debugging line

            # Handle ticket data (if applicable)
            ticket_types = request.POST.getlist('ticket_type[]')
            ticket_names = request.POST.getlist('ticket_name[]')
            ticket_quantities = request.POST.getlist('ticket_quantity[]')
            ticket_prices = request.POST.getlist('ticket_price[]')
            additional_fees = request.POST.getlist('additional_fee[]')
            ticket_sale_starts = request.POST.getlist('ticket_sale_start[]')
            ticket_sale_ends = request.POST.getlist('ticket_sale_end[]')
            min_purchases = request.POST.getlist('min_purchase[]')
            max_purchases = request.POST.getlist('max_purchase[]')

            for i in range(len(ticket_types)):
                Ticket.objects.create(
                    event=event,
                    ticket_type=ticket_types[i],
                    ticket_name=ticket_names[i],
                    quantity=ticket_quantities[i],
                    price=ticket_prices[i],
                    additional_fee=additional_fees[i] if additional_fees[i] else 0,
                    sale_start=ticket_sale_starts[i],
                    sale_end=ticket_sale_ends[i],
                    min_purchase=min_purchases[i],
                    max_purchase=max_purchases[i]
                )

            messages.success(request, "Event created successfully!")
            print("Redirecting to event detail page")  # Debugging line
            return redirect('events:event_detail', event_id=event.id)

        except Manager.DoesNotExist:
            messages.error(request, "You are not authorized to create an event.")
            return redirect('home')  # Redirect to a safe page

        except Exception as e:
            print("Error saving event:", e)  # Debugging line
            messages.error(request, "An error occurred while creating the event. Please try again.")

    return render(request, 'event_creation.html')

def event_list(request):
    current_time = timezone.now()

    # Show events where tickets are on sale OR event hasn't started yet
    events = Event.objects.filter(
        models.Q(tickets__sale_start__lte=current_time, tickets__sale_end__gte=current_time) |  # Tickets on sale
        models.Q(start_date__gte=current_time)  # Event hasn't started yet
    ).distinct()

    return render(request, "event_list.html", {"events": events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def select_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event=event)

    if request.method == "POST":
        selected_tickets = {}
        for ticket in tickets:
            quantity = int(request.POST.get(f"ticket_{ticket.id}", 0))
            if quantity > 0:
                selected_tickets[ticket.id] = quantity
            else:
                messages.error(request, f"Please select a valid quantity.")

        if selected_tickets:
            request.session['selected_tickets'] = selected_tickets
            request.session['event_id'] = event_id  # Store event_id in session
            return redirect('events:confirm_tickets', event_id=event_id)

    return render(request, 'select_tickets.html', {'event': event, 'tickets': tickets})

def confirm_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event=event)
    selected_tickets = request.session.get('selected_tickets', {})

    ticket_details = []
    total_amount = 0

    for ticket in tickets:
        quantity = selected_tickets.get(str(ticket.id), 0)
        if quantity > 0:
            subtotal = (ticket.price + (ticket.additional_fee or 0)) * quantity
            total_amount += subtotal
            ticket_details.append({
                'ticket': ticket,
                'quantity': quantity,
                'subtotal': subtotal
            })

    return render(request, 'confirm_tickets.html', {
        'event': event,
        'ticket_details': ticket_details,
        'total_amount': total_amount
    })

restore_tickets_timer = {}
def payment_view(request, event_id):
    """Handles ticket selection, temporary deduction, and payment."""
    selected_tickets = request.session.get("selected_tickets", {})

    if not selected_tickets:
        return redirect("events:select_tickets", event_id=event_id)

    event = get_object_or_404(Event, id=event_id)
    ticket_details = []
    total_amount = 0

    for ticket_id, quantity in selected_tickets.items():
        ticket = get_object_or_404(Ticket, id=int(ticket_id))
        subtotal = (ticket.price + (ticket.additional_fee or 0)) * quantity
        total_amount += subtotal
        ticket_details.append({"ticket": ticket, "quantity": quantity, "subtotal": subtotal})

        # Temporarily deduct ticket quantity
        ticket.quantity -= quantity
        ticket.save()

    # Restore tickets if payment fails or times out (200 sec)
    def restore_tickets():
        if "selected_tickets" in request.session:
            for item in ticket_details:
                ticket = item["ticket"]
                ticket.quantity += item["quantity"]
                ticket.save()
            request.session.pop("selected_tickets", None)  # Clear session to prevent double restore

    # Cancel existing timer (if any) to avoid multiple restorations
    if event_id in restore_tickets_timer:
        restore_tickets_timer[event_id].cancel()

    restore_tickets_timer[event_id] = threading.Timer(200, restore_tickets)
    restore_tickets_timer[event_id].start()

    return render(request, "payment.html", {"ticket_details": ticket_details, "total_amount": total_amount, "event": event})


logger = logging.getLogger(__name__)  # Create a logger

def payment_success(request):
    """Marks payment as successful and clears session data."""
    selected_tickets = request.session.get("selected_tickets", {})
    event_id = request.session.get("event_id")
    attendee_emails = request.session.get("attendee_emails", [])

    if not selected_tickets:
        return redirect("events:select_tickets", event_id=event_id)

    # Cancel restore_tickets() if payment is successful
    if event_id in restore_tickets_timer:
        restore_tickets_timer[event_id].cancel()
        del restore_tickets_timer[event_id]

    # Create bookings and finalize ticket deduction
    for ticket_id, quantity in selected_tickets.items():
        ticket = get_object_or_404(Ticket, id=int(ticket_id))
        total_price = (ticket.price + (ticket.additional_fee or 0)) * quantity

        Booking.objects.create(
            user=request.user,
            event=ticket.event,
            ticket=ticket,
            quantity=quantity,
            total_price=total_price,
            ticket_type=ticket.ticket_type,
            ticket_name=ticket.ticket_name
        )

    print("Collected Emails:", attendee_emails)  # Debugging Log

    if attendee_emails:
        subject = "Your Ticket Confirmation 🎟"
        from_email = settings.DEFAULT_FROM_EMAIL

        for email in attendee_emails:
            html_message = render_to_string("ticket_email.html", {
                "event_name": ticket.event.title,
                "ticket_name": ticket.ticket_name,
                "ticket_type": ticket.ticket_type,
                "quantity": quantity,
                "total_price": total_price,
                "event_date": ticket.event.start_date.strftime("%d-%m-%Y %I:%M %p"),
                "event_location": ticket.event.location,
            })
            plain_message = strip_tags(html_message)

            try:
                send_mail(subject, plain_message, from_email, [email], html_message=html_message, fail_silently=False)
                print(f"Email sent successfully to {email}")
            except Exception as e:
                print(f"Email sending failed to {email}: {e}")

    # Clear session data
    request.session.pop("selected_tickets", None)
    request.session.pop("event_id", None)
    request.session.pop("attendee_emails", None)

    messages.success(request, "Payment Successful! Your tickets are confirmed.")
    return redirect("events:bookings")

def save_attendee_data(request):
    """Saves attendee emails in session before payment."""
    if request.method == "POST":
        attendee_emails = []

        for key, value in request.POST.items():
            if "attendee_email" in key:
                attendee_emails.append(value)

        print("Collected Emails:", attendee_emails)  # Debugging Log

        if attendee_emails:
            request.session["attendee_emails"] = attendee_emails
            return JsonResponse({"message": "Attendee data saved successfully"}, status=200)
        
        return JsonResponse({"message": "No attendee emails found"}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=400)
    

def cancel_payment(request, event_id):
    """Restores ticket quantity on payment cancellation."""
    event = get_object_or_404(Event, id=event_id)
    selected_tickets = request.session.get("selected_tickets", {})

    if not selected_tickets:
        return redirect("events:event_list")

    for ticket_id, quantity in selected_tickets.items():
        ticket = get_object_or_404(Ticket, id=int(ticket_id))
        ticket.quantity += quantity  # Restore only if not already restored
        ticket.save()

    # Clear session after restoration
    request.session.pop("selected_tickets", None)

    messages.info(request, "Your ticket selection has been canceled.")
    return redirect("events:event_list")

def bookings(request):
    """Displays the user's bookings."""
    user_bookings = Booking.objects.filter(user=request.user)  # Fetch bookings for the logged-in user
    return render(request, 'bookings.html', {'bookings': user_bookings})

def cancel_booking(request, booking_id):
    """Handles user-initiated booking cancellations for partial tickets."""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if request.method == 'POST':
        cancel_count = int(request.POST.get('cancel_count', 0))
        
        if cancel_count > booking.quantity:
            messages.error(request, "Invalid cancellation request.")
            return redirect('profile')

        # Restore only the canceled tickets
        booking.ticket.quantity += cancel_count
        booking.ticket.save()

        # If all tickets are canceled, delete the booking
        if cancel_count == booking.quantity:
            booking.delete()
        else:
            booking.quantity -= cancel_count
            booking.total_price -= cancel_count * booking.ticket.price
            booking.save()

        messages.success(request, f"Successfully canceled {cancel_count} tickets.")
        return redirect('profile')