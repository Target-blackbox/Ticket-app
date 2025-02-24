from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import CustomRegisterForm, CustomLoginForm, ProfileUpdateForm
from django.contrib.auth import logout
from .models import Manager, UserProfile
from events.models import Booking, Event, Ticket
from django.contrib import messages
from django.utils import timezone
from .utils import generate_otp, send_otp_email
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from django.core.cache import cache
from collections import defaultdict
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Check if input looks like an email
            if '@' in username:
                messages.error(request, "Please enter your username, not email address.")
                return render(request, 'login.html', {'form': form})
            
            # Check if username exists in database
            User = get_user_model()
            try:
                user_exists = User.objects.filter(username=username).exists()
                if not user_exists:
                    messages.error(request, "Username does not exist. Please enter a valid username.")
                    return render(request, 'login.html', {'form': form})
                
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # Check if email already exists
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please use a different email or login.')
                return render(request, 'register.html', {'form': form})
                
            if request.POST.get('is_manager'):
                # Store form data in session
                request.session['user_form_data'] = {
                    'username': form.cleaned_data['username'],
                    'email': email,
                    'password1': form.cleaned_data['password1'],
                }
                # Generate and store OTP
                otp = generate_otp()
                request.session['manager_otp'] = otp
                # Send OTP email
                send_otp_email(email, otp)
                return redirect('verify_otp')
            else:
                # Normal user registration
                user = form.save()
                messages.success(request, f'Account created successfully for {user.username}! Please login to continue.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})

def verify_otp(request):
    if 'user_form_data' not in request.session:
        messages.error(request, 'Registration session expired.')
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('manager_otp')
        
        if entered_otp == stored_otp:
            # Get stored form data
            form_data = request.session['user_form_data']
            
            try:
                # Create user
                form = CustomRegisterForm({
                    'username': form_data['username'],
                    'email': form_data['email'],
                    'password1': form_data['password1'],
                    'password2': form_data['password1'],
                    'is_manager': True
                })
                
                if form.is_valid():
                    user = form.save()
                    # Create manager instance
                    manager = Manager.objects.create(
                        user=user,
                        name=user.username,
                        email=user.email,
                        is_manager=True,
                        created_at=timezone.now()
                    )
                    
                    # Clear only the OTP-related session data
                    if 'manager_otp' in request.session:
                        del request.session['manager_otp']
                    if 'user_form_data' in request.session:
                        del request.session['user_form_data']
                    
                    messages.success(request, 'Registration successful. Please log in.')
                    return redirect('login')
                else:
                    messages.error(request, 'Invalid form data. Please try registering again.')
                    return redirect('register')
                    
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
                return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'verify_otp.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

# Helper function to check if a user is a manager
def is_manager(user):
    return Manager.objects.filter(user=user, is_manager=True).exists()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            # Generate and store OTP
            otp = generate_otp()
            request.session['reset_password_otp'] = otp
            request.session['reset_password_email'] = email
            # Send OTP email
            send_otp_email(email, otp)
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_password_otp')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
    
    return render(request, 'forgot_password.html')

def verify_password_otp(request):
    if 'reset_password_otp' not in request.session:
        messages.error(request, 'Please start the password reset process again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('reset_password_otp')
        
        if entered_otp == stored_otp:
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'verify_password_otp.html')

def reset_password(request):
    if 'reset_password_email' not in request.session:
        messages.error(request, 'Password reset session expired.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'reset_password.html')
        
        try:
            # Update user's password
            User = get_user_model()
            user = User.objects.get(email=request.session['reset_password_email'])
            user.password = make_password(new_password)
            user.save()
            
            # Clear session data
            del request.session['reset_password_otp']
            del request.session['reset_password_email']
            
            messages.success(request, 'Password has been reset successfully. Please login with your new password.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'reset_password.html')  
otp_storage = {}
def profile_view(request):
    # ✅ Ensure a UserProfile exists for the user, preventing duplicate creation
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile)

        if form.is_valid():
            phone_number = form.cleaned_data['phone']
            request.session['profile_update_data'] = request.POST

            otp = generate_otp()
            cache.set(f'otp_{request.user.id}', otp, timeout=300)
            send_otp_email(request.user.email, otp)

            messages.info(request, 'An OTP has been sent to your email for phone number verification. Please verify.')
            return redirect('verify_profile_otp')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=user_profile)

    # Fetch user bookings
    user_bookings = Booking.objects.filter(user=request.user)

    # Group tickets by event and prepare cancellation range
    grouped_bookings = defaultdict(list)
    for booking in user_bookings:
        grouped_bookings[booking.event].append({
            'booking': booking,
            'cancel_range': range(1, booking.quantity + 1)  # Range for cancellation dropdown
        })

    return render(request, 'profile.html', {
        'form': form,
        'user': request.user,
        'user_bookings': dict(grouped_bookings)  # Convert defaultdict to dict
    })

def verify_profile_otp(request):
    if 'profile_update_data' not in request.session:
        messages.error(request, 'Session expired. Please update your profile again.')
        return redirect('profile')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = cache.get(f'otp_{request.user.id}')  # Retrieve OTP from cache
        
        if stored_otp and str(stored_otp) == entered_otp:
            # Retrieve and save profile update data
            profile_data = request.session.pop('profile_update_data', {})
            user_profile = request.user.userprofile
            form = ProfileUpdateForm(profile_data, request.FILES, instance=user_profile)

            if form.is_valid():
                form.save()
                user_profile.save()
                cache.delete(f'otp_{request.user.id}')  # Clear OTP from cache
                
                messages.success(request, 'Your phone number has been verified and your profile has been updated successfully.')
                return redirect('profile')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')


@login_required
def manager_bookings(request):
    user = request.user  # Get the logged-in user

    if user.is_superuser:
        # Admin sees all bookings
        bookings = Booking.objects.all()
        events = Event.objects.all()
    elif hasattr(user, 'manager'):  
        # Check if user is a manager
        events = Event.objects.filter(manager_id=user.manager.id)  # Fetch events created by this manager
        bookings = Booking.objects.filter(event__in=events)  # Fetch bookings for those events
    else:
        # If not an admin or manager, show nothing
        bookings = Booking.objects.none()
        events = Event.objects.none()

    # Apply filters (optional)
    event_name = request.GET.get('event_name', '')
    ticket_type = request.GET.get('ticket_type', '')

    if event_name:
        bookings = bookings.filter(event__title__icontains=event_name)
    if ticket_type:
        bookings = bookings.filter(ticket__ticket_type__icontains=ticket_type)

    return render(request, "manager_bookings.html", {"events": events, "bookings": bookings})