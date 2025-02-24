import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Manager Registration OTP Verification'
    message = f'Your OTP for manager registration is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)



def send_phone_verification_otp(email):
    """Send an OTP to the user's email for phone number verification."""
    otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
    subject = 'Your OTP Code for Phone Number Verification'
    message = f'Your OTP code for phone number verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    return otp  # Return the generated OTP for verification