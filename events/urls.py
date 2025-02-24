from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='event_creation'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('select_tickets/<int:event_id>/', views.select_tickets, name='select_tickets'),
    path('confirm-tickets/<int:event_id>/', views.confirm_tickets, name='confirm_tickets'),
    path("payment/<int:event_id>/", views.payment_view, name="payment"),  # Fix: Pass event_id here
    path("payment-success/", views.payment_success, name="payment_success"),
    path('events/payment/cancel/<int:event_id>/', views.cancel_payment, name="cancel_payment"),
    path('bookings/', views.bookings, name='bookings'),
    path('cancel/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path("save_attendee_data/", views.save_attendee_data, name="save_attendee_data"),
]
