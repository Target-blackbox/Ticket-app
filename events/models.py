from django.db import models
import random
import string
from django.contrib.auth.models import User
from users.models import Manager  # Assuming you are using Django's built-in User model

def generate_ticket_id():
    """Generate a random ticket ID consisting of digits."""
    return ''.join(random.choices(string.digits, k=10))  # Generates a random 10-digit number

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=100)  # e.g., Normal, VIP
    ticket_name = models.CharField(max_length=100)  # Name of the ticket
    quantity = models.PositiveIntegerField()  # Number of tickets available
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per ticket
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Additional fee
    sale_start = models.DateTimeField()  # Tickets available from
    sale_end = models.DateTimeField()  # Tickets available until
    min_purchase = models.PositiveIntegerField()  # Minimum ticket purchase
    max_purchase = models.PositiveIntegerField()  # Maximum ticket purchase
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_name} - {self.event.title}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who made the booking
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to the event
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)  # Link to the ticket type
    quantity = models.PositiveIntegerField()  # Number of tickets booked
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price for the booking
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the booking was created
    booking_id = models.CharField(max_length=10, unique=True, default=generate_ticket_id)  # Unique booking ID
    ticket_type = models.CharField(max_length=100, default='none')  # Type of the ticket (e.g., VIP, Regular)
    ticket_name = models.CharField(max_length=100, default='none')  # Name of the ticket

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.quantity} tickets - Booking ID: {self.booking_id}"

# Create your models here.
