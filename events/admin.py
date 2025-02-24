from django.contrib import admin
from .models import Event, Ticket, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'location', 'start_date', 'end_date')
    search_fields = ('title', 'event_type', 'location')
    list_filter = ('event_type', 'start_date')
    ordering = ('start_date',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'ticket_name', 'ticket_type', 'quantity', 'price', 'sale_start', 'sale_end')
    search_fields = ('ticket_name', 'ticket_type', 'event__title')
    list_filter = ('ticket_type', 'sale_start')
    ordering = ('sale_start',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket', 'quantity', 'total_price', 'created_at', 'booking_id')
    search_fields = ('user__username', 'event__title', 'ticket__ticket_name', 'booking_id')
    list_filter = ('event', 'created_at')
    ordering = ('-created_at',)